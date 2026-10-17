import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
const own = (value: object, key: string) => Object.prototype.hasOwnProperty.call(value, key);
const tagged = (value: unknown): value is { state: 'absent' } | { state: 'present'; value: unknown } => record(value)
  && (value.state === 'absent' ? Object.keys(value).length === 1
    : value.state === 'present' && own(value, 'value') && Object.keys(value).length === 2);
const sides = ['fade_in', 'fade_out'] as const;
const paths = ['effects', 'effects.fade_in', 'effects.fade_out', 'entrance', 'exit'];

/** Only the existing single-clip coupled fade caller owns this history family. */
export function isFadeHistoryBatch(commands: readonly EditCommand[]): boolean {
  if (commands.length !== 1) return false;
  const command = commands[0]; const args = command.args;
  if (command.op !== 'clip.set-fade' || !scoped(command.select)
    || command.resolved?.length !== 1 || command.resolved[0] !== command.select || !record(args)
    || Object.keys(args).some(key => !['fade_in', 'fade_out', 'clear'].includes(key))) return false;
  const clear = own(args, 'clear') ? args.clear : [];
  if (!Array.isArray(clear) || (own(args, 'clear') && !clear.length)
    || new Set(clear).size !== clear.length || clear.some(key => !sides.includes(key))) return false;
  if (!sides.some(side => own(args, side) || clear.includes(side))) return false;
  if (sides.some(side => own(args, side) && (clear.includes(side)
    || args[side] !== null && (typeof args[side] !== 'number' || !Number.isFinite(args[side]) || args[side] < 0)))) return false;
  if (!['effects', 'entrance', 'exit'].every(path => tagged(command.expect?.[path]))) return false;
  const effects = command.expect!.effects;
  return effects.state === 'absent' || effects.value === null || record(effects.value);
}

export function isFadeHistoryInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || Object.keys(command.args).length !== 2 || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  return writes.every((write: unknown) => record(write) && Object.keys(write).length === 4
    && Object.keys(write).every(key => ['id', 'path', 'before', 'after'].includes(key))
    && scoped(write.id) && paths.includes(String(write.path)) && tagged(write.before) && tagged(write.after))
    && new Set(writes.map(write => write.id)).size === 1
    && new Set(writes.map(write => write.path)).size === writes.length
    && !(writes.some(write => write.path === 'effects') && writes.some(write => String(write.path).startsWith('effects.')));
}

/** Consume D's actual receipt; never derive authored writes from the preview.
 * D uses effects.fade_* for an existing object and effects for absent/null.
 */
export function fadeHistoryInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isFadeHistoryInverse(commands[0]);
  if (!undo && !isFadeHistoryBatch(commands)) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const source = commands[0];
  const allowed = undo ? source.args.writes as Array<{ id: string; path: string }>
    : sides.filter(side => own(source.args, side) || (source.args.clear as string[] | undefined)?.includes(side)).flatMap(side => [
      { id: source.select!, path: side === 'fade_in' ? 'entrance' : 'exit' },
      { id: source.select!, path: source.expect!.effects.state === 'present' && record(source.expect!.effects.value) ? `effects.${side}` : 'effects' },
    ]);
  // Every submitted inverse row represents an authored change. A partial
  // recorder receipt cannot authorize a complete Redo; never fill its gaps.
  if (undo && result.change.direct_writes.length !== allowed.length) return undefined;
  if (result.change.direct_writes.some(write => !record(write) || !allowed.some(row => row.id === write.id && row.path === write.path))) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map(write => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write),
  } };
  if (!isFadeHistoryInverse(inverse)) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
