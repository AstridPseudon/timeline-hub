import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import { TRACK_SCALE_BAKE_MARKER } from '../lib/timeline-domain.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const trackId = (value: unknown): value is string => typeof value === 'string' && /^parent\/track:[^/\s]+$/.test(value);
const tagged = (value: unknown): value is { state: 'absent' } | { state: 'present'; value: unknown } => record(value)
  && (value.state === 'absent' ? Object.keys(value).length === 1
    : value.state === 'present' && Object.keys(value).length === 2 && Object.prototype.hasOwnProperty.call(value, 'value'));
const field = (path: unknown): path is string => typeof path === 'string' && (['label', 'role', 'scale', 'fit', 'opacity', 'volume', 'muted', 'blendMode'].includes(path)
  || /^app\.[A-Za-z0-9_-]+$/.test(path) && !['__proto__', 'constructor', 'prototype', TRACK_SCALE_BAKE_MARKER].includes(path.slice(4)));
const order = (value: unknown): value is string[] => Array.isArray(value) && value.length > 0
  && value.every(id => trackId(id) && !id.includes('::')) && new Set(value).size === value.length;
const sameOrder = (a: unknown, b: unknown) => order(a) && order(b) && a.length === b.length && a.every((id, i) => id === b[i]);
const permutation = (id: unknown, before: unknown, after: unknown) => order(before) && order(after)
  && before.includes(String(id)) && before.length === after.length && before.every(id => after.includes(id));
const orderWrite = (write: unknown): write is { id: string; path: 'track_order'; before: { state: 'present'; value: string[] }; after: { state: 'present'; value: string[] } } => record(write)
  && trackId(write.id) && write.path === 'track_order' && Object.keys(write).length === 4
  && tagged(write.before) && tagged(write.after) && write.before.state === 'present' && write.after.state === 'present'
  && permutation(write.id, write.before.value, write.after.value) && !sameOrder(write.before.value, write.after.value);

/** Parent track creation, explicit property patches and captured full-order reorders. */
export function isTrackHistoryBatch(commands: readonly EditCommand[]): boolean {
  if (!commands.length || !commands.every(command => trackId(command.select))) return false;
  if (commands.length === 1 && commands[0].op === 'timeline.reorder') {
    const command = commands[0];
    const expected = command.expect?.[`${command.select}::track_order`] ?? command.expect?.track_order;
    return Object.keys(command.args).length === 2 && !command.created?.length
      && permutation(command.select, command.args.expected_order, command.args.order)
      && tagged(expected) && expected.state === 'present' && sameOrder(expected.value, command.args.expected_order);
  }
  if (commands.length === 1 && commands[0].op === 'timeline.add') {
    const command = commands[0]; const row = command.args.track;
    return Object.keys(command.args).length === 1 && record(row) && row.id === command.select!.split(':')[1]
      && command.created?.length === 1 && command.created[0] === command.select
      && command.expect?.[`${command.select}::`]?.state === 'absent';
  }
  return new Set(commands.map(command => command.select)).size === commands.length && commands.every(command => {
    if (command.op !== 'timeline.set' || Object.keys(command.args).length !== 2
      || !record(command.args.values) || !Array.isArray(command.args.clear)) return false;
    const paths = [...Object.keys(command.args.values), ...command.args.clear];
    return paths.length > 0 && new Set(paths).size === paths.length && paths.every(path => field(path)
      && tagged(command.expect?.[`${command.select}::${path}`] ?? command.expect?.[path]));
  });
}

export function isTrackHistoryInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || Object.keys(command.args).length !== 2 || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  if (writes.some((write: unknown) => record(write) && write.path === 'track_order')) return writes.length === 1 && orderWrite(writes[0]);
  return writes.every((write: unknown) => record(write) && trackId(write.id) && Object.keys(write).length === 4
    && Object.keys(write).every(key => ['id', 'path', 'before', 'after'].includes(key)) && tagged(write.before) && tagged(write.after)
    && (write.path === '' ? writes.length === 1 && write.before.state !== write.after.state
      && [write.before, write.after].every(state => state.state === 'absent' || record(state.value) && state.value.id === String(write.id).split(':')[1]) : field(write.path)))
    && new Set(writes.map(write => `${write.id}::${write.path}`)).size === writes.length;
}

export function trackHistoryInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isTrackHistoryInverse(commands[0]);
  if (!undo && !isTrackHistoryBatch(commands)) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  // D156 supplies one direct write on the selected track. Bind both tagged
  // arrays to the admitted command; consequences/config snapshots are not authority.
  const reordered = commands.length === 1 && commands[0].op === 'timeline.reorder';
  const undoOrder = undo && (commands[0].args.writes as unknown[]).some(write => record(write) && write.path === 'track_order');
  if (reordered || undoOrder) {
    const write = result.change.direct_writes[0];
    const expected = reordered ? { id: commands[0].select, before: commands[0].args.expected_order, after: commands[0].args.order }
      : (() => { const row = (commands[0].args.writes as Array<{ id: string; before: { value: unknown }; after: { value: unknown } }>)[0];
        return { id: row.id, before: row.before.value, after: row.after.value }; })();
    if (result.change.direct_writes.length !== 1 || !orderWrite(write) || write.id !== expected.id
      || !sameOrder(write.before.value, expected.before) || !sameOrder(write.after.value, expected.after)) return undefined;
    const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
      writes: [{ ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) }] } };
    validateEditCommand(inverse); return inverse;
  }
  const allowed = undo ? commands[0].args.writes as Array<{ id: string; path: string }>
    : commands.flatMap(command => (command.op === 'timeline.add' ? [''] : [...Object.keys(command.args.values as Record<string, unknown>), ...command.args.clear as string[]])
      .map(path => ({ id: command.select!, path })));
  if (result.change.direct_writes.some(write => !record(write) || !allowed.some(row => row.id === write.id && row.path === write.path))) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map(write => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write),
  } };
  if (!isTrackHistoryInverse(inverse)) return undefined;
  validateEditCommand(inverse); return inverse;
}
