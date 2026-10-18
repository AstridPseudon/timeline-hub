// @vitest-environment jsdom
// Mounted App hooks + real SDK public loader/compiler, closed transport/evaluator.
import React, { useEffect } from 'react';
import { act, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
vi.mock('@/shared/media/clientThumbnailGenerator.ts', () => ({ generateClientThumbnail: vi.fn(async () => { throw Error('legacy upload'); }), uploadImageWithThumbnail: vi.fn() }));
vi.mock('@/shared/lib/media/imageUploader.ts', () => ({ uploadImageToStorage: vi.fn(async () => { throw Error('legacy upload'); }), uploadBlobToStorage: vi.fn() }));
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import { VideoEditorRuntimeProvider } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useAssetManagement } from '@/tools/video-editor/hooks/useAssetManagement.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { useTimelinePersistence } from '@/tools/video-editor/hooks/useTimelinePersistence.ts';
import { createTimelineCommands } from '@/tools/video-editor/hooks/useTimelineCommandsService.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';
import { loadTimelineDraft } from '@/tools/video-editor/data/timelineDraftIndexedDb.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { createShotTimelineDataProvider, createShotTimelineInitialData } from './shotTimelineDataProvider.ts';
const sdk = process.env.POPUP_MEDIA_226_SDK_ROOT!;
const evidence = process.env.POPUP_MEDIA_226_EVIDENCE!;
const python = process.env.POPUP_MEDIA_226_PYTHON ?? 'python3.11';
if (!sdk || !evidence) throw Error('Set the qualified SDK source and run-owned evidence paths for this coupled selector');
const json = (x: unknown) => new TextEncoder().encode(JSON.stringify(x));
function wire(file: string, action: string, body?: unknown) {
  const proc = spawnSync(python, ['-B', 'tests/sdk/popup_media_wire226.py', file, action], { cwd: sdk, env: { ...process.env, PYTHONPATH: '.:tests/sdk', PYTHONDONTWRITEBYTECODE: '1' }, input: body ? JSON.stringify(body) : undefined, encoding: 'utf8', timeout: 120000, maxBuffer: 8 * 1024 * 1024 });
  if (proc.status !== 0) throw Error(`Closed SDK wire failed: ${proc.stderr} ${proc.stdout}`);
  return JSON.parse(proc.stdout);
}
async function setup(label: string, occurrenceId = 'occ-copy') {
  mkdirSync(evidence, { recursive: true });
  const statefile = `${evidence}/app-${label}-wire.json`;
  let state = wire(statefile, 'init');
  const calls: Array<{ method: string; path: string; body?: unknown }> = [];
  const transport: Transport = async (method, path, headers, bytes) => {
    const body = bytes && path.endsWith('/commit') ? JSON.parse(typeof bytes === 'string' ? bytes : new TextDecoder().decode(bytes as Uint8Array)) : undefined;
    calls.push({ method, path, body });
    const ok = (value: unknown, status = 200) => ({ status, headers: {}, body: json(value) });
    if (path === '/v1/health') return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1 });
    if (path === '/v1/handshake') return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'closed-226', actor_id: 'reigh-product-connector', realm_id: 'closed-226', scopes: RUNTIME_CLIENT_SCOPES, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] });
    if (path === '/v1/realm') return ok({ realm_id: 'closed-226' });
    if (method === 'POST' && path.endsWith('/inspect')) return ok({ project_id: 'p', timeline_id: 't', representation: 'canonical_head', authority: 'runtime_parent_composition', is_current_head: true, head_revision_id: state.current, revision_id: state.current });
    if (method === 'POST' && path.endsWith('/media-imports')) return ok({ data: { provider: 'runtime', project: 'p', import_operation_id: headers['Idempotency-Key'], status: 'completed', generation_id: state.media.generation_id, variant_id: state.media.variant_id, asset_id: state.media.asset, entry: { object_id: state.media.object_id, media_type: 'image/png', filename: '226.png', size: 3 } }, receipt: { receipt_id: 'closed-226', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] } }, 201);
    if (method === 'GET' && path.includes('/media-imports/')) return ok({ error: { code: 'not_found' } }, 404);
    if (path.includes('/media-selection?')) return ok(state.media);
    if (method === 'POST' && path.endsWith('/commit')) { state = wire(statefile, 'commit', body); return ok(state.result); }
    const rid = decodeURIComponent(path.split('/').at(-1)!);
    for (const closure of Object.values(state.closures) as any[]) {
      if (path.includes('/composition-revisions/') && closure.parent_revision.revision_id === rid) return ok(closure.parent_revision);
      if (path.includes('/shots/')) { const row = closure.shot_revisions.find((r: any) => r.revision_id === rid); if (row) return ok(row); }
      const row = closure.internal_timeline_revisions.find((r: any) => r.revision_id === rid); if (row) return ok(row);
    }
    throw Error(`Unexpected closed wire ${method} ${path}`);
  };
  const session = new Map<string, string>();
  const runtime = new RuntimeDataProvider({ commitSessionStorage: { getItem: key => session.get(key) ?? null, setItem: (key, value) => { session.set(key, value); } }, projectId: 'p', baseUrl: 'http://fixture.invalid', token: 'closed-fixture-only', transport, commitRouting: { enabled: true } });
  const adapter = createShotCompositionAdapter(runtime.shotComposition);
  const composition = adapter.prepare(await runtime.shotComposition.load({ projectId: 'p', parentDocumentId: 't' }));
  const config = projectCanonicalComposition({ ...composition, occurrences: composition.occurrences.filter(row => row.occurrenceId === occurrenceId) }, { output: { resolution: '1920x1080', fps: 30, file: 'fixture.mp4' }, clips: [], tracks: [], registry: {} }, { clampToOccurrenceDuration: false }).config;
  // Same parent-to-popup local conversion as ShotTimelinePreview.
  const offset = composition.occurrences.find(row => row.occurrenceId === occurrenceId)!.atMs / 1000;
  config.clips = config.clips.map(clip => ({ ...clip, at: Math.max(0, clip.at - offset), app: { ...clip.app, canonicalTiming: { ...(clip.app?.canonicalTiming as object), occurrenceStartMs: 0 } } }));
  const editorHeadState = { current: { canonicalHeadRevisionId: 'rev-0', displayedHeadRevisionId: 'rev-0' } };
  const popup = createShotTimelineDataProvider(config, composition, occurrenceId, adapter, undefined, editorHeadState);
  const save = popup.saveTimelineAtHead!;
  popup.saveTimelineAtHead = async (...args) => { try { return await save(...args); } catch (error) { writeFileSync(`${evidence}/app-${label}-error.txt`, String(error) + '\n' + (error as Error).stack); throw error; } };
  const initial = createShotTimelineInitialData(config, 1, composition);
  const eventBus = new TimelineEventBus();
  const query = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
  const savedSeqRef = { current: 0 };
  const refs = { savedSeqRef, configVersionRef: { current: 1 }, headRevisionRef: { current: initial.head }, lastSavedSignatureRef: { current: initial.stableSignature }, interactionStateRef: { current: createInteractionState() } };
  const value = { provider: popup, assetResolver: { resolveAssetUrl: popup.resolveAssetUrl }, auth: {}, project: {}, shots: {}, mediaLightbox: {}, agentChat: {}, toast: { error: vi.fn(), warning: vi.fn(), info: vi.fn(), success: vi.fn() }, telemetry: {}, timelineId: 'popup-226', userId: null, extensions: {} } as any;
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, initialData: initial, lastSavedSignatureRef: refs.lastSavedSignatureRef });
    const persistence = useTimelinePersistence({ ...commit, ...refs, provider: popup, timelineId: 'popup-226', eventBus });
    useEffect(() => eventBus.on('scheduleSave', persistence.scheduleSave), [persistence.scheduleSave]);
    const assets = useAssetManagement({ dataRef: commit.dataRef, selectedTrackId: 'type', selectedProjectId: 'p', selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit: commit.applyEdit, patchRegistry: vi.fn(() => { throw Error('direct registry mutation'); }), invalidateAssetRegistry: vi.fn(), resolveAssetUrl: popup.resolveAssetUrl });
    const commands = createTimelineCommands({ getState: () => ({ data: { data: commit.data, dataRef: commit.dataRef }, ops: { applyEdit: commit.applyEdit }, availability: { mounted: true } }) } as any, { semanticCommandSaving: true, getTimelineOccurrenceMediaContext: popup.getTimelineOccurrenceMediaContext });
    return { commit, persistence, assets, commands };
  }, { wrapper: ({ children }) => <QueryClientProvider client={query}><VideoEditorRuntimeProvider value={value}>{children}</VideoEditorRuntimeProvider></QueryClientProvider> });
  return { ...hook, headRevisionRef: refs.headRevisionRef, savedSeqRef, calls, popup, initial, statefile, editorHeadState };
}
beforeEach(() => { vi.stubGlobal('indexedDB', createFakeIndexedDB()); });
afterEach(() => { resetFakeIndexedDB(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });
it.each(['add', 'swap'])('mounted popup %s traverses import/selection/scheduleSave/public SDK/exact readback', async kind => {
  const h = await setup(kind);
  const uploaded = await h.result.current.assets.uploadImageGeneration(new File(['226'], '226.png', { type: 'image/png' }));
  const prepared = h.result.current.assets.prepareGenerationAsset(uploaded)!;
  writeFileSync(`${evidence}/app-${kind}-prepared.json`, JSON.stringify({ prepared, initial: h.initial, context: h.popup.getTimelineOccurrenceMediaContext!() }, null, 2));
  expect(prepared.selectedMedia?.object_id).toBe(`sha256:${'a'.repeat(64)}`);
  expect(Object.keys(prepared.selectedMedia!).sort()).toEqual(['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'].sort());
  expect(h.result.current.assets.registerGenerationAsset(uploaded)).toBeNull();
  expect(h.result.current.assets.handleAssetDrop(prepared.assetKey, 'type', 0)).toBe(false);
  act(() => {
    if (kind === 'add') expect(h.result.current.assets.handleAssetDrop(prepared.assetKey, 'type', 0, false, false, prepared)).toBe(true);
    else expect(h.result.current.commands.addClip({ preparedAsset: prepared, replaceClipId: 'occ-copy:a-rocket' })).toMatchObject({ ok: true });
  });
  expect(h.result.current.commit.editSeqRef.current).toBe(1);
  await waitFor(() => expect(h.savedSeqRef.current === 1 || h.result.current.persistence.saveStatus === 'error').toBe(true), { timeout: 90000 });
  expect({ saved: h.savedSeqRef.current, status: h.result.current.persistence.saveStatus }).toEqual({ saved: 1, status: 'saved' });
  const state = JSON.parse(readFileSync(h.statefile, 'utf8'));
  expect(state.result.status).toBe('accepted');
  const body = state.requests[0];
  expect(body.scope).toMatchObject({ target: 'occurrence:occ-copy', content: 'this-occurrence' });
  expect(body.change.commands).toHaveLength(1);
  const command = body.change.commands[0];
  expect(command.op).toBe(kind === 'add' ? 'timeline.add' : 'clip.swap-asset');
  expect(command.select.startsWith('occurrence:occ-copy/')).toBe(true);
  expect(command.args.media).toEqual(state.media);
  if (kind === 'add') expect(command.args.at).toBe(8);
  expect(h.calls.filter(row => row.method === 'POST' && row.path.endsWith('/media-imports'))).toHaveLength(1);
  expect(h.calls.filter(row => row.path.includes('/media-selection?'))).toHaveLength(1);
  expect(h.calls.filter(row => row.method === 'POST' && row.path.endsWith('/commit'))).toHaveLength(1);
  expect(h.calls.some(row => row.method === 'POST' && row.path.includes('composition-revisions'))).toBe(false);
  expect(h.headRevisionRef.current?.headRevisionId).toBe('accepted-fixture');
  const next = await h.popup.loadTimeline('popup-226');
  const changed = kind === 'swap' ? next.config.clips.find(row => row.id === 'occ-copy:a-rocket') : next.config.clips.find(row => !h.initial.config.clips.some(old => old.id === row.id));
  expect(changed?.asset).toBe(state.media.asset);
  expect(() => h.popup.getTimelineOccurrenceMediaContext!()).toThrow('still adopting');
  h.unmount();
}, 180000);

it('persists a beyond-boundary frame command for recovery and refuses before any commit', async () => {
  const h = await setup('boundary', 'occ-A');
  const uploaded = await h.result.current.assets.uploadImageGeneration(new File(['226'], '226.png', { type: 'image/png' }));
  const prepared = h.result.current.assets.prepareGenerationAsset(uploaded)!;
  act(() => expect(h.result.current.commands.addClip({ preparedAsset: prepared, trackId: 'type', time: 0, clipSpanSeconds: 121 / 30 })).toMatchObject({ ok: true }));
  expect(h.result.current.commit.editSeqRef.current).toBe(1);
  await waitFor(() => expect(h.result.current.persistence.saveStatus).toBe('error'), { timeout: 10000 });
  expect(h.savedSeqRef.current).toBe(0);
  expect(h.calls.some(row => row.method === 'POST' && row.path.endsWith('/commit'))).toBe(false);
  const key = h.popup.getTimelineDraftRecoveryMetadata!().recoveryKey!;
  const draft = await loadTimelineDraft(key);
  expect((draft?.draft.editCommands as any[])?.[0]?.args.duration).toBeCloseTo(121 / 30, 5);
  expect(h.result.current.commit.dataRef.current?.config.clips).toEqual(h.initial.config.clips);
  h.unmount();
}, 30000);
