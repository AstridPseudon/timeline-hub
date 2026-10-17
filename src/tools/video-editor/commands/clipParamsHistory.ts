import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const exact = (value: Record<string, unknown>, keys: string[]) => Object.keys(value).length === keys.length && keys.every(key => Object.prototype.hasOwnProperty.call(value, key));
const scoped = (value: unknown): value is string => typeof value === 'string' && /^parent\/clip:[^/\s]+$/.test(value);
const param = (value: unknown): value is string => typeof value === 'string' && Boolean(value) && !/[.[\]\s]/.test(value)
  && !['__proto__', 'constructor', 'prototype'].includes(value);
const jsonValue = (value: unknown): boolean => value === null || typeof value === 'string' || typeof value === 'boolean'
  || typeof value === 'number' && Number.isFinite(value) || Array.isArray(value) && value.every(jsonValue)
  || record(value) && Object.values(value).every(jsonValue);
const tagged = (value: unknown): value is { state: 'absent' } | { state: 'present'; value: unknown } => record(value)
  && (value.state === 'absent' ? exact(value, ['state']) : value.state === 'present' && exact(value, ['state', 'value']) && jsonValue(value.value));
const equal = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);

/** W64's existing parent full-map caller only. No omission-to-clear inference. */
export function isClipParamsHistoryBatch(commands: readonly EditCommand[]): boolean {
  return commands.length > 0 && commands.every(command => command.op === 'clip.set-param' && scoped(command.select)
    && command.select === commands[0].select && command.resolved?.length === 1 && command.resolved[0] === command.select
    && record(command.args) && exact(command.args, ['path', 'value']) && param(command.args.path) && jsonValue(command.args.value)
    && record(command.expect) && exact(command.expect, [`params.${command.args.path}`]) && tagged(command.expect[`params.${command.args.path}`]))
    && new Set(commands.map(command => command.args.path)).size === commands.length;
}

/** Only direct params.<key> writes with exact tagged presence/null semantics. */
export function isClipParamsHistoryInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || !exact(command.args, ['publication', 'writes']) || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  return writes.every((write: unknown) => record(write) && exact(write, ['id', 'path', 'before', 'after']) && scoped(write.id)
    && write.id === writes[0].id && typeof write.path === 'string' && write.path.startsWith('params.') && param(write.path.slice(7))
    && tagged(write.before) && tagged(write.after) && !equal(write.before, write.after))
    && new Set(writes.map(write => write.path)).size === writes.length;
}

export function clipParamsHistoryInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isClipParamsHistoryInverse(commands[0]);
  if (!undo && !isClipParamsHistoryBatch(commands)) return undefined;
  const expected = undo ? commands[0].args.writes as Array<{ id: string; path: string; before: unknown; after: unknown }>
    : commands.map(command => ({ id: command.select!, path: `params.${command.args.path}`,
      before: command.expect![`params.${command.args.path}`], after: { state: 'present', value: command.args.value } }))
      .filter(write => !equal(write.before, write.after));
  const writes = result.change.direct_writes;
  if (!Array.isArray(writes)) return undefined;
  if (result.status === 'no_change') return !expected.length && !writes.length ? null : undefined;
  if (result.status !== 'accepted' || !result.accepted_publication_id || !expected.length || writes.length !== expected.length
    || !writes.every(write => record(write) && exact(write, ['id', 'path', 'before', 'after'])
      && tagged(write.before) && tagged(write.after) && expected.some(row => row.id === write.id && row.path === write.path
        && equal(row.before, write.before) && equal(row.after, write.after)))) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: writes.map(write => { const row = write as Record<string, unknown>; return { ...structuredClone(row), before: structuredClone(row.after), after: structuredClone(row.before) }; }),
  } };
  if (!isClipParamsHistoryInverse(inverse)) return undefined;
  validateEditCommand(inverse); return inverse;
}
