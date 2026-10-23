// Temporary A2 probe. This file is intentionally untracked and is not product
// or suite coverage; it exercises the mounted production caller only.
// @vitest-environment jsdom
import React from 'react';
import { act, renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { useTimelineSave } from './src/tools/video-editor/hooks/useTimelineSave.ts';
import { useClipEditing } from './src/tools/video-editor/hooks/useClipEditing.ts';
import { VideoEditorRuntimeProvider } from './src/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore } from './src/tools/video-editor/hooks/timelineStore.ts';
import { createInteractionState, type InteractionStateRef } from './src/tools/video-editor/lib/interaction-state.ts';
import { buildTimelineData } from './src/tools/video-editor/lib/timeline-data.ts';
import { createDefaultTimelineConfig } from './src/tools/video-editor/lib/defaults.ts';
import { acceptedCommit, fixtureDigest } from './src/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createCommitOutbox } from './src/tools/video-editor/commands/commitOutbox.ts';
import type { DataProvider } from './src/tools/video-editor/data/DataProvider.ts';
import type { UsePollSyncQueries } from './src/tools/video-editor/hooks/usePollSync.ts';
import type { VideoEditorRuntimeContextValue } from './src/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';

vi.stubGlobal('indexedDB', createFakeIndexedDB());
vi.mock('./src/integrations/runtime/generated-contract-metadata.ts', async (importOriginal) => ({
  ...await importOriginal<typeof import('./src/integrations/runtime/generated-contract-metadata.ts')>(),
  SCHEMA_DIGEST: 'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
}));
vi.mock('./src/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({
  invalidateReferencedTimelineCache: vi.fn(),
}));

const scope = { actorId: 'actor', realmId: 'realm', projectId: 'project-commit', timelineId: 'timeline-1' };
const head = { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: 'r0', headPublicationId: 'p0' };
const registry = { assets: { 'p1-video': { file: 'p1-video.mp4', type: 'video/mp4', duration: 8 } } };

function makeConfig() {
  const config = createDefaultTimelineConfig();
  config.clips = [{ id: 'p1-chain-source', at: 0, track: 'V1', clipType: 'media', asset: 'p1-video', from: 0,
    to: 8, speed: 1, hold: 8, app: { opaque: { keep: null }, astrid: { for: 8 }, 'org.example': { clear: null } } }];
  return config;
}

function reply(config: ReturnType<typeof makeConfig>, revision: string, publication: string, baseRevision: string, basePublication: string) {
  const response = acceptedCommit({ revision_id: revision, publication_id: publication },
    { revision_id: baseRevision, publication_id: basePublication }, { timelineId: scope.timelineId });
  const document = response.data.canonical_document;
  document.parent_revision.payload = { config: JSON.parse(JSON.stringify(config)), clips: JSON.parse(JSON.stringify(config.clips)), registry, occurrences: [] };
  document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
  response.data.document_digest = fixtureDigest(document);
  return { response, accepted: { revisionId: revision, publicationId: publication }, canonicalDocument: document,
    graph: {}, receipt: response.receipt };
}

