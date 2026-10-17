import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const parentClip = (value: unknown): value is string => typeof value === 'string' && /^parent\/clip:[^/\s]+$/.test(value);
const own = (value: object, key: string) => Object.prototype.hasOwnProperty.call(value, key);
const fields = ['transition', 'elementRef'] as const;
type State = { state: 'absent' } | { state: 'present'; value: unknown };
type Write = { id: string; path: string; before: State; after: State };
const tagged = (value: unknown): value is State => record(value) && (value.state === 'absent'
  ? Object.keys(value).length === 1
  : value.state === 'present' && Object.keys(value).length === 2 && own(value, 'value'));

// Compare JSON values without making object-key order part of field identity.
function equal(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (Array.isArray(a) || Array.isArray(b)) return Array.isArray(a) && Array.isArray(b)
    && a.length === b.length && a.every((value, index) => equal(value, b[index]));
  return record(a) && record(b) && Object.keys(a).length === Object.keys(b).length
    && Object.keys(a).every(key => own(b, key) && equal(a[key], b[key]));
}

function validWire(command: EditCommand): boolean {
  try { validateEditCommand(command); return true; } catch { return false; }
}

/** Parent assignment/update and captured bound clears. Null and occurrence
 * edits retain their existing behavior. No identity comes from config.
 */
export function isTransitionAssignmentBatch(commands: readonly EditCommand[]): boolean {
  const clearing = commands.some(command => record(command?.args) && own(command.args, 'clear'));
  return commands.length > 0 && new Set(commands.map(command => command?.select)).size === commands.length
    && commands.every(command => {
      if (!validWire(command) || command.op !== 'clip.set-transition' || !parentClip(command.select)
        || command.resolved?.length !== 1 || command.resolved[0] !== command.select
        || !record(command.args) || Object.keys(command.args).some(key => !(clearing ? ['clear'] : ['transition', 'elementRef', 'from_clip']).includes(key))
        || !fields.every(field => tagged(command.expect?.[field]))) return false;
      if (clearing) {
        const previous = command.expect!.transition;
        const binding = command.expect!.elementRef;
        return command.args.clear === true && previous.state === 'present' && record(previous.value)
          && binding.state === 'present' && record(binding.value)
          && typeof previous.value.type === 'string' && !!previous.value.type
          && typeof previous.value.revision === 'string' && !!previous.value.revision
          && !previous.value.revision.startsWith('draft-')
          && previous.value.type === binding.value.id && previous.value.revision === binding.value.revision
          && (binding.value.kind === undefined || ['transition', 'transitions'].includes(String(binding.value.kind)));
      }
      const transition = command.args.transition;
      const reference = command.args.elementRef;
      if (!record(transition) || !record(reference) || typeof transition.type !== 'string' || !transition.type
        || typeof transition.revision !== 'string' || !transition.revision || transition.revision.startsWith('draft-')
        || typeof transition.duration !== 'number' || !Number.isFinite(transition.duration) || transition.duration <= 0
        || (own(transition, 'params') && transition.params !== null && !record(transition.params))
        || reference.id !== transition.type || reference.revision !== transition.revision
        || (reference.kind !== undefined && !['transition', 'transitions'].includes(String(reference.kind)))) return false;
      if (own(command.args, 'from_clip')) return parentClip(command.args.from_clip) && command.args.from_clip !== command.select;
      // The actual update caller retains its captured binding and transition identity.
      const previous = command.expect!.transition;
      const binding = command.expect!.elementRef;
      return previous.state === 'present' && record(previous.value)
        && previous.value.type === transition.type && previous.value.revision === transition.revision
        && binding.state === 'present' && equal(binding.value, reference);
    });
}

function writesOf(value: unknown): value is Write[] {
  return Array.isArray(value) && value.length > 0 && value.every(write => record(write) && parentClip(write.id)
    && fields.includes(write.path as typeof fields[number]) && Object.keys(write).length === 4
    && Object.keys(write).every(key => ['id', 'path', 'before', 'after'].includes(key))
    && tagged(write.before) && tagged(write.after) && !equal(write.before, write.after))
    && new Set(value.map(write => `${write.id}::${write.path}`)).size === value.length;
}

export function isTransitionAssignmentInverse(command: EditCommand | undefined): boolean {
  return !!command && validWire(command) && command.op === 'timeline.inverse' && command.select === null
    && Object.keys(command.args).length === 2 && typeof command.args.publication === 'string' && !!command.args.publication
    && writesOf(command.args.writes);
}

/** The receipt must exactly close the command's changed tagged fields, including
 * every clip in a bulk transaction. Unchanged fields have no D direct-write row.
 * This only validates receipt ownership; Runtime remains the inverse authority.
 */
export function transitionAssignmentInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const forward = isTransitionAssignmentBatch(commands);
  if (!forward && !(commands.length === 1 && isTransitionAssignmentInverse(commands[0]))) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || typeof result.accepted_publication_id !== 'string' || !result.accepted_publication_id
    || !writesOf(result.change?.direct_writes)) return undefined;
  const expected: Write[] = forward ? commands.flatMap(command => fields.flatMap(path => {
    const before = command.expect![path] as State;
    const after: State = command.args.clear === true ? { state: 'absent' } : { state: 'present', value: command.args[path] };
    return equal(before, after) ? [] : [{ id: command.select!, path, before, after }];
  })) : commands[0].args.writes as Write[];
  const writes = result.change.direct_writes;
  if (writes.length !== expected.length || expected.some(write => !writes.some(row => equal(row, write)))
    || (!forward && result.accepted_publication_id === commands[0].args.publication)) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: {
    publication: result.accepted_publication_id,
    writes: writes.map(write => ({ ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) })),
  } };
  return isTransitionAssignmentInverse(inverse) ? inverse : undefined;
}
