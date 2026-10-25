// @vitest-environment jsdom
import React from 'react';
import { act, fireEvent, render, renderHook, screen, within } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { json, runtimeFixture } from '@/test/fakeWorkspaceRuntime.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import type { DataProvider } from '../data/DataProvider.ts';
import { loadTimelineDraft } from '../data/timelineDraftIndexedDb.ts';
import { createCommitOutbox } from '../commands/commitOutbox.ts';
import { createInteractionState } from '../lib/interaction-state.ts';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { createTimelineStore, TimelineStoreProvider } from './timelineStore.ts';
import { useClipEditing } from './useClipEditing.ts';
import { useTimelineSave } from './useTimelineSave.ts';
import { AgentChatProvider, useAgentChatBridge } from '@/shared/contexts/AgentChatContext';
import { systemResetSelectionForProjectChange } from '@/shared/state/selectionStore';
import { VideoEditorProvider } from '../contexts/VideoEditorProvider';
import { ElementsLibraryPanel } from '../components/ElementsLibraryPanel';
import { useTimelineEditorData, useTimelineEditorOps } from './timelineStore';
import type { AstridElementOperationAdapter } from '../runtime/element-adapter';

vi.mock('../compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));

it('sends a mounted split through the durable outbox with the current generated contract', async () => {
  // Keep generated metadata real: a stale capability allowlist must fail before transport.
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  const locks = Object.getOwnPropertyDescriptor(navigator, 'locks');
  Object.defineProperty(navigator, 'locks', { configurable: true, value: {
    request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
  } });
  const scope = { projectId: 'project-commit', timelineId: 'timeline-current-contract', realmId: 'realm', actorId: 'actor' };
  const head = { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: 'r0', headPublicationId: 'p0' };
  const config = createDefaultTimelineConfig();
  config.clips = [{ id: 'source', at: 0, track: 'V1', clipType: 'media', asset: 'video', from: 0, to: 8, speed: 1, hold: 8,
    app: { astrid: { for: 8 }, 'org.example': { clear: null } } }];
  const registry = { assets: { video: { file: 'video.webm', type: 'video/webm', duration: 8 } } };
  const original = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' }, scope);
  original.data.canonical_document.parent_revision.payload = { config, registry, clips: config.clips, occurrences: [] };
  original.data.canonical_document.parent_revision.content_digest = fixtureDigest(original.data.canonical_document.parent_revision.payload);
  const data = await buildTimelineData(config, registry, undefined, 1, undefined, head);
  const fixture = runtimeFixture();
  const transmit = vi.fn<Transport>(async (method, path, headers, body) => {
    if (method !== 'POST' || !path.endsWith('/commit')) return fixture.transport(method, path, headers, body);
    const raw = new TextDecoder().decode(body instanceof Blob ? await body.arrayBuffer() : body);
    const request = JSON.parse(raw);
    const [durable] = await createCommitOutbox().list(scope);
    expect(durable.pending?.request).toMatchObject({ body: raw, key: headers['Idempotency-Key'] });
    const reply = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' },
      { ...scope, commands: request.commands });
    reply.data.canonical_document = structuredClone(original.data.canonical_document);
    reply.data.canonical_document.parent_revision.revision_id = 'r1';
    const local = JSON.parse(JSON.stringify(save.result.current.dataRef.current!.config));
    reply.data.canonical_document.parent_revision.payload.config = local;
    reply.data.canonical_document.parent_revision.payload.clips = local.clips;
    reply.data.canonical_document.parent_revision.content_digest = fixtureDigest(reply.data.canonical_document.parent_revision.payload);
    reply.data.document_digest = fixtureDigest(reply.data.canonical_document);
    Object.assign(reply.data, { label: request.label, steps: request.steps, merge_mode: request.merge });
    reply.receipt.idempotency_key = headers['Idempotency-Key'];
    return { status: 200, headers: {}, body: json(reply) };
  });
  const runtime = new RuntimeDataProvider({ projectId: scope.projectId, transport: transmit });
  const legacySave = vi.fn(async () => { throw new Error('No legacy save'); });
  const provider: DataProvider = {
    persistenceEnabled: true, loadTimeline: async () => ({ config, configVersion: 1 }),
    loadAssetRegistry: async () => registry, resolveAssetUrl: async file => file, saveTimeline: legacySave,
    loadTimelineCommandBasis: async () => ({ head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: original.data.canonical_document }),
    getRecoverableIdentity: async () => ({ realmId: scope.realmId, actorId: scope.actorId }),
    commitTimeline: (request, key) => runtime.commitTimeline(request, key),
  };
  const store = createTimelineStore();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const context = { provider, timelineId: scope.timelineId, project: { projectId: scope.projectId },
    shots: {}, toast: { error: vi.fn() } } as unknown as VideoEditorRuntimeContextValue;
  const interaction = { current: createInteractionState() };
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <VideoEditorRuntimeProvider value={context}>
        <TimelineStoreProvider store={store}>{children}</TimelineStoreProvider>
      </VideoEditorRuntimeProvider>
    </QueryClientProvider>
  );
  const save = renderHook(() => useTimelineSave({ timelineQuery: { data: undefined, isLoading: false },
    assetRegistryQuery: { data: undefined } }, provider, interaction, store, data), { wrapper });
  const editing = renderHook(() => useClipEditing({ dataRef: save.result.current.dataRef,
    resolvedConfig: save.result.current.dataRef.current?.resolvedConfig ?? null,
    selectedClipId: null, selectedTrack: null, currentTime: 2,
    selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit: save.result.current.applyEdit }));
  try {
    await vi.waitFor(() => expect(save.result.current.localSaveState?.ownerId).toBeTruthy());
    await act(async () => { await loadTimelineDraft(scope.timelineId); });
    await act(async () => { editing.result.current.handleSplitClipAtTime('source', 2); });
    expect(save.result.current.dataRef.current?.config.clips).toHaveLength(2);
    await act(async () => { await save.result.current.flushPendingSave(); });
    const posts = transmit.mock.calls.filter(([method, path]) => method === 'POST' && path.endsWith('/commit'));
    expect(posts).toHaveLength(1);
    const body = posts[0][3];
    const request = JSON.parse(new TextDecoder().decode(body instanceof Blob ? await body.arrayBuffer() : body));
    expect(request).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0', merge: 'fields', dry_run: false,
      commands: [{ op: 'doc.patch', args: { changes: expect.arrayContaining([expect.objectContaining({ op: 'list.insert' })]) } }],
      steps: [{ command_ordinals: [0], patch: expect.any(Array) }], reads: expect.any(Array) });
    expect(save.result.current.localSaveState?.status).toBe('saved');
    expect(save.result.current.dataRef.current?.head?.headPublicationId).toBe('p1');
    expect((await createCommitOutbox().list(scope))[0].intents).toEqual([]);
    expect(legacySave).not.toHaveBeenCalled();
  } finally {
    editing.unmount();
    save.unmount();
    queryClient.clear();
    if (locks) Object.defineProperty(navigator, 'locks', locks);
    else Reflect.deleteProperty(navigator, 'locks');
    vi.unstubAllGlobals();
  }
});

