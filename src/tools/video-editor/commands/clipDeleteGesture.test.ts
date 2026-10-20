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
    const captured = captureClipDeleteEdit(port, current, 'x', 'parent');
    basis.original.at = 9;
    expect(captured.basis).toEqual({ original: { nullable: null, at: 5 } });
    expect(Object.isFrozen(captured.basis.original)).toBe(true);
    submitClipDeleteEdit(captured);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(port.finish).toHaveBeenCalledWith(captured.basis);
    expect(port.submit).toHaveBeenCalledWith({ command: { schema_version: 1, op: 'clip.delete', version: '1',
      select: 'parent/clip:x', args: {} }, preview: { version: 1, source: 'parentclip.delete', operations: [{ op: 'clip.remove', target: 'x' }] } });
  });
  it('refuses unavailable, missing, and duplicate display identities before capture', () => {
    const { port, current } = setup();
    expect(() => captureClipDeleteEdit(undefined, current, 'x', 'parent')).toThrow('unavailable');
    expect(() => captureClipDeleteEdit(port, current, 'missing', 'parent')).toThrow('unambiguous');
    current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
    expect(() => captureClipDeleteEdit(port, current, 'x', 'parent')).toThrow('unambiguous');
    expect(port.capture).not.toHaveBeenCalled();
  });
  it.each(['wrong-op', 'wrong-target', 'changed-args', 'wrong-version'])('refuses incompatible completion: %s', (fault) => {
    const { port, current } = setup();
    const captured = captureClipDeleteEdit(port, current, 'x', 'parent');
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
    const captured = captureClipDeleteEdit(port, current, 'x', 'parent');
    port.finish = () => { throw new Error('dependency changed'); };
    expect(() => submitClipDeleteEdit(captured)).toThrow('dependency changed');
    expect(captured.basis.original).toEqual({ nullable: null, at: 5 });
    expect(port.submit).not.toHaveBeenCalled();
  });
});

// Preview stays on today's local snapshot, including rows a prior gesture already authored.
describe('whole-row parent delete preview', () => {
  it.each(['accepted', 'local'] as const)('keeps opaque rows, typed data and the %s projection base', async (kind) => {
    const { assembleTimelineData } = await import('../lib/timeline-data.ts');
    const { clipDeletePreview, projectClipDeletePreview } = await import('./clipDeleteGesture.ts');
    const keep = { id: 'keep', track: 'V1', at: 2.017, hold: 1.013, opacity: null,
      from: null, app: { opaque: [null, false, {}] }, arbitrary: { literal: 'x' } };
    const config = { output: { fps: 30, resolution: '1920x1080' },
      clips: [{ id: 'x', track: 'V1', at: 0, hold: 1 }, keep], tracks: [{ id: 'V1', kind: 'visual' }],
      root: { opaque: [null, false] } } as unknown as TimelineData['config'];
    const head = { revisionId: 'r0', publicationId: 'p0' };
    const local = { kind: 'local', base: { revisionId: 'old-r', publicationId: 'old-p' }, generation: 17 } as const;
    const current = { ...assembleTimelineData({ config, configVersion: 3, registry: { assets: {} }, assetMap: {},
      resolvedConfig: { ...config, tracks: config.tracks!, registry: {} } }),
      rootMetadata: { unrelated: null },
      head: { projectId: 'project', timelineId: 'timeline', headRevisionId: 'r0', headPublicationId: 'p0' },
      editProjection: kind === 'local' ? local : { kind: 'accepted', head } as const,
      dataLanes: [{ opaque: 'lane' }] as unknown as TimelineData['dataLanes'],
      sourceItemsBySchemaRef: { 'schema:opaque': [{ preserve: null, provenance: { adapterId: 'opaque' } }] } as unknown as TimelineData['sourceItemsBySchemaRef'],
      transcriptReferences: { opaque: 'transcript' } as unknown as TimelineData['transcriptReferences'],
    };
    const before = structuredClone(current);
    const next = projectClipDeletePreview(clipDeletePreview('x'), current)! as typeof current;
    expect(next.config.clips).toEqual([keep]);
    expect(next.resolvedConfig.clips).toEqual([keep]);
    expect(next.config.clips[0]).toBe(keep);
    expect(next.config).toEqual({ ...config, clips: [keep] });
    expect(next.dataLanes).toBe(current.dataLanes);
    expect(next.transcriptReferences).toBe(current.transcriptReferences);
    expect(next.sourceItemsBySchemaRef).toBe(current.sourceItemsBySchemaRef);
    expect(next.rootMetadata).toBe(current.rootMetadata);
    expect(next.head).toBe(current.head);
    expect(next.editProjection).toEqual(kind === 'local' ? local : { kind: 'local', base: head, generation: 0 });
    expect(current).toEqual(before);
    expect(projectClipDeletePreview({ version: 1, operations: [] }, current)).toBeUndefined();
    expect(() => projectClipDeletePreview(clipDeletePreview('absent'), current)).toThrow('Invalid native');
    expect(current).toEqual(before);
  });
});
