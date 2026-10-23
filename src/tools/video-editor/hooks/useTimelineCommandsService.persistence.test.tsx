// @vitest-environment jsdom
import React, { useLayoutEffect, useMemo } from 'react';
import { act, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import type { CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import type { DataProvider, TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';
import { createInteractionState } from '../lib/interaction-state.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { applyPreparedMediaCommand, type PlacePreparedMediaCommand } from '../commands/media.ts';
import { createCommitOutbox } from '../commands/commitOutbox.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { TimelineStoreProvider, createTimelineStore } from './timelineStore.ts';
import { useTimelineCommandsService } from './useTimelineCommandsService.ts';
import { useTimelineSave } from './useTimelineSave.ts';

vi.stubGlobal('indexedDB', createFakeIndexedDB());
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
vi.mock('@/integrations/runtime/generated-contract-metadata.ts', async (importOriginal) => ({
  ...await importOriginal<typeof import('@/integrations/runtime/generated-contract-metadata.ts')>(),
  SCHEMA_DIGEST: 'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
}));

const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-1' };
const head = { revisionId: 'r0', publicationId: 'p0' };
const runtimeHead = { projectId: scope.projectId, timelineId: scope.timelineId,
  headRevisionId: head.revisionId, headPublicationId: head.publicationId };

const locksDescriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
beforeEach(() => {
  Object.defineProperty(navigator, 'locks', { configurable: true, value: {
    request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
  } });
});
afterEach(() => {
  vi.restoreAllMocks();
  if (locksDescriptor) Object.defineProperty(navigator, 'locks', locksDescriptor);
  else Reflect.deleteProperty(navigator, 'locks');
});

function authoredConfig(): TimelineConfig {
  return {
    ...createDefaultTimelineConfig(),
    tracks: [
      { id: 'V1', kind: 'visual', label: 'V1' },
      { id: 'V2', kind: 'visual', label: 'V2' },
    ],
    clips: [
      {
        id: 'anchor', at: 1, track: 'V1', clipType: 'media', asset: 'asset-source',
        from: 2, to: 6, speed: 2, opacity: 0.5,
        effects: { glow: 1 },
        transition: { type: 'crossfade', duration: 0.5, params: { opaque: [null, false] } },
        params: { opaque: { ordered: [null, false, 0] } },
        app: { opaque: { keep: null, ordered: [false, 0, ''] } },
      },
      { id: 'later', at: 5, track: 'V1', clipType: 'hold', hold: 1, asset: 'asset-peer' },
      { id: 'sibling', at: 5, track: 'V2', clipType: 'hold', hold: 1, asset: 'asset-peer' },
    ],
  };
}

function authoredDocument(config: TimelineConfig) {
  const payload = {
    config: structuredClone(config),
    clips: structuredClone(config.clips),
    registry: {
      assets: {
        'asset-source': { file: 'source.mp4', type: 'video/mp4', media_id: 'media-source' },
        'asset-peer': { file: 'peer.png', type: 'image/png' },
      },
    },
    occurrences: [],
    opaque: { keep: null },
  };
  const document = acceptedCommit({ revision_id: head.revisionId, publication_id: head.publicationId },
    { revision_id: head.revisionId, publication_id: head.publicationId }, { projectId: scope.projectId, timelineId: scope.timelineId })
    .data.canonical_document;
  document.parent_revision.payload = payload;
  document.parent_revision.content_digest = fixtureDigest(payload);
  return document;
}

function adoptedDocument(document: ReturnType<typeof authoredDocument>, data: Awaited<ReturnType<typeof buildTimelineData>>, revision: string) {
  const next = structuredClone(document);
  const payload = next.parent_revision.payload as Record<string, unknown>;
  payload.config = structuredClone(data.config);
  payload.clips = structuredClone(data.config.clips);
  payload.registry = structuredClone(data.registry);
  next.parent_revision.revision_id = revision;
  next.parent_revision.content_digest = fixtureDigest(payload);
  return next;
}

function acceptedReply(request: CommitRequest, document: ReturnType<typeof authoredDocument>, revision: string, key: string): TimelineCommitResult {
  const response = acceptedCommit({ revision_id: revision, publication_id: `p-${revision}` },
    { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, {
      projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands,
    });
  response.data.canonical_document = document;
  response.data.document_digest = fixtureDigest(document);
  Object.assign(response.data, {
    status: 'accepted',
    merge_mode: request.merge,
    steps: request.steps,
    label: request.label,
    source: request.source,
  });
  response.receipt.idempotency_key = key;
  response.receipt.result = response.data;
  return {
    response,
    accepted: { revisionId: revision, publicationId: `p-${revision}` },
    canonicalDocument: document,
    graph: {},
    receipt: response.receipt,
  };
}

function json(value: unknown): Uint8Array {
  return new TextEncoder().encode(JSON.stringify(value));
}

function runtimeDiscoveryTransport(
  transportCalls: Array<{ method: string; path: string; headers: Record<string, string>; rawBody?: string; body?: unknown }>,
  commit: (request: CommitRequest, key: string, path: string) => { status: number; headers: Record<string, string>; body: Uint8Array },
): Transport {
  return async (method, path, headers, body) => {
    const rawBody = body ? new TextDecoder().decode(body as Uint8Array) : undefined;
    transportCalls.push({ method, path, headers, ...(rawBody === undefined ? {} : { rawBody, body: JSON.parse(rawBody) }) });
    if (path === '/v1/health') {
      return { status: 200, headers: {}, body: json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        runtime_epoch: 1, runtime_session_id: 'session-commit', runtime_instance_id: 'instance-commit' }) };
    }
    if (path === '/v1/handshake') {
      return { status: 200, headers: {}, body: json({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        session_id: 'session-commit', actor_id: scope.actorId, realm_id: scope.realmId,
        scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'],
        capabilities: ['execution_binding.targeted.v1'] }) };
    }
    if (path === '/v1/realm') {
      return { status: 200, headers: {}, body: json({ realm_id: scope.realmId, display_name: 'commit fixture', version: 1,
        created_at: '2026-10-23T00:00:00Z' }) };
    }
    if (method === 'POST' && path === `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`) {
      return commit(JSON.parse(rawBody!) as CommitRequest, headers['Idempotency-Key']!, path);
    }
    throw new Error(`Unexpected Runtime request: ${method} ${path}`);
  };
}

function useMountedCommands(
  store: ReturnType<typeof createTimelineStore>,
  provider: DataProvider,
  initialData: Awaited<ReturnType<typeof buildTimelineData>>,
) {
  const interactionStateRef = useMemo(() => ({ current: createInteractionState() }), []);
  const save = useTimelineSave(
    { timelineQuery: { data: undefined, isLoading: false }, assetRegistryQuery: { data: undefined } },
    provider,
    interactionStateRef,
    store,
    initialData,
  );
  const data = useMemo(() => ({ ...store.getState().data, data: save.data, dataRef: save.dataRef,
    selectedClipId: save.selectedClipId, selectedTrackId: save.selectedTrackId }),
  [save.data, save.dataRef, save.selectedClipId, save.selectedTrackId, store]);
  const ops = useMemo(() => ({ ...store.getState().ops, applyEdit: save.applyEdit,
    patchRegistry: save.patchRegistry, unpatchRegistry: save.unpatchRegistry }),
  [save.applyEdit, save.patchRegistry, save.unpatchRegistry, store]);
  useLayoutEffect(() => { store.getState().syncSlices({ data, ops }); }, [data, ops, store]);
  return { save, commands: useTimelineCommandsService() };
}

function wrapperFor(store: ReturnType<typeof createTimelineStore>, provider: DataProvider) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider, timelineId: scope.timelineId, shots: { canonicalDraft: null },
    assetResolver: { resolveAssetUrl: async (file: string) => file } } as unknown as VideoEditorRuntimeContextValue;
  return ({ children }: { children: React.ReactNode }) => <QueryClientProvider client={queryClient}>
    <VideoEditorRuntimeProvider value={runtime}>
      <TimelineStoreProvider store={store}>{children}</TimelineStoreProvider>
    </VideoEditorRuntimeProvider>
  </QueryClientProvider>;
}

