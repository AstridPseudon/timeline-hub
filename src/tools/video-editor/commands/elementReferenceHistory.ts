import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import type { TimelineConfig } from '../types/index.ts';
import { canonicalJsonStringify, sha256Hex } from '../data/typed/timelineBundle.ts';

const record = (v: unknown): v is Record<string, any> => v !== null && typeof v === 'object' && !Array.isArray(v);
const own = (v: object, k: string) => Object.prototype.hasOwnProperty.call(v, k);
const equal = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);
export type ElementState = { state: 'absent' } | { state: 'present'; value: any };
const fields = ['elementRef', 'params', 'entrance'] as const;
const parentClip = (v: unknown): v is string => typeof v === 'string' && /^parent\/clip:[^/\s]+$/.test(v);
const tagged = (v: unknown): v is ElementState => record(v) && (v.state === 'absent'
  ? Object.keys(v).length === 1 : v.state === 'present' && own(v, 'value') && Object.keys(v).length === 2);
const state = (v: Record<string, any>, k: string): ElementState => own(v, k) && v[k] !== undefined
  ? { state: 'present', value: structuredClone(v[k]) } : { state: 'absent' };
const wire = (call: EditCommand) => { try { validateEditCommand(call); return true; } catch { return false; } };
type Write = { id: string; path: string; before: ElementState; after: ElementState; order?: string[] };
type ReferenceArgs = {
  intent: 'assign' | 'update' | 'clear' | 'overlay';
  fields: Record<typeof fields[number], ElementState>;
  source_path: string; source: ElementState;
  clip_id: string; track: string; at: number; duration: number; clip_type: string;
  expected_order: string[]; insertion_index: number;
  writes: Write[]; publication: string;
};
const sourcePath = (v: unknown): v is string => typeof v === 'string'
  && /^(?:config\.app|config\.app\.elements|config\.app\.elements\.[A-Za-z_][\w-]*|config\.app\.elements\["(?:[^"\\]|\\.)+"\])$/.test(v);

/** Capture full opaque source rows, including container absence, from the authored base. */
export async function elementReferenceCommand(before: TimelineConfig, after: TimelineConfig, clipId: string,
  intent: 'assign' | 'update' | 'clear' | 'overlay', paramsMode: 'keep' | 'merge' | 'replace' | 'clear'): Promise<EditCommand> {
  const old = before.clips.find(row => row.id === clipId);
  const next = after.clips.find(row => row.id === clipId);
  if (!next || (intent !== 'overlay' && !old) || next.app?.canonical || old?.app?.canonical
    || clipId.includes('/') || !clipId || before.clips.filter(row => row.id === clipId).length > 1) {
    throw new Error('Element command requires an exact parent clip owner.');
  }
  const ref = intent === 'clear' ? old?.elementRef : next.elementRef;
  const app = record(before.app) ? before.app : undefined;
  const elements = app && record(app.elements) ? app.elements : undefined;
  const path = !app ? 'config.app' : !elements || !ref ? 'config.app.elements'
    : /^[A-Za-z_][\w-]*$/.test(ref.id) ? `config.app.elements.${ref.id}` : `config.app.elements[${JSON.stringify(ref.id)}]`;
  const get = (config: TimelineConfig): ElementState => path === 'config.app' ? state(config, 'app')
    : path === 'config.app.elements' ? record(config.app) ? state(config.app, 'elements') : { state: 'absent' }
    : record(config.app) && record(config.app.elements) ? state(config.app.elements, ref!.id) : { state: 'absent' };
  const rows = record(after.app) && record(after.app.elements) ? after.app.elements : {};
  const row = ref ? state(rows, ref.id) : undefined;
  const rowJson = row ? canonicalJsonStringify(row) : undefined;
  const binding = ref ? { owner: 'parent', key: ref.id, reference: structuredClone(ref), row,
    row_json: rowJson!, content_digest: `sha256:${await sha256Hex(rowJson!)}` } : null;
  const select = `parent/clip:${clipId}`;
  const args: Record<string, any> = { intent, fields: Object.fromEntries(fields.map(key => [key, state(next, key)])),
    params_mode: paramsMode, binding, source_path: path, source: get(after) };
  const expect: NonNullable<EditCommand['expect']> = { [`parent::${path}`]: get(before) };
  if (intent === 'overlay') {
    const order = before.clips.map(row => row.id);
    Object.assign(args, { clip_id: clipId, track: next.track, at: next.at, duration: next.hold,
      time_domain: 'timeline-seconds', clip_type: next.clipType, expected_order: order,
      insertion_index: after.clips.findIndex(row => row.id === clipId) });
    expect[`${select}::`] = { state: 'absent' };
    expect[`${select}::clip_order`] = { state: 'present', value: order.map(id => `parent/clip:${id}`) };
    const tracks = before.tracks?.filter(row => row.id === next.track) ?? [];
    if (tracks.length !== 1) throw new Error('Element overlay requires an exact canonical track.');
    expect[`parent/track:${next.track}::kind`] = { state: 'present', value: tracks[0].kind };
  } else for (const key of fields) expect[key] = state(old!, key);
  const call: EditCommand = { op: intent === 'overlay' ? 'timeline.add' : 'clip.set-element',
    select: intent === 'overlay' ? null : select, resolved: [select], args, expect,
    ...(intent === 'overlay' ? { created: [select] } : {}) };
  validateEditCommand(call);
  return call;
}

