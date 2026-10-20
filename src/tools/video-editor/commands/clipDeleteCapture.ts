import type { AgentSelection, AgentState, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  AuthoredState,
  ClipMoveError,
  MoveRecording,
  assertFiniteJson,
  copy,
  equal,
  freezeJson,
  has,
  object,
} from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type ObjectValue = { [key: string]: JSON };

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RELATIONS = ['on', 'until', 'until_film_end', 'cut', 'formulas', 'sequence', 'sequence_index',
  'sequence_fit', 'sequence_shape_from', 'segment', 'words', 'beats', 'slot', 'replaces', 'standin',
  'standin_for', 'intended', 'group', 'duck'];

export type ClipDeleteBasis = { readonly bundle: AuthoredBundle; readonly command: EditCommand };

function present(value: JSON): AgentState {
  return { state: 'present', value: copy(value) };
}

function tagged(value: unknown, key: string): AgentState {
  if (!object(value) || !has(value, key)) return { state: 'absent' };
  const child = value[key];
  return present(Array.isArray(child) ? [] : object(child) ? {} : child);
}

function collectionRows(state: AuthoredState, owner: string, kind: 'clip' | 'occurrence'): ObjectValue[] {
  if (kind === 'occurrence') {
    if (!Array.isArray(state.bundle.placements)) throw new ClipMoveError('invalid occurrence collection', 'identity_conflict');
    return state.bundle.placements;
  }
  const config = state.config(owner);
  if (!object(config)) throw new ClipMoveError('collection owner must be an object', 'identity_conflict');
  if (owner === 'parent') {
    const parent = state.bundle.parent;
    const payload = parent.clips;
    const mirror = config.clips;
    if (Array.isArray(payload) && Array.isArray(mirror) && !equal(payload, mirror)) {
      throw new ClipMoveError('divergent parent clip mirrors', 'identity_conflict');
    }
    if (Array.isArray(payload) && (payload.length > 0 || !Array.isArray(mirror) || mirror.length === 0)) return payload as ObjectValue[];
  }
  if (!Array.isArray(config.clips)) throw new ClipMoveError('structural edit requires an authored entity collection', 'identity_conflict');
  return config.clips as ObjectValue[];
}

function identityRows(state: AuthoredState, owner: string, kind: 'clip' | 'occurrence'): string[] {
  const rows = collectionRows(state, owner, kind);
  const key = kind === 'clip' ? 'id' : 'occurrence_id';
  const refs = rows.map((row) => {
    const id = row[key];
    if (typeof id !== 'string' || id.length === 0 || id.includes('/') || id.includes('::')) {
      throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
    }
    return kind === 'clip' ? `${owner}/clip:${id}` : `occurrence:${id}`;
  });
  if (new Set(refs).size !== refs.length) throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  return refs;
}

function readCollection(ctx: MoveRecording, owner: string, kind: 'clip' | 'occurrence'): void {
  const ref = `${owner}/collection:${kind}`;
  const state: AgentState = kind === 'occurrence'
    ? present({ container: 'array' })
    : (() => {
      const config = ctx.state.config(owner);
      const result: Record<string, AgentState> = { members: tagged(config, 'clips') };
      if (owner === 'parent') {
        result.config = tagged(ctx.state.bundle.parent, 'config');
        result.payload_members = tagged(ctx.state.bundle.parent, 'clips');
      }
      return present(result);
    })();
  const read = { ref, path: [], state };
  if (!ctx.command.reads!.some((other) => equal(other, read))) ctx.command.reads!.push(read);
}

function selectCollection(ctx: MoveRecording, owner: string, kind: 'clip' | 'occurrence'): string[] {
  readCollection(ctx, owner, kind);
  const members = identityRows(ctx.state, owner, kind);
  const selection: AgentSelection = {
    key: `collection.${kind}s`, query_version: 1, owner, members: [...members], order: [...members],
    boundaries: [...members], policy: 'guard-membership',
  };
  if (!ctx.command.selections!.some((other) => equal(other, selection))) ctx.command.selections!.push(selection);
  if (owner !== 'parent') {
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    ctx.bind(`collection.owner:collection.${kind}s`, owner);
  }
  return members;
}

