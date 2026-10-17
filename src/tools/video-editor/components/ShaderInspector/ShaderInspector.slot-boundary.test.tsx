import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ShaderInspector } from './ShaderInspector.tsx';
import { createShaderEffectRegistry } from '../../shaders/registry/ShaderEffectRegistry.ts';
import type { ShaderEffectRegistryRecord } from '../../shaders/registry/types.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';
import { createTimelineClipShaderMetadata, createTimelinePostprocessShaderMetadata } from '../../lib/shader-catalog.ts';
const record = (scope: 'clip' | 'postprocess'): ShaderEffectRegistryRecord => ({ ownerExtensionId: 'extension', contributionId: 'contribution', shaderId: 'shader', label: 'Shader', pass: scope,
  status: 'active', source: { kind: 'inline', fragment: 'fragment' }, provenance: 'bundled-extension', renderability: { determinism: 'preview-only', capabilities: [] } });
describe.each(['clip', 'postprocess'] as const)('W28 %s inspector caller boundary', scope => {
  it.each(['missing', 'contribution', 'owner', 'pass', 'inactive', 'diagnostic', 'ambiguous', 'shape'] as const)('refuses %s edit and retains guarded explicit removal', reason => {
    let r = record(scope); const registry = createShaderEffectRegistry();
    const shader = scope === 'clip' ? createTimelineClipShaderMetadata(r) : createTimelinePostprocessShaderMetadata(r);
    if (reason === 'contribution') r = { ...r, contributionId: 'different' };
    if (reason === 'owner') r = { ...r, ownerExtensionId: 'different' };
    if (reason === 'pass') r = { ...r, pass: scope === 'clip' ? 'postprocess' : 'clip' };
    if (reason === 'inactive') r = { ...r, status: 'inactive' };
    if (reason === 'diagnostic') r = { ...r, diagnostics: [{ severity: 'error', code: 'blocked', message: 'Blocked' }] };
    if (reason !== 'missing') registry.register(r);
    const snapshot = registry.getSnapshot();
    const app = { keep: [null, { op: 'clear' }], [scope === 'clip' ? 'shader' : 'shaderPostprocess']: reason === 'shape' ? { ...shader, uniforms: null } : shader };
    const clip = { id: 'clip-1', at: 0, track: 'V1', clipType: 'hold', ...(scope === 'clip' ? { app } : {}) };
    const config = { output: { fps: 30, resolution: '1280x720', file: 'preview.mp4' }, registry: {}, tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }], clips: [clip], ...(scope === 'postprocess' ? { app } : {}) } as ResolvedTimelineConfig;
    const applyEdit = vi.fn();
    render(<ShaderInspector clip={scope === 'clip' ? config.clips[0] : null} postprocessShader={scope === 'postprocess' ? config.app?.shaderPostprocess : undefined} resolvedConfig={config}
      shaderSnapshot={reason === 'ambiguous' ? { ...snapshot, records: [...snapshot.records, snapshot.records[0]] } : snapshot} applyEdit={applyEdit} />);
    expect(screen.getByTestId('shader-inspector-compare-bypass')).toBeDisabled(); fireEvent.click(screen.getByTestId('shader-inspector-compare-bypass')); expect(applyEdit).not.toHaveBeenCalled();
    fireEvent.click(screen.getByText('Remove shader')); expect(applyEdit).toHaveBeenCalledOnce();
    const command = applyEdit.mock.calls[0][1].editCommands[0]; const id = scope === 'clip' ? 'parent/clip:clip-1' : 'parent'; const path = scope === 'clip' ? 'app.shader' : 'config.app.shaderPostprocess';
    expect(command).toMatchObject({ select: scope === 'clip' ? id : null, args: { shader: null }, expect: { [`${id}::${path}`]: { state: 'present', value: app[scope === 'clip' ? 'shader' : 'shaderPostprocess'] } } });
    expect(config.clips[0]).toEqual(clip);
  });
});
