import type {
  EditCommand,
  JSON,
  TrackCreateArgs as NativeTrackCreateArgs,
} from '@/integrations/runtime/timeline-commit-types.ts';
import {
  assertFiniteJson,
  ClipMoveError,
  copy,
  equal,
  freezeJson,
  has,
  MoveRecording,
  object,
} from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export { ClipMoveError as TrackCreateError } from './clipMovePrimitives.ts';
export type { AuthoredBundle } from './clipMovePrimitives.ts';

export type TrackCreateArgs = NativeTrackCreateArgs;
export type TrackCreateBasis = { readonly bundle: AuthoredBundle; readonly command: EditCommand };

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;

function assertArgs(args: unknown): asserts args is TrackCreateArgs {
  if (!object(args) || !equal(Object.keys(args), ['row']) || !object(args.row)) {
    throw new ClipMoveError('track.create requires a row object');
  }
  const row = args.row;
  if (typeof row.id !== 'string' || row.id.length === 0 || row.id.includes('/') || row.id.includes('::')) {
    throw new ClipMoveError('track.create row id must be a non-empty stable identity');
  }
  if (typeof row.kind !== 'string' || row.kind.length === 0) {
    throw new ClipMoveError('track.create row kind must be a non-empty string');
  }
}

function selection(owner: string, members: string[]) {
  return {
    key: 'track.create',
    query_version: 1,
    owner,
    members: [...members],
    order: [...members],
    boundaries: [...members],
    policy: 'guard-membership' as const,
  };
}

function create(bundle: AuthoredBundle, supplied: EditCommand) {
  if (supplied.schema_version !== 1 || supplied.op !== 'track.create' || supplied.version !== '1' ||
    supplied.select !== 'parent' || !equal(supplied.intent ?? {}, {})) {
    throw new ClipMoveError('track.create requires the parent owner and no intention overrides');
  }
  assertArgs(supplied.args);
  if (!object(bundle.parent) || !object(bundle.parent.config) || !Array.isArray(bundle.parent.config.tracks)) {
    throw new ClipMoveError('track.create requires an authored parent track collection', 'identity_conflict');
  }

  const ctx = new MoveRecording(bundle, { ...copy(supplied), intent: {} });
  ctx.command.resolved = [];
  const tracks = ctx.state.config('parent').tracks;
  const members: string[] = [];
  for (const row of tracks) {
    if (!object(row) || typeof row.id !== 'string' || row.id.length === 0 || row.id.includes('/') ||
      row.id.includes('::') || members.includes(`parent/track:${row.id}`)) {
      throw new ClipMoveError('missing or ambiguous parent track identity', 'identity_conflict');
    }
    members.push(`parent/track:${row.id}`);
  }
  const chosen = selection('parent', members);
  ctx.command.selections!.push(chosen);

  const ref = `parent/track:${supplied.args.row.id}`;
  ctx.read(ref, []);
  const before = ctx.state.get(ref, []);
  if (before.state !== 'absent') {
    throw new ClipMoveError('created identity is occupied', 'identity_conflict');
  }
  const after = { state: 'present' as const, value: copy(supplied.args.row) as unknown as JSON };
  ctx.command.expect![`${ref}::`] = copy(before);
  ctx.command.authorship![`${ref}::`] = 'direct';
  ctx.record.writes.push({ ref, path: [], before: copy(before), after: copy(after) });
  tracks.push(copy(supplied.args.row) as unknown as JSON);
  ctx.command.created!.push(ref);
  ctx.record.created.push({ ref, kind: 'track', owner: 'parent' });
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

function assertCaptureClaims(command: EditCommand, actual: EditCommand): void {
  for (const key of CLAIMS) {
    if (has(command, key) && !equal(command[key], actual[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
}

export function executeTrackCreate(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  const result = create(bundle, command);
  assertCaptureClaims(command, result.command);
  Object.assign(result.command, copy(command), { intent: result.command.intent });
  return result;
}

export function captureTrackCreate(bundle: AuthoredBundle, args: TrackCreateArgs): TrackCreateBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(args);
  assertArgs(args);
  const snapshot = copy(bundle);
  const command: EditCommand = {
    schema_version: 1,
    op: 'track.create',
    version: '1',
    select: 'parent',
    args: { row: copy(args.row) as unknown as JSON },
    intent: {},
  };
  const result = executeTrackCreate(snapshot, command);
  return freezeJson({ bundle: snapshot, command: result.command });
}

export function finishTrackCreate(basis: unknown, args: TrackCreateArgs) {
  assertFiniteJson(basis);
  assertFiniteJson(args);
  assertArgs(args);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete track create basis');
  }
  const command = copy(basis.command as EditCommand);
  command.args = { row: copy(args.row) as unknown as JSON };
  return executeTrackCreate(basis.bundle as AuthoredBundle, command);
}
