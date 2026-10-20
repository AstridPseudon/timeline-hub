import { describe, expect, it, vi } from 'vitest';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { captureClipParamsEdit, submitClipParamsEdit, type ClipParamsCapturePort } from './clipParamsGesture.ts';

function setup() {
  const basis = { select: 'parent/clip:x', original: { params: null as JSON } };
  const previewParams = { 'literal.key': null, opaque: { keep: [false, {}, ''] } };
  const port: ClipParamsCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn((_basis, args) => ({ command: { schema_version: 1, op: 'clip.set-params', version: '1',
      select: basis.select, args }, previewParams })),
    submit: vi.fn(),
  };
  const current = { resolvedConfig: { clips: [{ id: 'x', params: { displayOnly: true } }] } } as TimelineData;
  return { port, basis, previewParams, current };
}

describe('discrete clip params gesture', () => {
  it('captures before finish and submits native leaf args with a separate immutable local params preview', () => {
    const { port, basis, previewParams, current } = setup();
    const captured = captureClipParamsEdit(port, current, 'x');
    basis.original.params = {};
    const args = { values: { 'literal.key': null }, clear: ['old'] };
    submitClipParamsEdit(captured, args);
    expect(port.capture).toHaveBeenCalledExactlyOnceWith({ clipId: 'x', current });
    expect(port.finish).toHaveBeenCalledExactlyOnceWith(captured.basis, args);
    expect(captured.basis.original).toEqual({ params: null });
    expect(Object.isFrozen(captured.basis.original)).toBe(true);
    expect(port.submit).toHaveBeenCalledExactlyOnceWith({ command: { schema_version: 1, op: 'clip.set-params', version: '1',
      select: 'parent/clip:x', args }, preview: { version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { params: previewParams } },
    ] } });
    const submitted = vi.mocked(port.submit).mock.calls[0][0];
    expect(Object.isFrozen(submitted.command.args)).toBe(true);
    expect(Object.isFrozen(submitted.preview.operations[0].payload!.params)).toBe(true);
    expect(submitted.command.args).not.toHaveProperty('opaque');
  });
  it('refuses missing and duplicate identities before capture', () => {
    const { port, current } = setup();
    expect(() => captureClipParamsEdit(undefined, current, 'x')).toThrow('unavailable');
    expect(() => captureClipParamsEdit(port, current, 'missing')).toThrow('unambiguous');
    current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
    expect(() => captureClipParamsEdit(port, current, 'x')).toThrow('unambiguous');
    expect(port.capture).not.toHaveBeenCalled();
  });
  it('retains input and basis when completion refuses', () => {
    const { port, current } = setup();
    const captured = captureClipParamsEdit(port, current, 'x');
    const original = structuredClone(captured.basis);
    const args = { values: { text: 'keep this draft' }, clear: [] };
    port.finish = () => { throw new Error('changed'); };
    expect(() => submitClipParamsEdit(captured, args)).toThrow('changed');
    expect(args.values.text).toBe('keep this draft');
    expect(captured.basis).toEqual(original);
    expect(port.submit).not.toHaveBeenCalled();
  });
  it.each(['op', 'version', 'schema', 'target', 'args', 'preview'])(
    'refuses an incompatible host result: %s', (fault) => {
      const { port, current } = setup();
      const captured = captureClipParamsEdit(port, current, 'x');
      const finish = port.finish;
      port.finish = (basis, args) => {
        const result = finish(basis, args);
        if (fault === 'op') result.command.op = 'clip.update';
        if (fault === 'version') result.command.version = '2';
        if (fault === 'schema') Object.assign(result.command, { schema_version: 2 });
        if (fault === 'target') result.command.select = 'occurrence:o/clip:x';
        if (fault === 'args') result.command.args = { values: {}, clear: ['other'] };
        if (fault === 'preview') result.previewParams = [] as unknown as typeof result.previewParams;
        return result;
      };
      expect(() => submitClipParamsEdit(captured, { values: { x: 1 }, clear: [] })).toThrow('Unsupported');
      expect(port.submit).not.toHaveBeenCalled();
    },
  );
  it.each([NaN, Infinity, undefined, new Date()])('refuses non-JSON input %s before finish', (value) => {
    const { port, current } = setup();
    const captured = captureClipParamsEdit(port, current, 'x');
    expect(() => submitClipParamsEdit(captured, { values: { value } as never, clear: [] })).toThrow('finite JSON');
    expect(port.finish).not.toHaveBeenCalled();
    expect(port.submit).not.toHaveBeenCalled();
  });
});
