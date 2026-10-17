import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const exact = (value: Record<string, unknown>, keys: readonly string[]) => Object.keys(value).length === keys.length && keys.every(key => Object.prototype.hasOwnProperty.call(value, key));
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
const json = (value: unknown): boolean => value === null || typeof value === 'string' || typeof value === 'boolean'
  || typeof value === 'number' && Number.isFinite(value) || Array.isArray(value) && value.every(json)
  || record(value) && Object.values(value).every(json);
const tagged = (value: unknown): boolean => record(value) && (value.state === 'absent' ? exact(value, ['state'])
  : value.state === 'present' && exact(value, ['state', 'value']) && json(value.value));
const equal = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);
const paths = ['keyframes', 'keyframeOrigin'];

/** D's full App-seconds map. Parameter names and array positions are opaque. */
export function isAppKeyframePayload(value: unknown): boolean {
  return record(value) && json(value) && Object.values(value).every(keys => Array.isArray(keys) && keys.every(key => record(key)
    && typeof key.time === 'number' && Number.isFinite(key.time)
    && (typeof key.value === 'string' || typeof key.value === 'boolean' || typeof key.value === 'number' && Number.isFinite(key.value))
    && (key.interpolation === 'linear' || key.interpolation === 'hold')
    && (!Object.prototype.hasOwnProperty.call(key, 'easing') || typeof key.easing === 'string')));
}

/** Selected inspector and existing bulk API, with a captured pair per owner. */
export function isAppKeyframeHistoryBatch(commands: readonly EditCommand[]): boolean {
  if (!commands.length || new Set(commands.map(command => command.select)).size !== commands.length) return false;
  return commands.every(command => command.op === 'clip.set' && scoped(command.select) && command.resolved?.length === 1 && command.resolved[0] === command.select
    && record(command.args) && exact(command.args, paths) && isAppKeyframePayload(command.args.keyframes)
    && typeof command.args.keyframeOrigin === 'number' && Number.isFinite(command.args.keyframeOrigin)
    && record(command.expect) && exact(command.expect, paths) && paths.every(path => tagged(command.expect![path])));
}

/** Inverse values may restore absent/null/opaque legacy maps. */
export function isAppKeyframeHistoryInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || !exact(command.args, ['publication', 'writes']) || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  return writes.every((write: unknown) => record(write) && exact(write, ['id', 'path', 'before', 'after']) && scoped(write.id)
    && typeof write.path === 'string' && paths.includes(write.path) && tagged(write.before) && tagged(write.after))
    && new Set(writes.map(write => JSON.stringify([write.id, write.path]))).size === writes.length;
}

/** Only accepted direct receipts authorize history. Never use preview diffs. */
export function appKeyframeHistoryInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isAppKeyframeHistoryInverse(commands[0]);
  if (!undo && !isAppKeyframeHistoryBatch(commands)) return undefined;
  const expected = undo ? commands[0].args.writes as Array<{ id: string; path: string; before: unknown; after: unknown }>
    : commands.flatMap(command => paths.map(path => ({ id: command.select!, path, before: command.expect![path], after: { state: 'present', value: command.args[path] } })));
  const writes = result.change?.direct_writes;
  if (!Array.isArray(writes)) return undefined;
  const changed = expected.filter(write => !equal(write.before, write.after));
  // Forward clip.set records the whole pair even on a no-op. Inverse
  // receipts record only changed properties; neither may omit a required row.
  const required = undo ? changed : expected;
  const complete = writes.length === required.length
    && writes.every(write => record(write) && exact(write, ['id', 'path', 'before', 'after']) && tagged(write.before) && tagged(write.after)
      && required.some(row => row.id === write.id && row.path === write.path && equal(row.before, write.before) && equal(row.after, write.after)))
    && new Set(writes.map(write => { const row = write as Record<string, unknown>; return JSON.stringify([row.id, row.path]); })).size === writes.length;
  if (result.status === 'no_change') return !changed.length && complete && result.accepted_publication_id === null ? null : undefined;
  if (result.status !== 'accepted' || !result.accepted_publication_id || !changed.length || !complete) return undefined;
  // SDK receipt ordering is independent of selection order. Retain the captured
  // owner order through Undo and receipt-derived Redo, using only exact rows.
  const owners = [...new Set(expected.map(write => write.id))];
  const ordered = owners.flatMap(id => writes.filter(write => (write as Record<string, unknown>).id === id));
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: ordered.map(write => { const row = write as Record<string, unknown>; return { ...structuredClone(row), before: structuredClone(row.after), after: structuredClone(row.before) }; }),
  } };
  if (!isAppKeyframeHistoryInverse(inverse)) return undefined;
  validateEditCommand(inverse); return inverse;
}
