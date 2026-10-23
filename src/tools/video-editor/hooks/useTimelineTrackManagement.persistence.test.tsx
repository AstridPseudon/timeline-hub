// @vitest-environment jsdom
import React from 'react';
import { act, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { ApiError } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { DataProvider, TimelineCommandBasis, TimelineCommitResult, TimelineHeadRevision } from '@/tools/video-editor/data/DataProvider.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useTimelineSave } from '@/tools/video-editor/hooks/useTimelineSave.ts';
import { useTimelineTrackManagement } from '@/tools/video-editor/hooks/useTimelineTrackManagement.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';

vi.mock('@/integrations/runtime/generated-contract-metadata.ts', async (importOriginal) => ({
  ...await importOriginal<typeof import('@/integrations/runtime/generated-contract-metadata.ts')>(),
  SCHEMA_DIGEST: 'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
}));
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({
  invalidateReferencedTimelineCache: vi.fn(),
}));
vi.mock('@/tools/video-editor/hooks/usePollSync.ts', () => ({ usePollSync: vi.fn() }));

const scope = { realmId: 'realm-track', actorId: 'actor-track', projectId: 'project-track', timelineId: 'timeline-track' };
const initialHead: TimelineHeadRevision = {
  projectId: scope.projectId,
  timelineId: scope.timelineId,
  headRevisionId: 'r0',
  headPublicationId: 'p0',
};

const trackOrder = ['picture', 'audio', 'overlay'];
const reorderedTrackOrder = ['overlay', 'picture', 'audio'];

function authoredConfig(): TimelineConfig {
  return {
    output: { resolution: '1280x720', fps: 30, file: 'tracks.mp4', background: null, background_scale: null },
    tracks: [
      { id: 'picture', kind: 'visual', label: 'Picture', scaleAppliesToPositionedClips: true, app: { lane: 'main', opaque: { keep: null }, scaleAppliesToPositionedClips: true } },
      { id: 'audio', kind: 'audio', label: 'Audio', scaleAppliesToPositionedClips: true, app: { nullValue: null, falseValue: false, zeroValue: 0, scaleAppliesToPositionedClips: true } },
      { id: 'overlay', kind: 'visual', label: 'Overlay', scaleAppliesToPositionedClips: true, app: { opaque: [null, false, 0], scaleAppliesToPositionedClips: true } },
    ],
    clips: [{
      id: 'clip-picture', track: 'picture', clipType: 'hold', at: 0, hold: 2,
      app: { opaque: { keep: null, false: false, zero: 0 } },
    }],
    app: { timelineDataLanePlacement: { 'data-1': 'between' }, opaque: { keep: null, sibling: [false, 0] } },
  };
}

function makeCanonicalDocument(config: TimelineConfig, revisionId = 'r0'): CanonicalDocument {
  const parentPayload = {
    config: structuredClone(config),
    clips: structuredClone(config.clips),
    registry: { assets: {} },
    occurrences: [],
    opaque_parent: { keep: null, sibling: [false, 0] },
  };
  const response = acceptedCommit(
    { revision_id: revisionId, publication_id: revisionId === 'r0' ? 'p0' : 'p1' },
    { revision_id: 'r0', publication_id: 'p0' },
    { projectId: scope.projectId, timelineId: scope.timelineId },
  );
  const document = structuredClone(response.data.canonical_document) as CanonicalDocument;
  document.project_id = scope.projectId;
  document.timeline_id = scope.timelineId;
  document.parent_revision.revision_id = revisionId;
  document.parent_revision.payload = parentPayload;
  document.parent_revision.content_digest = fixtureDigest(parentPayload);
  return document;
}

function makeBasis(config: TimelineConfig): TimelineCommandBasis {
  return { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: makeCanonicalDocument(config) };
}

