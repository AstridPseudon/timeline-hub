// @vitest-environment jsdom
import React from 'react';
import assert from 'node:assert/strict';
import { cleanup, render, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ShotEditorView } from './ShotEditorView.tsx';
import fixture from '@/tools/video-editor/data/shotComposition.fixture.json';
import { createShotCompositionAdapter, type ShotCompositionPublishRequest } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { StaleWriteError } from '@/tools/video-editor/data/shotComposition.ts';
import { updateCanonicalShotName, updateCanonicalShotSettings } from '@/tools/video-editor/data/shotCompositionEditor.ts';
import type { Shot } from '@/domains/generation/types';
import { toRuntimePublication } from '@/integrations/runtime/dataProvider.ts';
import { createEntityStore } from '@/shared/state/createEntityStore';
import { normalizeVideoTravelSettings } from '../settings';

const capture = vi.hoisted(() => ({ persistence: null as any, onName: null as any, errors: vi.fn() }));
vi.mock('../components/ShotEditor', () => ({ ShotSettingsEditor: (props: any) => { capture.onName = props.onUpdateShotName; return null; } }));
vi.mock('../providers', () => ({
  VideoTravelSettingsProvider: (props: any) => { capture.persistence = props.shotSettingsPersistence; return props.children; },
  useVideoTravelSettingsMutations: () => ({ settings: {}, status: 'loading' }),
}));
vi.mock('../components/ShotTimelinePreview.tsx', () => ({ ShotTimelinePreview: () => null }));
vi.mock('../components/VideoTravelFloatingOverlay', () => ({ VideoTravelFloatingOverlay: () => null }));
vi.mock('@/shared/state/selectionStore', () => ({ useCurrentShot: () => ({ setCurrentShotId: vi.fn() }) }));
vi.mock('@/shared/hooks/mobile', () => ({ useIsMobile: () => false }));
vi.mock('@/shared/hooks/shots/useShotNavigation', () => ({ useShotNavigation: () => ({ navigateToPreviousShot: vi.fn(), navigateToNextShot: vi.fn() }) }));
vi.mock('@/shared/hooks/shots', () => ({ useUpdateShotName: () => ({ mutate: vi.fn() }) }));
vi.mock('@/shared/hooks/shots/useShotImages', () => ({ usePrimeShotImagesCache: () => undefined }));
vi.mock('@/shared/hooks/invalidation/useGenerationInvalidation', () => ({ useEnqueueGenerationsInvalidation: () => vi.fn() }));
vi.mock('@/shared/hooks/projects/useProjectVideoCountsCache', () => ({ useProjectVideoCountsCache: () => ({ getFinalVideoCount: vi.fn(), getHasStructureVideo: vi.fn() }) }));
vi.mock('@/shared/hooks/projects/useProjectGenerationModesCache', () => ({ useProjectGenerationModesCache: () => ({ updateShotMode: vi.fn() }) }));
vi.mock('@/shared/hooks/gallery/useVideoGalleryPreloader', () => ({ useVideoGalleryPreloader: () => undefined }));
vi.mock('../hooks/useStickyHeader', () => ({ useStickyHeader: () => ({}) }));
vi.mock('../hooks/navigation/useNavigationState', () => ({ useNavigationState: () => ({ sortedShots: [], hasPrevious: false, hasNext: false }) }));
vi.mock('../hooks/useOperationTracking', () => ({ useOperationTracking: () => ({ setIsDraggingInTimeline: vi.fn(), signalShotOperation: vi.fn() }) }));
vi.mock('@/shared/state/panesStore', () => ({ usePanesStore: (select: any) => select({}) }));
vi.mock('@/shared/lib/errorHandling/runtimeError.ts', () => ({ normalizeAndPresentError: capture.errors }));

afterEach(() => { cleanup(); capture.errors.mockClear(); capture.persistence = null; capture.onName = null; });

