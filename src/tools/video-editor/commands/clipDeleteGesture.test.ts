import { describe, expect, it, vi } from 'vitest';
import type { TimelineData } from '../lib/timeline-data.ts';
import { captureClipDeleteEdit, submitClipDeleteEdit, type ClipDeleteCapturePort } from './clipDeleteGesture.ts';

function setup() {
  const basis = { original: { nullable: null, at: 5 } };
  const port: ClipDeleteCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn(() => ({ command: { schema_version: 1, op: 'clip.delete', version: '1',
      select: 'parent/clip:x', args: {} } })),
    submit: vi.fn(),
  };
  const current = { resolvedConfig: { clips: [{ id: 'x' }] } } as TimelineData;
  return { port, basis, current };
}

describe('clip delete gesture', () => {
  it('freezes the original capture and submits only a same-ID removal preview', () => {
    const { port, basis, current } = setup();
    const captured = captureClipDeleteEdit(port, current, 'x');
    basis.original.at = 9;
    expect(captured.basis).toEqual({ original: { nullable: null, at: 5 } });
    expect(Object.isFrozen(captured.basis.original)).toBe(true);
    submitClipDeleteEdit(captured);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(port.finish).toHaveBeenCalledWith(captured.basis);
    expect(port.submit).toHaveBeenCalledWith({ command: { schema_version: 1, op: 'clip.delete', version: '1',
      select: 'parent/clip:x', args: {} }, preview: { version: 1, operations: [{ op: 'clip.remove', target: 'x' }] } });
  });
  it('refuses unavailable, missing, and duplicate display identities before capture', () => {
    const { port, current } = setup();
    expect(() => captureClipDeleteEdit(undefined, current, 'x')).toThrow('unavailable');
    expect(() => captureClipDeleteEdit(port, current, 'missing')).toThrow('unambiguous');
    current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
    expect(() => captureClipDeleteEdit(port, current, 'x')).toThrow('unambiguous');
    expect(port.capture).not.toHaveBeenCalled();
  });
  it.each(['wrong-op', 'wrong-target', 'changed-args', 'wrong-version'])('refuses incompatible completion: %s', (fault) => {
    const { port, current } = setup();
    const captured = captureClipDeleteEdit(port, current, 'x');
    const finish = port.finish;
    port.finish = (basis) => {
      const result = finish(basis);
      if (fault === 'wrong-op') result.command.op = 'clip.move';
      if (fault === 'wrong-target') result.command.select = 'occurrence:o/clip:x';
      if (fault === 'changed-args') result.command.args = { force: true };
      if (fault === 'wrong-version') result.command.version = '2';
      return result;
    };
    expect(() => submitClipDeleteEdit(captured)).toThrow('Unsupported');
    expect(port.submit).not.toHaveBeenCalled();
  });
  it('retains the original capture when the host refuses', () => {
    const { port, current } = setup();
    const captured = captureClipDeleteEdit(port, current, 'x');
    port.finish = () => { throw new Error('dependency changed'); };
    expect(() => submitClipDeleteEdit(captured)).toThrow('dependency changed');
    expect(captured.basis.original).toEqual({ nullable: null, at: 5 });
    expect(port.submit).not.toHaveBeenCalled();
  });
});
