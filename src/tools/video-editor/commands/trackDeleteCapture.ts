import type {
  AgentState as NativeAgentState,
  CommandRecord,
  EditCommand,
  JSON as JsonValue,
} from '@/integrations/runtime/timeline-commit-types.ts';
import {
  AuthoredState,
  ClipMoveError,
  MoveRecording,
  assertFiniteJson,
  copy,
  equal,
  freezeJson,
  object,
} from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export type TrackDeleteResult = {
  readonly command: EditCommand;
  readonly bundle: AuthoredBundle;
  readonly record: CommandRecord;
};

type AgentState = NativeAgentState;
type CollectionKind = 'track' | 'clip' | 'occurrence' | 'shot';

const TRACK_REF = /^parent\/track:(?!.*::)[^/]+$/;
const REFERENCE_KEYS = ['track_ref', 'owner_ref', 'track', 'track_id'] as const;

function state(value: JsonValue): AgentState {
  return { state: 'present', value };
}

function absent(): AgentState {
  return { state: 'absent' };
}

function collectionRows(authored: AuthoredState, owner: string, kind: CollectionKind): JsonValue[] {
  if (kind === 'occurrence') return authored.bundle.placements;
  if (kind === 'shot') return Object.values(authored.bundle.shots);

  const config = authored.config(owner);
  if (kind === 'clip' && owner === 'parent') {
    const parent = authored.bundle.parent;
    const primary = parent.clips;
    const mirror = config.clips;
    if (Array.isArray(primary) && (primary.length > 0 || !Array.isArray(mirror) || mirror.length === 0)) {
      return primary;
    }
  }
  const rows = config[`${kind}s`];
  if (!Array.isArray(rows)) throw new ClipMoveError('structural edit requires an authored entity collection');
  return rows;
}

function refFor(owner: string, kind: CollectionKind, row: JsonValue): string {
  if (!object(row)) throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  if (kind === 'occurrence') {
    if (typeof row.occurrence_id !== 'string' || !row.occurrence_id) {
      throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
    }
    return `occurrence:${row.occurrence_id}`;
  }
  if (kind === 'shot') {
    if (typeof row.shot_id !== 'string' || !row.shot_id) {
      throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
    }
    return `shot:${row.shot_id}`;
  }
  if (typeof row.id !== 'string' || !row.id) {
    throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  }
  return `${owner}/${kind}:${row.id}`;
}

function collectionShape(authored: AuthoredState, owner: string, kind: CollectionKind): JsonValue {
  if (kind === 'occurrence') return { container: 'array' };
  if (kind === 'shot') return { container: 'object' };
  const config = authored.config(owner);
  const shape: Record<string, AgentState> = {
    members: Array.isArray(config[`${kind}s`]) ? state([]) : absent(),
  };
  if (owner === 'parent') {
    shape.config = authored.bundle.parent.config == null ? absent() : state({});
    if (kind === 'clip') {
      shape.payload_members = Array.isArray(authored.bundle.parent.clips) ? state([]) : absent();
    }
  }
  return Object.fromEntries(Object.entries(shape).filter(([, value]) => value.state !== 'absent')) as JsonValue;
}

function readCollection(ctx: MoveRecording, authored: AuthoredState, owner: string, kind: CollectionKind): void {
  const ref = `${owner}/collection:${kind}`;
  const value = collectionShape(authored, owner, kind);
  const reads = ctx.command.reads!;
  const read = { ref, path: [], state: state(value) };
  if (!reads.some((prior) => equal(prior, read))) reads.push(read);
}

function selectCollection(
  ctx: MoveRecording,
  authored: AuthoredState,
  key: `collection.${CollectionKind}s`,
  owner: string,
): string[] {
  const kind = key.slice('collection.'.length, -1) as CollectionKind;
  readCollection(ctx, authored, owner, kind);
  if (owner !== 'parent') {
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    ctx.bind(`collection.owner:${key}`, owner);
  }
  const members = collectionRows(authored, owner, kind).map((row) => refFor(owner, kind, row));
  const selection = {
    key,
    query_version: 1,
    owner,
    members,
    order: [...members],
    boundaries: [...members],
    policy: 'guard-membership' as const,
  };
  if (!ctx.command.selections!.some((prior) => equal(prior, selection))) {
    ctx.command.selections!.push(selection);
  }
  return members;
}

function readDirect(ctx: MoveRecording, ref: string, path: string[], value: AgentState): void {
  const read = { ref, path, state: value };
  if (!ctx.command.reads!.some((prior) => equal(prior, read))) ctx.command.reads!.push(read);
}

function readShotAudioBindings(ctx: MoveRecording, authored: AuthoredState, shotId: string): JsonValue | undefined {
  const shot = authored.bundle.shots[shotId];
  if (!shot || !object(shot.payload)) throw new ClipMoveError('missing authored shot', 'identity_conflict');
  const payload = shot.payload;
  const value = Object.prototype.hasOwnProperty.call(payload, 'audio_bindings')
    ? state(payload.audio_bindings)
    : absent();
  readDirect(ctx, `shot:${shotId}`, ['payload', 'audio_bindings'], value);
  return value.state === 'present' ? value.value : undefined;
}

function references(
  ctx: MoveRecording,
  row: JsonValue,
  other: string | null,
  site: string | undefined,
  path: string[],
  target: string,
  identity: string,
): boolean {
  if (!object(row)) throw new ClipMoveError('unsupported declared reference row', 'surviving_dependents');
  for (const key of REFERENCE_KEYS) {
    if (site) ctx.read(site, [...path, key]);
    const value = row[key];
    if (value !== undefined && value !== null && typeof value !== 'string') {
      throw new ClipMoveError('unsupported declared reference edge', 'surviving_dependents');
    }
    if ((key === 'track_ref' || key === 'owner_ref') && value === target) return true;
  }
  return other === 'parent' && (row.track === identity || row.track_id === identity);
}

