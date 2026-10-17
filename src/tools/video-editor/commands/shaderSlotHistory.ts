import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { equal, object, shaderLayout, type SlotState } from './shaderSlots.ts';
const exact = (v: Record<string, unknown>, keys: string[]) => Object.keys(v).length === keys.length && keys.every(k => Object.prototype.hasOwnProperty.call(v, k));
const tagged = (v: unknown): v is SlotState => object(v) && (v.state === 'absent' ? exact(v, ['state']) : v.state === 'present' && exact(v, ['state', 'value']));
const owner = (id: unknown): id is string => typeof id === 'string' && (id === 'parent' || /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(id));
type Write = { id: string; path: string; before: SlotState; after: SlotState };
function expected(command: EditCommand): Write | undefined {
  const id = command.op === 'timeline.set-shader-postprocess' ? 'parent' : command.select;
  if (!owner(id)) return;
  const layout = shaderLayout(id);
  if (command.op !== layout.op || (id === 'parent' ? command.select !== null || !!command.resolved?.length
    : command.resolved?.length !== 1 || command.resolved[0] !== id) || !object(command.args) || !exact(command.args, ['shader'])) return;
  const slot = command.expect?.[`${id}::${layout.path}`];
  const app = command.expect?.[`${id}::${layout.app}`];
  if (!tagged(slot) || !object(command.expect) || Object.keys(command.expect).some(k => ![`${id}::${layout.path}`, `${id}::${layout.app}`].includes(k))) return;
  if (app !== undefined && (!tagged(app) || (app.state === 'present' && app.value !== null) || slot.state !== 'absent')) return;
  if (command.args.shader !== null && (!object(command.args.shader) || command.args.shader.scope !== layout.scope)) return;
  return { id, path: app ? layout.app : layout.path, before: app ?? slot,
    after: command.args.shader === null ? app ?? { state: 'absent' } : { state: 'present', value: app ? { [layout.slot]: command.args.shader } : command.args.shader } };
}
export function isShaderSlotBatch(commands: readonly EditCommand[]): boolean { return commands.length === 1 && !!expected(commands[0]); }
function writes(value: unknown): value is Write[] {
  return Array.isArray(value) && value.length === 1 && value.every(w => object(w) && exact(w, ['id', 'path', 'before', 'after']) && owner(w.id)
    && [shaderLayout(w.id).path, shaderLayout(w.id).app].includes(String(w.path)) && tagged(w.before) && tagged(w.after) && !equal(w.before, w.after)
    && (w.path !== shaderLayout(w.id).app || [w.before, w.after].some(state => state.state === 'present' && object(state.value)
      && exact(state.value, [shaderLayout(String(w.id)).slot])) && [w.before, w.after].some(state => state.state === 'absent' || state.value === null)))
    && new Set(value.map(w => `${w.id}::${w.path}`)).size === value.length;
}
export function isShaderSlotInverse(c: EditCommand | undefined): boolean { return !!c && c.op === 'timeline.inverse' && c.select === null && object(c.args)
  && exact(c.args, ['publication', 'writes']) && typeof c.args.publication === 'string' && !!c.args.publication && writes(c.args.writes); }
/** Consume the exact D direct-write closure; Undo and Redo both use accepted receipts. */
export function shaderSlotInverse(commands: readonly EditCommand[], result: { status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] } }): EditCommand | null | undefined {
  const forward = isShaderSlotBatch(commands);
  if (!forward && !(commands.length === 1 && isShaderSlotInverse(commands[0]))) return;
  const rows = forward ? [expected(commands[0])!].filter(w => !equal(w.before, w.after)) : commands[0].args.writes as Write[];
  const actual = result.change?.direct_writes;
  if (result.status === 'no_change') return rows.length === 0 && Array.isArray(actual) && actual.length === 0 ? null : undefined;
  if (result.status !== 'accepted' || !result.accepted_publication_id || !writes(actual) || actual.length !== rows.length
    || rows.some(w => !actual.some(a => equal(a, w))) || (!forward && result.accepted_publication_id === commands[0].args.publication)) return;
  return { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: actual.map(w => ({ ...structuredClone(w), before: structuredClone(w.after), after: structuredClone(w.before) })) } };
}
