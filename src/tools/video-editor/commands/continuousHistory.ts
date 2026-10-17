import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';
import type { ClipMeta } from '../lib/timeline-data.ts';

const record = (v: unknown): v is Record<string, unknown> => v !== null && typeof v === 'object' && !Array.isArray(v);
const own = (v: object, k: string) => Object.prototype.hasOwnProperty.call(v, k);
const exact = (v: Record<string, unknown>, keys: string[]) => Object.keys(v).length === keys.length && keys.every(k => own(v, k));
const scoped = (v: unknown): v is string => typeof v === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(v);
export const continuousJson = (v: unknown): boolean => v === null || typeof v === 'string' || typeof v === 'boolean'
  || typeof v === 'number' && Number.isFinite(v) || Array.isArray(v) && Object.keys(v).length === v.length && v.every(continuousJson)
  || record(v) && (Object.getPrototypeOf(v) === Object.prototype || Object.getPrototypeOf(v) === null) && Object.values(v).every(continuousJson);
export const sameContinuous = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);
export const validContinuous = (v: unknown): v is Record<string, unknown> => record(v) && continuousJson(v)
  && typeof v.type === 'string' && Boolean(v.type.trim())
  && (!own(v, 'intensity') || typeof v.intensity === 'number' && Number.isFinite(v.intensity))
  && (!own(v, 'params') || record(v.params));
type State = { state: 'absent' } | { state: 'present'; value: unknown };
type Write = { id: string; path: string; before: State; after: State };
const tagged = (v: unknown): v is State => record(v) && (v.state === 'absent' ? exact(v, ['state'])
  : v.state === 'present' && exact(v, ['state', 'value']) && continuousJson(v.value));

// This records the actual ParameterControls intent; it never discovers a patch
// by comparing configs. The full UI value remains available for legacy fallback.
const parameterIntents = new WeakMap<object, Record<string, unknown>>();
export function continuousParameterPatch(continuous: NonNullable<ClipMeta['continuous']>, params: Record<string, unknown>): Partial<ClipMeta> {
  const patch = { continuous: { ...continuous, params: { ...continuous.params, ...params } } };
  parameterIntents.set(patch.continuous, structuredClone(params));
  return patch;
}
export function continuousParameterIntent(value: object): Record<string, unknown> | undefined {
  return parameterIntents.get(value);
}

export function isContinuousHistoryBatch(commands: readonly EditCommand[]): boolean {
  return commands.length > 0 && commands.every(c => {
    if (c.op !== 'clip.set-continuous' || !scoped(c.select) || c.resolved?.length !== 1 || c.resolved[0] !== c.select
      || !record(c.args) || Object.keys(c.args).length !== 1 || !record(c.expect) || !exact(c.expect, ['continuous']) || !tagged(c.expect.continuous)) return false;
    if (own(c.args, 'continuous')) return validContinuous(c.args.continuous);
    if (own(c.args, 'clear')) return c.args.clear === true;
    return own(c.args, 'params') && record(c.args.params) && Object.keys(c.args.params).length > 0 && continuousJson(c.args.params)
      && c.expect.continuous.state === 'present' && validContinuous(c.expect.continuous.value);
  }) && new Set(commands.map(c => c.select)).size === commands.length;
}
export function isContinuousHistoryInverse(c: EditCommand | undefined): boolean {
  if (!c || c.op !== 'timeline.inverse' || c.select !== null || !record(c.args) || !exact(c.args, ['publication', 'writes'])
    || typeof c.args.publication !== 'string' || !c.args.publication || !Array.isArray(c.args.writes) || !c.args.writes.length) return false;
  const writes = c.args.writes;
  return writes.every((w: unknown) => record(w) && exact(w, ['id', 'path', 'before', 'after']) && scoped(w.id)
    && w.path === 'continuous' && tagged(w.before) && tagged(w.after) && !sameContinuous(w.before, w.after))
    && new Set(writes.map(w => w.id)).size === writes.length;
}
export function continuousHistoryInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isContinuousHistoryInverse(commands[0]);
  if (!undo && !isContinuousHistoryBatch(commands)) return undefined;
  const expected: Write[] = undo ? commands[0].args.writes as Write[] : commands.map(c => {
    const before = c.expect!.continuous as State;
    const after: State = own(c.args, 'clear') ? { state: 'absent' } : { state: 'present', value: own(c.args, 'continuous') ? c.args.continuous
      : { ...(before as { value: Record<string, unknown> }).value,
        params: { ...((before as { value: { params?: object } }).value.params), ...(c.args.params as object) } } };
    return { id: c.select!, path: 'continuous', before, after };
  }).filter(w => !sameContinuous(w.before, w.after));
  const writes = result.change?.direct_writes;
  if (!Array.isArray(writes)) return undefined;
  if (result.status === 'no_change') return !expected.length && !writes.length && result.accepted_publication_id === null ? null : undefined;
  if (result.status !== 'accepted' || typeof result.accepted_publication_id !== 'string' || !result.accepted_publication_id
    || undo && result.accepted_publication_id === commands[0].args.publication
    || !expected.length || writes.length !== expected.length) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: writes.map(w => record(w) ? { ...structuredClone(w), before: structuredClone(w.after), after: structuredClone(w.before) } : w) } };
  if (!isContinuousHistoryInverse(inverse) || !writes.every(w => record(w) && expected.some(e => e.id === w.id
    && e.path === w.path && sameContinuous(e.before, w.before) && sameContinuous(e.after, w.after)))) return undefined;
  validateEditCommand(inverse); return inverse;
}