async function setup(input = fixture) {
  let current = structuredClone(input);
  const publications: Record<string, any>[] = [];
  const publish = vi.fn(async (request: ShotCompositionPublishRequest) => {
    if (request.expectedHeadRevisionId !== current.primary_timeline.head.revision_id) throw new StaleWriteError('fixture competing immutable head');
    publications.push(await toRuntimePublication(request.graph, request.projectId, request.parentDocumentId, request.expectedHeadRevisionId));
    current = request.graph as typeof current;
    return current;
  });
  const adapter = createShotCompositionAdapter({ load: async () => current, publish });
  const base = await adapter.load({ projectId: 'project-001', parentDocumentId: 'document-primary' });
  const occurrence = base.occurrences.find((value) => value.occurrenceId === 'occ-1')!;
  render(<MemoryRouter initialEntries={['/tools/travel-between-images?localProject=project-001&localTimeline=document-primary']}>
    <ShotEditorView shotToEdit={{ id: 'shot-alpha', name: 'Original', images: [] } as unknown as Shot}
      selectedProjectId="project-001" isNewlyCreatedShot={false} shotFromState={undefined} shots={[]}
      availableLoras={[]} canonicalComposition={base} canonicalShotComposition={adapter}
      canonicalOccurrence={occurrence} />
  </MemoryRouter>);
  return { base, publish, publications, read: () => current, compete: (graph: typeof current) => { current = graph; } };
}

describe('current App shot editing base', () => {
  it.each(['name', 'settings'] as const)('rejects a competing %s edit instead of silently adopting its new head', async (field) => {
    const state = await setup();
    if (field === 'settings') await capture.persistence.load('shot-alpha');
    const competing = field === 'name'
      ? await updateCanonicalShotName(state.base.contract, 'occ-1', 'Competing name')
      : await updateCanonicalShotSettings(state.base.contract, 'occ-1', { prompt: 'Competing prompt' });
    state.compete(competing as typeof fixture);
    if (field === 'name') {
      capture.onName('My older name');
      await waitFor(() => expect(capture.errors).toHaveBeenCalled());
      expect(capture.errors.mock.calls[0]?.[0]).toBeInstanceOf(StaleWriteError);
    } else {
      await expect(capture.persistence.save('shot-alpha', { prompt: 'My older prompt' })).rejects.toBeInstanceOf(StaleWriteError);
    }
    expect(state.publish).toHaveBeenCalledWith(expect.objectContaining({ expectedHeadRevisionId: state.base.headRevisionId }));
    expect(state.read()).toEqual(competing);
  });

  it('keeps the immutable editing head for an independent competing field too', async () => {
    const state = await setup();
    await capture.persistence.load('shot-alpha');
    const competing = await updateCanonicalShotName(state.base.contract, 'occ-1', 'Independent name');
    state.compete(competing as typeof fixture);
    await expect(capture.persistence.save('shot-alpha', { prompt: 'My prompt' })).rejects.toBeInstanceOf(StaleWriteError);
    expect(state.read()).toEqual(competing);
  });
  it.each(['name', 'settings'] as const)('publishes an uncontended %s edit from its captured head', async (field) => {
    const state = await setup();
    if (field === 'name') {
      capture.onName('My name');
      await waitFor(() => expect(state.publish).toHaveBeenCalledOnce());
      expect(capture.errors).not.toHaveBeenCalled();
    } else {
      await capture.persistence.load('shot-alpha');
      await capture.persistence.save('shot-alpha', { prompt: 'First prompt' });
      const ownHead = state.read().primary_timeline.head.revision_id;
      await capture.persistence.save('shot-alpha', { prompt: 'Second prompt' });
      expect(state.publish.mock.calls[1]?.[0].expectedHeadRevisionId).toBe(ownHead);
    }
    expect(state.publish.mock.calls[0]?.[0].expectedHeadRevisionId).toBe(state.base.headRevisionId);
    expect(state.read().primary_timeline.head.revision_id).not.toBe(state.base.headRevisionId);
  });

});

