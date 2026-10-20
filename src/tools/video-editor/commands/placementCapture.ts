import type { AgentRead, AgentSelection, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { executeClipMove } from './clipMoveCapture.ts';
import { AuthoredState, ClipMoveError, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export type PlacementBasis = { readonly bundle: AuthoredBundle; readonly command: EditCommand };
export type PlacementOwnership = 'parent' | 'occurrence';

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const INTENT = { ripple: 'none', anchor: 'fixed', position: 'absolute' } as const;

function intent(select: string): EditCommand['intent'] {
  return select.startsWith('occurrence:') ? { ...INTENT, ownership: 'occurrence' } : { ...INTENT };
}

function ownerScope(owner: unknown): 'parent' | 'occurrence' | undefined {
  if (owner === 'parent') return 'parent';
  return typeof owner === 'string' && /^occurrence:[^/]+$/.test(owner) && !owner.includes('::')
    ? 'occurrence' : undefined;
}

function assertRequest(owner: unknown, clipId: unknown, ownership: unknown): asserts owner is string {
  const scope = ownerScope(owner);
  if (scope === undefined || ownership !== scope) {
    throw new ClipMoveError('placement requires matching explicit parent or occurrence ownership', 'unsupported_ownership');
  }
  if (typeof clipId !== 'string' || !clipId.trim() || clipId.includes('/') || clipId.includes('::')) {
    throw new ClipMoveError('placement requires a raw clip identity', 'identity_conflict');
  }
}

function sourceReads(state: AuthoredState, owner: string, asset: JSON | undefined): AgentRead[] {
  if (asset == null) return [];
  if (typeof asset !== 'string') throw new ClipMoveError('placement requires a canonical asset identity');
  const path = ['registry', 'assets', asset];
  const refs = owner === 'parent'
    ? [['parent', path], ['parent', ['config', ...path]]]
    : [[`${owner}/source`, path]];
  return refs.map(([ref, readPath]) => ({
    ref: ref as string,
    path: readPath as string[],
    state: state.get(ref as string, readPath as string[]),
  }));
}

function ownersSelection(state: AuthoredState, owner: string): AgentSelection {
  const row = state.occurrence(owner);
  const members = state.bundle.placements
    .filter((other) => other.shot_id === row.shot_id)
    .map((other) => `occurrence:${other.occurrence_id}`);
  if (!equal(members, [owner])) {
    throw new ClipMoveError('shared authored placement is unsupported', 'unsupported_ownership');
  }
  return {
    boundaries: [`shot:${String(row.shot_id)}`],
    key: 'placement.owners',
    members,
    order: [...members],
    owner,
    policy: 'guard-membership',
    query_version: 1,
  };
}

function durationWrite(record: CommandRecord, ref: string): number {
  const write = record.writes.find((candidate) => candidate.ref === ref &&
    equal(candidate.path, ['app', 'astrid', 'for']));
  if (!write || write.after.state !== 'present' || typeof write.after.value !== 'number') {
    throw new ClipMoveError('placement requires an unambiguous positive clip duration', 'unsupported_timing');
  }
  return write.after.value;
}

function assertOccurrenceExtent(bundle: AuthoredBundle, result: ReturnType<typeof executeClipMove>, owner: string, ref: string): void {
  if (owner === 'parent') return;
  const row = new AuthoredState(bundle).occurrence(owner);
  if (typeof row.duration_ms !== 'number' || !Number.isFinite(row.duration_ms) || row.duration_ms <= 0) {
    throw new ClipMoveError('placement requires a positive occurrence duration', 'unsupported_timing');
  }
  const clip = new AuthoredState(result.bundle).entity(ref)!;
  const start = typeof clip.at === 'number' ? clip.at : typeof clip.at_ms === 'number' ? clip.at_ms / 1000 : NaN;
  const end = start + durationWrite(result.record, ref);
  if (!Number.isFinite(start) || end > row.duration_ms / 1000 + 1e-9) {
    throw new ClipMoveError('placed interval exceeds occurrence duration', 'occurrence_boundary');
  }
}

function apply(bundle: AuthoredBundle, supplied: EditCommand) {
  if (supplied.schema_version !== 1 || supplied.op !== 'placement.move' || supplied.version !== '1' ||
    typeof supplied.select !== 'string' || !equal(Object.keys(supplied.args), ['on'])) {
    throw new ClipMoveError('unsupported placement.move v1 command');
  }
  const ref = supplied.select;
  if (!/^((parent)|(occurrence:[^/]+))\/clip:[^/]+$/.test(ref) || ref.includes('::')) {
    throw new ClipMoveError('placement requires a stable scoped clip identity', 'identity_conflict');
  }
  const owner = ref.slice(0, ref.lastIndexOf('/'));
  const expectedIntent = intent(ref);
  if (!equal({ ...expectedIntent, ...supplied.intent }, expectedIntent)) {
    throw new ClipMoveError('unsupported placement.move v1 intention');
  }
  const state = new AuthoredState(bundle);
  const clip = state.entity(ref);
  const asset = has(clip, 'asset') ? clip.asset : clip.asset_id;
  const ownership = owner === 'parent' ? undefined : ownersSelection(state, owner);
  const guards = sourceReads(state, owner, asset);
  const moveCommand = copy(supplied);
  moveCommand.op = 'clip.move';
  for (const key of CLAIMS) delete moveCommand[key];
  const moved = executeClipMove(bundle, moveCommand);
  assertOccurrenceExtent(bundle, moved, owner, ref);

  const reads = [...guards, ...moved.command.reads!];
  const selections = ownership ? [ownership, ...moved.command.selections!] : moved.command.selections!;
  const command: EditCommand = {
    ...moved.command,
    op: 'placement.move',
    reads: copy(reads),
    selections: copy(selections),
    intent: expectedIntent,
  };
  const record: CommandRecord = {
    ...moved.record,
    command,
    reads: copy(reads),
    selections: copy(selections),
  };
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command, bundle: moved.bundle, record, previewAt: moved.previewAt };
}

/**
 * Capture an explicit-owner absolute placement before preview or ACK.
 *
 * This is intentionally narrower than the legacy place/unplace/new-generation
 * writers: it moves one existing raw clip and never pools, selects media, or
 * creates/deletes an occurrence, shot, track, or clip.
 */
export function capturePlacement(bundle: AuthoredBundle, owner: string, clipId: string, on: number,
  ownership: PlacementOwnership): PlacementBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(owner);
  assertFiniteJson(clipId);
  assertFiniteJson(on);
  assertRequest(owner, clipId, ownership);
  const snapshot = copy(bundle);
  const ref = `${owner}/clip:${clipId}`;
  const { command } = apply(snapshot, {
    schema_version: 1,
    op: 'placement.move',
    version: '1',
    select: ref,
    args: { on },
    intent: intent(ref),
  });
  return freezeJson({ bundle: snapshot, command });
}

/** Finish a portable original capture without refreshing guards from a new head. */
export function finishPlacement(basis: unknown, on: number) {
  assertFiniteJson(basis);
  assertFiniteJson(on);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !object(basis.command.args) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete placement basis');
  }
  const command = copy(basis.command as EditCommand);
  return apply(basis.bundle as AuthoredBundle, { ...command, args: { ...command.args, on } });
}