function findDependents(ctx: MoveRecording, authored: AuthoredState, target: string): void {
  const [, identity] = target.split('/track:');
  const owners = ['parent', ...authored.bundle.placements.map((row) => `occurrence:${String(row.occurrence_id)}`)];
  selectCollection(ctx, authored, 'collection.occurrences', 'parent');
  selectCollection(ctx, authored, 'collection.shots', 'parent');

  for (const owner of owners) {
    const clips = collectionRows(authored, owner, 'clip');
    const config = authored.config(owner);
    if (Array.isArray(config.clips) || (owner === 'parent' && Array.isArray(authored.bundle.parent.clips))) {
      selectCollection(ctx, authored, 'collection.clips', owner);
    } else {
      readCollection(ctx, authored, owner, 'clip');
      if (owner !== 'parent') {
        ctx.read(owner, ['occurrence_id']);
        ctx.read(`${owner}/shot`, ['shot_id']);
      }
    }
    for (const clip of clips) {
      if (references(ctx, clip, owner, `${owner}/clip:${String((clip as Record<string, JsonValue>).id)}`, [], target, identity)) {
        throw new ClipMoveError('track has surviving dependents', 'surviving_dependents');
      }
    }
    for (const key of ['audio', 'effects'] as const) {
      ctx.read(`${owner}/source`, [key]);
      const rows = config[key];
      if (Array.isArray(rows) && rows.some((row) => references(ctx, row, owner, undefined, [], target, identity))) {
        throw new ClipMoveError('track has surviving dependents', 'surviving_dependents');
      }
    }
    if (owner !== 'parent') {
      const occurrence = authored.occurrence(owner);
      const shotId = String(occurrence.shot_id);
      const bindings = readShotAudioBindings(ctx, authored, shotId);
      if (Array.isArray(bindings) && bindings.some((row) => references(ctx, row, owner, undefined, [], target, identity))) {
        throw new ClipMoveError('track has surviving dependents', 'surviving_dependents');
      }
    }
  }

  for (const row of authored.bundle.placements) {
    const site = `occurrence:${String(row.occurrence_id)}`;
    if (references(ctx, row, 'parent', site, [], target, identity) ||
      references(ctx, row.placement ?? {}, 'parent', site, ['placement'], target, identity)) {
      throw new ClipMoveError('track has surviving dependents', 'surviving_dependents');
    }
  }
  for (const shot of Object.values(authored.bundle.shots)) {
    const shotId = String(shot.shot_id);
    const bindings = readShotAudioBindings(ctx, authored, shotId);
    if (Array.isArray(bindings) && bindings.some((row) => references(ctx, row, null, undefined, [], target, identity))) {
      throw new ClipMoveError('track has surviving dependents', 'surviving_dependents');
    }
  }
}

function clearEntity(ctx: MoveRecording, authored: AuthoredState, ref: string): void {
  const before = authored.get(ref, []);
  if (before.state !== 'present') throw new ClipMoveError('track disappeared', 'identity_conflict');
  ctx.record.writes.push({ ref, path: [], before, after: { state: 'absent' } });
  ctx.command.expect![`${ref}::`] = copy(before);
  ctx.command.authorship![`${ref}::`] = 'direct';
  const config = authored.config('parent');
  if (!Array.isArray(config.tracks)) throw new ClipMoveError('structural edit requires an authored entity collection');
  const index = config.tracks.findIndex((row) => object(row) && row.id === ref.slice('parent/track:'.length));
  if (index < 0) throw new ClipMoveError('track disappeared', 'identity_conflict');
  config.tracks.splice(index, 1);
}

function capture(bundle: AuthoredBundle, select: string): TrackDeleteResult {
  if (typeof select !== 'string' || !TRACK_REF.test(select)) {
    throw new ClipMoveError('track.delete v1 requires a parent track identity');
  }
  const command = { schema_version: 1, op: 'track.delete', version: '1', select, args: {}, intent: {} } as EditCommand;
  const ctx = new MoveRecording(bundle, command);
  const authored = ctx.state;
  selectCollection(ctx, authored, 'collection.tracks', 'parent');
  if (!ctx.read(select, [])) throw new ClipMoveError('track disappeared', 'identity_conflict');
  ctx.bind('delete.target', select);
  findDependents(ctx, authored, select);
  clearEntity(ctx, authored, select);
  ctx.compile();
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export function captureTrackDelete(bundle: AuthoredBundle, select: string): TrackDeleteResult {
  assertFiniteJson(bundle);
  const result = capture(copy(bundle), select);
  return {
    command: freezeJson(result.command),
    bundle: freezeJson(result.bundle),
    record: freezeJson(result.record),
  };
}

export function executeTrackDelete(bundle: AuthoredBundle, command: EditCommand): TrackDeleteResult {
  assertFiniteJson(bundle);
  if (command.schema_version !== 1 || command.op !== 'track.delete' || command.version !== '1' ||
    !equal(Object.keys(command.args), [])) {
    throw new ClipMoveError('unsupported track.delete v1 command');
  }
  if (typeof command.select !== 'string') throw new ClipMoveError('track.delete requires a stable selection');
  const result = capture(bundle, command.select);
  for (const field of ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const) {
    if (Object.prototype.hasOwnProperty.call(command, field) && !equal(command[field], result.command[field])) {
      throw new ClipMoveError(`submitted ${field} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(result.command, copy(command));
  return result;
}
