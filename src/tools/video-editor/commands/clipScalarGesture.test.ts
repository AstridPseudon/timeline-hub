import { describe, expect, it, vi } from 'vitest';
import type { TimelineData } from '../lib/timeline-data.ts';
import { captureClipScalarEdit, submitClipScalarEdit, type ClipScalarArgs, type ClipScalarCapturePort } from './clipScalarGesture.ts';

function setup() {
  const basis = { select: 'occurrence:o1/clip:raw', original: { asset: { state: 'present', value: null } } };
  const submit = vi.fn();
  const port: ClipScalarCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn((_basis, args) => ({ command: { schema_version: 1, op: 'clip.set', version: '1', select: basis.select, args } })),
    submit,
  };
  const current = { resolvedConfig: { clips: [{ id: 'o1:raw' }] } } as TimelineData;
  return { port, basis, current, submit };
}

describe('clip scalar gesture', () => {
  it.each<ClipScalarArgs>([
    { values: { hold: 4 }, clear: [] },
    { values: {}, clear: ['asset'] },
    { values: {}, clear: ['transition'] },
    { values: {}, clear: ['hold'] },
  ])('retains exact args and explicit removal metadata through JSON: %j', (args) => {
    const { port, basis, current, submit } = setup();
    const captured = captureClipScalarEdit(port, current, 'o1:raw', 'occurrence:o1');
    basis.original.asset.value = 'changed' as never;
    expect(captured.basis.original).toEqual({ asset: { state: 'present', value: null } });
    expect(Object.isFrozen(captured.basis.original)).toBe(true);
    submitClipScalarEdit(captured, args);
    expect(port.capture).toHaveBeenCalledWith({ current, clipId: 'o1:raw', ownerRef: 'occurrence:o1' });
    expect(submit.mock.calls[0][0]).toEqual(JSON.parse(JSON.stringify({ command: {
      schema_version: 1, op: 'clip.set', version: '1', select: basis.select, args },
    preview: { version: 1, operations: [{ op: 'clip.update', target: 'o1:raw', payload: args.values, clear: args.clear }] } })));
  });
  it('refuses missing/ambiguous display identities before capture', () => {
    const { port, current } = setup();
    expect(() => captureClipScalarEdit(undefined, current, 'o1:raw', 'occurrence:o1')).toThrow('unavailable');
    expect(() => captureClipScalarEdit(port, current, 'missing', 'parent')).toThrow('unambiguous');
    current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
    expect(() => captureClipScalarEdit(port, current, 'o1:raw', 'occurrence:o1')).toThrow('unambiguous');
    expect(port.capture).not.toHaveBeenCalled();
  });
  it('keeps typed input when the host refuses completion', () => {
    const { port, current, submit } = setup();
    const captured = captureClipScalarEdit(port, current, 'o1:raw', 'occurrence:o1');
    port.finish = () => { throw new Error('changed'); };
    const args: ClipScalarArgs = { values: { hold: 4 }, clear: [] };
    expect(() => submitClipScalarEdit(captured, args)).toThrow('changed');
    expect(args.values.hold).toBe(4);
    expect(submit).not.toHaveBeenCalled();
  });
  it.each(['clip.move', 'wrong-owner', 'changed-args'])('refuses incompatible host output: %s', (failure) => {
    const { port, current, submit } = setup();
    const captured = captureClipScalarEdit(port, current, 'o1:raw', 'occurrence:o1');
    const finish = port.finish;
    port.finish = (basis, args) => {
      const result = finish(basis, args);
      if (failure === 'clip.move') result.command.op = 'clip.move';
      if (failure === 'wrong-owner') result.command.select = 'parent/clip:raw';
      if (failure === 'changed-args') result.command.args = { values: { hold: 99 }, clear: [] };
      return result;
    };
    expect(() => submitClipScalarEdit(captured, { values: {}, clear: ['asset'] })).toThrow('Unsupported');
    expect(submit).not.toHaveBeenCalled();
  });
});
