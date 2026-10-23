// @vitest-environment jsdom
import React from 'react';
import { act, renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { useTimelineHistory } from './useTimelineHistory';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { json, runtimeFixture } from '@/test/fakeWorkspaceRuntime.ts';
import type { HistoryEntry, HistoryPage, CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import { useTimelineSave } from './useTimelineSave';
import { useClipEditing } from './useClipEditing';
import { VideoEditorRuntimeProvider } from '../contexts/VideoEditorRuntimeContext';
import { createTimelineStore } from './timelineStore';
import { createInteractionState, type InteractionStateRef } from '../lib/interaction-state';
import { buildTimelineData, configToRows, type TimelineData } from '../lib/timeline-data';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { getConfigSignature, getStableConfigSignature } from '../lib/config-utils';
import { createDefaultTimelineConfig } from '../lib/defaults';
import { TimelineVersionConflictError, type DataProvider } from '../data/DataProvider';
import { loadTimelineDraft, saveTimelineDraft } from '../data/timelineDraftIndexedDb';
import type { VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext';
import type { TimelineEditability } from '../lib/timeline-editability';
import { createCommitOutbox } from '../commands/commitOutbox.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';

vi.mock('@/integrations/runtime/generated-contract-metadata.ts', async (importOriginal) => ({
  ...await importOriginal<typeof import('@/integrations/runtime/generated-contract-metadata.ts')>(),
  SCHEMA_DIGEST: 'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
}));

vi.stubGlobal('indexedDB', createFakeIndexedDB());
vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({
  invalidateReferencedTimelineCache: vi.fn(),
}));

function makeTimelineData(label: string): TimelineData {
  const base = createDefaultTimelineConfig();
  const config = {
    ...base,
    output: { ...base.output, file: `output-${label}.mp4` },
    tracks: (base.tracks ?? []).map((track) => ({ ...track })),
    clips: [{
      id: `clip-${label}`,
      at: 0,
      track: 'V1' as const,
      clipType: 'hold' as const,
      hold: 1,
    }],
  };
  const rowData = configToRows(config);
  const resolvedConfig = {
    output: { ...config.output },
    tracks: (config.tracks ?? []).map((track) => ({ ...track })),
    clips: config.clips.map((clip) => ({ ...clip, assetEntry: undefined })),
    registry: {},
  };
  return {
    config,
    configVersion: 1,
    registry: { assets: {} },
    resolvedConfig,
    rows: rowData.rows,
    meta: rowData.meta,
    effects: rowData.effects,
    assetMap: {},
    output: { ...config.output },
    tracks: (config.tracks ?? []).map((track) => ({ ...track })),
    clipOrder: rowData.clipOrder,
    signature: getConfigSignature(resolvedConfig),
    stableSignature: getStableConfigSignature(config, { assets: {} }),
  };
}

interface SetupResult {
  hook: {
    result: { current: ReturnType<typeof useTimelineSave> & { history: ReturnType<typeof useTimelineHistory> } };
    unmount: () => void;
  };
  saveTimeline: ReturnType<typeof vi.fn>;
  toast: { error: ReturnType<typeof vi.fn>; success: ReturnType<typeof vi.fn> };
}

function setup(
  saveTimelineImpl: DataProvider['saveTimeline'],
  timelineEditability?: TimelineEditability,
  original?: { data: TimelineData; loadBasis: DataProvider['loadTimelineCommandBasis']; capabilities?: Partial<DataProvider>; strict?: boolean },
): SetupResult {
  const saveTimeline = vi.fn(saveTimelineImpl);
  const provider: DataProvider = {
    persistenceEnabled: true,
    loadTimeline: vi.fn(async () => ({ config: createDefaultTimelineConfig(), configVersion: 1 })),
    loadAssetRegistry: vi.fn(async () => ({ assets: {} })),
    saveTimeline,
    resolveAssetUrl: vi.fn(async (file: string) => file),
    ...(original ? { loadTimelineCommandBasis: original.loadBasis } : {}),
    ...original?.capabilities,
  };
  const queries = {
    timelineQuery: { data: undefined, isLoading: false },
    assetRegistryQuery: { data: undefined },
  };
  const interactionStateRef: InteractionStateRef = { current: createInteractionState() };
  const store = createTimelineStore();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const toast = { error: vi.fn(), success: vi.fn() };
  const runtime = {
    provider,
    project: { projectId: 'project-commit' },
    toast,
    timelineId: 'timeline-1',
    shots: { canonicalDraft: null },
    assetResolver: { resolveAssetUrl: vi.fn(async (file: string) => file) },
    shots: {
      shots: undefined,
      isLoading: false,
      error: null,
      refetchShots: vi.fn(),
    },
    timelineEditability,
  } as unknown as VideoEditorRuntimeContextValue;
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <VideoEditorRuntimeProvider value={runtime}>{original?.strict ? <React.StrictMode>{children}</React.StrictMode> : children}</VideoEditorRuntimeProvider>
    </QueryClientProvider>
  );
  const hook = renderHook(
    () => {
      const save = useTimelineSave(queries, provider, interactionStateRef, store, original?.data);
      const history = useTimelineHistory({ dataRef: save.dataRef, commitData: save.commitData,
        interactionStateRef, pendingOpsRef: save.pendingOpsRef, remoteHistory: save.localDocumentSave });
      return { ...save, history };
    },
    { wrapper },
  );
  return { hook, saveTimeline, toast };
}

async function flush() {
  await act(async () => {
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
  });
}

// The hook freezes writes (including owned flushes) until its one-time
// IndexedDB recovery check settles. IndexedDB requests complete in issue
// order, so a read issued after the hook's read resolves only once that check
// has resolved; flush the check's trailing promise handlers afterwards.
async function settleInitialRecoveryCheck() {
  await loadTimelineDraft('timeline-1');
  await flush();
}

describe('useTimelineSave — recovered draft durability', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    resetFakeIndexedDB();
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.useRealTimers();
  });

  it('persists an inspector trim of the locally split new ID while its split is awaiting acceptance', async () => {
    const descriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
    Object.defineProperty(navigator, 'locks', { configurable: true, value: {
      request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
    } });
    const head = { projectId: 'project-commit', timelineId: 'timeline-1', headRevisionId: 'r0', headPublicationId: 'p0' };
    const config = createDefaultTimelineConfig();
    config.clips = [{ id: 'p1-chain-source', at: 0, track: 'V1', clipType: 'media', asset: 'p1-video', from: 0, to: 8, speed: 1, hold: 8,
      app: { opaque: { keep: null }, astrid: { for: 8 }, 'org.example': { clear: null } } }];
    const registry = { assets: { 'p1-video': { file: 'p1-video.mp4', type: 'video/mp4', duration: 8 } } };
    const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' },
      { timelineId: 'timeline-1' }).data.canonical_document;
    document.parent_revision.payload = { config, clips: config.clips, registry, occurrences: [] };
    document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
    const initial = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: document };
    const data = await buildTimelineData(config, registry, undefined, 1, undefined, head);
    let acknowledge!: (value: Awaited<ReturnType<NonNullable<DataProvider['commitTimeline']>>>) => void;
    const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>().mockImplementationOnce(() => new Promise((resolve) => { acknowledge = resolve; }));
    const harness = setup(async () => { throw new Error('Legacy save must not be called'); }, undefined, {
      data, loadBasis: vi.fn(async () => initial), capabilities: {
        commitTimeline: send, getRecoverableIdentity: vi.fn(async () => ({ actorId: 'actor', realmId: 'realm' })),
      },
    });
    const editing = renderHook(() => useClipEditing({
      dataRef: harness.hook.result.current.dataRef,
      resolvedConfig: harness.hook.result.current.dataRef.current?.resolvedConfig ?? null,
      selectedClipId: harness.hook.result.current.selectedClipId,
      selectedTrack: null, currentTime: 2, selectClip: vi.fn(), setSelectedTrackId: vi.fn(),
      applyEdit: harness.hook.result.current.applyEdit,
    }));
    try {
      await vi.waitFor(() => expect(harness.hook.result.current.localSaveState?.ownerId).toBeTruthy());
      await settleInitialRecoveryCheck();
      await act(async () => { editing.result.current.handleSplitClipAtTime('p1-chain-source', 2); });
      await act(async () => { await vi.advanceTimersByTimeAsync(500); });
      await vi.waitFor(() => expect(send).toHaveBeenCalledTimes(1));
      const rightId = harness.hook.result.current.selectedClipId!;
      expect(rightId).not.toBe('p1-chain-source');
      const splitConfig = structuredClone(harness.hook.result.current.dataRef.current!.config);
      editing.rerender();
      await act(async () => { editing.result.current.handleSelectedClipChange({ from: 3 }); });
      const [owner] = await createCommitOutbox().list({ realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-1' });
      expect(owner.intents).toHaveLength(2);
      expect(owner.intents[1].basis).toEqual({ after: owner.intents[0].id });
      expect(owner.intents[1].payload).toMatchObject({ documentIntent: {
        changes: expect.arrayContaining([{ op: 'set', ref: 'parent', path: ['clips', `id:${rightId}`, 'from'],
          before: { state: 'present', value: 0 }, value: 3 }]),
        reads: expect.arrayContaining([{ kind: 'field', ref: 'parent', path: ['config', 'clips', `id:${rightId}`, 'from'],
          state: { state: 'present', value: 0 } }]),
      } });
      const trimmedConfig = structuredClone(harness.hook.result.current.dataRef.current!.config);
      const reply = (config: typeof splitConfig, revision: string, publication: string) => {
        const response = acceptedCommit({ revision_id: revision, publication_id: publication },
          { revision_id: 'r0', publication_id: 'p0' }, { timelineId: 'timeline-1' });
        response.data.canonical_document = structuredClone(document);
        response.data.canonical_document.parent_revision.revision_id = revision;
        response.data.canonical_document.parent_revision.payload.config = JSON.parse(JSON.stringify(config));
        response.data.canonical_document.parent_revision.payload.clips = JSON.parse(JSON.stringify(config.clips));
        response.data.canonical_document.parent_revision.content_digest = fixtureDigest(response.data.canonical_document.parent_revision.payload);
        return { response, accepted: { revisionId: revision, publicationId: publication },
          canonicalDocument: response.data.canonical_document, graph: {}, receipt: response.receipt };
      };
      let adopted: TimelineData | null = null;
      send.mockImplementationOnce(async () => {
        adopted = harness.hook.result.current.dataRef.current;
        return reply(trimmedConfig, 'r2', 'p2');
      });
      await act(async () => { acknowledge(reply(splitConfig, 'r1', 'p1')); });
      await act(async () => { await vi.advanceTimersByTimeAsync(500); });
      await vi.waitFor(() => expect(harness.hook.result.current.localSaveState?.status).toBe('saved'));
      expect(send).toHaveBeenCalledTimes(2);
      expect(adopted!.head?.headRevisionId).toBe('r1');
      expect(adopted!.config.clips).toEqual(splitConfig.clips);
      const request = send.mock.calls[1][0];
      expect(request).toMatchObject({ api_version: 1, project_id: head.projectId, timeline_id: head.timelineId,
        base_revision_id: 'r1', base_publication_id: 'p1', merge: 'fields', dry_run: false,
        commands: [{ op: 'doc.patch', args: { changes: expect.arrayContaining([
          { op: 'set', ref: 'parent', path: ['clips', `id:${rightId}`, 'from'],
            before: { state: 'present', value: 0 }, value: 3 },
        ]) } }],
        reads: expect.arrayContaining([{ kind: 'field', ref: 'parent', path: ['config', 'clips', `id:${rightId}`, 'from'],
          state: { state: 'present', value: 0 } }]),
      });
      expect(request.steps?.[0].patch).toEqual(request.commands[0].args.changes);
      expect(harness.saveTimeline).not.toHaveBeenCalled();
      expect(harness.hook.result.current.dataRef.current?.head?.headRevisionId).toBe('r2');
      expect(harness.hook.result.current.dataRef.current?.config.clips.find((clip) => clip.id === rightId)).toEqual({
        ...config.clips[0], id: rightId, at: 2, hold: 6, from: 3,
      });
      const [saved] = await createCommitOutbox().list({ realmId: 'realm', actorId: 'actor', projectId: head.projectId, timelineId: head.timelineId });
      expect(saved.intents).toHaveLength(0);
    } finally {
      // Settle the held transport before releasing this mounted durable owner.
      if (acknowledge) {
        send.mockRejectedValue(new ApiError(409, 'conflict', 'Consumed read changed', '', { path: ['hold'], hint: 'Read latest' }));
        const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' }, { timelineId: 'timeline-1' });
        response.data.canonical_document = structuredClone(document);
        response.data.canonical_document.parent_revision.revision_id = 'r1';
        await act(async () => { acknowledge({ response, accepted: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: response.data.canonical_document, graph: {}, receipt: response.receipt }); });
      }
      editing.unmount();
      harness.hook.unmount();
      if (descriptor) Object.defineProperty(navigator, 'locks', descriptor);
      else Reflect.deleteProperty(navigator, 'locks');
    }
  });

  it.each(['accepted', 'merged', 'lost acknowledgement', 'later_write', 'aba_write', 'history_unavailable', 'invalid', 'legacy_unknown'] as const)(
    'mounted Undo uses the public client, authoritative history and reload (%s)', async (outcome) => {
      const locks = new Set<string>();
      const descriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
      Object.defineProperty(navigator, 'locks', { configurable: true, value: {
        request: async (name: string, _options: unknown, work: (lock: object | null) => Promise<unknown>) => {
          if (locks.has(name)) return work(null);
          locks.add(name);
          try { return await work({}); } finally { locks.delete(name); }
        },
      } });
      const fixture = runtimeFixture();
      const timelineId = 'timeline-1';
      const projectId = 'project-commit';
      const baseConfig = createDefaultTimelineConfig();
      const authoredConfig = { ...baseConfig, output: { ...baseConfig.output, file: 'authored.mp4' } };
      const makeResponse = (ordinal: number, config = authoredConfig) => {
        const response = acceptedCommit({ revision_id: `r${ordinal}`, publication_id: `p${ordinal}` },
          { revision_id: `r${Math.max(0, ordinal - 1)}`, publication_id: `p${Math.max(0, ordinal - 1)}` }, { timelineId });
        response.data.canonical_document.parent_revision.payload = { config: structuredClone(config), clips: [],
          occurrences: [], registry: { assets: {} }, opaque: { keep: null, agent: true } };
        response.data.canonical_document.parent_revision.content_digest = fixtureDigest(response.data.canonical_document.parent_revision.payload);
        response.data.document_digest = fixtureDigest(response.data.canonical_document);
        return response;
      };
      const bootstrap = makeResponse(0, baseConfig);
      let current = bootstrap;
      const images = new Map([['r0', bootstrap.data.canonical_document]]);
      const entry = (response: typeof current, undoOf: string[] = []): HistoryEntry => ({
        publication_id: response.receipt.receipt_id, revision_id: response.data.accepted_revision_id,
        previous: response.receipt.receipt_id === 'p0' ? null
          : { revision_id: response.data.previous_revision_id, publication_id: response.data.previous_publication_id },
        receipt: response.receipt, intent: response.receipt.receipt_id === 'p0' ? 'bootstrap' : 'recorded',
        records: { schema_version: 1, commands: [], steps: response.data.steps, undo_of: undoOf, undo_steps: null, restored_from: null },
        publisher: response.data.publisher, provider_version: response.data.provider_version,
        compiler_version: response.data.compiler_version, label: response.data.label,
      });
      const items = [entry(bootstrap)];
      const posted: { body: string; key: string; path: string }[] = [];
      let lost = false;
      const refused = ['later_write', 'aba_write', 'history_unavailable', 'invalid'].includes(outcome);
      const transport: typeof fixture.transport = async (method, path, headers, body) => {
        if (method === 'GET' && path.includes('/commits?')) {
          const history: HistoryPage = { items, next_cursor: null,
            head: { revision_id: current.data.accepted_revision_id, publication_id: current.receipt.receipt_id } };
          return { status: 200, headers: {}, body: json(history) };
        }
        if (method === 'GET' && path.includes('/composition-revisions/')) {
          const document = images.get(decodeURIComponent(path.split('/').at(-1)!))!;
          return { status: 200, headers: {}, body: json({ project_id: projectId, timeline_id: timelineId,
            revision_id: document.parent_revision.revision_id, payload: document.parent_revision.payload,
            content_digest: document.parent_revision.content_digest, dependency_manifest: document.dependency_manifest }) };
        }
        if (method === 'POST' && path.endsWith('/commit')) {
          const bytes = new TextDecoder().decode(body as Uint8Array);
          const request = JSON.parse(bytes) as CommitRequest;
          if (request.commands[0].op === 'doc.patch') {
            expect(request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId,
              base_revision_id: 'r0', base_publication_id: 'p0', label: 'Edit timeline', merge: 'atomic', dry_run: false,
              steps: [{ command_ordinals: [0], patch: request.commands[0].args.changes }] });
            current = makeResponse(1);
            current.data.commands = request.commands;
            current.data.steps = request.steps;
            current.receipt.idempotency_key = headers['Idempotency-Key'];
            images.set('r1', current.data.canonical_document);
            items.push(entry(current));
            if (outcome === 'legacy_unknown') { items[1].intent = 'legacy_unknown'; items[1].records = null; }
            return { status: 200, headers: {}, body: json(current) };
          }
          posted.push({ body: bytes, key: headers['Idempotency-Key'], path });
          if (refused) return { status: outcome === 'invalid' ? 422 : 409, headers: {}, body: json({
            code: outcome, message: 'Guarded inverse refused', request_id: 'undo-refusal', details: {
              status: outcome === 'invalid' ? 'invalid' : 'refused', reason: outcome, code: outcome,
              path: ['config', 'output', 'file'], hint: 'Reload authoritative history',
              base: { revision_id: 'r1', publication_id: 'p1' }, current: { revision_id: 'r1', publication_id: 'p1' }, conflicts: [],
            },
          }) };
          if (!(lost && posted.length === 2)) {
            const ordinal = items.length;
            current = makeResponse(ordinal, ordinal % 2 === 0 ? baseConfig : authoredConfig);
            current.data.commands = request.commands;
            current.data.label = request.label;
            current.data.steps = request.steps;
            current.data.merge_mode = 'fields';
            if (outcome === 'merged') {
              current.data.status = 'merged';
              current.data.rebased_onto = { revision_id: 'agent-r', publication_id: 'agent-p' };
            }
            current.receipt.idempotency_key = headers['Idempotency-Key'];
            images.set(current.data.accepted_revision_id, current.data.canonical_document);
            items.push(entry(current, request.commands[0].args.publications as string[]));
          }
          if (outcome === 'lost acknowledgement' && !lost) { lost = true; throw new Error('Lost acknowledgement'); }
          return { status: 200, headers: {}, body: json(current) };
        }
        return fixture.transport(method, path, headers, body);
      };
      const runtime = new RuntimeDataProvider({ projectId, transport });
      const scope = { actorId: 'actor', realmId: 'realm', projectId, timelineId };
      const mount = async () => {
        const basis = await runtime.loadTimelineCommandBasis(timelineId);
        const head = { projectId, timelineId, headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId };
        const data = await buildTimelineData(basis.canonicalDocument.parent_revision.payload.config as unknown as typeof baseConfig,
          { assets: {} }, undefined, 1, undefined, head);
        return setup(async () => { throw new Error('No snapshot save'); }, undefined, { data,
          loadBasis: () => runtime.loadTimelineCommandBasis(timelineId), capabilities: {
            commitTimeline: (request, key) => runtime.commitTimeline(request, key), getRecoverableIdentity: async () => scope,
          } });
      };
      let harness: Awaited<ReturnType<typeof mount>> | undefined;
      try {
        harness = await mount();
        await vi.waitFor(() => expect(harness!.hook.result.current.localSaveState?.ownerId).toBeTruthy());
        expect(harness.hook.result.current.history.canUndo).toBe(false);
        const edited = await buildTimelineData(authoredConfig, { assets: {} }, undefined, 1, undefined,
          { projectId, timelineId, headRevisionId: 'r0', headPublicationId: 'p0' });
        await act(async () => {
          harness!.hook.result.current.commitData(edited, { save: true });
          await harness!.hook.result.current.flushPendingSave();
        });
        if (outcome === 'legacy_unknown') {
          expect(harness.hook.result.current.history.canUndo).toBe(false);
          act(() => harness!.hook.result.current.history.undo());
          expect(posted).toHaveLength(0);
          expect(harness.saveTimeline).not.toHaveBeenCalled();
          return;
        }
        await vi.waitFor(() => expect(harness!.hook.result.current.history.canUndo).toBe(true));
        act(() => harness!.hook.result.current.history.undo());
        await vi.waitFor(() => expect(posted).toHaveLength(1));
        const sent = JSON.parse(posted[0].body);
        expect(sent).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId,
          base_revision_id: 'r1', base_publication_id: 'p1', label: 'Undo timeline', merge: 'fields', dry_run: false,
          commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['p1'] } }],
          steps: [{ label: 'Undo timeline', command_ordinals: [0], patch: [] }] });
        expect(sent).not.toHaveProperty('reads');
        expect(posted[0].path).toBe(`/v1/projects/${projectId}/timelines/${timelineId}/commit`);
        if (refused || lost) {
          await vi.waitFor(() => expect(harness!.toast.error).toHaveBeenCalled());
          expect(harness.hook.result.current.history.canUndo).toBe(false);
          expect(harness.hook.result.current.history.canRedo).toBe(false);
          const [stored] = await createCommitOutbox().list(scope);
          expect(stored.pending!.request).toMatchObject({ body: posted[0].body, key: posted[0].key });
          if (refused) {
            expect(stored.pending!.outcome).toMatchObject({ kind: 'rejected', error: { code: outcome,
              details: { code: outcome, path: ['config', 'output', 'file'], hint: 'Reload authoritative history' } } });
            expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe('authored.mp4');
            expect(harness.hook.result.current.localSaveState?.status).toBe('conflict');
            expect(harness.hook.result.current.saveStatus).toBe('error');
            harness.hook.unmount();
            await vi.waitFor(() => expect(locks.size).toBe(0));
            harness = await mount();
            await vi.waitFor(() => expect(harness!.hook.result.current.localSaveState?.status).toBe('conflict'));
            expect(harness.hook.result.current.history.canUndo).toBe(false);
            expect(posted).toHaveLength(1);
            const [retained] = await createCommitOutbox().list(scope);
            expect(retained.pending).toEqual(stored.pending);
            expect(harness.saveTimeline).not.toHaveBeenCalled();
            return;
          }
          expect(harness.hook.result.current.saveStatus).toBe('error');
        } else {
          await vi.waitFor(() => expect(harness!.hook.result.current.history.canRedo).toBe(true));
          expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe(baseConfig.output.file);
          expect(harness.hook.result.current.dataRef.current?.head?.headPublicationId).toBe('p2');
          const [stored] = await createCommitOutbox().list(scope);
          expect(stored.accepted!.value).toMatchObject({ response: current, receipt: current.receipt,
            canonicalDocument: current.data.canonical_document });
        }
        harness.hook.unmount();
        await vi.waitFor(() => expect(locks.size).toBe(0));
        harness = await mount();
        await vi.waitFor(() => expect(harness!.hook.result.current.history.canRedo).toBe(true));
        if (lost) expect(posted[1]).toEqual(posted[0]);
        act(() => harness!.hook.result.current.history.redo());
        await vi.waitFor(() => expect(harness!.hook.result.current.history.canUndo).toBe(true));
        expect(JSON.parse(posted.at(-1)!.body).commands[0].args.publications).toEqual(['p2']);
        expect(posted.at(-1)!.key).not.toBe(posted[0].key);
        expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe('authored.mp4');
        harness.hook.unmount();
        await vi.waitFor(() => expect(locks.size).toBe(0));
        harness = await mount();
        await vi.waitFor(() => expect(harness!.hook.result.current.history.canUndo).toBe(true));
        act(() => harness!.hook.result.current.history.undo());
        await vi.waitFor(() => expect(harness!.hook.result.current.history.canRedo).toBe(true));
        expect(JSON.parse(posted.at(-1)!.body).commands[0].args.publications).toEqual(['p3']);
        expect(harness.saveTimeline).not.toHaveBeenCalled();
      } finally {
        harness?.hook.unmount();
        await vi.waitFor(() => expect(locks.size).toBe(0));
        if (descriptor) Object.defineProperty(navigator, 'locks', descriptor);
        else Reflect.deleteProperty(navigator, 'locks');
      }
    });

  it.each(['accepted', 'merged', 'conflict', 'invalid', 'restart', 'dependent', 'merged dependent', 'late reply', 'strict'] as const)(
    'the production caller uses it: mounted local document %s', async (outcome) => {
      const dependent = outcome === 'dependent' || outcome === 'merged dependent';
      const locks = new Set<string>();
      const descriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
      Object.defineProperty(navigator, 'locks', { configurable: true, value: {
        request: async (name: string, _options: unknown, work: (lock: object | null) => Promise<unknown>) => {
          if (locks.has(name)) return work(null);
          locks.add(name);
          try { return await work({}); } finally { locks.delete(name); }
        },
      } });
      const head = { projectId: 'project-commit', timelineId: 'timeline-1', headRevisionId: 'r0', headPublicationId: 'p0' };
      const config = createDefaultTimelineConfig();
      const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' },
        { timelineId: 'timeline-1' }).data.canonical_document;
      document.parent_revision.payload = { config, clips: [], registry: { assets: {} }, occurrences: [], opaque: { keep: null } };
      document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
      const data = await buildTimelineData(config, { assets: {} }, undefined, 1, undefined, head);
      const initial = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: document };
      const edited = await buildTimelineData({ ...config, output: { ...config.output, file: 'authored.mp4' } }, data.registry,
        undefined, 1, undefined, head);
      const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' },
        { timelineId: 'timeline-1' });
      response.data.canonical_document = structuredClone(document);
      response.data.canonical_document.parent_revision.revision_id = 'r1';
      response.data.canonical_document.parent_revision.payload.config = JSON.parse(JSON.stringify(edited.config));
      response.data.canonical_document.parent_revision.payload.opaque = { keep: null, agent: outcome === 'merged' || outcome === 'merged dependent' };
      if (outcome === 'merged' || outcome === 'merged dependent') Object.assign(response.data, { status: 'merged' });
      const accepted = { response, accepted: { revisionId: 'r1', publicationId: 'p1' },
        canonicalDocument: response.data.canonical_document, graph: {}, receipt: response.receipt };
      const send = vi.fn<DataProvider['commitTimeline'] & object>().mockResolvedValue(accepted);
      let acknowledge!: () => void;
      if (dependent || outcome === 'late reply') {
        send.mockImplementationOnce(() => new Promise((resolve) => { acknowledge = () => resolve(accepted); }));
      }
      if (outcome === 'conflict' || outcome === 'invalid') send.mockRejectedValueOnce(new ApiError(
        outcome === 'conflict' ? 409 : 422, outcome, 'Retain original intent', '', { status: outcome, path: ['output'], hint: 'Read latest' }));
      if (outcome === 'restart') send.mockRejectedValueOnce(new Error('Lost acknowledgement'));
      const original = { data, loadBasis: vi.fn(async () => initial), strict: outcome === 'strict', capabilities: {
        commitTimeline: send, getRecoverableIdentity: vi.fn(async () => ({ actorId: 'actor', realmId: 'realm' })),
      } };
      const harness = setup(async () => { throw new Error('Legacy save must not be called'); }, undefined, original);
      try {
        await vi.waitFor(() => expect(harness.hook.result.current.localSaveState?.ownerId).toBeTruthy());
        await act(async () => { harness.hook.result.current.commitData(edited, { save: true }); });
        if (dependent) {
          const second = await buildTimelineData({ ...edited.config, output: { ...edited.config.output, file: 'dependent.mp4' } },
            data.registry, undefined, 1, undefined, head);
          await act(async () => { harness.hook.result.current.commitData(second, { save: true }); });
          const next = structuredClone(accepted);
          next.accepted = { revisionId: 'r2', publicationId: 'p2' };
          next.canonicalDocument.parent_revision.revision_id = 'r2';
          next.canonicalDocument.parent_revision.payload.config = JSON.parse(JSON.stringify(second.config));
          send.mockImplementationOnce(async (request) => {
            // Observe the mounted assembly at transmission, before B can ACK.
            expect(harness.hook.result.current.dataRef.current?.head?.headRevisionId).toBe('r1');
            expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe('authored.mp4');
            expect(request).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
              commands: [{ args: { changes: [{ before: { state: 'present', value: 'authored.mp4' }, value: 'dependent.mp4' }] } }] });
            return next;
          });
        }
        if (dependent || outcome === 'late reply') {
          await act(async () => { await vi.advanceTimersByTimeAsync(500); });
          await vi.waitFor(() => expect(send).toHaveBeenCalledTimes(1));
          if (outcome === 'late reply') {
            const visible = harness.hook.result.current.dataRef.current;
            harness.hook.unmount();
            await vi.waitFor(() => expect(locks.size).toBe(0));
            await act(async () => { acknowledge(); await Promise.resolve(); });
            expect(harness.hook.result.current.dataRef.current).toBe(visible);
            const [durable] = await createCommitOutbox().list({ realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-1' });
            expect(durable.pending?.request.key).toBe(send.mock.calls[0][1]);
            expect(durable.accepted).toBeUndefined();
            return;
          }
          await act(async () => { acknowledge(); await Promise.resolve(); });
        }
        const flushing = act(async () => {
          if (outcome === 'conflict' || outcome === 'invalid' || outcome === 'restart') {
            await expect(harness.hook.result.current.flushPendingSave()).rejects.toThrow();
          } else await harness.hook.result.current.flushPendingSave();
        });
        await flushing;
        const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-1' };
        const [stored] = await createCommitOutbox().list(scope);
        expect(harness.saveTimeline).not.toHaveBeenCalled();
        expect(send.mock.calls[0][0]).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0',
          label: 'Edit timeline', merge: 'atomic', dry_run: false,
          commands: [{ op: 'doc.patch', args: { changes: [{ op: 'set', ref: 'parent', path: ['config', 'output', 'file'],
            before: { state: 'present', value: config.output.file }, value: 'authored.mp4' }] } }],
          steps: [{ command_ordinals: [0], intent: 'Save local editor changes' }] });
        if (outcome === 'conflict' || outcome === 'invalid') {
          expect(stored.intents).toHaveLength(1);
          expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe(config.output.file);
          expect(harness.hook.result.current.localSaveState?.status).toBe('conflict');
        } else if (outcome === 'restart') {
          const exact = structuredClone(send.mock.calls[0]);
          const pending = structuredClone(stored.pending?.request);
          harness.hook.unmount();
          await vi.waitFor(() => expect(locks.size).toBe(0));
          const recovered = setup(async () => { throw new Error('Legacy save must not be called'); }, undefined, original);
          try {
            await vi.waitFor(() => expect(recovered.hook.result.current.localSaveState?.status).toBe('saved'));
            expect(send.mock.calls[1]).toEqual(exact);
            expect(JSON.stringify(send.mock.calls[1][0])).toBe(pending?.body);
            expect(recovered.hook.result.current.dataRef.current?.head?.headRevisionId).toBe('r1');
          } finally { recovered.hook.unmount(); }
        } else {
          expect(stored.intents).toHaveLength(0);
          expect(stored.accepted?.value).toMatchObject({ canonicalDocument: dependent
            ? { parent_revision: { revision_id: 'r2' } } : accepted.canonicalDocument });
          expect(harness.hook.result.current.dataRef.current?.head?.headRevisionId).toBe(dependent ? 'r2' : 'r1');
          expect(harness.hook.result.current.dataRef.current?.config.output.file).toBe(dependent ? 'dependent.mp4' : 'authored.mp4');
          if (dependent) {
            expect(send.mock.calls[1][0]).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
              commands: [{ args: { changes: [{ before: { state: 'present', value: 'authored.mp4' }, value: 'dependent.mp4' }] } }] });
          }
        }
      } finally {
        harness.hook.unmount();
        await vi.waitFor(() => expect(locks.size).toBe(0));
        if (descriptor) Object.defineProperty(navigator, 'locks', descriptor);
        else Reflect.deleteProperty(navigator, 'locks');
      }
    });

  it.each(['original', 'head moved', 'edited during read'])('stages the original verified closure in the real mounted hook (%s)', async (kind) => {
    const head = { projectId: 'project-commit', timelineId: 'timeline-1', headRevisionId: 'r0', headPublicationId: 'p0' };
    const config = createDefaultTimelineConfig();
    const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' },
      { timelineId: 'timeline-1' }).data.canonical_document;
    document.parent_revision.payload = { config, clips: [], registry: { assets: {} }, occurrences: [], opaque: { keep: null } };
    document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
    const data = await buildTimelineData(config, { assets: {} }, undefined, 1, undefined, head);
    const basis = { head: { revisionId: kind === 'head moved' ? 'newer-r' : 'r0', publicationId: kind === 'head moved' ? 'newer-p' : 'p0' }, canonicalDocument: document };
    let finishRead!: (value: typeof basis) => void;
    const loadBasis = vi.fn(() => kind === 'edited during read'
      ? new Promise<typeof basis>((resolve) => { finishRead = resolve; }) : Promise.resolve(basis));
    const harness = setup(async () => 2, undefined, { data, loadBasis });
    await settleInitialRecoveryCheck();
    if (kind === 'edited during read') {
      const edited = await buildTimelineData({ ...config, clips: [{ id: 'new', track: 'V1', at: 0, hold: 1 }] },
        { assets: {} }, undefined, 1, undefined, head);
      act(() => harness.hook.result.current.commitData(edited));
      await act(async () => { finishRead(basis); });
      expect(harness.hook.result.current.originalLocalSaveBasis).toMatchObject({ status: 'unavailable', reason: expect.stringContaining('Local edits preceded completion') });
      expect(harness.hook.result.current.dataRef.current?.config).toEqual(edited.config);
    } else if (kind === 'head moved') {
      expect(harness.hook.result.current.originalLocalSaveBasis).toMatchObject({ status: 'unavailable', reason: expect.stringContaining('original verified authoring head') });
    } else {
      expect(harness.hook.result.current.originalLocalSaveBasis).toMatchObject({ status: 'ready', value: {
        initial: basis, source: { config: data.config, head },
        authoringBundle: { source_mapping: { _runtime_document: document } },
      } });
    }
    expect(loadBasis).toHaveBeenCalledExactlyOnceWith('timeline-1');
    expect(harness.saveTimeline).not.toHaveBeenCalled();
    if (kind === 'edited during read') {
      // Finish this test's actual pending draft/save before the next mount.
      await act(async () => { await harness.hook.result.current.flushPendingSave(); });
    }
    harness.hook.unmount();
  });

  it('passes the exact owned registration target through the existing durable save pipeline', async () => {
    let acknowledge!: (version: number) => void;
    const harness = setup(() => new Promise<number>((resolve) => { acknowledge = resolve; }));
    act(() => harness.hook.result.current.commitData(makeTimelineData('baseline'), { save: false }));
    await settleInitialRecoveryCheck();
    let receipt!: ReturnType<typeof harness.hook.result.current.registrationOwner.patchRegistryOwned>;
    let target!: ReturnType<typeof harness.hook.result.current.registrationOwner.captureSaveTarget>;
    let barrier!: Promise<number>;
    let settled = false;
    await act(async () => {
      const owner = harness.hook.result.current.registrationOwner;
      receipt = owner.patchRegistryOwned('asset-registered', { file: 'registered.png' });
      target = owner.captureSaveTarget(receipt.editSeq);
      barrier = owner.flushSaveTarget(target).then((version) => { settled = true; return version; });
    });
    expect(settled).toBe(false);
    expect(harness.saveTimeline).toHaveBeenCalledTimes(1);
    expect(harness.saveTimeline.mock.calls[0][3]?.assets['asset-registered'].file).toBe('registered.png');
    await act(async () => { acknowledge(2); await barrier; });
    expect(settled).toBe(true);
    expect(harness.hook.result.current.registrationOwner.rollbackRegistration(receipt, target, new Error('late unknown'))).toBe(false);
    harness.hook.unmount();
  });

  it('rolls back a proven no-write registry mutation and never sends its old queued payload', async () => {
    const cause = new TimelineVersionConflictError('CAS denied');
    const harness = setup(async () => { throw cause; });
    act(() => harness.hook.result.current.commitData(makeTimelineData('baseline'), { save: false }));
    await settleInitialRecoveryCheck();
    let receipt!: ReturnType<typeof harness.hook.result.current.registrationOwner.patchRegistryOwned>;
    let target!: ReturnType<typeof harness.hook.result.current.registrationOwner.captureSaveTarget>;
    let failure: unknown;
    await act(async () => {
      const owner = harness.hook.result.current.registrationOwner;
      receipt = owner.patchRegistryOwned('asset-registered', { file: 'registered.png' });
      target = owner.captureSaveTarget(receipt.editSeq);
      failure = await owner.flushSaveTarget(target).catch((error) => error);
    });
    expect(failure).toMatchObject({ target, certainty: 'definitely-uncommitted' });
    act(() => { expect(harness.hook.result.current.registrationOwner.rollbackRegistration(receipt, target, failure)).toBe(true); });
    expect(harness.hook.result.current.dataRef.current?.registry.assets['asset-registered']).toBeUndefined();
    await act(async () => { vi.advanceTimersByTime(2000); });
    expect(harness.saveTimeline).toHaveBeenCalledTimes(1);
    await flush();
    const draft = await loadTimelineDraft('timeline-1');
    expect((draft?.draft.registry as TimelineData['registry'] | undefined)?.assets['asset-registered']).toBeUndefined();
    harness.hook.unmount();
  });

  it('silently clears a recovery slot that already matches the loaded server snapshot', async () => {
    const harness = setup(async () => 2);
    const server = makeTimelineData('already-saved');
    await saveTimelineDraft(
      'timeline-1',
      { config: server.config, registry: server.registry },
      server.configVersion,
    );

    act(() => {
      harness.hook.result.current.commitData(server, { save: false });
    });
    await flush();
    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    expect(harness.hook.result.current.recoveryDraft).toBeNull();
    expect(await loadTimelineDraft('timeline-1')).toBeNull();
    harness.hook.unmount();
  });

  it('does not offer a draft created by an edit after the one-time recovery check began', async () => {
    const harness = setup(async () => 2);
    const baseline = makeTimelineData('baseline-before-edit');
    act(() => {
      harness.hook.result.current.commitData(baseline, { save: false });
    });
    await flush();
    expect(harness.hook.result.current.recoveryDraft).toBeNull();

    const edited = makeTimelineData('current-session-edit');
    act(() => {
      harness.hook.result.current.commitData(edited);
    });
    await flush();
    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    expect(await loadTimelineDraft('timeline-1')).not.toBeNull();
    expect(harness.hook.result.current.recoveryDraft).toBeNull();
    harness.hook.unmount();
  });

  it('uses the draft baseVersion for CAS and clears only after a successful ACK', async () => {
    const harness = setup(async () => 8);
    const recovered = makeTimelineData('recovered');
    await saveTimelineDraft('timeline-1', { config: recovered.config, registry: recovered.registry }, 7);
    act(() => {
      harness.hook.result.current.commitData(makeTimelineData('server'), { save: false });
    });
    await flush();

    await act(async () => {
      await harness.hook.result.current.retryRecoveredDraft();
    });
    await act(async () => {
      vi.advanceTimersByTime(600);
      await flush();
    });

    expect(harness.saveTimeline).toHaveBeenCalledTimes(1);
    expect(harness.saveTimeline.mock.calls[0]?.[0]).toBe('timeline-1');
    expect(harness.saveTimeline.mock.calls[0]?.[1].output.file).toBe('output-recovered.mp4');
    expect(harness.saveTimeline.mock.calls[0]?.[2]).toBe(7);
    expect(await loadTimelineDraft('timeline-1')).toBeNull();
    harness.hook.unmount();
  });

  it('does not retry a recovered draft while whole-timeline editing is denied', async () => {
    const harness = setup(async () => 8, {
      checkTimeline: () => ({ allowed: false, reason: 'timeline_read_only' }),
    });
    const recovered = makeTimelineData('blocked-recovery');
    await saveTimelineDraft('timeline-1', { config: recovered.config, registry: recovered.registry }, 7);
    act(() => {
      harness.hook.result.current.commitData(makeTimelineData('server'), { save: false });
    });
    await flush();

    await act(async () => {
      await harness.hook.result.current.retryRecoveredDraft();
    });
    await act(async () => {
      vi.advanceTimersByTime(600);
      await flush();
    });

    expect(harness.saveTimeline).not.toHaveBeenCalled();
    expect(harness.hook.result.current.data?.config.output.file).toBe('output-server.mp4');
    expect(await loadTimelineDraft('timeline-1')).not.toBeNull();
    harness.hook.unmount();
  });

  it.each([
    ['409', async () => { throw new TimelineVersionConflictError(); }],
    ['transport failure', async () => { throw new Error('bridge unavailable'); }],
  ])('retains the recovered draft after a %s', async (_label, saveImpl) => {
    const harness = setup(saveImpl);
    const recovered = makeTimelineData('failed-recovery');
    await saveTimelineDraft('timeline-1', { config: recovered.config, registry: recovered.registry }, 7);
    act(() => {
      harness.hook.result.current.commitData(makeTimelineData('server'), { save: false });
    });
    await flush();

    await act(async () => {
      await harness.hook.result.current.retryRecoveredDraft();
    });
    await act(async () => {
      vi.advanceTimersByTime(600);
      await flush();
    });

    expect(harness.saveTimeline).toHaveBeenCalledTimes(1);
    expect(harness.saveTimeline.mock.calls[0]?.[0]).toBe('timeline-1');
    expect(harness.saveTimeline.mock.calls[0]?.[1].output.file).toBe('output-failed-recovery.mp4');
    expect(harness.saveTimeline.mock.calls[0]?.[2]).toBe(7);
    expect(await loadTimelineDraft('timeline-1')).not.toBeNull();
    harness.hook.unmount();
  });
});
