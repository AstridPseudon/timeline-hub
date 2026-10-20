import { describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { captureClipSplitBatchEdit, clipSplitBatchPreview, projectClipSplitBatchPreview } from './clipSplitBatchGesture.ts';
import type { ClipSplitBatchCapturePort } from './clipSplitBatchGesture.ts';
import type { JsonObject } from './types.ts';
import { copy } from './clipMovePrimitives.ts';
import { clipSplitPreview, projectClipSplitPreview } from './clipSplitGesture.ts';
import fixture from './fixtures/recipe_m2_clip_split_batch.json';

const golden = fixture as unknown as { input: CanonicalDocument; after_bundle: { parent: { clips: JsonObject[] } } };
async function display() {
  const payload = golden.input.parent_revision.payload;
  return buildTimelineData(payload.config as never, payload.registry as never, undefined, 1, undefined,
    { projectId: 'project-1', timelineId: 'film', headRevisionId: 'parent-1', headPublicationId: 'pub-0' });
}
function preview() {
  const [a, ar, b, br] = golden.after_bundle.parent.clips;
  return clipSplitBatchPreview([{ clipId: 'clip-b', left: b, right: br }, { clipId: 'clip-a', left: a, right: ar }]);
}

describe('split batch planning and atomic preview', () => {
  it('freezes ordered valid original inputs, eligibility, time and IDs once', async () => {
    const current = await display();
    const reserve = vi.fn((_used: string[], clipId: string) => `right:${clipId}`);
    const capture = vi.fn(() => ({ original: true }));
    const port = { capture } as unknown as ClipSplitBatchCapturePort;
    const inputs = ['missing', 'clip-b', 'clip-a', 'clip-b', 'uploading-x'];
    const result = captureClipSplitBatchEdit(port, current, inputs, 3, reserve)!;
    inputs.reverse();
    expect(result.clipIds).toEqual(['clip-b', 'clip-a']);
    expect(result.members).toEqual([{ clipId: 'clip-b', rightId: 'right:clip-b' }, { clipId: 'clip-a', rightId: 'right:clip-a' }]);
    expect(result.on).toBe(3);
    expect(Object.isFrozen(result.members[0])).toBe(true);
    expect(capture).toHaveBeenCalledTimes(1);
    expect(reserve).toHaveBeenCalledTimes(2);
    expect(reserve.mock.calls[1][0]).toContain('right:clip-b');
    expect(() => Object.assign(result.members[0], { rightId: 'changed' })).toThrow();
  });

  it('retains boundary/outside no-ops without allocating or capturing', async () => {
    const current = await display();
    const reserve = vi.fn();
    for (const on of [0, 1, 5, 10]) {
      expect(captureClipSplitBatchEdit(undefined, current, ['clip-a', 'clip-b'], on, reserve)).toBeUndefined();
    }
    expect(reserve).not.toHaveBeenCalled();
  });

  it('preserves full native rows, resolved assets, opaque metadata and projection basis', async () => {
    const current = await display();
    current.sourceItemsBySchemaRef = {
      'custom/v1': [{ id: 'source-1', shape: 'point', domain: 'timeline_seconds', extent: { start: 0 },
        schemaRef: 'custom/v1', payload: { keep: [null, false] }, sourceArtifactRef: { assetId: 'picture' },
        provenance: { adapterId: 'test', adapterVersion: '1' } }],
    };
    current.transcriptReferences = { schema: 'media.transcript.references/v1',
      associations: [{ assetId: 'picture', documentId: 'transcript-1' }] };
    current.editProjection = { kind: 'local', base: { revisionId: 'base', publicationId: 'base-pub' }, generation: 7 };
    const before = copy(current);
    const next = projectClipSplitBatchPreview(preview(), current)!;
    expect(next.config.clips).toEqual(golden.after_bundle.parent.clips);
    expect(next.config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right:a', 'clip-b', 'right:b']);
    expect(next.registry).toBe(current.registry);
    expect(next.output).toEqual(current.output);
    expect(next.sourceItemsBySchemaRef).toBe(current.sourceItemsBySchemaRef);
    expect(next.transcriptReferences).toBe(current.transcriptReferences);
    expect(next.dataLanes).toBe(current.dataLanes);
    expect(next.editProjection).toBe(current.editProjection);
    expect(next.resolvedConfig.clips[1].assetEntry).toBe(current.resolvedConfig.clips[0].assetEntry);
    expect(current).toEqual(before);
  });

  it('refuses malformed later preview operations without changing the input', async () => {
    const current = await display();
    const patch = preview();
    const before = copy(current);
    const bad = { ...patch, operations: [patch.operations[0], { ...patch.operations[1], target: 'missing' }] };
    expect(() => projectClipSplitBatchPreview(bad, current)).toThrow('Invalid native');
    expect(current).toEqual(before);
    expect(() => projectClipSplitPreview({ ...patch, source: 'clip.split' }, current)).toThrow();
    const single = clipSplitPreview('clip-a', golden.after_bundle.parent.clips[0], golden.after_bundle.parent.clips[1]);
    expect(projectClipSplitBatchPreview(single, current)).toBeUndefined();
  });
});
