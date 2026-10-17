import type { EditCommand } from '@/integrations/runtime/generated.ts';
import type { ShaderEffectRegistryRecord, ShaderEffectRegistrySnapshot } from '../shaders/registry/types.ts';
import { getShaderPassKind } from '../lib/shader-catalog.ts';
import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';

export const object = (v: unknown): v is Record<string, unknown> => v !== null && typeof v === 'object' && !Array.isArray(v);
const own = (v: object, k: string) => Object.prototype.hasOwnProperty.call(v, k);
export const equal = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);
const jsonValue = (value: unknown): boolean => value === null || typeof value === 'string' || typeof value === 'boolean'
  || typeof value === 'number' && Number.isFinite(value) || Array.isArray(value) && value.every(jsonValue)
  || object(value) && [Object.prototype, null].includes(Object.getPrototypeOf(value)) && Object.values(value).every(jsonValue);
export type SlotState = { state: 'absent' } | { state: 'present'; value: unknown };
export const slotState = (v: Record<string, unknown>, key: string): SlotState => own(v, key)
  ? { state: 'present', value: structuredClone(v[key]) } : { state: 'absent' };
export type ShaderOwner = { id: string; value: { app?: unknown } };
export const shaderLayout = (id: string) => id === 'parent'
  ? { scope: 'postprocess', slot: 'shaderPostprocess', path: 'config.app.shaderPostprocess', app: 'config.app', op: 'timeline.set-shader-postprocess' }
  : { scope: 'clip', slot: 'shader', path: 'app.shader', app: 'app', op: 'clip.set-shader' };

/** The actual registry lookup is authoritative for UI selection, never for replay. */
export function selectedShaderRecord(shader: unknown, scope: string, snapshot?: ShaderEffectRegistrySnapshot): ShaderEffectRegistryRecord | undefined {
  if (!object(shader) || !jsonValue(shader) || shader.scope !== scope || typeof shader.shaderId !== 'string' || !shader.shaderId
    || typeof shader.extensionId !== 'string' || typeof shader.contributionId !== 'string' || !shader.contributionId) return;
  for (const field of ['label', 'sourceHash']) if (own(shader, field) && typeof shader[field] !== 'string') return;
  if (own(shader, 'enabled') && typeof shader.enabled !== 'boolean') return;
  for (const field of ['uniforms', 'textures', 'keyframes', 'metadata']) if (own(shader, field) && !object(shader[field])) return;
  if (object(shader.keyframes) && Object.values(shader.keyframes).some(rows => !Array.isArray(rows) || rows.some(row => !object(row)
    || typeof row.time !== 'number' || !Number.isFinite(row.time) || !own(row, 'value') || !['linear', 'hold'].includes(String(row.interpolation))))) return;
  if (object(shader.textures) && Object.values(shader.textures).some(row => !object(row)
    || !['clip-frame', 'static-image-asset', 'live-generated-frame'].includes(String(row.kind)) || (own(row, 'ref') && typeof row.ref !== 'string'))) return;
  const record = snapshot?.get(shader.shaderId, shader.extensionId);
  const matches = snapshot?.records.filter(candidate => candidate.shaderId === shader.shaderId && (candidate.ownerExtensionId ?? '') === shader.extensionId);
  if (!record || matches?.length !== 1 || matches[0] !== record || record.shaderId !== shader.shaderId
    || (record.ownerExtensionId ?? '') !== shader.extensionId || (shader.extensionId === '' && record.provenance !== 'built-in') || record.contributionId !== shader.contributionId
    || getShaderPassKind(record) !== scope || record.status !== 'active') return;
  const diagnostics = [...(record.diagnostics ?? []), ...(snapshot?.diagnostics ?? []).filter(diagnostic => {
    const detail = diagnostic.detail as Record<string, unknown> | undefined;
    return diagnostic.extensionId === shader.extensionId || diagnostic.contributionId === shader.contributionId
      || detail?.shaderId === shader.shaderId || detail?.ownerExtensionId === shader.extensionId || detail?.contributionId === shader.contributionId;
  })];
  return diagnostics.some(d => d.severity === 'error') ? undefined : record;
}

/** Capture before local mutation. Explicit null clears even an orphaned legacy value. */
export function shaderSlotCommand(owner: ShaderOwner, shader: unknown, snapshot?: ShaderEffectRegistrySnapshot): EditCommand | undefined {
  if (owner.id !== 'parent' && !/^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(owner.id)) return;
  const layout = shaderLayout(owner.id);
  const app = owner.value.app;
  if (app !== undefined && app !== null && !object(app)) return;
  if (shader !== null && !selectedShaderRecord(shader, layout.scope, snapshot)) return;
  const expect: NonNullable<EditCommand['expect']> = { [`${owner.id}::${layout.path}`]: object(app) ? slotState(app, layout.slot) : { state: 'absent' } };
  if (!object(app)) expect[`${owner.id}::${layout.app}`] = slotState(owner.value as Record<string, unknown>, 'app');
  return structuredClone({ op: layout.op, select: owner.id === 'parent' ? null : owner.id,
    ...(owner.id === 'parent' ? {} : { resolved: [owner.id] }), args: { shader }, expect });
}
