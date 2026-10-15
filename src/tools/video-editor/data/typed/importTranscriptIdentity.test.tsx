// @vitest-environment jsdom
import React, { useEffect } from 'react';
import { act, renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import type { DataLaneRenderItem } from '@/sdk/index.ts';
import { createHostGeneratedObjectMeta } from '@/sdk/video/timeline/sourceMap.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import type { DataProvider } from '@/tools/video-editor/data/DataProvider.ts';
import {
  buildTranscriptCaptionPatch, transcriptCaptionClipId,
  TRANSCRIPT_LANE_EXTENSION_ID, TRANSCRIPT_CAPTION_TRACK_ID,
} from '@/tools/video-editor/dev/transcript-lane/extension.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { useTimelineHistory } from '@/tools/video-editor/hooks/useTimelineHistory.ts';
import { useTimelinePersistence } from '@/tools/video-editor/hooks/useTimelinePersistence.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { AssetRegistry, TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { normalizeTranscriptSource, TRANSCRIPT_SCHEMA_REF } from './adaptTranscript.ts';
import type { SourceFrozenDataItem } from './envelope.ts';
import { createTranscriptImportCallback } from './importTranscriptHandoff.ts';
import { mapReplacedTranscriptIdentities } from './reconcileTranscriptReferences.ts';
import { parseTimelineBundle, type TimelineBundleEnvelope } from './timelineBundle.ts';

vi.stubGlobal('indexedDB', createFakeIndexedDB());
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({
  invalidateReferencedTimelineCache: vi.fn(),
}));

const reviewKey = (id: string) => `transcript-source-review:${encodeURIComponent(id)}`;
const documentFor = (assetId = 'audio-a') => ({
  assetId, sourceId: 'capture-1',
  segments: [{ id: 'segment-1', start: 0, end: 2, text: 'Source text',
    words: [{ id: 'word-1', start: 0, end: 1, text: 'Source' }] }],
});
const canonicalSource = (assetId = 'audio-a') => normalizeTranscriptSource(documentFor(assetId))[0];
const legacySource = (assetId = 'audio-a'): SourceFrozenDataItem => {
  const canonical = canonicalSource(assetId);
  return JSON.parse(JSON.stringify(canonical).replaceAll(
    `transcript-source:${assetId}:source:capture-1:segment:`,
    'transcript-source:capture-1:segment:',
  )) as SourceFrozenDataItem;
};
const review = (sourceItemId: string) => ({
  schemaVersion: 1, sourceSchemaRef: TRANSCRIPT_SCHEMA_REF, sourceItemId,
  status: 'accepted-for-source-update', proposedText: 'Human correction',
  proposedTimelineStart: 0.1, proposedTimelineEnd: 2.4,
  sourceFingerprintAtGeneration: 'original-source-fingerprint',
  currentSourceFingerprint: 'reviewed-source-fingerprint',
  generatedOutputFingerprint: 'original-output-fingerprint',
  editedOutputFingerprint: 'human-output-fingerprint', generatorVersion: '1.3.0',
  handoffFingerprint: 'accepted-handoff-fingerprint', decisionRevision: 12,
});
const registry: AssetRegistry = { assets: {
  'audio-a': { file: 'audio-a.wav', type: 'audio/wav', duration: 8 },
  'audio-b': { file: 'audio-b.wav', type: 'audio/wav', duration: 8 },
} };
function configFor(oldId: string, withReferences = true): TimelineConfig {
  return {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'A1', kind: 'audio', label: 'Audio', muted: false },
      { id: TRANSCRIPT_CAPTION_TRACK_ID, kind: 'visual', label: 'Captions', muted: false }],
    clips: [
      { id: 'media-a', asset: 'audio-a', track: 'A1', clipType: 'audio', at: 0, from: 0, to: 8 },
      ...(withReferences ? [{
        id: transcriptCaptionClipId(`${oldId}@media-a`), track: TRANSCRIPT_CAPTION_TRACK_ID,
        clipType: 'text' as const, at: 0.1, hold: 2.3, x: 143, y: 620,
        text: { content: 'Human correction', color: '#cc3377', fontSize: 51 },
        app: { retained: 'custom metadata', __generated__: createHostGeneratedObjectMeta({
          extensionId: TRANSCRIPT_LANE_EXTENSION_ID, contributionId: 'transcript-caption-foundry',
          extensionVersion: '1.3.0', sourceSchemaRef: TRANSCRIPT_SCHEMA_REF,
          sourceItemId: oldId, sourceValue: { sourceItemId: oldId }, outputValue: 'original text',
        }) },
      }] : []),
    ],
    ...(withReferences ? { app: { unrelated: { keep: true }, [TRANSCRIPT_LANE_EXTENSION_ID]: {
      preferences: { color: 'blue' }, [reviewKey(oldId)]: review(oldId),
    } } } : {}),
  };
}
async function dataFor(sources = [legacySource()], withReferences = true) {
  return buildTimelineData(configFor(sources[0].id, withReferences), registry, (file) => file, 1,
    { [TRANSCRIPT_SCHEMA_REF]: sources });
}
function importer(data: TimelineData) {
  const dataRef = { current: data };
  const commitData = vi.fn((next: TimelineData) => { dataRef.current = next; });
  return { dataRef, commitData, importTranscript: createTranscriptImportCallback({ dataRef, commitData }) };
}