function unrelated(ctx: MoveRecording, ref: string, prefixes: string[][], keys: string[]): void {
  for (const prefix of prefixes) {
    for (const key of keys) {
      const value = ctx.read(ref, [...prefix, key]);
      if (value !== undefined && value !== null && value !== '' && !equal(value, {}) && !equal(value, [])) {
        throw new ClipMoveError('clip.delete cannot prove declared semantic dependencies safe', 'unsupported_dependency');
      }
    }
  }
}

function removeRoot(ctx: MoveRecording, ref: string): void {
  const before = ctx.state.get(ref, []);
  if (before.state !== 'present') throw new ClipMoveError('delete target disappeared', 'identity_conflict');
  const address = `${ref}::`;
  ctx.command.expect![address] = before;
  ctx.command.authorship![address] = 'direct';
  ctx.record.writes.push({ ref, path: [], before, after: { state: 'absent' } });

  const owner = ref.slice(0, ref.lastIndexOf('/'));
  const id = ref.slice('parent/clip:'.length);
  const rows = collectionRows(ctx.state, owner, 'clip');
  const index = rows.findIndex((row) => row.id === id);
  if (index < 0) throw new ClipMoveError('delete target disappeared', 'identity_conflict');
  rows.splice(index, 1);
}

function apply(bundle: AuthoredBundle, supplied: EditCommand) {
  if (supplied.schema_version !== 1 || supplied.op !== 'clip.delete' || supplied.version !== '1' ||
    typeof supplied.select !== 'string' || !/^parent\/clip:(?!.*::)[^/]+$/.test(supplied.select) ||
    !object(supplied.args) || Object.keys(supplied.args).length !== 0 ||
    (has(supplied, 'intent') && !equal(supplied.intent, {}))) {
    throw new ClipMoveError('unsupported clip.delete v1 command');
  }

  const ref = supplied.select;
  const ctx = new MoveRecording(bundle, { ...supplied, intent: {} });
  const members = selectCollection(ctx, 'parent', 'clip');
  if (!members.includes(ref)) throw new ClipMoveError('delete target disappeared', 'identity_conflict');
  ctx.read(ref, []);
  const row = ctx.state.entity(ref);
  if (!row) throw new ClipMoveError('delete target disappeared', 'identity_conflict');
  if (row.clipType === 'shot' || row.clip_type === 'shot') {
    throw new ClipMoveError('clip.delete cannot remove legacy shot ownership', 'unsupported_ownership');
  }
  if ((has(row, 'clips') && row.clips !== null) || (has(row, 'children') && row.children !== null)) {
    throw new ClipMoveError('clip.delete cannot remove nested clip ownership', 'unsupported_ownership');
  }

  const owners = ['parent', ...selectCollection(ctx, 'parent', 'occurrence')];
  for (const owner of owners) {
    const configRef = owner === 'parent' ? 'parent' : `${owner}/source`;
    const prefix = owner === 'parent' ? ['config'] : [];
    unrelated(ctx, configRef, [prefix], ['pinnedShotGroups']);
    unrelated(ctx, configRef, [prefix, [...prefix, 'app'], [...prefix, 'app', 'astrid']],
      ['sequences', 'formulas', 'slots']);
    for (const member of selectCollection(ctx, owner, 'clip')) {
      unrelated(ctx, member, [[]], ['transition']);
      unrelated(ctx, member, [['app'], ['app', 'astrid']], RELATIONS);
    }
  }
  removeRoot(ctx, ref);
  ctx.compile();
  // Native Recording.compile_mirrors also records removal of the final row.
  const parent = ctx.state.bundle.parent;
  const config = ctx.state.config('parent');
  if (Array.isArray(parent.clips) && parent.clips.length === 0 && Array.isArray(config.clips) && config.clips.length > 0) {
    const before = ctx.state.get('parent', ['config', 'clips']);
    const after = present([]);
    ctx.record.derived_writes.push({ ref: 'parent', path: ['config', 'clips'], before, after, cause: 0 });
    ctx.state.set('parent', ['config', 'clips'], after);
  }
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record as CommandRecord };
}

export function executeClipDelete(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  return apply(bundle, command);
}

export function captureClipDelete(bundle: AuthoredBundle, select: string): ClipDeleteBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(select);
  const snapshot = copy(bundle);
  const { command } = apply(snapshot, {
    schema_version: 1, op: 'clip.delete', version: '1', select, args: {}, intent: {},
  });
  return freezeJson({ bundle: snapshot, command });
}

export function finishClipDelete(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete clip delete basis');
  }
  return apply(basis.bundle as AuthoredBundle, copy(basis.command as EditCommand));
}