describe('direct shot writer raw payload preservation', () => {
  const opaque = JSON.parse('{"not_namespaced":{"nested":[null,false,0,"item-1"]},"nullable":null,"ordered":[3,1,2,1],"__proto__":{"literal":true},"constructor":{"prototype":0},"prototype":false}');

  function inputGraph() {
    const graph = structuredClone(fixture) as Record<string, any>;
    Object.assign(graph, { opaque: structuredClone(opaque) });
    graph.parent_composition = { ...graph.parent_composition, ...opaque };
    graph.parent_composition.config = { ...graph.parent_composition.config, ...opaque };
    const revision = graph.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha');
    graph.shot_revisions[graph.shot_revisions.indexOf(revision)] = {
      ...revision, ...opaque,
      output: { ...opaque },
      config: { ...opaque },
      settings: {
        ...opaque, prompt: 'Original', negativePrompt: null,
        pairConfigs: [{ id: 'pair-1', prompt: 'Pair', frames: 61, ...opaque }],
        modelSettingsByModel: { 'wan-2.2': { batchVideoFrames: 61, batchVideoSteps: 6, ...opaque }, future_model: null },
      },
      provenance: { ...revision.provenance, ...opaque },
      internal_timeline_revision: {
        ...revision.internal_timeline_revision, ...opaque,
        timeline: {
          ...revision.internal_timeline_revision.timeline, ...opaque,
          output: { fps: 30, width: 1920, height: 1080, ...opaque },
          config: { ...opaque },
          tracks: revision.internal_timeline_revision.timeline.tracks.map((row: Record<string, any>) => ({ ...row, ...opaque })),
          clips: revision.internal_timeline_revision.timeline.clips.map((row: Record<string, any>) => ({ ...row, ...opaque })),
        },
      },
    };
    graph.occurrences = graph.occurrences.map((row: Record<string, any>) => ({ ...row, ...opaque }));
    return graph as typeof fixture;
  }

  it.each(['name', 'settings'] as const)('keeps every unrelated raw field in the %s writer graph and Runtime payload', async (field) => {
    const input = inputGraph();
    const before = structuredClone(input);
    const state = await setup(input);
    const source = state.base.occurrences.find((row) => row.occurrenceId === 'occ-1')!.revision as Record<string, any>;
    if (field === 'name') {
      capture.onName('Renamed');
      await waitFor(() => expect(state.publications).toHaveLength(1));
      expect(capture.errors).not.toHaveBeenCalled();
    } else {
      const loaded = await capture.persistence.load('shot-alpha');
      expect(Object.hasOwn(loaded, 'not_namespaced')).toBe(false);
      await capture.persistence.save('shot-alpha', { ...loaded, prompt: 'Revised' });
    }
    const graph = state.read() as Record<string, any>;
    const selected = graph.occurrences.find((row: Record<string, any>) => row.occurrence_id === 'occ-1');
    const revision = graph.shot_revisions.find((row: Record<string, any>) => row.revision_id === selected.revision_id);
    assert.deepStrictEqual(revision.settings, field === 'settings' ? { ...source.settings, prompt: 'Revised' } : source.settings);
    assert.deepStrictEqual(revision.provenance, field === 'name' ? { ...source.provenance, name: 'Renamed' } : source.provenance);
    const expectedInternal = {
      ...source.internal_timeline_revision,
      revision_id: revision.internal_timeline_revision.revision_id,
      content_digest: revision.internal_timeline_revision.content_digest,
      publish: true,
      timeline: {
        ...source.internal_timeline_revision.timeline,
        clips: source.internal_timeline_revision.timeline.clips.map((row: Record<string, any>) => ({ ...row, id: `${selected.shot_id}:${row.id}` })),
      },
    };
    assert.deepStrictEqual(revision, {
      ...source,
      shot_id: selected.shot_id,
      revision_id: selected.revision_id,
      content_digest: revision.content_digest,
      publish: true,
      settings: field === 'settings' ? { ...source.settings, prompt: 'Revised' } : source.settings,
      provenance: field === 'name' ? { ...source.provenance, name: 'Renamed' } : source.provenance,
      internal_timeline_revision: expectedInternal,
    });
    assert.deepStrictEqual(graph.shot_revisions.slice(0, -1), before.shot_revisions);
    assert.deepStrictEqual(graph.occurrences.slice(1), before.occurrences.slice(1));
    assert.deepStrictEqual(graph.opaque, opaque);
    assert.deepStrictEqual(input, before);
    const wire = state.publications[0];
    const { shot_id, revision_id, document_role, content_digest, internal_timeline_revision, publish, ...payload } = revision;
    assert.deepStrictEqual(wire.shot_revisions, [{ shot_id, revision_id, internal_timeline_revision_id: internal_timeline_revision.revision_id, payload }]);
    assert.deepStrictEqual(wire.internal_timeline_revisions[0].payload, internal_timeline_revision.timeline);
    const { occurrences, config, ...parentEnvelope } = wire.parent_composition;
    assert.deepStrictEqual(config, before.parent_composition.config);
    assert.deepStrictEqual(parentEnvelope, { ...opaque, registry: {}, clips: [] });
    for (const occurrence of occurrences) {
      for (const key of Object.keys(opaque)) assert.deepStrictEqual(occurrence[key], opaque[key]);
    }
    expect(Object.hasOwn(payload.settings, 'customWidth')).toBe(false);
    expect(Object.hasOwn(payload.settings, '__proto__')).toBe(true);
    expect(Object.getPrototypeOf(payload.settings)).toBe(Object.prototype);
  });

  it.each(['pairConfigs', 'modelSettingsByModel'] as const)('visibly keeps the draft when a changed %s would replace hidden authored data', async (key) => {
    const state = await setup(inputGraph());
    const persistence = capture.persistence;
    const loaded = await persistence.load('shot-alpha');
    const store = createEntityStore<Record<string, any>>({
      toolId: 'shot-settings-preservation',
      defaults: {},
      load: async () => ({ db: loaded, lastUsed: null }),
      save: persistence.save,
    });
    await store.getState().ensureEntity('shot-alpha');
    const value = key === 'pairConfigs'
      ? loaded.pairConfigs.map((pair: Record<string, any>) => ({ ...pair, prompt: 'Changed pair' }))
      : { ...loaded.modelSettingsByModel, 'wan-2.2': { ...loaded.modelSettingsByModel['wan-2.2'], batchVideoSteps: 12 } };
    store.getState().updateFields('shot-alpha', { prompt: 'Also pending', [key]: value });
    const draft = structuredClone(store.getState().entities['shot-alpha'].settings);
    await expect(store.getState().saveImmediate('shot-alpha')).rejects.toThrow(`Cannot safely replace shot setting ${key}`);
    expect(capture.errors).toHaveBeenCalledWith(expect.any(Error), expect.objectContaining({ toastTitle: 'Shot settings draft kept' }));
    expect(store.getState().entities['shot-alpha'].status).toBe('error');
    expect(store.getState().isDirty('shot-alpha')).toBe(true);
    assert.deepStrictEqual(store.getState().entities['shot-alpha'].settings, draft);
    assert.deepStrictEqual(store.getState().entities['shot-alpha'].cleanSnapshot, loaded);
    expect(state.publish).not.toHaveBeenCalled();
    assert.deepStrictEqual(state.read(), inputGraph());
    // A refused batch has not advanced the editing base or poisoned its queue.
    await persistence.save('shot-alpha', { ...loaded, prompt: 'Safe prompt' });
    expect(state.publish).toHaveBeenCalledOnce();
  });

  it.each(['absent', 'null', 'empty'] as const)('keeps an unchanged %s settings root without publishing display defaults', async (shape) => {
    const input = structuredClone(fixture) as Record<string, any>;
    const source = input.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha');
    if (shape === 'absent') delete source.settings;
    else source.settings = shape === 'null' ? null : {};
    const before = structuredClone(input);
    const state = await setup(input as typeof fixture);
    const loaded = await capture.persistence.load('shot-alpha');
    await capture.persistence.save('shot-alpha', loaded ?? normalizeVideoTravelSettings(null));
    expect(state.publish).not.toHaveBeenCalled();
    assert.deepStrictEqual(state.read(), before);
    assert.deepStrictEqual(input, before);
  });

  it.each(['absent', 'null'] as const)('authors only the changed prompt when initializing an %s settings root', async (shape) => {
    const input = structuredClone(fixture) as Record<string, any>;
    const source = input.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha');
    if (shape === 'absent') delete source.settings;
    else source.settings = null;
    const before = structuredClone(input);
    const state = await setup(input as typeof fixture);
    await capture.persistence.load('shot-alpha');
    await capture.persistence.save('shot-alpha', { ...normalizeVideoTravelSettings(null), prompt: 'First authored prompt' });
    assert.deepStrictEqual(state.publications[0].shot_revisions[0].payload.settings, { prompt: 'First authored prompt' });
    assert.deepStrictEqual(state.read().shot_revisions.slice(0, -1), before.shot_revisions);
    assert.deepStrictEqual(input, before);
  });

  it.each([['opaque-root', null], 'opaque-root', false, 0].map((raw) => ({ raw })))('keeps the draft before replacing an unrepresented raw settings root $raw', async ({ raw }) => {
    const input = structuredClone(fixture) as Record<string, any>;
    input.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha').settings = raw;
    const before = structuredClone(input);
    const state = await setup(input as typeof fixture);
    const persistence = capture.persistence;
    await persistence.load('shot-alpha');
    const loaded = normalizeVideoTravelSettings(raw);
    const store = createEntityStore<Record<string, any>>({
      toolId: 'shot-settings-root-preservation', defaults: {},
      load: async () => ({ db: loaded, lastUsed: null }), save: persistence.save,
    });
    await store.getState().ensureEntity('shot-alpha');
    store.getState().updateFields('shot-alpha', { prompt: 'Pending prompt' });
    const draft = structuredClone(store.getState().entities['shot-alpha'].settings);
    await expect(store.getState().saveImmediate('shot-alpha')).rejects.toThrow('Cannot safely replace shot settings');
    expect(capture.errors).toHaveBeenCalledWith(expect.any(Error), expect.objectContaining({ toastTitle: 'Shot settings draft kept' }));
    expect(store.getState().entities['shot-alpha'].status).toBe('error');
    expect(store.getState().isDirty('shot-alpha')).toBe(true);
    assert.deepStrictEqual(store.getState().entities['shot-alpha'].settings, draft);
    assert.deepStrictEqual(store.getState().entities['shot-alpha'].cleanSnapshot, loaded);
    expect(state.publish).not.toHaveBeenCalled();
    assert.deepStrictEqual(state.read(), before);
    assert.deepStrictEqual(input, before);
  });

  it('ignores nested object key order while preserving the complete raw settings on a prompt edit', async () => {
    const input = inputGraph();
    const source = input.shot_revisions.find((row) => row.shot_id === 'shot-alpha')! as Record<string, any>;
    const state = await setup(input);
    const loaded = await capture.persistence.load('shot-alpha');
    const reorder = (value: any): any => Array.isArray(value)
      ? value.map(reorder)
      : value && typeof value === 'object'
        ? Object.fromEntries(Object.entries(value).reverse().map(([key, child]) => [key, reorder(child)]))
        : value;
    await capture.persistence.save('shot-alpha', { ...reorder(loaded), prompt: 'Reordered form' });
    expect(capture.errors).not.toHaveBeenCalled();
    assert.deepStrictEqual(state.publications[0].shot_revisions[0].payload.settings, { ...source.settings, prompt: 'Reordered form' });
  });

  it('keeps ordinary compound edits, array order, and explicit root clears working', async () => {
    const input = structuredClone(fixture) as Record<string, any>;
    const source = input.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha');
    source.settings = {
      prompt: 'Before', selectedPhasePresetId: 'preset-1',
      pairConfigs: [
        { id: 'pair-2', prompt: 'Second', negativePrompt: '', frames: 61, context: 0 },
        { id: 'pair-1', prompt: 'First', negativePrompt: '', frames: 61, context: 0 },
      ],
    };
    const state = await setup(input as typeof fixture);
    const loaded = await capture.persistence.load('shot-alpha');
    const pairs = loaded.pairConfigs.map((pair: Record<string, any>) => ({ ...pair, frames: 81 }));
    await capture.persistence.save('shot-alpha', { ...loaded, pairConfigs: pairs, selectedPhasePresetId: null });
    const payload = state.publications[0].shot_revisions[0].payload;
    assert.deepStrictEqual(payload.settings, { ...source.settings, pairConfigs: pairs, selectedPhasePresetId: null });
    await capture.persistence.save('shot-alpha', { ...loaded, pairConfigs: pairs, selectedPhasePresetId: undefined });
    expect(Object.hasOwn(state.publications[1].shot_revisions[0].payload.settings, 'selectedPhasePresetId')).toBe(false);
  });

  it.each([null, undefined])('keeps an explicit compound root clear %j working when the form contains its complete authored value', async (clear) => {
    const input = structuredClone(fixture) as Record<string, any>;
    const source = input.shot_revisions.find((row: Record<string, any>) => row.shot_id === 'shot-alpha');
    source.settings = { prompt: 'Before', phaseConfig: { steps: [1, 2, 1], note: null } };
    const state = await setup(input as typeof fixture);
    const loaded = await capture.persistence.load('shot-alpha');
    await capture.persistence.save('shot-alpha', { ...loaded, phaseConfig: clear });
    assert.deepStrictEqual(state.publications[0].shot_revisions[0].payload.settings, {
      prompt: 'Before', ...(clear === undefined ? {} : { phaseConfig: null }),
    });
  });
});