export function isElementReferenceBatch(calls: readonly EditCommand[]): boolean {
  return calls.length === 1 && calls.every(call => {
    const a = call.args as unknown as ReferenceArgs;
    const overlay = call.op === 'timeline.add' && a?.intent === 'overlay';
    return wire(call) && (overlay || call.op === 'clip.set-element' && ['assign', 'update', 'clear'].includes(a?.intent))
      && (overlay ? call.select === null && call.created?.length === 1 && call.resolved?.[0] === call.created[0]
        : parentClip(call.select) && call.resolved?.[0] === call.select)
      && call.resolved?.length === 1 && parentClip(call.resolved[0])
      && record(a.fields) && Object.keys(a.fields).length === 3 && fields.every(k => tagged(a.fields[k]))
      && sourcePath(a.source_path) && tagged(a.source) && tagged(call.expect?.[`parent::${a.source_path}`])
      && (overlay ? tagged(call.expect?.[`${call.created![0]}::`]) && Array.isArray(a.expected_order)
        && Number.isInteger(a.insertion_index) : fields.every(k => tagged(call.expect?.[k])));
  });
}

function writesOf(v: unknown): v is Write[] {
  return Array.isArray(v) && v.length > 0 && v.every(w => record(w) && typeof w.path === 'string'
    && (w.id === 'parent' ? sourcePath(w.path) : parentClip(w.id) && (fields.includes(w.path as any)
      || w.path === '' && [w.before, w.after].some(s => tagged(s) && s.state === 'present' && record(s.value) && record(s.value.elementRef))))
    && Object.keys(w).every(k => ['id', 'path', 'before', 'after', 'order'].includes(k))
    && tagged(w.before) && tagged(w.after) && !equal(w.before, w.after)
    && (w.order === undefined || w.path === '' && Array.isArray(w.order) && w.order.every(parentClip)
      && new Set(w.order).size === w.order.length && w.order.includes(w.id)))
    && new Set(v.map(w => `${w.id}::${w.path}`)).size === v.length;
}
export function isElementReferenceInverse(call: EditCommand | undefined): boolean {
  return !!call && wire(call) && call.op === 'timeline.inverse' && call.select === null
    && Object.keys(call.args).length === 2 && typeof call.args.publication === 'string' && !!call.args.publication
    && writesOf(call.args.writes);
}

export function elementReferenceInverse(calls: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const forward = isElementReferenceBatch(calls);
  if (!forward && !(calls.length === 1 && isElementReferenceInverse(calls[0]))) return undefined;
  const call = calls[0], a = call.args as unknown as ReferenceArgs;
  const expected: Write[] = forward ? (() => {
    const sid = call.resolved![0];
    const writes: Write[] = [{ id: 'parent', path: a.source_path, before: call.expect![`parent::${a.source_path}`], after: a.source }];
    if (a.intent === 'overlay') {
      const value: Record<string, any> = { id: a.clip_id, at: a.at, hold: a.duration, track: a.track, clipType: a.clip_type };
      for (const key of fields) if (a.fields[key].state === 'present') value[key] = a.fields[key].value;
      writes.push({ id: sid, path: '', before: { state: 'absent' }, after: { state: 'present', value } });
    } else for (const path of fields) writes.push({ id: sid, path, before: call.expect![path], after: a.fields[path] });
    return writes.filter(w => !equal(w.before, w.after));
  })() : a.writes;
  const writes = result.change?.direct_writes;
  if (result.status === 'no_change') return expected.length === 0 && writes?.length === 0 ? null : undefined;
  if (result.status !== 'accepted' || !result.accepted_publication_id || !writesOf(writes)
    || writes.length !== expected.length || expected.some(w => !writes.some(row => row.id === w.id && row.path === w.path
      && equal(row.before, w.before) && equal(row.after, w.after)))
    || !forward && result.accepted_publication_id === a.publication) return undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: writes.map(w => {
      const prior = forward ? undefined : expected.find(p => p.id === w.id && p.path === w.path);
      const order = forward && a.intent === 'overlay' && w.path === '' ? [...a.expected_order] : undefined;
      if (order) order.splice(a.insertion_index, 0, a.clip_id);
      return { ...structuredClone(w), before: structuredClone(w.after), after: structuredClone(w.before),
        ...(order ? { order: order.map(id => `parent/clip:${id}`) } : prior?.order ? { order: structuredClone(prior.order) } : {}) };
    }),
  } };
  return isElementReferenceInverse(inverse) ? inverse : undefined;
}