describe('transcript legacy reference reconciliation', () => {
  it('maps segment/word identities only within the exact replaced asset and source', () => {
    const old = legacySource();
    const next = canonicalSource();
    const mapping = mapReplacedTranscriptIdentities([old, legacySource('audio-b')], [next], 'audio-a', 'capture-1');
    expect([...mapping.segments]).toEqual([[old.id, next.id]]);
    expect([...mapping.words]).toEqual([[`${old.id}:word:word-1`, `${next.id}:word:word-1`]]);
    expect(mapReplacedTranscriptIdentities([old], [next], 'audio-b', 'capture-1').segments.size).toBe(0);
    expect(mapReplacedTranscriptIdentities([old], [next], 'audio-a', 'other-source').segments.size).toBe(0);
  });

  it('reimports legacy captions and review references in one semantic save, retaining human edits and review state', async () => {
    const data = await dataFor();
    const original = structuredClone(data.config);
    const host = importer(data);
    host.importTranscript({ document: documentFor() });
    const next = host.dataRef.current;
    const old = legacySource().id;
    const canonical = canonicalSource().id;
    expect(host.commitData).toHaveBeenCalledExactlyOnceWith(next, { save: true, semantic: true });
    expect(next.config.clips[1]).toEqual({
      ...original.clips[1], id: transcriptCaptionClipId(`${canonical}@media-a`),
      app: { ...original.clips[1].app, __generated__: {
        ...original.clips[1].app!.__generated__ as object,
        provenance: { ...(original.clips[1].app!.__generated__ as { provenance: object }).provenance,
          sourceItemId: canonical },
      } },
    });
    expect(next.config.app?.[TRANSCRIPT_LANE_EXTENSION_ID]).toEqual({
      preferences: { color: 'blue' }, [reviewKey(canonical)]: { ...review(old), sourceItemId: canonical },
    });
    expect(next.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF]).toEqual([canonicalSource()]);
    expect(data.config).toEqual(original);
  });

  it('repeated import and preserve-mode caption materialization keep one edited caption and one review', async () => {
    const host = importer(await dataFor());
    host.importTranscript({ document: documentFor() });
    const first = structuredClone(host.dataRef.current.config);
    host.importTranscript({ document: documentFor() });
    expect(host.dataRef.current.config).toEqual(first);
    const source = canonicalSource();
    const caption = host.dataRef.current.config.clips[1];
    const patch = buildTranscriptCaptionPatch({
      baseVersion: 2, outputMetadata: { resolution: '1920x1080', fps: 30 },
      tracks: [{ id: TRANSCRIPT_CAPTION_TRACK_ID, kind: 'visual' }],
      clips: [{ id: caption.id, track: caption.track }],
    } as Parameters<typeof buildTranscriptCaptionPatch>[0], [{
      id: `${source.id}@media-a`, sourceItemId: source.id, payload: source.payload,
      timelineStart: 0, timelineEnd: 2,
    } as DataLaneRenderItem]);
    expect(patch.operations).toEqual([]);
    expect(host.dataRef.current.config.clips.filter((clip) => clip.track === TRANSCRIPT_CAPTION_TRACK_ID)).toHaveLength(1);
    expect(host.dataRef.current.config.clips[1].text?.content).toBe('Human correction');
    expect(Object.keys(host.dataRef.current.config.app![TRANSCRIPT_LANE_EXTENSION_ID] as object)).toHaveLength(2);
  });

  it('leaves ambiguous shared reviews and asset-level captions unresolved through sequential imports', async () => {
    const data = await dataFor([legacySource(), legacySource('audio-b')]);
    const old = legacySource().id;
    data.config.clips[1].id = transcriptCaptionClipId(`${old}@source`);
    const config = structuredClone(data.config);
    const host = importer(data);
    host.importTranscript({ document: documentFor() });
    host.importTranscript({ document: documentFor('audio-b') });
    host.importTranscript({ document: documentFor() });
    expect(host.dataRef.current.config).toEqual(config);
    expect(host.dataRef.current.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF]).toEqual([
      canonicalSource('audio-b'), canonicalSource(),
    ]);
    expect(host.dataRef.current.config.app?.[TRANSCRIPT_LANE_EXTENSION_ID]).toHaveProperty(reviewKey(old));
    expect(host.dataRef.current.config.app?.[TRANSCRIPT_LANE_EXTENSION_ID]).not.toHaveProperty(reviewKey(canonicalSource().id));
  });

  it('uses a media occurrence to resolve a shared caption without assigning the ambiguous review', async () => {
    const host = importer(await dataFor([legacySource(), legacySource('audio-b')]));
    host.importTranscript({ document: documentFor('audio-b') });
    expect(host.dataRef.current.config.clips[1].id).toBe(transcriptCaptionClipId(`${legacySource().id}@media-a`));
    host.importTranscript({ document: documentFor() });
    expect(host.dataRef.current.config.clips[1].id).toBe(transcriptCaptionClipId(`${canonicalSource().id}@media-a`));
    expect(host.dataRef.current.config.app?.[TRANSCRIPT_LANE_EXTENSION_ID]).toHaveProperty(reviewKey(legacySource().id));
  });

  it('preserves omitted-source fallback identities and references', async () => {
    const { assetId, segments } = documentFor();
    const document = { assetId, segments };
    const fallback = normalizeTranscriptSource(document)[0];
    const data = await buildTimelineData(configFor(fallback.id), registry, (file) => file, 1,
      { [TRANSCRIPT_SCHEMA_REF]: [fallback] });
    const host = importer(data);
    host.importTranscript({ document });
    expect(host.dataRef.current.config).toEqual(data.config);
    expect(host.dataRef.current.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF]).toEqual([fallback]);
  });
});