describe('mounted prepared-media command persistence', () => {
  it('adopts an after-anchor prepared duplicate through the real v2 outbox request', async () => {
    const config = authoredConfig();
    const document = authoredDocument(config);
    const initial: TimelineCommandBasis = { head, canonicalDocument: document };
    const initialData = await buildTimelineData(config, document.parent_revision.payload.registry as unknown as AssetRegistry,
      async (file) => file, 1, undefined, runtimeHead);
    const preparedData = applyPreparedMediaCommand(initialData, {
      type: 'place-prepared-media',
      payload: {
        asset: { assetKey: 'asset-copy', mediaType: 'video', durationSeconds: 2,
          entry: { file: 'copy.mp4', type: 'video/mp4', media_id: 'media-copy', generationId: 'generation-copy' },
          source: 'registered' },
        selectedTrackId: null, at: 0, afterClipId: 'anchor', forceNewTrack: false, insertAtTop: false,
      },
    } satisfies PlacePreparedMediaCommand);
    expect(preparedData).not.toBeNull();
    let latest = initial;
    const transportCalls: Array<{ method: string; path: string; headers: Record<string, string>; rawBody?: string; body?: unknown }> = [];
    const transport = runtimeDiscoveryTransport(transportCalls, (request, key, path) => {
      const accepted = acceptedReply(request, adoptedDocument(document, preparedData!.nextData, 'r1'), 'r1', key);
      accepted.receipt.request_hash = fixtureDigest({ operation: 'commitTimeline', path,
        publisher: accepted.response.data.publisher, request }).slice(7);
      accepted.receipt.result = accepted.response.data;
      latest = { head: accepted.accepted, canonicalDocument: accepted.canonicalDocument };
      return { status: 200, headers: {}, body: json(accepted.response) };
    });
    const runtimeClient = new AstridRuntimeClient({ baseUrl: 'http://runtime.test', token: 'runtime-token', transport });
    const provider = new RuntimeDataProvider({ projectId: scope.projectId, runtimeClient });
    vi.spyOn(provider, 'loadTimelineCommandBasis').mockImplementation(async () => structuredClone(latest));
    const actualCommit = provider.commitTimeline.bind(provider);
    const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>().mockImplementation(
      (request, key) => actualCommit(request, key),
    );
    provider.commitTimeline = send;
    const store = createTimelineStore();
    const mounted = renderHook(() => useMountedCommands(store, provider, initialData), { wrapper: wrapperFor(store, provider) });
    try {
      await waitFor(() => expect(mounted.result.current.save.localSaveState).not.toBeNull());
      expect(mounted.result.current.save.localSaveState).toMatchObject({ status: 'saved', ownerId: expect.any(String) });
      let result: ReturnType<typeof mounted.result.current.commands.addClip>;
      act(() => {
        result = mounted.result.current.commands.addClip({
          preparedAsset: { assetKey: 'asset-copy', mediaType: 'video', durationSeconds: 2,
            entry: { file: 'copy.mp4', type: 'video/mp4', media_id: 'media-copy', generationId: 'generation-copy' },
            source: 'registered' },
          trackId: 'V1', afterClipId: 'anchor', time: 0,
        });
      });
      expect(result!).toEqual({ ok: true, data: { clipId: 'clip-0', trackId: 'V1' } });
      expect(mounted.result.current.save.dataRef.current?.config.clips).toEqual(preparedData!.nextData.config.clips);
      expect(mounted.result.current.save.dataRef.current?.config.clips.map((clip) => clip.id))
        .toEqual(['anchor', 'clip-0', 'later', 'sibling']);
      expect(mounted.result.current.save.dataRef.current?.config.clips.find((clip) => clip.id === 'clip-0'))
        .toMatchObject({ from: 2, to: 6, speed: 2, opacity: 0.5,
          transition: { type: 'crossfade', duration: 0.5, params: { opaque: [null, false] } },
          params: { opaque: { ordered: [null, false, 0] } }, app: { opaque: { keep: null, ordered: [false, 0, ''] } } });
      expect(mounted.result.current.save.dataRef.current?.config.clips.find((clip) => clip.id === 'clip-0'))
        .not.toHaveProperty('hold');
      await act(async () => { await mounted.result.current.save.flushPendingSave(); });
      expect(send).toHaveBeenCalledOnce();
      const [request, key] = send.mock.calls[0]!;
      expect(request).toMatchObject({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
        base_revision_id: 'r0', base_publication_id: 'p0', label: 'Edit timeline', merge: 'atomic', dry_run: false,
        source: { via: 'app' }, commands: [{ schema_version: 1, op: 'doc.patch', version: '1', select: null, created: ['parent/clip:clip-0'] }],
        steps: [{ id: expect.any(String), label: 'Edit timeline', intent: 'Save local editor changes', tags: [], command_ordinals: [0] }],
      });
      expect(request).not.toHaveProperty('reads');
      expect(request.commands[0]?.args.changes).toEqual(expect.arrayContaining([
        { op: 'list.insert', ref: 'parent', path: ['clips'], id: 'clip-0', before: { state: 'absent' },
          value: expect.objectContaining({ id: 'clip-0', at: 3, track: 'V1', asset: 'asset-copy', from: 2, to: 6, speed: 2,
            opacity: 0.5, effects: { glow: 1 }, transition: { type: 'crossfade', duration: 0.5, params: { opaque: [null, false] } },
            params: { opaque: { ordered: [null, false, 0] } }, app: { opaque: { keep: null, ordered: [false, 0, ''] } } }),
          order_before: ['anchor', 'later', 'sibling'], after_id: 'anchor' },
        { op: 'set', ref: 'parent', path: ['clips', 'id:later', 'at'], before: { state: 'present', value: 5 }, value: 7 },
      ]));
      expect(request.steps?.[0]?.patch).toEqual(request.commands[0]?.args.changes);
      expect(request.commands[0]?.args.changes).toEqual(expect.arrayContaining([
        { op: 'set', ref: 'parent', path: ['registry', 'assets', 'asset-copy'], before: { state: 'absent' },
          value: { file: 'copy.mp4', type: 'video/mp4', media_id: 'media-copy', generationId: 'generation-copy' } },
      ]));
      const commitCalls = transportCalls.filter((call) => call.path.endsWith('/commit'));
      expect(commitCalls).toHaveLength(1);
      const [wire] = commitCalls;
      expect(wire.method).toBe('POST');
      expect(wire.path).toBe(`/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`);
      expect(wire.headers).toMatchObject({
        Accept: 'application/json', Authorization: 'Bearer runtime-token', 'Content-Type': 'application/json',
        'Idempotency-Key': key,
      });
      expect(wire.rawBody).toBe(JSON.stringify(request));
      expect(wire.body).toEqual(request);
      const accepted = await send.mock.results[0]!.value as TimelineCommitResult;
      expect(accepted.response.data).toMatchObject({
        status: 'accepted', base_revision_id: 'r0', base_publication_id: 'p0',
        previous_revision_id: 'r0', previous_publication_id: 'p0', accepted_revision_id: 'r1', rebased_onto: null,
        document_digest: fixtureDigest(accepted.canonicalDocument), commands: request.commands,
        merge_mode: 'atomic', steps: request.steps, label: 'Edit timeline', source: { via: 'app' },
      });
      expect(accepted.response.data.canonical_document).toEqual(accepted.canonicalDocument);
      expect(accepted.response.data.canonical_document.parent_revision).toMatchObject({
        revision_id: 'r1', content_digest: fixtureDigest(accepted.canonicalDocument.parent_revision.payload),
      });
      expect(accepted.receipt).toMatchObject({
        receipt_id: 'p-r1', command_kind: 'timeline.commit', idempotency_key: key,
        project_id: scope.projectId, project_seq: [1, 1], event_ids: ['event-p-r1'],
        request_hash: fixtureDigest({ operation: 'commitTimeline', path: wire.path,
          publisher: accepted.response.data.publisher, request }).slice(7),
      });
      expect(accepted.receipt.result).toEqual(accepted.response.data);
      const [stored] = await createCommitOutbox().list(scope);
      expect(stored.intents).toEqual([]);
      expect(stored.accepted?.value).toMatchObject({ response: { data: { status: 'accepted', merge_mode: 'atomic' } } });
      expect(key).toBe(stored.accepted?.value && stored.accepted?.value !== null ? stored.accepted?.value.response?.receipt?.idempotency_key : undefined);
      expect(mounted.result.current.save.dataRef.current?.config.clips).toEqual(preparedData!.nextData.config.clips);
      expect(mounted.result.current.save.dataRef.current?.config.clips.find((clip) => clip.id === 'later')?.at).toBe(7);
      expect(mounted.result.current.save.dataRef.current?.config.clips.find((clip) => clip.id === 'sibling')?.at).toBe(5);
    } finally {
      mounted.unmount();
      await new Promise((resolve) => setTimeout(resolve, 0));
    }
  });

  it('rolls back an accepted preview when the mounted save receives a real conflict', async () => {
    const config = authoredConfig();
    const document = authoredDocument(config);
    const initial: TimelineCommandBasis = { head, canonicalDocument: document };
    const initialData = await buildTimelineData(config, document.parent_revision.payload.registry as unknown as AssetRegistry,
      async (file) => file, 1, undefined, runtimeHead);
    const latestConfig = structuredClone(config);
    latestConfig.clips = latestConfig.clips.map((clip) => clip.id === 'later' ? { ...clip, at: 6 } : clip);
    const latestDocument = adoptedDocument(document, {
      config: latestConfig,
      registry: document.parent_revision.payload.registry,
    } as Awaited<ReturnType<typeof buildTimelineData>>, 'agent-r');
    let latest = initial;
    const transportCalls: Array<{ method: string; path: string; headers: Record<string, string>; rawBody?: string; body?: unknown }> = [];
    const transport = runtimeDiscoveryTransport(transportCalls, (request) => {
      latest = { head: { revisionId: 'agent-r', publicationId: 'agent-p' }, canonicalDocument: latestDocument };
      return { status: 409, headers: {}, body: json({
        code: 'dependency_changed', message: 'The prepared after-anchor source changed', request_id: 'request-prepared',
        details: {
          status: 'conflict', reason: 'dependency_changed',
          base: { revision_id: request.base_revision_id, publication_id: request.base_publication_id },
          current: { revision_id: 'agent-r', publication_id: 'agent-p' }, conflicts: [],
          code: 'dependency_changed', path: ['parent', 'clips', 'id:anchor', 'at'],
          hint: 'Reload the timeline and retry the prepared placement.', suggested_command: 'show timeline',
        },
      }) };
    });
    const runtimeClient = new AstridRuntimeClient({ baseUrl: 'http://runtime.test', token: 'runtime-token', transport });
    const provider = new RuntimeDataProvider({ projectId: scope.projectId, runtimeClient });
    vi.spyOn(provider, 'loadTimelineCommandBasis').mockImplementation(async () => structuredClone(latest));
    const actualCommit = provider.commitTimeline.bind(provider);
    const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>().mockImplementation(
      (request, key) => actualCommit(request, key),
    );
    provider.commitTimeline = send;
    const store = createTimelineStore();
    const mounted = renderHook(() => useMountedCommands(store, provider, initialData), { wrapper: wrapperFor(store, provider) });
    try {
      await waitFor(() => expect(mounted.result.current.save.localSaveState).not.toBeNull());
      expect(mounted.result.current.save.localSaveState).toMatchObject({ status: 'saved', ownerId: expect.any(String) });
      act(() => mounted.result.current.commands.addClip({
        preparedAsset: { assetKey: 'asset-copy', mediaType: 'video', durationSeconds: 2,
          entry: { file: 'copy.mp4', type: 'video/mp4', media_id: 'media-copy', generationId: 'generation-copy' },
          source: 'registered' },
        trackId: 'V1', afterClipId: 'anchor', time: 0,
      }));
      expect(mounted.result.current.save.dataRef.current?.config.clips.some((clip) => clip.id === 'clip-0')).toBe(true);
      await waitFor(() => expect(mounted.result.current.save.localSaveState?.status).toBe('dirty'));
      const ownerId = mounted.result.current.save.localSaveState!.ownerId!;
      await waitFor(async () => expect((await createCommitOutbox().list(scope)).find((record) => record.ownerId === ownerId)?.intents).toHaveLength(1));
      latest = { head: { revisionId: 'agent-r', publicationId: 'agent-p' }, canonicalDocument: latestDocument };
      await act(async () => { await expect(mounted.result.current.save.flushPendingSave()).rejects.toThrow('draft retained'); });
      await waitFor(() => expect(mounted.result.current.save.localSaveState?.status).toBe('conflict'));
      expect(mounted.result.current.save.dataRef.current?.config.clips.some((clip) => clip.id === 'clip-0')).toBe(false);
      expect(mounted.result.current.save.dataRef.current?.config.clips.find((clip) => clip.id === 'later')?.at).toBe(6);
      expect(send).toHaveBeenCalledOnce();
      const refusal = await send.mock.results[0]!.value.catch((error: unknown) => error);
      expect(refusal).toMatchObject({ status: 409, code: 'dependency_changed', details: {
        status: 'conflict', reason: 'dependency_changed',
        base: { revision_id: 'r0', publication_id: 'p0' }, current: { revision_id: 'agent-r', publication_id: 'agent-p' },
        conflicts: [], code: 'dependency_changed', path: ['parent', 'clips', 'id:anchor', 'at'],
        hint: 'Reload the timeline and retry the prepared placement.', suggested_command: 'show timeline',
      } });
      expect(refusal.details).not.toHaveProperty('head');
      const commitCalls = transportCalls.filter((call) => call.path.endsWith('/commit'));
      expect(commitCalls).toHaveLength(1);
      const [wire] = commitCalls;
      expect(wire).toMatchObject({ method: 'POST', path: `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`,
        headers: { Accept: 'application/json', Authorization: 'Bearer runtime-token', 'Content-Type': 'application/json',
          'Idempotency-Key': expect.any(String) } });
      expect(wire.body).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0', merge: 'atomic' });
      expect((await createCommitOutbox().list(scope)).find((record) => record.ownerId === ownerId)?.pending?.outcome).toMatchObject({
        kind: 'rejected', error: { kind: 'conflict', code: 'dependency_changed',
          message: 'dependency_changed: The prepared after-anchor source changed', details: {
            status: 'conflict', reason: 'dependency_changed', current: { revision_id: 'agent-r', publication_id: 'agent-p' },
          } },
      });
    } finally {
      mounted.unmount();
      await new Promise((resolve) => setTimeout(resolve, 0));
    }
  });
});
