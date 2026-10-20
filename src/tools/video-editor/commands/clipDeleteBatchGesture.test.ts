import { describe, expect, it, vi } from 'vitest';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { ClipDeleteBatchMember } from './clipDeleteBatchCapture.ts';
import { captureClipDeleteBatchEdit, clipDeleteBatchPreview, projectClipDeleteBatchPreview, submitClipDeleteBatchEdit,
  type ClipDeleteBatchCapturePort } from './clipDeleteBatchGesture.ts';

function setup() {
  const keep = { id: 'keep', track: 'V1', at: 2.017, hold: 1.013, from: null, opacity: null,
    app: { canonical: null, opaque: [null, false] }, arbitrary: { literal: 'x' } };
  const config = { output: { fps: 30, resolution: '1920x1080' }, root: { nullable: null },
    tracks: [{ id: 'V1', kind: 'visual' }],
    clips: [{ id: 'x', track: 'V1', at: 0, hold: 1 }, keep, { id: 'y', track: 'V1', at: 5, hold: 1 }] } as unknown as TimelineData['config'];
  const current = { ...assembleTimelineData({ config, configVersion: 7, registry: { assets: {} }, assetMap: {},
    resolvedConfig: { ...config, tracks: config.tracks!, registry: {} } }),
    head: { projectId: 'project', timelineId: 'timeline', headRevisionId: 'r0', headPublicationId: 'p0' },
    editProjection: { kind: 'accepted', head: { revisionId: 'r0', publicationId: 'p0' } } as TimelineData['editProjection'],
    dataLanes: [{ opaque: 'lane' }] as unknown as TimelineData['dataLanes'],
    sourceItemsBySchemaRef: { opaque: [{ preserve: null, provenance: { adapterId: 'opaque' } }] } as unknown as TimelineData['sourceItemsBySchemaRef'],
    transcriptReferences: { opaque: 'transcript' } as unknown as TimelineData['transcriptReferences'],
  };
  const members: ClipDeleteBatchMember[] = [{ clipId: 'y', ownerRef: 'parent' }, { clipId: 'x', ownerRef: 'parent' }];
  const basis = { original: { nullable: null, order: ['y', 'x'] } };
  const port: ClipDeleteBatchCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn(() => ({ commands: ['y', 'x'].map((id) => ({ schema_version: 1, op: 'clip.delete', version: '1',
      select: `parent/clip:${id}`, args: {} })), preview: clipDeleteBatchPreview(['y', 'x']) })),
    submit: vi.fn(),
  };
  return { current, keep, members, basis, port };
}

describe('parent multi-delete gesture primitive without UI ingress', () => {
  it('freezes original ordered targets and capture, then submits once', () => {
    const { current, members, basis, port } = setup();
    const edit = captureClipDeleteBatchEdit(port, current, members);
    members.reverse();
    basis.original.order.reverse();
    expect(edit.members.map((member) => member.clipId)).toEqual(['y', 'x']);
    expect(edit.basis.original).toEqual({ nullable: null, order: ['y', 'x'] });
    expect(Object.isFrozen(edit.members[0])).toBe(true);
    submitClipDeleteBatchEdit(edit);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(port.submit).toHaveBeenCalledOnce();
    expect(port.submit).toHaveBeenCalledWith(port.finish(edit.basis));
  });

  it.each(['empty', 'duplicate', 'missing', 'occurrence', 'display-duplicate'])(
    'atomically refuses the original %s target set without capture', (fault) => {
      const { current, members, port } = setup();
      if (fault === 'empty') members.length = 0;
      if (fault === 'duplicate') members.push(members[0]);
      if (fault === 'missing') members[1] = { ...members[1], clipId: 'missing' };
      if (fault === 'occurrence') members[1] = { ...members[1], ownerRef: 'occurrence:o' as 'parent' };
      if (fault === 'display-duplicate') current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
      expect(() => captureClipDeleteBatchEdit(port, current, members)).toThrow('distinct original');
      expect(port.capture).not.toHaveBeenCalled();
      expect(port.submit).not.toHaveBeenCalled();
    });

  it.each(['order', 'args', 'ownership', 'count', 'preview'])(
    'retains the original capture when completion changes %s', (fault) => {
      const { current, members, port } = setup();
      const edit = captureClipDeleteBatchEdit(port, current, members);
      const result = port.finish(edit.basis);
      if (fault === 'order') result.commands.reverse();
      if (fault === 'args') result.commands[1].args = { force: true };
      if (fault === 'ownership') result.commands[1].select = 'occurrence:o/clip:x';
      if (fault === 'count') result.commands.pop();
      if (fault === 'preview') result.preview.operations.reverse();
      port.finish = () => result;
      expect(() => submitClipDeleteBatchEdit(edit)).toThrow('Unsupported');
      expect(edit.basis.original).toEqual({ nullable: null, order: ['y', 'x'] });
      expect(port.submit).not.toHaveBeenCalled();
    });

  // Local projector proof only: accepted Runtime projection of unknown root fields is separate.
  it.each(['accepted', 'local'] as const)('composes complete row removals preserving local data and %s base fact', (kind) => {
    const { current, keep } = setup();
    if (kind === 'local') current.editProjection = { kind: 'local', base: { revisionId: 'old-r', publicationId: 'old-p' }, generation: 17 };
    const before = structuredClone(current);
    const next = projectClipDeleteBatchPreview(clipDeleteBatchPreview(['y', 'x']), current)!;
    expect(next.config).toEqual({ ...current.config, clips: [keep] });
    expect(next.resolvedConfig).toEqual({ ...current.resolvedConfig, clips: [keep] });
    expect(next.config.clips[0]).toBe(keep);
    for (const key of ['registry', 'assetMap', 'output', 'dataLanes', 'transcriptReferences', 'sourceItemsBySchemaRef', 'head'] as const) {
      expect(next[key]).toBe(current[key]);
    }
    expect(next.editProjection).toEqual(kind === 'local' ? current.editProjection
      : { kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' }, generation: 0 });
    expect(current).toEqual(before);
  });

  it('never installs a partial preview if a later removal or patch shape is invalid', () => {
    const { current } = setup();
    const before = structuredClone(current);
    for (const ids of [['y', 'missing'], ['y', 'y'], []]) {
      expect(() => projectClipDeleteBatchPreview(clipDeleteBatchPreview(ids), current)).toThrow();
      expect(current).toEqual(before);
    }
    const forged = clipDeleteBatchPreview(['y', 'x']);
    forged.operations[1].payload = { force: true };
    expect(() => projectClipDeleteBatchPreview(forged, current)).toThrow('Invalid native');
    expect(projectClipDeleteBatchPreview({ version: 1, operations: [] }, current)).toBeUndefined();
  });
});
