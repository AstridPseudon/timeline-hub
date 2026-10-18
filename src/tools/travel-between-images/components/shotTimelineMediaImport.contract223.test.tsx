// @vitest-environment jsdom
// Contract diagnosis only: these tests characterize why an import-only bridge
// cannot safely complete the shared-child popup journey. No accepted edit claim.
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
function setup() {
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
    if (method === 'POST' && path.endsWith('/media-imports')) return ok({ data: { provider: 'runtime', project: 'project-001', import_operation_id: headers['Idempotency-Key'], status: 'completed', generation_id: selection.generation_id, variant_id: selection.variant_id, asset_id: selection.asset, entry: { object_id: selection.object_id, media_type: 'image/png', filename: '223.png', size: 3 } }, receipt: { receipt_id: 'fixture-223', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] } }, 201);
    if (path.includes('/media-selection?')) return ok(selection);
    throw new Error(`Unexpected fixture call ${method} ${path}`);
  };
  const runtime = new RuntimeDataProvider({ projectId: 'project-001', baseUrl: 'http://fixture.invalid', token: 'fixture-only', transport, commitRouting: { enabled: true } });
  const publish = vi.fn(async (_request: ShotCompositionPublishRequest) => { throw new StaleWriteError('fixture publication refusal'); });
  const adapter = createShotCompositionAdapter({ load: async () => graph, publish, semanticCommandSaving: true, saveTimelineAtHead: runtime.saveTimelineAtHead.bind(runtime) });
  const composition = adapter.prepare(graph);
  const config = projectCanonicalComposition({ ...composition, occurrences: [composition.occurrences[0]] }, { output: { resolution: '1920x1080', fps: 30, file: 'fixture.mp4' }, clips: [], tracks: [], registry: {} }, { clampToOccurrenceDuration: false }).config;
  const popup = createShotTimelineDataProvider(config, composition, 'occ-1', adapter);
  const initial = createShotTimelineInitialData(config, 1, composition);
  return { runtime, popup, graph, composition, initial, calls, publish };
}
function runtimeValue(provider: VideoEditorRuntimeContextValue['provider']) {
  return { provider, assetResolver: { resolveAssetUrl: provider.resolveAssetUrl }, auth: {}, project: {}, shots: {}, mediaLightbox: {}, agentChat: {}, toast: { error: vi.fn(), warning: vi.fn(), info: vi.fn(), success: vi.fn() }, telemetry: {}, timelineId: 'popup-223', userId: null, extensions: {} } as unknown as VideoEditorRuntimeContextValue;
}
function assets(h: ReturnType<typeof setup>, provider = h.popup) {
  const applyEdit = vi.fn();
  const hook = renderHook(() => useAssetManagement({ dataRef: { current: h.initial }, selectedTrackId: 'video', selectedProjectId: 'project-001', selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit, patchRegistry: vi.fn(), invalidateAssetRegistry: vi.fn(), resolveAssetUrl: provider.resolveAssetUrl }), { wrapper: ({ children }) => <VideoEditorRuntimeProvider value={runtimeValue(provider)}>{children}</VideoEditorRuntimeProvider> });
  return { ...hook, applyEdit };
}
beforeEach(() => { vi.stubGlobal('indexedDB', createFakeIndexedDB()); });
afterEach(() => { resetFakeIndexedDB(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

describe('popup media-import contract 223 (source diagnosis)', () => {
  it('cannot reach the existing Runtime importer from the actual popup hook provider', async () => {
    const h = setup();
    expect(h.runtime.prepareMediaImport).toBeTypeOf('function');
    expect(h.runtime.getProjectMediaSelection).toBeTypeOf('function');
    expect(h.popup.prepareMediaImport).toBeUndefined();
    expect(h.popup.getProjectMediaSelection).toBeUndefined();
    const hook = assets(h);
    await expect(hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }))).rejects.toThrow('legacy-import-refused-by-fixture');
    expect(h.calls).toEqual([]);
    captures.actualPopup = { importerAvailable: false, selectionAvailable: false, runtimeCalls: h.calls };
    hook.unmount();
  });

  it('shows that forwarding only the public importer/selector still emits parent placement intent', async () => {
    const h = setup();
    // Diagnostic counterfactual only, not production wiring or a registry shim.
    const bridge = { ...h.popup, supportsDirectAssetUpload: true, prepareMediaImport: h.runtime.prepareMediaImport.bind(h.runtime), getProjectMediaSelection: h.runtime.getProjectMediaSelection.bind(h.runtime) };
    const hook = assets(h, bridge);
    const uploaded = await hook.result.current.uploadImageGeneration(new File(['223'], '223.png', { type: 'image/png' }));
    const prepared = hook.result.current.prepareGenerationAsset(uploaded)!;
    expect(prepared.selectedMedia).toEqual(selection);
    expect(prepared.entry.media_id).toBe(selection.object_id);
    expect(hook.result.current.handleAssetDrop(prepared.assetKey, 'video', 0, false, false, prepared)).toBe(true);
    const command = hook.applyEdit.mock.calls[0][1]!.editCommands![0];
    expect(command).toMatchObject({ op: 'timeline.add', select: 'parent/track:video', args: { media: selection }, created: [expect.stringMatching(/^parent\/clip:/)] });
    expect(h.calls.filter(row => row.path.endsWith('/media-imports'))).toHaveLength(1);
    expect(h.calls.filter(row => row.path.includes('/media-selection?'))).toHaveLength(1);
    expect(h.calls.some(row => row.path.endsWith('/commit'))).toBe(false);
    captures.forwardOnly = { import: uploaded.mediaImport, command, calls: h.calls };
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
    if (process.env.POPUP_223_EVIDENCE) writeFileSync(process.env.POPUP_223_EVIDENCE, JSON.stringify(captures, null, 2));
    hook.unmount(); query.clear();
  });
});
