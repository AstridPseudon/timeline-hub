// @vitest-environment node
import { describe, expect, it, vi } from 'vitest';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureClipSplit, finishClipSplit } from './clipSplitCapture.ts';
import { captureClipSplitEdit, clipSplitPreview, projectClipSplitPreview, submitClipSplitEdit } from './clipSplitGesture.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import type { JsonObject } from './types.ts';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import fixture from './fixtures/recipe_m2_clip_split.json';

async function setup() {
  const document = structuredClone(fixture.input) as CanonicalDocument;
  const parent = document.parent_revision.payload;
  const current = await buildTimelineData(parent.config as never, parent.registry as never, undefined, 1, undefined,
    { projectId: 'project-1', timelineId: 'film', headRevisionId: 'parent-1', headPublicationId: 'pub-0' });
  const raw = await authoringBundleFromDocument(document);
  const basis = captureClipSplit(raw, 'parent/clip:clip-a', { on: 3, right_id: 'right' });
  const result = finishClipSplit(basis);
  const [left, right] = result.bundle.parent.clips as JsonObject[];
  return { current, basis, command: result.command, preview: clipSplitPreview('clip-a', left, right) };
}

describe('single-parent split preview adapter', () => {
  it('preserves opaque config, source metadata, registry and unchanged rows through existing assembly', async () => {
    const { current, preview } = await setup();
    const opaque = { literal: 'clip-a', unknown: [null, false] };
    Object.assign(current.config, { opaque });
    Object.assign(current.resolvedConfig, { opaque });
    current.editProjection = { kind: 'accepted', head: { revisionId: 'parent-1', publicationId: 'pub-0' } };
    const before = structuredClone(current);
    const next = projectClipSplitPreview(preview, current)!;
    expect(next.config.clips).toEqual(fixture.output.parent_revision.payload.clips);
    expect(next.config).toHaveProperty('opaque', opaque);
    expect(next.config.output).toBe(current.config.output);
    expect(next.registry).toBe(current.registry);
    expect(next.sourceItemsBySchemaRef).toBe(current.sourceItemsBySchemaRef);
    expect(next.transcriptReferences).toBe(current.transcriptReferences);
    expect(next.dataLanes).toBe(current.dataLanes);
    expect(next.config.clips[2]).toBe(current.config.clips[1]);
    expect(next.resolvedConfig.clips[1].assetEntry).toBe(current.resolvedConfig.clips[0].assetEntry);
    expect(next.editProjection).toEqual({ kind: 'local', base: { revisionId: 'parent-1', publicationId: 'pub-0' }, generation: 0 });
    expect(current).toEqual(before);
  });

  it('does not intercept ordinary or compound patches and refuses malformed native previews atomically', async () => {
    const { current, preview } = await setup();
    const before = structuredClone(current);
    expect(projectClipSplitPreview({ version: 1, operations: [] }, current)).toBeUndefined();
    expect(projectClipSplitPreview({ ...preview, source: 'other' }, current)).toBeUndefined();
    expect(() => projectClipSplitPreview({ ...preview, operations: [...preview.operations, ...preview.operations] }, current)).toThrow('Invalid');
    expect(() => projectClipSplitPreview({ ...preview, operations: [] }, current)).toThrow('Invalid');
    const forged = structuredClone(preview);
    forged.operations[0].payload!.right = { id: 'clip-b' };
    expect(() => projectClipSplitPreview(forged, current)).toThrow('Invalid');
    expect(current).toEqual(before);
  });

  it('freezes one reserved identity before preview and refuses missing ports or forged completions', async () => {
    const { current, basis, command, preview } = await setup();
    const port = { capture: vi.fn(() => structuredClone(basis)), finish: vi.fn(() => ({ command, preview })), submit: vi.fn() };
    expect(() => captureClipSplitEdit(undefined, current, 'clip-a', 3, 'right')).toThrow('unavailable');
    const captured = captureClipSplitEdit(port, current, 'clip-a', 3, 'right');
    expect(Object.isFrozen(captured.basis.command)).toBe(true);
    submitClipSplitEdit(captured);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(port.submit).toHaveBeenCalledWith({ command, preview });
    expect(Object.isFrozen(port.submit.mock.calls[0][0].command.args)).toBe(true);
    port.finish.mockReturnValue({ command: { ...command, args: { on: 4, right_id: 'different' } }, preview });
    expect(() => submitClipSplitEdit(captured)).toThrow('Unsupported');
    expect(port.submit).toHaveBeenCalledOnce();
  });
});