function acceptedResult(request: CommitRequest, before: TimelineCommandBasis): TimelineCommitResult {
  const nextConfig = structuredClone(before.canonicalDocument.parent_revision.payload.config) as TimelineConfig;
  nextConfig.tracks = reorderedTrackOrder.map((id) => nextConfig.tracks!.find((track) => track.id === id)!);
  const canonicalDocument = structuredClone(before.canonicalDocument);
  canonicalDocument.parent_revision.revision_id = 'r1';
  canonicalDocument.parent_revision.payload.config = nextConfig as unknown as Record<string, unknown>;
  canonicalDocument.parent_revision.payload.clips = structuredClone(nextConfig.clips);
  canonicalDocument.parent_revision.content_digest = fixtureDigest(canonicalDocument.parent_revision.payload);
  const response = acceptedCommit(
    { revision_id: 'r1', publication_id: 'p1' },
    { revision_id: 'r0', publication_id: 'p0' },
    { projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands },
  );
  response.data.canonical_document = canonicalDocument;
  response.data.document_digest = fixtureDigest(canonicalDocument);
  response.data.label = request.label;
  response.data.steps = request.steps;
  response.data.merge_mode = request.merge;
  response.data.source = request.source;
  response.receipt.idempotency_key = 'mounted-track-key';
  response.receipt.result = response.data;
  return {
    response,
    accepted: { revisionId: 'r1', publicationId: 'p1' },
    canonicalDocument,
    graph: {},
    receipt: response.receipt,
  };
}

type MountedHarness = {
  hook: ReturnType<typeof renderHook<{
    save: ReturnType<typeof useTimelineSave>;
    tracks: ReturnType<typeof useTimelineTrackManagement>;
  }, unknown>>;
  provider: DataProvider;
  send: ReturnType<typeof vi.fn<NonNullable<DataProvider['commitTimeline']>>>;
  basis: TimelineCommandBasis;
  data: TimelineData;
};

async function mountHarness(outcome: 'accepted' | 'refused') : Promise<MountedHarness> {
  const config = authoredConfig();
  const basis = makeBasis(config);
  let latest = basis;
  const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>().mockImplementation(async (request, key) => {
    if (outcome === 'refused') {
      throw new ApiError(409, 'selection_changed', 'Track order changed at the Runtime head', 'request-track', {
        status: 'conflict', reason: 'selection_changed',
        base: { revision_id: 'r0', publication_id: 'p0' },
        current: { revision_id: 'remote-r1', publication_id: 'remote-p1' },
        conflicts: [], code: 'selection_changed', path: ['parent', 'config', 'tracks'],
        hint: 'Reload the timeline and retry the reorder.', suggested_command: 'show timeline',
      });
    }
    const result = acceptedResult(request, basis);
    result.receipt.idempotency_key = key;
    latest = { head: result.accepted, canonicalDocument: result.canonicalDocument, graph: result.graph };
    return result;
  });
  const provider: DataProvider = {
    persistenceEnabled: true,
    loadTimeline: vi.fn(async () => ({ config, configVersion: 1, head: initialHead })),
    loadAssetRegistry: vi.fn(async () => ({ assets: {} })),
    loadTimelineCommandBasis: vi.fn(async () => latest),
    getRecoverableIdentity: vi.fn(async () => ({ realmId: scope.realmId, actorId: scope.actorId, projectId: scope.projectId, timelineId: scope.timelineId })),
    commitTimeline: send,
    resolveAssetUrl: vi.fn(async (file: string) => file),
    getTimelineDraftRecoveryMetadata: () => ({ recoveryKey: scope.timelineId, draftIdentity: `mounted-track-${outcome}` }),
  };
  const data = await buildTimelineData(config, { assets: {} }, provider.resolveAssetUrl, 1, undefined, initialHead);
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const store = createTimelineStore();
  const interactionStateRef = { current: createInteractionState() };
  const queries = { timelineQuery: { data: undefined, isLoading: false }, assetRegistryQuery: { data: undefined } } as never;
  const runtime = {
    project: { projectId: scope.projectId },
    timelineId: scope.timelineId,
    assetResolver: null,
    shots: { shots: undefined, isLoading: false, error: null, refetchShots: vi.fn(), canonicalDraft: null },
  } as unknown as VideoEditorRuntimeContextValue;
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <VideoEditorRuntimeProvider value={runtime}>{children}</VideoEditorRuntimeProvider>
    </QueryClientProvider>
  );
  const hook = renderHook(() => {
    const save = useTimelineSave(queries, provider, interactionStateRef, store, data);
    const tracks = useTimelineTrackManagement({
      dataRef: save.dataRef,
      resolvedConfig: save.dataRef.current?.resolvedConfig ?? null,
      selectedClipId: null,
      setSelectedTrackId: save.setSelectedTrackId,
      applyEdit: save.applyEdit,
    });
    return { save, tracks };
  }, { wrapper });
  await waitFor(() => expect(hook.result.current.save.localSaveState?.ownerId).toBeTruthy());
  await waitFor(() => expect(hook.result.current.save.localSaveState?.status).toBe('saved'));
  return { hook, provider, send, basis, data };
}

