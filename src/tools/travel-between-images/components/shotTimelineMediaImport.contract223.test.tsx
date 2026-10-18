// @vitest-environment jsdom
// Import/selection forwarding and refusal guards. The sealed 223 probe remains
// diagnostic evidence; the coupled 226 selector owns prepared SDK acceptance.
import React, { useEffect } from 'react';
import { act, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { writeFileSync } from 'node:fs';
// @ts-expect-error Local JavaScript fixture has no declarations.
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
vi.mock('@/shared/media/clientThumbnailGenerator.ts', () => ({ generateClientThumbnail: vi.fn(async () => { throw new Error('legacy-import-refused-by-fixture'); }), uploadImageWithThumbnail: vi.fn() }));
vi.mock('@/shared/lib/media/imageUploader.ts', () => ({ uploadImageToStorage: vi.fn(async () => { throw new Error('legacy-import-refused-by-fixture'); }), uploadBlobToStorage: vi.fn() }));
import fixture from '@/tools/video-editor/data/shotComposition.fixture.json';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import { createShotCompositionAdapter, type ShotCompositionPublishRequest } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { StaleWriteError } from '@/tools/video-editor/data/shotComposition.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { handleFileDrop } from '@/tools/video-editor/lib/external-drop-utils.ts';
import { useAssetManagement } from '@/tools/video-editor/hooks/useAssetManagement.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { useTimelinePersistence } from '@/tools/video-editor/hooks/useTimelinePersistence.ts';
import { useClipEditing } from '@/tools/video-editor/hooks/useClipEditing.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { loadTimelineDraft } from '@/tools/video-editor/data/timelineDraftIndexedDb.ts';
import { createShotTimelineDataProvider, createShotTimelineInitialData } from './shotTimelineDataProvider.ts';

const json = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
const selection = { asset: `sha256:${'a'.repeat(64)}`, generation_id: 'generation-223', variant_id: 'variant-223', object_id: `sha256:${'a'.repeat(64)}`, catalog_digest: `sha256:${'b'.repeat(64)}` };
const captures: Record<string, unknown> = {};
function setup(options: { importRefused?: boolean; selectionRefused?: boolean; selectionMismatch?: boolean; wrongImportProject?: boolean; importGate?: Promise<void>; readOnly?: boolean; withoutImporter?: boolean; stale?: boolean } = {}) {
  const graph = structuredClone(fixture);
  // Existing authored clip fixture; assets remain the canonical graph's assets.
  const revision = graph.shot_revisions.find(row => row.shot_id === 'shot-alpha' && row.revision_id === 'rev-a')!;
  (revision.internal_timeline_revision.timeline as unknown as Record<string, unknown>).clips = [{ id: 'clip-223', clipType: 'hold', at: 0, hold: 2, track: 'video', app: { opaque: [null, { keep: true }] } }];
  const calls: Array<{ method: string; path: string; headers: Record<string, string> }> = [];
  const transport: Transport = async (method, path, headers) => {
    calls.push({ method, path, headers });
    const ok = (body: unknown, status = 200) => ({ status, headers: {}, body: json(body) });
    if (path === '/v1/health') return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1 });
    if (path === '/v1/handshake') return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'fixture-223', actor_id: 'reigh-product-connector', realm_id: 'fixture-223', scopes: RUNTIME_CLIENT_SCOPES, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] });
    if (path === '/v1/realm') return ok({ realm_id: 'fixture-223' });
    if (method === 'POST' && path.endsWith('/media-imports')) {
      await options.importGate;
      if (options.importRefused) return ok({ error: { code: 'forbidden', message: 'fixture import refusal' } }, 403);
      return ok({ data: { provider: 'runtime', project: options.wrongImportProject ? 'other-project' : 'project-001', import_operation_id: headers['Idempotency-Key'], status: 'completed', generation_id: selection.generation_id, variant_id: selection.variant_id, asset_id: selection.asset, entry: { object_id: selection.object_id, media_type: 'image/png', filename: '223.png', size: 3 } }, receipt: { receipt_id: 'fixture-223', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] } }, 201);
    }
    if (method === 'GET' && path.includes('/media-imports/')) return ok({ error: { code: 'not_found', message: 'fixture operation not found' } }, 404);
    if (path.includes('/media-selection?')) {
      if (options.selectionRefused) return ok({ error: { code: 'forbidden', message: 'fixture selection refusal' } }, 403);
      return ok(options.selectionMismatch ? { ...selection, variant_id: 'other-variant' } : selection);
    }
    throw new Error(`Unexpected fixture call ${method} ${path}`);
  };
  const runtime = new RuntimeDataProvider({ projectId: 'project-001', baseUrl: 'http://fixture.invalid', token: 'fixture-only', transport, commitRouting: { enabled: true } });
  const publish = vi.fn(async (_request: ShotCompositionPublishRequest) => { throw new StaleWriteError('fixture publication refusal'); });
  const adapter = createShotCompositionAdapter({
    ...runtime.shotComposition,
    load: async () => graph, publish: options.readOnly ? undefined : publish,
    // Preserve the 223 boundary fixture's legacy recovery slot. This does not
    // replace the Runtime import or selection operations under test.
    getTimelineDraftRecoveryMetadata: undefined,
    ...(options.withoutImporter ? { prepareMediaImport: undefined, getProjectMediaSelection: undefined } : {}),
  });
  const composition = adapter.prepare(graph);
  const config = projectCanonicalComposition({ ...composition, occurrences: [composition.occurrences[0]] }, { output: { resolution: '1920x1080', fps: 30, file: 'fixture.mp4' }, clips: [], tracks: [], registry: {} }, { clampToOccurrenceDuration: false }).config;
  const editorHeadState = { current: { canonicalHeadRevisionId: composition.headRevisionId, displayedHeadRevisionId: options.stale ? 'stale-display' : composition.headRevisionId } };
  const popup = createShotTimelineDataProvider(config, composition, 'occ-1', adapter, undefined, editorHeadState);
  const initial = createShotTimelineInitialData(config, 1, composition);
  return { runtime, popup, graph, composition, initial, calls, publish, editorHeadState };
}
function runtimeValue(provider: VideoEditorRuntimeContextValue['provider']) {
  return { provider, assetResolver: { resolveAssetUrl: provider.resolveAssetUrl }, auth: {}, project: {}, shots: {}, mediaLightbox: {}, agentChat: {}, toast: { error: vi.fn(), warning: vi.fn(), info: vi.fn(), success: vi.fn() }, telemetry: {}, timelineId: 'popup-223', userId: null, extensions: {} } as unknown as VideoEditorRuntimeContextValue;
}
function assets(h: ReturnType<typeof setup>, provider = h.popup) {
  const applyEdit = vi.fn();
  const patchRegistry = vi.fn();
  const eventBus = new TimelineEventBus();
  const lastSavedSignatureRef = { current: h.initial.stableSignature };
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, initialData: h.initial, lastSavedSignatureRef });
    const management = useAssetManagement({ dataRef: commit.dataRef, selectedTrackId: 'video', selectedProjectId: 'project-001',
      selectClip: vi.fn(), setSelectedTrackId: vi.fn(),
      applyEdit: (mutation, options) => { applyEdit(mutation, options); commit.applyEdit(mutation, options); },
      patchRegistry, invalidateAssetRegistry: vi.fn(), resolveAssetUrl: provider.resolveAssetUrl });
    return { ...management, dataRef: commit.dataRef };
  }, { wrapper: ({ children }) => <VideoEditorRuntimeProvider value={runtimeValue(provider)}>{children}</VideoEditorRuntimeProvider> });
  return { ...hook, applyEdit, patchRegistry, dataRef: hook.result.current.dataRef };
}
beforeEach(() => { vi.stubGlobal('indexedDB', createFakeIndexedDB()); });
afterEach(() => { resetFakeIndexedDB(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

describe('popup media-import forwarding 224 (catalog only)', () => {
  it('forwards import and selection once and stages only a guarded occurrence command', async () => {
    const h = setup();
    const hook = assets(h);
    const original = structuredClone(h.initial);
    const uploaded = await hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }));
    const prepared = hook.result.current.prepareGenerationAsset(uploaded)!;
    expect(uploaded.mediaImport).toMatchObject({ project: 'project-001', provider: 'runtime', assetId: selection.asset, selectedMedia: selection });
    expect(Object.keys(prepared.selectedMedia!).sort()).toEqual(Object.keys(selection).sort());
    expect(prepared.selectedMedia).toBe(uploaded.mediaImport!.selectedMedia);
    expect(prepared.entry.media_id).toBe(selection.object_id);
    expect(prepared.entry.content_sha256).toBe(selection.object_id);
    expect(hook.result.current.handleAssetDrop(prepared.assetKey, 'video', 0, false, false, prepared)).toBe(true);
    expect(hook.result.current.handleAssetDrop(prepared.assetKey, 'video', 0)).toBe(false);
    expect(hook.result.current.registerGenerationAsset(uploaded)).toBeNull();
    expect(hook.applyEdit).toHaveBeenCalledTimes(1);
    expect(hook.applyEdit.mock.calls[0]).toMatchObject([{ type: 'commands' }, { occurrenceContext: { occurrenceId: 'occ-1' }, editCommands: [{ op: 'timeline.add', select: 'occurrence:occ-1/track:video', args: { media: selection } }] }]);
    expect(hook.patchRegistry).not.toHaveBeenCalled();
    expect(hook.dataRef.current?.config.clips).toEqual(original.config.clips);
    expect(h.calls.filter(row => row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.filter(row => row.path.includes('/media-selection?'))).toHaveLength(1);
    expect(h.calls.some(row => row.path.endsWith('/commit') || row.path.endsWith('/composition-revisions'))).toBe(false);
    expect(h.publish).not.toHaveBeenCalled();
    captures.actualPopup = { import: uploaded.mediaImport, calls: h.calls, placementEnabled: h.popup.preparedMediaPlacementEnabled, editorMutations: hook.applyEdit.mock.calls };
    hook.unmount();
  });

  it('refuses another project before import or selection IO at both forwarding boundaries', async () => {
    const h = setup();
    const file = new File(['223'], '223.png', { type: 'image/png' });
    await expect(h.runtime.shotComposition.prepareMediaImport!({ projectId: 'other-project' }, file)).rejects.toThrow('different project');
    await expect(h.popup.getProjectMediaSelection!({ projectId: 'other-project', asset: selection.asset, generationId: selection.generation_id, variantId: selection.variant_id })).rejects.toThrow('different project');
    expect(h.calls).toEqual([]);
  });

  it.each([
    ['stale display', { stale: true }, 'still adopting'],
    ['read-only popup', { readOnly: true }, 'read-only'],
    ['missing importer', { withoutImporter: true }, 'does not support Runtime'],
  ] as const)('refuses %s without a legacy upload or editor mutation', async (_label, options, message) => {
    const h = setup(options);
    const hook = assets(h);
    await expect(hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }))).rejects.toThrow(message);
    expect(h.calls).toEqual([]);
    expect(hook.applyEdit).not.toHaveBeenCalled();
    expect(hook.patchRegistry).not.toHaveBeenCalled();
    hook.unmount();
  });

  it('refuses a changed display after a held import response without selecting or placing media', async () => {
    let release!: () => void;
    const h = setup({ importGate: new Promise<void>(resolve => { release = resolve; }) });
    const hook = assets(h);
    const outcome = hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' })).then(value => ({ value }), error => ({ error }));
    await waitFor(() => expect(h.calls.some(row => row.path.endsWith('/media-imports'))).toBe(true));
    h.editorHeadState.current.displayedHeadRevisionId = 'stale-display';
    release();
    expect(await outcome).toMatchObject({ error: expect.objectContaining({ message: expect.stringContaining('still adopting') }) });
    expect(h.calls.filter(row => row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.some(row => row.path.includes('/media-selection?'))).toBe(false);
    expect(hook.applyEdit).not.toHaveBeenCalled();
    expect(hook.patchRegistry).not.toHaveBeenCalled();
    hook.unmount();
  });

  it('rejects an import belonging to another project before selection', async () => {
    const h = setup({ wrongImportProject: true });
    const hook = assets(h);
    await expect(hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }))).rejects.toThrow('not project-001');
    expect(h.calls.filter(row => row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.some(row => row.path.includes('/media-selection?'))).toBe(false);
    expect(hook.applyEdit).not.toHaveBeenCalled();
    hook.unmount();
  });

  it.each([
    ['refused', { selectionRefused: true }],
    ['mismatched', { selectionMismatch: true }],
  ] as const)('keeps %s selection from becoming a placement or registry write', async (_label, options) => {
    const h = setup(options);
    const hook = assets(h);
    const uploaded = await hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }));
    const prepared = hook.result.current.prepareGenerationAsset(uploaded)!;
    expect(prepared.selectedMedia).toBeUndefined();
    expect(prepared.entry.media_id).toBe(selection.object_id);
    expect(hook.result.current.handleAssetDrop(prepared.assetKey, 'video', 0, false, false, prepared)).toBe(false);
    expect(hook.result.current.registerGenerationAsset(uploaded)).toBeNull();
    expect(h.calls.filter(row => row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.filter(row => row.path.includes('/media-selection?'))).toHaveLength(1);
    expect(hook.applyEdit).not.toHaveBeenCalled();
    expect(hook.patchRegistry).not.toHaveBeenCalled();
    hook.unmount();
  });

  it.each([false, true])('cleans temporary import rows and pending work on refusal (transport refused: %s)', async (importRefused) => {
    const h = setup({ importRefused });
    const hook = assets(h);
    const pendingOpsRef = { current: 0 };
    const onAssetDropError = vi.fn();
    await act(async () => { await handleFileDrop({ files: [new File(['223'], '223.png', { type: 'image/png' })], dataRef: hook.dataRef,
      pendingOpsRef, dropPosition: { trackId: 'video', time: 0, rowIndex: 0, trackKind: 'visual', trackName: 'video', isNewTrack: false, isNewTrackTop: false, isReject: false, newTrackKind: null, screenCoords: { rowTop: 0, rowLeft: 0, rowWidth: 100, rowHeight: 40, clipLeft: 0, clipWidth: 10, ghostCenter: 5 } }, insertAtTop: false,
      selectedTrackId: 'video', applyEdit: hook.applyEdit, invalidateAssetRegistry: vi.fn(), resolveAssetUrl: h.popup.resolveAssetUrl,
      registerGenerationAsset: hook.result.current.registerGenerationAsset, prepareGenerationAsset: hook.result.current.prepareGenerationAsset,
      uploadImageGeneration: hook.result.current.uploadImageGeneration, uploadVideoGeneration: hook.result.current.uploadVideoGeneration,
      dropAsset: hook.result.current.handleAssetDrop, directAssetUploadAllFiles: true, mediaImportForImageVideo: true, onAssetDropError }); });
    await waitFor(() => expect(pendingOpsRef.current).toBe(0));
    expect(hook.applyEdit).toHaveBeenCalledTimes(2);
    const skeleton = Object.keys(hook.applyEdit.mock.calls[0][0].metaUpdates!)[0];
    expect(hook.applyEdit.mock.calls[1]).toEqual([expect.objectContaining({ metaDeletes: [skeleton] }), { save: false }]);
    expect(hook.applyEdit.mock.calls.every(([, options]) => options?.save === false && !options.editCommands)).toBe(true);
    expect(hook.patchRegistry).not.toHaveBeenCalled();
    expect(hook.dataRef.current?.config.clips.map(clip => clip.id)).toEqual(h.initial.config.clips.map(clip => clip.id));
    expect(hook.dataRef.current?.rows.flatMap(row => row.actions).some(action => action.id.startsWith('uploading-'))).toBe(false);
    expect(hook.dataRef.current?.registry).toEqual(h.initial.registry);
    expect(h.calls.filter(row => row.method === 'POST' && row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.some(row => row.path.endsWith('/commit'))).toBe(false);
    expect(onAssetDropError).toHaveBeenCalledTimes(importRefused ? 1 : 0);
    captures[importRefused ? 'importRefusal' : 'placementRefusalCleanup'] = { calls: h.calls, temporaryRows: hook.applyEdit.mock.calls, pending: pendingOpsRef.current };
    hook.unmount();
  });

  it('keeps a refused 4s draft recoverable and exposes sub-frame quantization in the public edit hook', async () => {
    const h = setup();
    const eventBus = new TimelineEventBus();
    const query = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    const lastSavedSignatureRef = { current: h.initial.stableSignature };
    const refs = { savedSeqRef: { current: 0 }, configVersionRef: { current: 1 }, headRevisionRef: { current: h.initial.head }, lastSavedSignatureRef, interactionStateRef: { current: createInteractionState() } };
    const hook = renderHook(() => {
      const commit = useTimelineCommit({ eventBus, initialData: h.initial, lastSavedSignatureRef });
      const persistence = useTimelinePersistence({ ...commit, ...refs, provider: h.popup, timelineId: 'popup-223', eventBus });
      useEffect(() => eventBus.on('scheduleSave', persistence.scheduleSave), [persistence.scheduleSave]);
      const editing = useClipEditing({ ...commit, selectedClipId: 'occ-1:clip-223', selectedTrack: h.initial.tracks[0], currentTime: 0, selectClip: vi.fn(), resolvedConfig: commit.data?.resolvedConfig ?? null });
      return { editing, persistence, commit };
    }, { wrapper: ({ children }) => <QueryClientProvider client={query}><VideoEditorRuntimeProvider value={runtimeValue(h.popup)}>{children}</VideoEditorRuntimeProvider></QueryClientProvider> });
    act(() => hook.result.current.editing.handleSelectedClipChange({ hold: 4 }));
    await waitFor(() => expect(h.publish).toHaveBeenCalledTimes(1), { timeout: 2500 });
    act(() => hook.result.current.editing.handleSelectedClipChange({ hold: 4.001 }));
    const key = h.popup.getTimelineDraftRecoveryMetadata!().recoveryKey;
    await waitFor(async () => {
      const draft = await loadTimelineDraft(key);
      expect((draft?.draft.config as { clips: Array<{ hold: number }> })?.clips[0].hold).toBe(4);
      expect(hook.result.current.commit.dataRef.current?.config.clips[0].hold).toBe(4);
    }, { timeout: 2500 });
    await waitFor(() => expect(hook.result.current.persistence.saveStatus).toBe('error'), { timeout: 2500 });
    expect(h.publish).toHaveBeenCalledTimes(1);
    expect(refs.savedSeqRef.current).toBe(0);
    expect(refs.headRevisionRef.current).toEqual(h.initial.head);
    expect(h.graph).toEqual(h.composition.contract);
    const attemptedGraph = h.publish.mock.calls[0][0].graph;
    expect(attemptedGraph.occurrences.slice(1)).toEqual(h.graph.occurrences.slice(1));
    expect(attemptedGraph.parent_composition).toEqual(h.graph.parent_composition);
    expect(hook.result.current.commit.dataRef.current?.config.clips[0].app).toMatchObject({ opaque: [null, { keep: true }] });
    captures.boundary = { persistedDraft: await loadTimelineDraft(key), publicationAttempts: h.publish.mock.calls, savedSequence: refs.savedSeqRef.current, head: refs.headRevisionRef.current, imported: false, attemptedHold: 4.001, actualHookHold: hook.result.current.commit.dataRef.current?.config.clips[0].hold, overBoundaryGuardExercised: false };
    if (process.env.POPUP_224_EVIDENCE) writeFileSync(process.env.POPUP_224_EVIDENCE, JSON.stringify(captures, null, 2));
    hook.unmount(); query.clear();
  });
});
