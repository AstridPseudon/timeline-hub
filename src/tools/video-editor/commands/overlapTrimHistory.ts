import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);

/** The bounded overlap consumer's command, also used to own its receipt/undo. */
export function isOverlapTrimCommand(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'clip.trim' || !scoped(command.select)
    || command.resolved?.length !== 1 || command.resolved[0] !== command.select
    || !record(command.args) || Object.keys(command.args).some((key) => !['out_s', 'relation_choices'].includes(key))
    || typeof command.args.out_s !== 'number' || !Number.isFinite(command.args.out_s)
    || !Array.isArray(command.args.relation_choices) || command.args.relation_choices.length !== 1) return false;
  const choice = command.args.relation_choices[0];
  return record(choice) && scoped(choice.target) && choice.target !== command.select
    && choice.target.split('/')[0] === command.select.split('/')[0] && choice.edge === 'start'
    && ['keep', 'detach', 'adjust-offset', 're-anchor'].includes(String(choice.choice));
}

function isLeftTrimChoices(value: unknown, primary: string): boolean {
  return Array.isArray(value) && value.length > 0
    && value.every((choice) => record(choice) && scoped(choice.target) && choice.target !== primary
      && choice.target.split('/')[0] === primary.split('/')[0] && choice.edge === 'start'
      && ['keep', 'detach', 'adjust-offset', 're-anchor'].includes(String(choice.choice)))
    && new Set(value.map((choice) => choice.target)).size === value.length;
}

/** Exactly the admitted source-in trim followed by a frame nudge. */
export function isOverlapTrimBatch(commands: readonly EditCommand[]): boolean {
  if (commands.length === 1) return isOverlapTrimCommand(commands[0]);
  if (commands.length !== 2) return false;
  const [trim, nudge] = commands;
  return trim.op === 'clip.trim' && scoped(trim.select) && trim.select.startsWith('parent/')
    && trim.resolved?.length === 1 && trim.resolved[0] === trim.select
    && Object.keys(trim.args).length === 2
    && ['in_s', 'out_s'].every((key) => typeof trim.args[key] === 'number' && Number.isFinite(trim.args[key]))
    && (trim.args.in_s as number) >= 0 && (trim.args.in_s as number) < (trim.args.out_s as number)
    && nudge.op === 'clip.nudge' && nudge.select === trim.select
    && nudge.resolved?.length === 1 && nudge.resolved[0] === trim.select
    && Object.keys(nudge.args).length === 2 && Number.isSafeInteger(nudge.args.frames) && nudge.args.frames !== 0
    && isLeftTrimChoices(nudge.args.relation_choices, trim.select);
}

/** Accept only the direct fields this bounded producer actually records.
 * Consequence rows, whole documents and locally synthesized diffs never enter
 * history. Runtime validates the publication and per-write expectations again.
 */
export function isOverlapTrimInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || typeof command.args.publication !== 'string' || !command.args.publication
    || Object.keys(command.args).some((key) => !['publication', 'writes'].includes(key))
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  if (!writes.every((write: unknown) => record(write) && scoped(write.id) && typeof write.path === 'string'
    && Object.keys(write).every((key) => ['id', 'path', 'before', 'after'].includes(key))
    && [write.before, write.after].every((state) => record(state)
      && (state.state === 'absent' ? Object.keys(state).length === 1
        : state.state === 'present' && Object.prototype.hasOwnProperty.call(state, 'value') && Object.keys(state).length === 2)))) return false;
  const left = writes.some((write) => write.path === 'from');
  const primaryIds = [...new Set(writes.filter((write) => write.path === (left ? 'from' : 'to')).map((write) => write.id))];
  if (primaryIds.length !== 1 || (left && !primaryIds[0].startsWith('parent/'))) return false;
  const ids = [...new Set(writes.map((write) => write.id))];
  return (left || ids.length <= 2) && ids.every((id) => id.split('/')[0] === primaryIds[0].split('/')[0])
    && new Set(writes.map((write) => `${write.id}::${write.path}`)).size === writes.length
    && writes.every((write) => (write.id === primaryIds[0] ? (left ? ['from', 'at', 'hold'] : ['to', 'hold']) : ['at', 'intent.on', 'intent.fixed_start']).includes(write.path));
}

export function overlapTrimInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  if (!(isOverlapTrimBatch(commands) || (commands.length === 1 && isOverlapTrimInverse(commands[0])))) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: {
    publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map((write) => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write),
  } };
  if (!isOverlapTrimInverse(inverse)) return undefined;
  const source = commands[0];
  const allowedIds = source.op === 'clip.trim'
    ? [source.select, ...((commands.length === 2 ? commands[1] : source).args.relation_choices as Array<{ target: string }>).map((choice) => choice.target)]
    : (source.args.writes as Array<{ id: string }>).map((write) => write.id);
  if (source.op === 'clip.trim') {
    const left = commands.length === 2;
    const writes = inverse.args.writes as Array<{ id: string; path: string }>;
    if (!writes.some((write) => write.id === source.select && write.path === (left ? 'from' : 'to'))
      || writes.some((write) => !(write.id === source.select
        ? (left ? ['from', 'at', 'hold'] : ['to', 'hold'])
        : ['at', 'intent.on', 'intent.fixed_start']).includes(write.path))) return undefined;
  } else {
    const sourceWrites = source.args.writes as Array<{ id: string; path: string }>;
    // A left-trim inverse can only reverse the recorded field identities. It
    // cannot promote a dependent to primary or acquire another dependent field.
    if (sourceWrites.some((write) => write.path === 'from')
      && (inverse.args.writes as Array<{ id: string; path: string }>).some((write) =>
        !sourceWrites.some((original) => original.id === write.id && original.path === write.path))) return undefined;
  }
  if ((inverse.args.writes as Array<{ id: string }>).some((write) => !allowedIds.includes(write.id))) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