it.each(['accepted', 'merged', 'refused', 'panel reopened', 'editor restarted'] as const)(
  'propagates the element outcome through the actual mounted caller: %s', async outcome => {
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
    systemResetSelectionForProjectChange();
    const locks = Object.getOwnPropertyDescriptor(navigator, 'locks');
    const heldLocks = new Set<string>();
    Object.defineProperty(navigator, 'locks', { configurable: true, value: {
      request: async (name: string, _options: unknown, work: (lock: object | null) => Promise<unknown>) => {
        if (heldLocks.has(name)) return work(null);
        heldLocks.add(name);
        try { return await work({}); } finally { heldLocks.delete(name); }
      },
    } });
    const scope = { projectId: 'project-commit', timelineId: 'timeline-element-outcome', realmId: 'realm', actorId: 'actor' };
    const head = { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: 'r0', headPublicationId: 'p0' };
    const config = createDefaultTimelineConfig();
    config.clips = [{ id: 'source', at: 0, track: 'V1', hold: 2 }];
    const registry = { assets: {} };
    const seed = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' }, scope);
    const original = seed.data.canonical_document;
    original.parent_revision.payload = { config, registry, clips: structuredClone(config.clips), occurrences: [], opaque: { keep: null } };
    original.parent_revision.content_digest = fixtureDigest(original.parent_revision.payload);
    const data = await buildTimelineData(config, registry, undefined, 1, undefined, head);
    const initial = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: original };
    let latest = initial;
    let release!: (response: Awaited<ReturnType<Transport>>) => void;
    const fixture = runtimeFixture();
    const transmit = vi.fn<Transport>(async (method, path, headers, body) => {
      if (method !== 'POST' || !path.endsWith('/commit')) return fixture.transport(method, path, headers, body);
      return new Promise(resolve => { release = resolve; });
    });
    const posts = () => transmit.mock.calls.filter(([method, path]) => method === 'POST' && path.endsWith('/commit'));
    const runtime = new RuntimeDataProvider({ projectId: scope.projectId, transport: transmit });
    const legacy = vi.fn(async () => { throw new Error('Legacy save route used'); });
    const provider: DataProvider = {
      persistenceEnabled: true, loadTimeline: async () => ({ config, configVersion: 1, head }),
      loadAssetRegistry: async () => registry, resolveAssetUrl: async file => file, saveTimeline: legacy,
      loadTimelineCommandBasis: async () => latest,
      getRecoverableIdentity: async () => ({ realmId: scope.realmId, actorId: scope.actorId }),
      commitTimeline: (request, key) => runtime.commitTimeline(request, key),
    };
    let editor!: ReturnType<typeof useTimelineEditorData>;
    let ops!: ReturnType<typeof useTimelineEditorOps>;
    let chat!: ReturnType<typeof useAgentChatBridge>;
    let showPanel!: (open: boolean) => void;
    let panelMounts = 0;
    function Panel() {
      React.useEffect(() => { panelMounts++; }, []);
      return <ElementsLibraryPanel open onOpenChange={showPanel} onOpenCreationPrompt={() => {}} />;
    }
    function Caller() {
      editor = useTimelineEditorData();
      ops = useTimelineEditorOps();
      chat = useAgentChatBridge();
      const [open, setOpen] = React.useState(true);
      showPanel = setOpen;
      return open ? <Panel /> : null;
    }
    const clients: QueryClient[] = [];
    const mount = () => {
      const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
      clients.push(client);
      return render(<MemoryRouter><QueryClientProvider client={client}><AgentChatProvider>
        <VideoEditorProvider dataProvider={provider} projectId={scope.projectId} projectSlug={scope.projectId}
          timelineId={scope.timelineId} userId={null} initialTimelineData={data}><Caller /></VideoEditorProvider>
      </AgentChatProvider></QueryClientProvider></MemoryRouter>);
    };
    let view = mount();
    try {
      await vi.waitFor(() => expect(chat.editorContext?.elementOperationAdapter).toBeDefined());
      await act(async () => { ops.selectClip('source'); });
      await vi.waitFor(() => expect(chat.editorContext?.elementContext?.selectedClips[0]?.id).toBe('source'));
      await vi.waitFor(async () => expect(await createCommitOutbox().list(scope)).toHaveLength(1));
      const adapter = chat.editorContext!.elementOperationAdapter!;
      const originalCapture = adapter.captureForTurn.bind(adapter);
      let captured!: AstridElementOperationAdapter;
      let execute!: ReturnType<typeof vi.spyOn<AstridElementOperationAdapter, 'execute'>>;
      const capture = vi.spyOn(adapter, 'captureForTurn').mockImplementation(() => {
        captured = originalCapture();
        execute = vi.spyOn(captured, 'execute');
        return captured;
      });
      fireEvent.change(screen.getByPlaceholderText('Search elements'), { target: { value: 'am-burst' } });
      const apply = screen.getByRole('button', { name: 'Apply' });
      const dialog = screen.getByRole('dialog');
      fireEvent.click(apply);
      await vi.waitFor(() => expect(posts()).toHaveLength(1));
      expect(capture).toHaveBeenCalledOnce();
      expect(execute).toHaveBeenCalledOnce();
      const execution = execute.mock.results[0].value;
      // Attach both branches immediately; a refusal must reject this same promise.
      const settled = vi.fn();
      void execution.then(() => settled('resolved'), () => settled('rejected'));
      expect(within(dialog).queryByRole('status')).toBeNull();
      expect(apply).toHaveTextContent('Applying');
      expect(apply).toBeDisabled();
      expect(settled).not.toHaveBeenCalled();
      expect(panelMounts).toBe(1);
      const preview = structuredClone(editor.data!.config);
      expect(preview.clips).toHaveLength(2);
      const [pending] = await createCommitOutbox().list(scope);
      const body = posts()[0][3];
      const raw = new TextDecoder().decode(body instanceof Blob ? await body.arrayBuffer() : body);
      const key = posts()[0][2]['Idempotency-Key'];
      const request = JSON.parse(raw);
      expect(pending.pending?.request).toMatchObject({ body: raw, key });
      expect(request).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0', merge: 'atomic', dry_run: false,
        commands: [{ op: 'doc.patch' }], steps: [{ intent: 'timeline.apply_element', command_ordinals: [0] }] });
      // A context/selection rerender must keep this dialog and captured invocation alive.
      await act(async () => { ops.selectClip(preview.clips[1].id); });
      expect(screen.getByRole('dialog')).toBe(dialog);
      expect(panelMounts).toBe(1);
      expect(settled).not.toHaveBeenCalled();
      if (outcome === 'panel reopened') {
        act(() => { showPanel(false); });
        expect(screen.queryByRole('dialog')).toBeNull();
        act(() => { showPanel(true); });
        expect(panelMounts).toBe(2);
      }
      if (outcome === 'editor restarted') {
        view.unmount();
        release({ status: 503, headers: {}, body: json({ code: 'unavailable', message: 'Acknowledgement lost' }) });
        await vi.waitFor(() => expect(settled).toHaveBeenCalledWith('rejected'));
        view = mount();
        await vi.waitFor(() => expect(posts()).toHaveLength(2));
        expect(posts()[1][2]['Idempotency-Key']).toBe(key);
        expect(posts()[1][3]).toEqual(body);
      }
      const reply = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' },
        { ...scope, commands: request.commands });
      const canonical = structuredClone(original);
      canonical.parent_revision.revision_id = 'r1';
      if (outcome === 'merged') preview.output = { ...preview.output, file: 'remote-merged.mp4' };
      canonical.parent_revision.payload = { ...canonical.parent_revision.payload, config: preview, clips: structuredClone(preview.clips) };
      canonical.parent_revision.content_digest = fixtureDigest(canonical.parent_revision.payload);
      reply.data.canonical_document = canonical;
      reply.data.document_digest = fixtureDigest(canonical);
      Object.assign(reply.data, { status: outcome === 'merged' ? 'merged' : 'accepted', label: request.label,
        steps: request.steps, merge_mode: request.merge });
      reply.receipt.idempotency_key = key;
      if (outcome !== 'refused') latest = { head: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: canonical };
      await act(async () => {
        release(outcome === 'refused'
          ? { status: 409, headers: {}, body: json({ code: 'conflict', message: 'Element changed',
            details: { status: 'conflict', reason: 'field_changed', head: initial.head } }) }
          : { status: 200, headers: {}, body: json(reply) });
      });
      if (outcome === 'refused') {
        await vi.waitFor(() => expect(settled).toHaveBeenCalledWith('rejected'));
        expect(screen.getByRole('status')).toHaveTextContent('unacknowledged');
        expect(screen.getByRole('status')).not.toHaveTextContent('applied');
        expect(editor.data?.config.clips).toEqual(data.config.clips);
        const [retained] = await createCommitOutbox().list(scope);
        expect(retained.intents).toHaveLength(1);
        expect(retained.pending?.outcome?.kind).toBe('rejected');
      } else {
        await vi.waitFor(() => expect(editor.data?.head?.headRevisionId).toBe('r1'));
        await vi.waitFor(async () => expect((await createCommitOutbox().list(scope))[0].intents).toEqual([]));
        expect(editor.data?.config).toEqual(preview);
        const [accepted] = await createCommitOutbox().list(scope);
        expect(accepted.accepted?.value).toMatchObject({ canonicalDocument: JSON.parse(JSON.stringify(canonical)) });
        if (outcome === 'accepted' || outcome === 'merged') {
          await vi.waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('applied'));
          expect(settled).toHaveBeenCalledWith('resolved');
          expect(screen.getByRole('dialog')).toBe(dialog);
          expect(panelMounts).toBe(1);
          expect(apply).toBeEnabled();
        } else {
          // A replacement panel has fresh local status, while the durable ACK survives.
          expect(screen.queryByRole('status')).toBeNull();
          expect(panelMounts).toBe(2);
        }
      }
      expect(legacy).not.toHaveBeenCalled();
    } finally {
      view.unmount();
      clients.forEach(client => client.clear());
      vi.restoreAllMocks();
      if (locks) Object.defineProperty(navigator, 'locks', locks);
      else Reflect.deleteProperty(navigator, 'locks');
      vi.unstubAllGlobals();
    }
  });
