import type { AgentState, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { ClipMoveError, MoveRecording, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type Row = Record<string, JSON>;
const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RELATIONS = ['on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence',
  'sequence_index', 'sequence_fit', 'orphan', 'formulas', 'anchor', 'standin', 'standin_intent'];

function identity(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && !value.includes('/') && !value.includes('::');
}

function validate(command: EditCommand): Row {
  const fields = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS];
  if (Object.keys(command).some((key) => !fields.includes(key)) ||
    (has(command, 'rationale') && typeof command.rationale !== 'string') ||
    (has(command, 'group_id') && (typeof command.group_id !== 'string' || !command.group_id))) {
    throw new ClipMoveError('clip.add requires the closed EditCommand envelope');
  }
  if (command.schema_version !== 1 || command.op !== 'clip.add' || command.version !== '1' || command.select !== 'parent') {
    throw new ClipMoveError('clip.add v1 requires parent ownership');
  }
  if (!object(command.args) || !equal(Object.keys(command.args), ['row']) || !object(command.args.row)) {
    throw new ClipMoveError('clip.add requires closed args containing a complete row');
  }
  if (command.intent !== undefined && !equal(command.intent, {})) throw new ClipMoveError('unsupported operation intention policy');
  const row = command.args.row;
  if (!identity(row.id) || !identity(row.track) || typeof row.clipType !== 'string' || !row.clipType ||
    typeof row.at !== 'number' || !Number.isFinite(row.at) || row.at < 0 ||
    typeof row.hold !== 'number' || !Number.isFinite(row.hold) || row.hold <= 0) {
    throw new ClipMoveError('clip.add requires explicit stable id, track, clipType and literal at/hold seconds');
  }
  if (['media', 'image', 'video', 'audio'].includes(row.clipType.toLowerCase()) ||
    ['asset', 'asset_id', 'media_id', 'object_id'].some((key) => has(row, key))) {
    throw new ClipMoveError('clip.add v1 does not support media clips or selectors', 'unsupported_media');
  }
  for (const key of ['sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'source',
    'from', 'to', 'from_ms', 'to_ms', 'at_ms', 'duration', 'duration_ms', 'time_map', 'timeMap',
    'clips', 'children', 'clip_type', 'anchor']) {
    if (row[key] != null) throw new ClipMoveError(`clip.add v1 does not support ${key}`, 'unsupported_timing');
  }
  if (row.speed != null && row.speed !== 1) throw new ClipMoveError('clip.add v1 requires literal hold timing', 'unsupported_timing');
  const app = row.app;
  if (app != null && !object(app)) throw new ClipMoveError('clip.add intent container must be object or null');
  const nested = object(app) ? app.astrid : undefined;
  if (nested != null && !object(nested)) throw new ClipMoveError('clip.add intent container must be object or null');
  for (const container of [row, app, nested]) {
    if (object(container)) for (const key of RELATIONS) {
      if (container[key] != null) throw new ClipMoveError(`clip.add v1 does not support ${key}`, 'unsupported_timing');
    }
  }
  return row;
}

// Agent _collections.shape records container presence/type without reading unrelated row values.
function tagged(container: Row, key: string): AgentState {
  if (!has(container, key)) return { state: 'absent' };
  const value = container[key];
  return { state: 'present', value: Array.isArray(value) ? [] : object(value) ? {} : copy(value) };
}

/** Local authored execution of Agent 027bd16d clip.add; accepted history/inverses stay on the server. */
export function executeParentClipAdd(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  const row = validate(command);
  const ctx = new MoveRecording(bundle, command);
  ctx.command.intent = {};
  ctx.command.resolved = [];
  const trackRef = `parent/track:${row.track}`;
  for (const key of ['id', 'kind', 'role', 'enabled', 'active', 'disabled', 'hidden', 'deleted']) ctx.read(trackRef, [key]);
  const track = ctx.state.entity(trackRef, true);
  if (!track) throw new ClipMoveError('clip.add destination track is missing', 'identity_conflict');
  if ((track.kind !== 'visual' && track.kind !== 'audio') || (has(track, 'role') && track.role !== 'output') ||
    track.enabled === false || track.active === false || ['disabled', 'hidden', 'deleted'].some((key) => track[key] === true)) {
    throw new ClipMoveError('clip.add requires an active output track');
  }
  ctx.bind('add.track', trackRef);
  const parent = ctx.state.bundle.parent;
  const config = ctx.state.config('parent');
  if (!object(config)) throw new ClipMoveError('collection owner must be an object', 'identity_conflict');
  const direct = parent.clips, mirror = config.clips;
  if (Array.isArray(direct) && Array.isArray(mirror) && !equal(direct, mirror)) {
    throw new ClipMoveError('divergent parent clip mirrors', 'identity_conflict');
  }
  // Match State.parent_clip_path, including empty arrays and absent/null secondary codecs.
  const rows = Array.isArray(direct) && (direct.length > 0 || !Array.isArray(mirror) || mirror.length === 0)
    ? direct : Array.isArray(mirror) ? mirror : [];
  if (!Array.isArray(direct) && !Array.isArray(mirror)) throw new ClipMoveError('structural edit requires an authored entity collection');
  const ids = rows.map((item) => object(item) ? item.id : undefined);
  if (ids.some((id) => !identity(id)) || new Set(ids).size !== ids.length) {
    throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  }
  const members = ids.map((id) => `parent/clip:${id}`);
  ctx.command.reads!.push({ ref: 'parent/collection:clip', path: [], state: { state: 'present', value: {
    members: tagged(config, 'clips'), config: tagged(parent, 'config'), payload_members: tagged(parent, 'clips'),
  } } });
  ctx.command.selections!.push({ key: 'collection.clips', query_version: 1, owner: 'parent',
    members: [...members], order: [...members], boundaries: [...members], policy: 'guard-membership' });
  const ref = `parent/clip:${row.id}`;
  if (members.includes(ref)) throw new ClipMoveError('created identity is occupied', 'identity_collision');
  ctx.read(ref, []);
  ctx.command.expect![`${ref}::`] = { state: 'absent' };
  ctx.command.authorship![`${ref}::`] = 'direct';
  ctx.record.writes.push({ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: copy(row) } });
  ctx.record.created.push({ ref, kind: 'clip', owner: 'parent' });
  ctx.command.created!.push(ref);
  rows.push(copy(row));
  // Native Recording remembers equality before creation, including two empty mirrors.
  if (Array.isArray(direct) && Array.isArray(mirror)) {
    const before = ctx.state.get('parent', ['config', 'clips']);
    const after: AgentState = { state: 'present', value: copy(direct) };
    if (!equal(before, after)) {
      ctx.record.derived_writes.push({ ref: 'parent', path: ['config', 'clips'], before, after, cause: 0 });
      ctx.state.set('parent', ['config', 'clips'], after);
    }
  }
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(command, key) && !equal(command[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(ctx.command, copy(command), { intent: {} });
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export type ParentClipAddBasis = { readonly bundle: AuthoredBundle; readonly command: EditCommand };

/** The caller reserves row.id once before capture. No allocator or refreshed ACK state enters this basis. */
export function captureParentClipAdd(bundle: AuthoredBundle, select: string, row: Row): ParentClipAddBasis {
  const command: EditCommand = { schema_version: 1, op: 'clip.add', version: '1', select, args: { row }, intent: {} };
  const result = executeParentClipAdd(bundle, command);
  return freezeJson({ bundle: copy(bundle), command: result.command });
}

/** Finish consumes only the original finite-JSON capture, retaining its guards and explicit ID. */
export function finishParentClipAdd(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) || !CLAIMS.every((key) => has(basis.command as Row, key))) {
    throw new ClipMoveError('incomplete parent clip add basis');
  }
  return executeParentClipAdd(basis.bundle as AuthoredBundle, basis.command as EditCommand);
}
