import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const fields: Record<string, string> = {
  opacity: 'opacity', volume: 'volume', crop_top: 'cropTop', crop_right: 'cropRight', crop_bottom: 'cropBottom', crop_left: 'cropLeft',
};
const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
type State = { state: 'absent' } | { state: 'present'; value: number };
type Write = { id: string; path: string; before: State; after: State };
const tagged = (value: unknown): value is State => record(value) && (value.state === 'absent' ? Object.keys(value).length === 1
  : value.state === 'present' && Object.keys(value).length === 2 && typeof value.value === 'number' && Number.isFinite(value.value));
const same = (a: State, b: State) => a.state === b.state && (a.state === 'absent' || b.state === 'present' && a.value === b.value);
const key = (write: Pick<Write, 'id' | 'path'>) => `${write.id}::${write.path}`;

/** Only authored numeric style writes emitted by W63. Placement, clears and
 * composite effects keep their existing history/fallback owners. */
export function isClipLookStyleBatch(commands: readonly EditCommand[]): boolean {
  const keys: string[] = [];
  return commands.length > 0 && commands.every(command => {
    if (command.op !== 'clip.set-look' || !scoped(command.select) || !record(command.args)
      || command.resolved?.length !== 1 || command.resolved[0] !== command.select || !record(command.expect)) return false;
    const args = Object.entries(command.args);
    if (!args.length || Object.keys(command.expect).length !== args.length) return false;
    return args.every(([name, value]) => {
      const path = fields[name];
      if (!path || typeof value !== 'number' || !Number.isFinite(value)) return false;
      const expectation = command.expect![path] ?? command.expect![`${command.select}::${path}`];
      keys.push(`${command.select}::${path}`);
      return tagged(expectation);
    });
  }) && new Set(commands.map(command => command.select!.split('/')[0])).size === 1 && new Set(keys).size === keys.length;
}

export function isClipLookStyleInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || Object.keys(command.args).length !== 2 || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  return writes.every((write: unknown) => record(write) && Object.keys(write).length === 4
    && ['id', 'path', 'before', 'after'].every(name => Object.prototype.hasOwnProperty.call(write, name))
    && scoped(write.id) && Object.values(fields).includes(String(write.path)) && tagged(write.before) && tagged(write.after)
    && !same(write.before, write.after))
    && new Set(writes.map(write => write.id.split('/')[0])).size === 1 && new Set(writes.map(key)).size === writes.length;
}

/** Receipt states, never config differences, are the sole inverse authority.
 * Exact coverage permits omitted no-op fields but rejects missing changed fields. */
export function clipLookStyleInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isClipLookStyleInverse(commands[0]);
  if (!undo && !isClipLookStyleBatch(commands)) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id || !Array.isArray(result.change.direct_writes)) return undefined;
  const expected: Write[] = undo ? commands[0].args.writes as Write[] : commands.flatMap(command => Object.entries(command.args).map(([name, value]) => {
    const path = fields[name];
    return { id: command.select!, path, before: (command.expect![path] ?? command.expect![`${command.select}::${path}`]) as State,
      after: { state: 'present' as const, value: value as number } };
  })).filter(write => !same(write.before, write.after));
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map(write => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write),
  } };
  if (!isClipLookStyleInverse(inverse) || result.change.direct_writes.length !== expected.length) return undefined;
  if (!(result.change.direct_writes as Write[]).every(write => expected.some(row => key(row) === key(write)
    && same(row.before, write.before) && same(row.after, write.after)))) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
