import { describe, expect, it } from 'vitest';
import { createShaderEffectRegistry } from '../shaders/registry/ShaderEffectRegistry.ts';
import type { ShaderEffectRegistryRecord } from '../shaders/registry/types.ts';
import { createTimelineClipShaderMetadata, createTimelinePostprocessShaderMetadata } from '../lib/shader-catalog.ts';
import { selectedShaderRecord, shaderSlotCommand } from './shaderSlots.ts';
import { shaderSlotInverse } from './shaderSlotHistory.ts';
const record = (pass: 'clip' | 'postprocess' = 'clip'): ShaderEffectRegistryRecord => ({ ownerExtensionId: 'ext', shaderId: 'wash', contributionId: 'contribution', label: 'Wash', pass,
  source: { kind: 'inline', fragment: 'void main() {}' }, status: 'active', provenance: 'bundled-extension', renderability: { determinism: 'preview-only', capabilities: [] } });
describe('W28 shader slot capture and exact receipts', () => {
  it.each(['clip', 'postprocess'] as const)('%s captures full values without revision or sourceHash, separate owner and container presence', scope => {
    const registry = createShaderEffectRegistry(); registry.register(record(scope));
    const shader = scope === 'clip' ? createTimelineClipShaderMetadata(record(scope)) : createTimelinePostprocessShaderMetadata(record(scope));
    const id = scope === 'clip' ? 'parent/clip:clip-1' : 'parent'; const slot = scope === 'clip' ? 'shader' : 'shaderPostprocess'; const prefix = scope === 'clip' ? '' : 'config.';
    for (const value of [{}, { app: null }, { app: {} }, { app: { [slot]: null, keep: [null, { op: 'clear' }] } }]) {
      const captured = structuredClone(value); const c = shaderSlotCommand({ id, value }, shader, registry.getSnapshot())!;
      expect(c).toBeDefined(); expect(c.select).toBe(scope === 'clip' ? id : null);
      expect(c.expect![`${id}::${prefix}app.${slot}`]).toEqual('app' in value && value.app && slot in value.app ? { state: 'present', value: null } : { state: 'absent' });
      const appState = c.expect![`${id}::${prefix}app`];
      const write = { id, path: `${prefix}app${appState ? '' : `.${slot}`}`, before: appState ?? c.expect![`${id}::${prefix}app.${slot}`], after: { state: 'present', value: appState ? { [slot]: shader } : shader } };
      const inverse = shaderSlotInverse([c], { status: 'accepted', accepted_publication_id: 'pub', change: { direct_writes: [write] } })!;
      expect(inverse.args.writes).toEqual([{ ...write, before: write.after, after: write.before }]);
      expect(shaderSlotInverse([c], { status: 'accepted', accepted_publication_id: 'pub', change: { direct_writes: [{ ...write, id: 'parent/clip:foreign' }] } })).toBeUndefined();
      expect(value).toEqual(captured); expect(c.args.shader).not.toHaveProperty('revision'); expect(c.args.shader).not.toHaveProperty('sourceHash');
    }
  });
  it.each(['missing', 'contribution', 'pass', 'owner', 'inactive', 'error', 'diagnostic', 'ambiguous', 'shape', 'non-json'] as const)('refuses %s assignment/edit and allows orphan clear', kind => {
    const registry = createShaderEffectRegistry(); let r = record();
    if (kind === 'contribution') r = { ...r, contributionId: 'wrong' };
    if (kind === 'pass') r = { ...r, pass: 'postprocess' };
    if (kind === 'owner') r = { ...r, ownerExtensionId: 'other' };
    if (kind === 'inactive') r = { ...r, status: 'inactive' };
    if (kind === 'error') r = { ...r, status: 'error' };
    if (kind === 'diagnostic') r = { ...r, diagnostics: [{ severity: 'error', code: 'bad', message: 'Bad' }] };
    if (kind !== 'missing') registry.register(r);
    const shader = { ...createTimelineClipShaderMetadata(record()), ...(kind === 'shape' ? { uniforms: null } : kind === 'non-json' ? { uniforms: { intensity: NaN } } : {}) };
    const snapshot = registry.getSnapshot(); const s = kind === 'ambiguous' ? { ...snapshot, records: [...snapshot.records, r] } : snapshot;
    expect(selectedShaderRecord(shader, 'clip', s)).toBeUndefined();
    expect(shaderSlotCommand({ id: 'parent/clip:a', value: { app: { shader: { legacy: true } } } }, shader, s)).toBeUndefined();
    expect(shaderSlotCommand({ id: 'parent/clip:a', value: { app: { shader: { legacy: true } } } }, null)?.expect).toEqual({ 'parent/clip:a::app.shader': { state: 'present', value: { legacy: true } } });
  });
  it('permits an empty extension ID only for an actual built-in record', () => {
    const registry = createShaderEffectRegistry();
    const external = { ...record(), ownerExtensionId: undefined };
    registry.register(external);
    const shader = createTimelineClipShaderMetadata(external);
    expect(shader.extensionId).toBe('');
    expect(shaderSlotCommand({ id: 'parent/clip:a', value: {} }, shader, registry.getSnapshot())).toBeUndefined();
    registry.unregister(shader.shaderId);
    registry.register({ ...external, provenance: 'built-in' });
    expect(shaderSlotCommand({ id: 'parent/clip:a', value: {} }, shader, registry.getSnapshot())?.args.shader).toEqual(shader);
  });
  it('keeps container inverses exclusive to this single shader owner', () => {
    const c = { op: 'timeline.inverse', select: null, args: { publication: 'pub', writes: [{ id: 'parent', path: 'config.app', before: { state: 'absent' }, after: { state: 'present', value: { unrelated: true } } }] } };
    expect(shaderSlotInverse([c], { status: 'accepted', accepted_publication_id: 'next', change: { direct_writes: c.args.writes } })).toBeUndefined();
  });
  it('freezes capture against changed input/registry and distinguishes no-change clear', () => {
    const registry = createShaderEffectRegistry(); registry.register(record());
    const shader = createTimelineClipShaderMetadata(record()); const owner = { id: 'parent/clip:a', value: { app: { shader: null, keep: 1 } } };
    const c = shaderSlotCommand(owner, shader, registry.getSnapshot())!; const bytes = JSON.stringify(c);
    shader.metadata!.later = 'changed'; owner.value.app.keep = 2; registry.unregister('wash', 'ext');
    expect(JSON.stringify(c)).toBe(bytes);
    const clear = shaderSlotCommand({ id: 'parent', value: {} }, null)!;
    expect(shaderSlotInverse([clear], { status: 'no_change', accepted_publication_id: null, change: { direct_writes: [] } })).toBeNull();
  });
});
