import { describe, expect, it, vi } from 'vitest';
import type { TimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { captureClipTrimEdit, submitClipTrimEdit, type ClipTrimCapturePort } from './clipTrimGesture.ts';
import { environment, trimDocument } from './__tests__/commitSessionEnvironment.ts';

function setup() {
  const basis = { original: { from: 2, to: 6, hold: 17 } };
  const preview = { version: 1, source: 'clip.trim', operations: [
    { op: 'clip.update' as const, target: 'x', payload: { from: 1, to: 5, hold: 4 } },
  ] };
  const port: ClipTrimCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn((_basis, args) => ({ command: { schema_version: 1, op: 'clip.trim', version: '1',
      select: 'parent/clip:x', args: { in_s: args.in_s ?? null, out_s: args.out_s ?? null } }, preview })),
    submit: vi.fn(),
  };
  const current = { resolvedConfig: { clips: [{ id: 'x', from: 99, to: 100, speed: 4 }] } } as TimelineData;
  return { port, basis, current, preview };
}

describe('clip trim gesture adapter', () => {
  it.each([{ in_s: 1, out_s: 5 }, { out_s: 5 }, {}])('finishes source endpoints %j against the original begin basis', (args) => {
    const { port, basis, current, preview } = setup();
    const captured = captureClipTrimEdit(port, current, 'x');
    basis.original.from = 9;
    current.resolvedConfig.clips[0].from = 1000;
    submitClipTrimEdit(captured, args);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(port.finish).toHaveBeenCalledWith(captured.basis, args);
    expect(captured.basis.original).toEqual({ from: 2, to: 6, hold: 17 });
    expect(Object.isFrozen(captured.basis.original)).toBe(true);
    expect(port.submit).toHaveBeenCalledWith({ command: { schema_version: 1, op: 'clip.trim', version: '1',
      select: 'parent/clip:x', args: { in_s: args.in_s ?? null, out_s: args.out_s ?? null } }, preview });
  });
  it('refuses unavailable or ambiguous capture before contacting the port', () => {
    const { port, current } = setup();
    expect(() => captureClipTrimEdit(undefined, current, 'x')).toThrow('unavailable');
    expect(() => captureClipTrimEdit(port, current, 'missing')).toThrow('unambiguous');
    current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
    expect(() => captureClipTrimEdit(port, current, 'x')).toThrow('unambiguous');
    expect(port.capture).not.toHaveBeenCalled();
  });
  it.each(['op', 'select', 'args'] as const)('refuses an incompatible %s result without submitting', (key) => {
    const { port, current } = setup();
    const captured = captureClipTrimEdit(port, current, 'x');
    const finish = port.finish;
    port.finish = (basis, args) => {
      const result = finish(basis, args);
      Object.assign(result.command, { [key]: key === 'op' ? 'clip.move' : key === 'select' ? 'occurrence:o/clip:x' : { in_s: 7 } });
      return result;
    };
    expect(() => submitClipTrimEdit(captured, { in_s: 1, out_s: 5 })).toThrow('Unsupported');
    expect(port.submit).not.toHaveBeenCalled();
  });
  it('retains the begin basis and endpoint input after a failed finish', () => {
    const { port, current } = setup();
    const captured = captureClipTrimEdit(port, current, 'x');
    const args = { in_s: -1, out_s: 5 };
    port.finish = () => { throw new Error('unsupported source window'); };
    expect(() => submitClipTrimEdit(captured, args)).toThrow('unsupported');
    expect(args).toEqual({ in_s: -1, out_s: 5 });
    expect(captured.basis.original).toEqual({ from: 2, to: 6, hold: 17 });
    expect(port.submit).not.toHaveBeenCalled();
  });
  it('projects exact native source writes without row quantization, opaque loss, or unrelated row changes', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const current = env.current();
    const before = structuredClone(current.config);
    const basis = session.clipTrimPort.capture({ clipId: 'x', current });
    const { preview } = session.clipTrimPort.finish(basis, { in_s: 9.8999, out_s: 10 });
    const next = compileTimelinePatch(preview, current).nextData!;
    expect(next.config.clips[0]).toEqual({ ...before.clips[0], from: 9.8999, to: 10, hold: 0.1001,
      app: { astrid: { opaque: [null, false] }, 'org.example': { literal: 'x', clear: null } } });
    expect(next.resolvedConfig.clips[0]).toMatchObject({ from: 9.8999, to: 10, hold: 0.1001, speed: 2 });
    expect(next.meta.x).toMatchObject({ from: 9.8999, to: 10, hold: 0.1001, speed: 2 });
    expect(next.config.clips[1]).toEqual(before.clips[1]);
    expect(current.config).toEqual(before);
    const rebuilt = await buildTimelineData(next.config, next.registry);
    expect(rebuilt.config.clips).toEqual(next.config.clips);
    await session.dispose();
  });
  it('refuses a mixed native preview through the same compiler', async () => {
    const env = await environment(trimDocument());
    const { preview } = setup();
    expect(compileTimelinePatch({ ...preview, operations: [{ ...preview.operations[0],
      payload: { ...preview.operations[0].payload, asset: 'other' } }] }, env.current()).valid).toBe(false);
  });
});

describe('native trim preview opaque closure', () => {
  it('keeps own prototype-looking metadata and untouched tracks/registry exact through the one compiler', async () => {
    const env = await environment(trimDocument());
    const current = env.current();
    const opaque = JSON.parse('{"__proto__":{"literal":"x"},"constructor":null,"prototype":[false,0]}');
    current.config.clips[0].unknown = opaque;
    current.config.tracks[0].opaque = structuredClone(opaque);
    const before = structuredClone(current);
    const session = await env.mount();
    const prepared = session.clipTrimPort.finish(session.clipTrimPort.capture({ clipId: 'x', current }), { out_s: 5 });
    const compiled = compileTimelinePatch(prepared.preview, current);
    expect(compiled.valid).toBe(true);
    expect(compiled.mutation).toBeNull();
    expect(compiled.nextData!.config.clips[0].unknown).toStrictEqual(opaque);
    expect(Object.prototype.hasOwnProperty.call(compiled.nextData!.config.clips[0].unknown, '__proto__')).toBe(true);
    expect(compiled.nextData!.config.clips[1]).toStrictEqual(before.config.clips[1]);
    expect(compiled.nextData!.config.tracks).toStrictEqual(before.config.tracks);
    expect(compiled.nextData!.registry).toStrictEqual(before.registry);
    expect(compiled.nextData!.rows.flatMap((row) => row.actions).find((action) => action.id === 'x'))
      .toMatchObject({ start: 1, end: 2.5 });
    expect(current).toStrictEqual(before);
    await session.dispose();
  });
});