async function settle() {
  await act(async () => { await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
}

describe('A2 controlled mounted split -> accepted -> immediate Source In', () => {
  beforeEach(() => { vi.useFakeTimers(); vi.setSystemTime(new Date('2026-10-23T15:00:00.000Z')); resetFakeIndexedDB(); vi.stubGlobal('indexedDB', createFakeIndexedDB()); });
  afterEach(() => { vi.clearAllTimers(); vi.useRealTimers(); });

  it('captures the accepted split before Source In and sends the dependent guarded request', async () => {
    const descriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
    const locks = new Set<string>();
    Object.defineProperty(navigator, 'locks', { configurable: true, value: {
      request: async (name: string, _options: unknown, work: (lock: object | null) => Promise<unknown>) => {
        if (locks.has(name)) return work(null);
        locks.add(name);
        try { return await work({}); } finally { locks.delete(name); }
      },
    } });
    const config = makeConfig();
    const initialReply = reply(config, 'r0', 'p0', 'r0', 'p0');
    const initial = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: initialReply.canonicalDocument };
    const data = await buildTimelineData(config, registry, undefined, 1, undefined, head);
    const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>();
    let acknowledge!: (value: Awaited<ReturnType<NonNullable<DataProvider['commitTimeline']>>>) => void;
    send.mockImplementationOnce(() => new Promise((resolve) => { acknowledge = resolve; }));
    const provider: DataProvider = {
      persistenceEnabled: true, loadTimeline: vi.fn(), loadAssetRegistry: vi.fn(),
      saveTimeline: vi.fn(async () => { throw new Error('legacy writer called'); }),
      resolveAssetUrl: vi.fn(async (file: string) => file), loadTimelineCommandBasis: vi.fn(async () => initial),
      commitTimeline: send, getRecoverableIdentity: vi.fn(async () => ({ actorId: scope.actorId, realmId: scope.realmId })),
    };
    const queries: UsePollSyncQueries = { timelineQuery: { data: undefined, isLoading: false }, assetRegistryQuery: { data: undefined } };
    const interactionStateRef: InteractionStateRef = { current: createInteractionState() };
    const store = createTimelineStore();
    const runtime = { provider, project: { projectId: scope.projectId }, timelineId: scope.timelineId,
      assetResolver: { resolveAssetUrl: vi.fn(async (file: string) => file) }, shots: { shots: undefined, isLoading: false, error: null,
        refetchShots: vi.fn() } } as unknown as VideoEditorRuntimeContextValue;
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
    const wrapper = ({ children }: { children: React.ReactNode }) => <QueryClientProvider client={queryClient}>
      <VideoEditorRuntimeProvider value={runtime}>{children}</VideoEditorRuntimeProvider>
    </QueryClientProvider>;
    const harness = renderHook(() => useTimelineSave(queries, provider, interactionStateRef, store, data), { wrapper });
    const editing = renderHook(() => useClipEditing({ dataRef: harness.result.current.dataRef,
      resolvedConfig: harness.result.current.dataRef.current?.resolvedConfig ?? null,
      selectedClipId: harness.result.current.selectedClipId, selectedTrack: null, currentTime: 2,
      selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit: harness.result.current.applyEdit }));
    try {
      await vi.waitFor(() => expect(harness.result.current.localSaveState?.ownerId).toBeTruthy());
      await settle();
      await act(async () => { editing.result.current.handleSplitClipAtTime('p1-chain-source', 2); });
      await act(async () => { await vi.advanceTimersByTimeAsync(500); });
      await vi.waitFor(() => expect(send).toHaveBeenCalledTimes(1));
      const splitConfig = structuredClone(harness.result.current.dataRef.current!.config);
      const rightId = harness.result.current.selectedClipId!;
      expect(rightId).not.toBe('p1-chain-source');
      const splitRequest = structuredClone(send.mock.calls[0][0]);
      const splitResult = reply(splitConfig, 'r1', 'p1', 'r0', 'p0');
      expect(splitResult.response).toMatchObject({ data: expect.any(Object), receipt: expect.any(Object) });
      await act(async () => { acknowledge(splitResult); await settle(); });
      await vi.waitFor(() => expect(harness.result.current.localSaveState).toMatchObject({ status: 'saved' }));
      expect(harness.result.current.dataRef.current?.head?.headRevisionId).toBe('r1');

      // No poll, debounce, or owner replacement between split ACK and the real inspector caller.
      editing.rerender();
      await act(async () => { editing.result.current.handleSelectedClipChange({ from: 3 }); });
      await settle();
      const ownersBeforeTransport = await createCommitOutbox().list(scope);
      const ownerBeforeTransport = ownersBeforeTransport.find((owner) => owner.intents.length === 1);
      expect(ownerBeforeTransport).toBeDefined();
      expect(ownerBeforeTransport!.intents[0].basis).toEqual({ after: ownerBeforeTransport!.accepted!.intentId });
      expect(ownerBeforeTransport!.intents[0].payload).toMatchObject({ documentIntent: {
        changes: [{ op: 'set', ref: 'parent', path: ['clips', `id:${rightId}`, 'from'],
          before: { state: 'present', value: 0 }, value: 3 }],
      } });
      expect(ownerBeforeTransport!.intents[0].payload).toMatchObject({ after: { parent_revision: { payload: {
        config: { clips: expect.arrayContaining([expect.objectContaining({ id: rightId, from: 3 })]) },
      } } } });
      const rightBefore = harness.result.current.dataRef.current!.config.clips.find((clip) => clip.id === rightId)!;
      expect(rightBefore.app).toEqual({ opaque: { keep: null }, astrid: { for: 8 }, 'org.example': { clear: null } });

      send.mockImplementationOnce(async (_request) => reply(harness.result.current.dataRef.current!.config, 'r2', 'p2', 'r1', 'p1'));
      await act(async () => { await vi.advanceTimersByTimeAsync(500); });
      await vi.waitFor(() => expect(send).toHaveBeenCalledTimes(2));
      const trimRequest = send.mock.calls[1][0];
      expect(send.mock.calls[0][1]).toEqual(expect.any(String));
      expect(send.mock.calls[1][1]).toEqual(expect.any(String));
      expect(send.mock.calls[1][1]).not.toBe(send.mock.calls[0][1]);
      expect(trimRequest).toMatchObject({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
        base_revision_id: 'r1', base_publication_id: 'p1', label: 'Edit timeline', merge: 'fields', dry_run: false,
        source: { via: 'app' }, commands: [{ schema_version: 1, op: 'doc.patch', version: '1', select: null,
          created: [], args: { changes: [{ op: 'set', ref: 'parent', path: ['clips', `id:${rightId}`, 'from'],
            before: { state: 'present', value: 0 }, value: 3 }] } }],
        steps: [{ command_ordinals: [0] }], reads: expect.arrayContaining([{ kind: 'field', ref: 'parent',
          path: ['config', 'clips', `id:${rightId}`, 'from'], state: { state: 'present', value: 0 } }]) });
      expect(trimRequest.steps?.[0].patch).toEqual(trimRequest.commands[0].args.changes);
      expect(harness.result.current.dataRef.current?.head?.headRevisionId).toBe('r2');
      const finalRight = harness.result.current.dataRef.current!.config.clips.find((clip) => clip.id === rightId)!;
      expect(finalRight).toMatchObject({ id: rightId, from: 3 });
      expect(finalRight.app).toEqual({ opaque: { keep: null }, astrid: { for: 8 }, 'org.example': { clear: null } });
      const outboxAfter = await createCommitOutbox().list(scope);
      expect(outboxAfter.find((owner) => owner.ownerId === ownerBeforeTransport!.ownerId)?.intents).toHaveLength(0);
      console.log(JSON.stringify({
        controlled: 'PASS', schedule: 'accepted split -> immediate Source In', mountedCaller: 'useClipEditing.handleSelectedClipChange',
        rightId, splitRequest, trimRequest, idempotencyKeys: [send.mock.calls[0][1], send.mock.calls[1][1]],
        ownerId: ownerBeforeTransport!.ownerId, ownerStatusAfter: harness.result.current.localSaveState,
        outboxBeforeTransport: { intentCount: 1, predecessor: ownerBeforeTransport!.intents[0].basis },
        outboxAfterTransport: { intentCount: outboxAfter.find((owner) => owner.ownerId === ownerBeforeTransport!.ownerId)?.intents.length ?? -1 },
        rawApp: finalRight.app,
      }, null, 2));
    } finally {
      editing.unmount();
      harness.unmount();
      if (descriptor) Object.defineProperty(navigator, 'locks', descriptor);
      else Reflect.deleteProperty(navigator, 'locks');
    }
  });
});
