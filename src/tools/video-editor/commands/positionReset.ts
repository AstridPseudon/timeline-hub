import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

/** Complete D W32 top-level geometry contract; element params are unrelated. */
export const positionResetFields = {
  position_x: 'x', position_y: 'y', position_width: 'width', position_height: 'height',
  crop_top: 'cropTop', crop_bottom: 'cropBottom', crop_left: 'cropLeft', crop_right: 'cropRight',
} as const;
const paths = Object.values(positionResetFields);
const keys = Object.keys(positionResetFields);
const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const exact = (value: Record<string, unknown>, names: readonly string[]) => Object.keys(value).length === names.length
  && names.every(name => Object.prototype.hasOwnProperty.call(value, name));
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
type State = { state: 'absent' } | { state: 'present'; value: number | null };
type Write = { id: string; path: string; before: State; after: State };
const tagged = (value: unknown): value is State => record(value) && (value.state === 'absent' ? exact(value, ['state'])
  : value.state === 'present' && exact(value, ['state', 'value']) && (value.value === null || typeof value.value === 'number' && Number.isFinite(value.value)));
const same = (a: State, b: State) => a.state === b.state && (a.state === 'absent' || b.state === 'present' && a.value === b.value);

export function isPositionResetBatch(commands: readonly EditCommand[]): boolean {
  return commands.length > 0 && commands.every(command => command.op === 'clip.clear' && scoped(command.select)
    && command.resolved?.length === 1 && command.resolved[0] === command.select && record(command.args)
    && exact(command.args, ['keys']) && Array.isArray(command.args.keys) && command.args.keys.length === keys.length
    && command.args.keys.every((key, index) => key === keys[index]) && record(command.expect) && exact(command.expect, paths)
    && paths.every(path => tagged(command.expect![path])))
    && new Set(commands.map(command => command.select)).size === commands.length
    && new Set(commands.map(command => command.select!.split('/')[0])).size === 1;
}

/** All eight guards, including absent→absent, remain in Undo and receipt-only Redo. */
export function isPositionResetInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || !exact(command.args, ['publication', 'writes']) || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const groups = new Map<string, Set<string>>();
  for (const value of command.args.writes) {
    if (!record(value) || !exact(value, ['id', 'path', 'before', 'after']) || !scoped(value.id)
      || !paths.includes(value.path as typeof paths[number]) || !tagged(value.before) || !tagged(value.after)) return false;
    const group = groups.get(value.id) ?? new Set<string>();
    if (group.has(String(value.path))) return false;
    group.add(String(value.path)); groups.set(value.id, group);
  }
  return [...groups.values()].every(group => group.size === paths.length)
    && new Set([...groups.keys()].map(id => id.split('/')[0])).size === 1;
}

export function positionResetInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isPositionResetInverse(commands[0]);
  if (!undo && !isPositionResetBatch(commands)) return undefined;
  const expected: Write[] = undo ? commands[0].args.writes as Write[] : commands.flatMap(command => paths.map(path => ({
    id: command.select!, path, before: command.expect![path] as State, after: { state: 'absent' as const },
  })));
  const writes = result.change.direct_writes;
  if (!Array.isArray(writes) || writes.length !== expected.length) return undefined;
  if (result.status === 'no_change') return expected.every(write => same(write.before, write.after))
    && new Set(writes.map(write => record(write) ? `${write.id}::${write.path}` : '')).size === expected.length
    && writes.every(write => record(write) && exact(write, ['id', 'path', 'before', 'after'])
      && tagged(write.before) && tagged(write.after) && expected.some(row => row.id === write.id && row.path === write.path
        && same(row.before, write.before as State) && same(row.after, write.after as State))) ? null : undefined;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: writes.map(value => record(value) ? { ...structuredClone(value), before: structuredClone(value.after), after: structuredClone(value.before) } : value),
  } };
  if (!isPositionResetInverse(inverse) || !(writes as Write[]).every(write => expected.some(row => row.id === write.id && row.path === write.path
    && same(row.before, write.before) && same(row.after, write.after)))) return undefined;
  validateEditCommand(inverse); return inverse;
}
