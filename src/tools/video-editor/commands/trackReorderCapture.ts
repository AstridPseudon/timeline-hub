import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
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

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const COLLECTION_REF = 'parent/collection:track';
const ORDER_ADDRESS = 'parent::track_order';

export type TrackReorderArgs = {
  readonly order: readonly string[];
  readonly expected_order: readonly string[];
};

export type TrackReorderBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
};

type TrackRow = { [key: string]: JSON };

function isAuthoredBundle(value: unknown): value is AuthoredBundle {
  return object(value) && object(value.parent) && Array.isArray(value.placements) && object(value.shots);
}

function isEditCommand(value: unknown): value is EditCommand {
  return object(value) && value.schema_version === 1 && typeof value.op === 'string' &&
    typeof value.version === 'string' && (value.select === null || typeof value.select === 'string') &&
    object(value.args);
}

function trackRefs(bundle: AuthoredBundle): string[] {
  if (!object(bundle.parent.config) || !Array.isArray(bundle.parent.config.tracks)) {
    throw new ClipMoveError('track reorder requires an authored parent track collection');
  }
  const rows = bundle.parent.config.tracks;
  const refs: string[] = [];
  const seen = new Set<string>();
  for (const row of rows) {
    if (!object(row) || typeof row.id !== 'string' || !row.id || row.id.includes('/') || row.id.includes('::')) {
      throw new ClipMoveError('track reorder requires unique stable parent track identities', 'identity_conflict');
    }
    const ref = `parent/track:${row.id}`;
    if (seen.has(ref)) throw new ClipMoveError('track reorder refuses duplicate parent track identities', 'identity_conflict');
    seen.add(ref);
    refs.push(ref);
  }
  return refs;
}

function orderArgs(value: unknown): value is TrackReorderArgs {
  return object(value) && Object.keys(value).sort().join(',') === 'expected_order,order' &&
    Array.isArray(value.order) && Array.isArray(value.expected_order) &&
    value.order.every((ref) => typeof ref === 'string') &&
    value.expected_order.every((ref) => typeof ref === 'string');
}

function assertPermutation(order: readonly string[], expected: readonly string[], label: string): void {
  if (order.length !== expected.length || new Set(order).size !== order.length ||
    !order.every((ref) => /^parent\/track:[^/]+$/.test(ref)) ||
    !order.every((ref) => expected.includes(ref))) {
    throw new ClipMoveError(`${label} must be a complete unique parent track permutation`, 'selection_changed');
  }
}

function assertCommand(command: EditCommand): asserts command is EditCommand & { args: TrackReorderArgs } {
  const allowed = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS];
  if (Object.keys(command).some((key) => !allowed.includes(key)) ||
    (has(command, 'rationale') && typeof command.rationale !== 'string') ||
    (has(command, 'group_id') && (typeof command.group_id !== 'string' || !command.group_id)) ||
    command.schema_version !== 1 || command.op !== 'track.reorder' || command.version !== '1' ||
    command.select !== 'parent' || !orderArgs(command.args) || !equal(command.intent ?? {}, {})) {
    throw new ClipMoveError('track.reorder requires the closed media-only EditCommand envelope');
  }
}

function recordCollectionRead(ctx: MoveRecording, refs: readonly string[]): void {
  const read = { ref: COLLECTION_REF, path: [], state: { state: 'present' as const, value: [...refs] } };
  if (!ctx.command.reads!.some((prior) => equal(prior, read))) ctx.command.reads!.push(read);
  ctx.command.selections!.push({ key: 'collection.tracks', query_version: 1, owner: 'parent',
    members: [...refs], order: [...refs], boundaries: [...refs], policy: 'guard-membership' });
}

function applyTrackReorder(bundle: AuthoredBundle, supplied: EditCommand) {
  assertCommand(supplied);
  const current = trackRefs(bundle);
  const expected = supplied.args.expected_order;
  const desired = supplied.args.order;
  assertPermutation(expected, current, 'expected_order');
  assertPermutation(desired, current, 'order');
  if (!equal(current, expected)) {
    throw new ClipMoveError('original parent track order changed', 'selection_changed');
  }

  const ctx = new MoveRecording(bundle, { ...copy(supplied), intent: {} });
  recordCollectionRead(ctx, current);
  ctx.command.expect![ORDER_ADDRESS] = { state: 'present', value: copy(current) };
  ctx.command.authorship![ORDER_ADDRESS] = 'direct';
  ctx.record.writes.push({ ref: 'parent', path: ['track_order'], before: { state: 'present', value: copy(current) },
    after: { state: 'present', value: [...desired] } });

  const config = ctx.state.config('parent');
  const rows = config.tracks;
  if (!Array.isArray(rows)) throw new ClipMoveError('track reorder requires an authored parent track collection');
  const byRef = new Map<string, TrackRow>();
  for (const row of rows) {
    if (object(row) && typeof row.id === 'string') byRef.set(`parent/track:${row.id}`, row);
  }
  config.tracks = desired.map((ref) => byRef.get(ref)!);

  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export function captureTrackReorder(bundle: AuthoredBundle, desiredOrder: unknown): TrackReorderBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(desiredOrder);
  if (!Array.isArray(desiredOrder)) {
    throw new ClipMoveError('media-only track reorder does not accept lane-bearing input');
  }
  const snapshot = copy(bundle);
  const expectedOrder = trackRefs(snapshot);
  const command: EditCommand = {
    schema_version: 1,
    op: 'track.reorder',
    version: '1',
    select: 'parent',
    args: { order: copy(desiredOrder), expected_order: copy(expectedOrder) },
    intent: {},
  };
  const captured = applyTrackReorder(snapshot, command);
  return freezeJson({ bundle: snapshot, command: captured.command });
}

export function finishTrackReorder(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis)) throw new ClipMoveError('incomplete track reorder basis');
  const bundle = basis.bundle;
  const command = basis.command;
  if (!isAuthoredBundle(bundle) || !isEditCommand(command) || !CLAIMS.every((key) => has(command, key))) {
    throw new ClipMoveError('incomplete track reorder basis');
  }
  return applyTrackReorder(bundle, copy(command));
}

export function executeTrackReorder(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  return applyTrackReorder(bundle, command);
}
