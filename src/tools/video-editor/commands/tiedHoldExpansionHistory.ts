import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const parentClip = (value: unknown): value is string => typeof value === 'string' && /^parent\/clip:[^/\s]+$/.test(value);

/** Only the admitted tiny parent hold command owns this native receipt path. */
export function isTiedHoldExpansionCommand(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'clip.set-duration' || !parentClip(command.select)
    || command.resolved?.length !== 1 || command.resolved[0] !== command.select
    || command.args.seconds !== 0.5 || Object.keys(command.args).some((key) => !['seconds', 'relation_choices'].includes(key))
    || !Array.isArray(command.args.relation_choices) || command.args.relation_choices.length !== 1) return false;
  const captured = command.expect?.[''];
  const clip = captured?.state === 'present' ? captured.value : undefined;
  if (!record(clip) || command.select !== `parent/clip:${clip.id}` || clip.clipType !== 'hold'
    || typeof clip.hold !== 'number' || !Number.isFinite(clip.hold) || clip.hold <= 0 || clip.hold >= 0.5
    || !record(clip.app) || !record(clip.app.astrid) || typeof clip.app.astrid.until !== 'string') return false;
  const choice = command.args.relation_choices[0];
  if (!record(choice) || choice.target !== command.select || choice.edge !== 'end') return false;
  if (choice.choice === 'detach') return Object.keys(choice).length === 3;
  if (!['adjust-offset', 're-anchor'].includes(String(choice.choice))
    || typeof choice.offset_seconds !== 'number' || !Number.isFinite(choice.offset_seconds)
    || !Number.isSafeInteger(choice.offset_frames)) return false;
  return choice.choice === 're-anchor'
    ? Object.keys(choice).length === 6 && typeof choice.anchor === 'string' && Boolean(choice.anchor.trim())
    : Object.keys(choice).length === 5;
}

/** Astrid records only authored end fields here. Resolved hold geometry is a
 * consequence, so neither geometry nor a snapshot becomes a local Undo diff.
 */
export function isTiedHoldExpansionInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || typeof command.args.publication !== 'string' || !command.args.publication
    || Object.keys(command.args).some((key) => !['publication', 'writes'].includes(key))
    || !Array.isArray(command.args.writes) || !command.args.writes.length || command.args.writes.length > 2) return false;
  const writes = command.args.writes;
  return writes.every((write: unknown) => record(write) && parentClip(write.id)
    && write.id === writes[0].id && ['intent.until', 'intent.for'].includes(String(write.path))
    && Object.keys(write).length === 4 && Object.keys(write).every((key) => ['id', 'path', 'before', 'after'].includes(key))
    && [write.before, write.after].every((state) => record(state)
      && (state.state === 'absent' ? Object.keys(state).length === 1
        : state.state === 'present' && Object.prototype.hasOwnProperty.call(state, 'value') && Object.keys(state).length === 2)))
    && new Set(writes.map((write) => write.path)).size === writes.length;
}

export function tiedHoldExpansionInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  if (commands.length !== 1 || !(isTiedHoldExpansionCommand(commands[0]) || isTiedHoldExpansionInverse(commands[0]))) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: {
    publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map((write) => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write),
  } };
  if (!isTiedHoldExpansionInverse(inverse)) return undefined;
  const source = commands[0];
  const owner = source.op === 'clip.set-duration' ? source.select : (source.args.writes as Array<{ id: string }>)[0].id;
  if ((inverse.args.writes as Array<{ id: string }>).some((write) => write.id !== owner)) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