async function settlePromises() {
  await act(async () => {
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
  });
}

describe('mounted track reorder persistence through A2', () => {
  beforeEach(() => {
    resetFakeIndexedDB();
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
    vi.stubGlobal('navigator', { locks: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('uses the real hook consumer and persists a guarded generic doc.patch list.move', async () => {
    const mounted = await mountHarness('accepted');
    try {
      act(() => mounted.hook.result.current.tracks.handleMoveTrack('overlay', 'picture'));
      await waitFor(() => expect(mounted.send).toHaveBeenCalledTimes(1), { timeout: 3000 });
      await waitFor(() => expect(mounted.hook.result.current.save.localSaveState?.status).toBe('saved'));

      const [request, key] = mounted.send.mock.calls[0];
      expect(request).toMatchObject({
        api_version: 1,
        project_id: scope.projectId,
        timeline_id: scope.timelineId,
        base_revision_id: 'r0',
        base_publication_id: 'p0',
        label: 'Edit timeline',
        merge: 'atomic',
        dry_run: false,
        source: { via: 'app' },
      });
      expect(request).not.toHaveProperty('reads');
      expect(key).toMatch(/^[0-9a-f-]{36}$/);
      expect(request.commands).toHaveLength(1);
      const command = request.commands[0];
      expect(command).toMatchObject({ schema_version: 1, op: 'doc.patch', version: '1', select: null, created: [] });
      const change = command.args.changes[0];
      expect(change).toMatchObject({
        op: 'list.move', ref: 'parent', path: ['config', 'tracks'], id: 'overlay',
        order_before: trackOrder, after_id: null,
      });
      expect(change.before).toEqual({ state: 'present', value: mounted.basis.canonicalDocument.parent_revision.payload.config.tracks![2] });
      expect(request.steps).toEqual([{
        id: expect.any(String), label: 'Edit timeline', intent: 'Save local editor changes', tags: [],
        command_ordinals: [0], patch: [change],
      }]);

      expect(mounted.hook.result.current.save.dataRef.current?.head).toMatchObject({ headRevisionId: 'r1', headPublicationId: 'p1' });
      expect(mounted.hook.result.current.save.dataRef.current?.config.tracks?.map((track) => track.id)).toEqual(reorderedTrackOrder);
      expect(mounted.hook.result.current.save.dataRef.current?.config.app).toEqual(authoredConfig().app);
      expect(mounted.hook.result.current.save.dataRef.current?.config.clips?.[0]?.app)
        .toEqual({ opaque: { keep: null, false: false, zero: 0 } });
      expect(mounted.hook.result.current.save.dataRef.current?.config.tracks?.find((track) => track.id === 'audio')?.app)
        .toEqual({ nullValue: null, falseValue: false, zeroValue: 0, scaleAppliesToPositionedClips: true });
      expect(mounted.hook.result.current.save.dataRef.current?.config.tracks?.find((track) => track.id === 'overlay')?.app)
        .toEqual({ opaque: [null, false, 0], scaleAppliesToPositionedClips: true });
      expect(request.steps?.[0]).not.toHaveProperty('reads');

      const [stored] = await createCommitOutbox().list(scope);
      expect(stored.intents).toHaveLength(0);
      expect(stored.accepted?.value).toMatchObject({
        accepted: { revisionId: 'r1', publicationId: 'p1' },
        response: { data: { status: 'accepted', label: 'Edit timeline', merge_mode: 'atomic' } },
      });
      expect((stored.accepted?.value as any).canonicalDocument.parent_revision.payload.opaque_parent)
        .toEqual({ keep: null, sibling: [false, 0] });
    } finally {
      mounted.hook.unmount();
      await settlePromises();
    }
  });

  it('retains the durable intent and rolls the mounted UI back on a structured refusal', async () => {
    const mounted = await mountHarness('refused');
    try {
      act(() => mounted.hook.result.current.tracks.handleMoveTrack('overlay', 'picture'));
      await waitFor(() => expect(mounted.send).toHaveBeenCalledTimes(1), { timeout: 3000 });
      await waitFor(() => expect(mounted.hook.result.current.save.localSaveState?.status).toBe('conflict'));

      expect(mounted.hook.result.current.save.saveStatus).toBe('error');
      expect(mounted.hook.result.current.save.localSaveState?.error).toMatchObject({
        kind: 'conflict', code: 'selection_changed',
        message: expect.stringContaining('selection_changed'),
        details: expect.objectContaining({ path: ['parent', 'config', 'tracks'], hint: 'Reload the timeline and retry the reorder.' }),
      });
      expect(mounted.hook.result.current.save.dataRef.current?.head).toMatchObject({ headRevisionId: 'r0', headPublicationId: 'p0' });
      expect(mounted.hook.result.current.save.dataRef.current?.config.tracks?.map((track) => track.id)).toEqual(trackOrder);
      expect(mounted.hook.result.current.save.dataRef.current?.config.app).toEqual(authoredConfig().app);
      expect(mounted.hook.result.current.save.dataRef.current?.config.clips?.[0]?.app)
        .toEqual({ opaque: { keep: null, false: false, zero: 0 } });

      const [stored] = await createCommitOutbox().list(scope);
      expect(stored.intents).toHaveLength(1);
      expect(stored.pending?.outcome).toMatchObject({ kind: 'rejected', error: { code: 'selection_changed' } });
      const intent = stored.intents[0].payload as any;
      expect(intent.label).toBe('Edit timeline');
      expect(intent.documentIntent.changes[0]).toMatchObject({
        op: 'list.move', ref: 'parent', path: ['config', 'tracks'], id: 'overlay',
        before: { state: 'present', value: mounted.basis.canonicalDocument.parent_revision.payload.config.tracks![2] },
        order_before: trackOrder, after_id: null,
      });
      expect(intent.documentIntent.after.parent_revision.payload.config.tracks.map((track: { id: string }) => track.id))
        .toEqual(reorderedTrackOrder);
      expect(intent.documentIntent.after.parent_revision.payload.config.clips[0].app)
        .toEqual({ opaque: { keep: null, false: false, zero: 0 } });
      expect(intent.documentIntent.after.parent_revision.payload.opaque_parent)
        .toEqual({ keep: null, sibling: [false, 0] });
    } finally {
      mounted.hook.unmount();
      await settlePromises();
    }
  });

  it('classifies same-order legacy explicit write separately: the current mounted UI is a no-op', async () => {
    const mounted = await mountHarness('accepted');
    try {
      act(() => mounted.hook.result.current.tracks.handleMoveTrack('picture', 'picture'));
      await settlePromises();
      expect(mounted.send).not.toHaveBeenCalled();
      expect(mounted.hook.result.current.save.dataRef.current?.config.tracks?.map((track) => track.id)).toEqual(trackOrder);
      const records = await createCommitOutbox().list(scope);
      expect(records[0]?.intents).toHaveLength(0);
    } finally {
      mounted.hook.unmount();
      await settlePromises();
    }
  });
});