describe('canonical import history and persistence', () => {
  it.each([false, true])('undoes/redoes then saves and reopens sources and references together (references: %s)', async (withReferences) => {
    const initial = await dataFor([legacySource()], withReferences);
    let saved: { config: TimelineConfig; registry: AssetRegistry; bundle: TimelineBundleEnvelope } | undefined;
    const provider: DataProvider = {
      persistenceEnabled: true,
      loadTimeline: vi.fn(async () => ({ config: initial.config, configVersion: 1 })),
      loadAssetRegistry: vi.fn(async () => registry), resolveAssetUrl: (file) => file,
      saveTimeline: vi.fn(async (_id, config, _version, assets, bundle) => {
        saved = JSON.parse(JSON.stringify({ config, registry: assets, bundle }));
        return 2;
      }),
    };
    const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={client}><VideoEditorRuntimeProvider value={{
        provider, timelineId: 'identity-integration', project: { projectId: 'project-1' },
      } as VideoEditorRuntimeContextValue}>{children}</VideoEditorRuntimeProvider></QueryClientProvider>
    );
    const eventBus = new TimelineEventBus();
    const lastSavedSignatureRef = { current: initial.stableSignature };
    const interactionStateRef = { current: createInteractionState() };
    const savedSeqRef = { current: 0 };
    const configVersionRef = { current: 1 };
    const hook = renderHook(() => {
      const commit = useTimelineCommit({ initialData: initial, eventBus, lastSavedSignatureRef });
      const history = useTimelineHistory({ dataRef: commit.dataRef, commitData: commit.commitData,
        interactionStateRef, pendingOpsRef: commit.pendingOpsRef });
      const persistence = useTimelinePersistence({ provider, timelineId: 'identity-integration', eventBus,
        dataRef: commit.dataRef, commitData: commit.commitData, selectedClipIdRef: commit.selectedClipIdRef,
        selectedTrackIdRef: commit.selectedTrackIdRef, editSeqRef: commit.editSeqRef, savedSeqRef,
        configVersionRef, lastSavedSignatureRef, interactionStateRef });
      useEffect(() => eventBus.on('beforeCommit', history.onBeforeCommit), [history.onBeforeCommit]);
      useEffect(() => eventBus.on('scheduleSave', persistence.scheduleSave), [persistence.scheduleSave]);
      return { commit, history, persistence };
    }, { wrapper });
    act(() => createTranscriptImportCallback(hook.result.current.commit)({ document: documentFor() }));
    const imported = hook.result.current.commit.dataRef.current!;
    act(() => hook.result.current.history.undo());
    expect(hook.result.current.commit.dataRef.current!.sourceItemsBySchemaRef).toEqual(initial.sourceItemsBySchemaRef);
    expect(hook.result.current.commit.dataRef.current!.config).toEqual(initial.config);
    act(() => hook.result.current.history.redo());
    expect(hook.result.current.commit.dataRef.current!.sourceItemsBySchemaRef).toEqual(imported.sourceItemsBySchemaRef);
    expect(hook.result.current.commit.dataRef.current!.config).toEqual(imported.config);
    await act(async () => { await hook.result.current.persistence.flushPendingSave(); });
    expect(saved).toBeDefined();
    const reopened = await buildTimelineData(saved!.config, saved!.registry, (file) => file, 2,
      parseTimelineBundle(saved!.bundle).itemsBySchemaRef);
    expect(reopened.sourceItemsBySchemaRef).toEqual(imported.sourceItemsBySchemaRef);
    expect(reopened.config).toEqual(imported.config);
    if (!withReferences) expect(imported.config).toEqual(initial.config);
    hook.unmount();
    client.clear();
  });
});
