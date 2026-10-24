// Offline A2/P2 causal control at c0fe88994405fd517b58473c14678a0d1b73056d.
// Requires the retained D45/13583 trace, Node 20, and the normal mounted Vitest aliases.
// No server, HTTP, acceptance fixture, injected gesture basis, or product edits.
import React from 'react';
import { readFileSync } from 'node:fs';
import { act, fireEvent, renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { RuntimeDataProvider } from './src/integrations/runtime/dataProvider.ts';
import { json, runtimeFixture } from './src/test/fakeWorkspaceRuntime.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from './src/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from './src/tools/video-editor/hooks/timelineStore.ts';
import { useTimelineSave } from './src/tools/video-editor/hooks/useTimelineSave.ts';
import { useTimelineTrackManagement } from './src/tools/video-editor/hooks/useTimelineTrackManagement.ts';
import { useDragCoordinator } from './src/tools/video-editor/hooks/useDragCoordinator.ts';
import { useClipDrag } from './src/tools/video-editor/hooks/useClipDrag.ts';
import { createInteractionState } from './src/tools/video-editor/lib/interaction-state.ts';
import { buildTimelineData } from './src/tools/video-editor/lib/timeline-data.ts';
import { buildTimelineRowLayout } from './src/tools/video-editor/lib/timeline-row-layout.ts';
import { publishTimelineRowLayout } from './src/tools/video-editor/lib/drop-position.ts';
import { loadTimelineDraft } from './src/tools/video-editor/data/timelineDraftIndexedDb.ts';
import { createCommitOutbox } from './src/tools/video-editor/commands/commitOutbox.ts';
import type { CommitRequest } from './src/integrations/runtime/timeline-commit-types.ts';

// The renderer's cache invalidator is unrelated to owner/capture; jsdom has no renderer.
vi.mock('./src/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));

// A2_FIXTURE is private JSON prepared from resources/<sha1>.json in D45/13583's
// parent trace.zip. Verify each resource's SHA-1, then assemble these six keys:
// parent=d9a136733945bf0bd8ad622379e6e093f01358ab
// shot=5bb6bed55e89f700da3d641ad8ce8e572713fefe
// internal=3963b500da676e9b328546d93883ab0d7a3e1cb1
// history=4fb745fbe558c85ad8b1472f4f2d523423408f24
// inspection=558234f80972c964fd4a932fe9bf3b75920d2f07
// timeline=ff8e7a23654008f673056ff24a45292cee86a233
// No headers, raw wire logs, credentials, or environment are copied or printed.
const fixture = JSON.parse(readFileSync(process.env.A2_FIXTURE!, 'utf8'));
const projectId = fixture.parent.project_id;
const timelineId = fixture.parent.timeline_id;
const head = { projectId, timelineId, headRevisionId: fixture.history.head.revision_id,
  headPublicationId: fixture.history.head.publication_id };
const queries = { timelineQuery: { data: undefined, isLoading: false }, assetRegistryQuery: { data: undefined } };
const drain = async () => { await act(async () => { for (let i = 0; i < 50; i++) await Promise.resolve(); }); };
const advance = async (ms: number) => { await act(async () => { await vi.advanceTimersByTimeAsync(ms); }); await drain(); };
function changedPaths(before: unknown, after: unknown, path = ''): string[] {
  if (JSON.stringify(before) === JSON.stringify(after)) return [];
  if (before && after && typeof before === 'object' && typeof after === 'object') {
    return [...new Set([...Object.keys(before), ...Object.keys(after)])].flatMap(key => changedPaths(before[key], after[key], `${path}/${key}`));
  }
  return [path];
}
function gate() {
  let resolve!: () => void;
  const promise = new Promise<void>(done => { resolve = done; });
  return { promise, resolve };
}
function rect(left: number, top: number, width: number, height: number): DOMRect {
  return { x: left, y: top, left, top, right: left + width, bottom: top + height, width, height, toJSON: () => ({}) };
}

afterEach(() => { vi.clearAllTimers(); vi.useRealTimers(); vi.unstubAllGlobals(); });

it.each(['ready', 'pending-original-read', 'pending-identity'] as const)(
  'original 0→5 mounted pointer/save boundary: %s', async mode => {
    vi.useFakeTimers();
    resetFakeIndexedDB();
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
    Object.defineProperty(navigator, 'locks', { configurable: true, value: {
      request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
    } });
    const diagnostics: Array<Record<string, unknown>> = [];
    const observe = (event: Event) => diagnostics.push((event as CustomEvent).detail);
    Object.assign(window, { __timelineSaveDiagnosticsEnabled: true });
    window.addEventListener('timeline:save-diagnostic', observe);
    const originalRead = gate();
    const identity = gate();
    const fixtureRuntime = runtimeFixture({ projectId, timelineId });
    const sends: Array<{ request: CommitRequest; key: string }> = [];
    // Every transport call is in-memory. A dispatched mutation stays pending: no fake ACK.
    const provider = new RuntimeDataProvider({ projectId, transport: async (method, path, headers, body) => {
      if (method === 'POST' && path.endsWith('/commit')) {
        sends.push({ request: JSON.parse(new TextDecoder().decode(body)), key: headers['Idempotency-Key'] });
        return new Promise(() => {});
      }
      let value;
      if (path.includes('/commits?')) { if (mode === 'pending-original-read') await originalRead.promise; value = fixture.history; }
      else if (path.includes('/composition-revisions/')) value = fixture.parent;
      else if (path.includes('/shots/') && path.includes('/revisions/')) value = fixture.shot;
      else if (path.includes('/revisions/')) value = fixture.internal;
      else if (path.endsWith('/inspect')) value = fixture.inspection;
      else if (path.endsWith(`/timelines/${timelineId}`)) value = fixture.timeline;
      if (value) return { status: 200, headers: {}, body: json(value) };
      return fixtureRuntime.transport(method, path, headers, body);
    } });
    // Explicit offline identity-read gate; the actual provider identity implementation still runs.
    const readIdentity = provider.getRecoverableIdentity.bind(provider);
    if (mode === 'pending-identity') provider.getRecoverableIdentity = async () => { await identity.promise; return readIdentity(); };
    const loaded = await provider.loadTimeline(timelineId);
    const registry = await provider.loadAssetRegistry(timelineId);
    const data = await buildTimelineData(loaded.config, registry,
      async file => file, loaded.configVersion, undefined, loaded.head);
    expect(data.config.clips.find(clip => clip.id === 'f2-app-clip')?.at).toBe(0);
    expect(data.config.clips.find(clip => clip.id === 'f2-transition-clip')?.at).toBe(15);
    expect(fixture.parent.payload.occurrences).toHaveLength(1);
    const store = createTimelineStore();
    const interaction = { current: createInteractionState() };
    const selected = { current: new Set(['f2-app-clip']) };
    const wrapperNode = document.createElement('div');
    wrapperNode.className = 'timeline-wrapper';
    wrapperNode.getBoundingClientRect = () => rect(0, 0, 1000, 200);
    const editArea = document.createElement('div');
    editArea.className = 'timeline-canvas-edit-area';
    editArea.dataset.timelineRowLayout = 'managed';
    editArea.getBoundingClientRect = () => rect(0, 0, 1000, 200);
    const clipNode = document.createElement('div');
    clipNode.className = 'clip-action';
    clipNode.dataset.clipId = 'f2-app-clip';
    clipNode.dataset.rowId = 'V1';
    clipNode.getBoundingClientRect = () => rect(144, 0, 96, 36);
    editArea.appendChild(clipNode); wrapperNode.appendChild(editArea); document.body.appendChild(wrapperNode);
    const wrapperRef = { current: wrapperNode };
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const runtime = { provider, timelineId, project: { projectId }, assetResolver: null,
      shots: { shots: undefined, isLoading: false, error: null, refetchShots: async () => {} },
    } as unknown as VideoEditorRuntimeContextValue;
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}><VideoEditorRuntimeProvider value={runtime}>
        <TimelineStoreProvider store={store}>{children}</TimelineStoreProvider>
      </VideoEditorRuntimeProvider></QueryClientProvider>
    );
    const hook = renderHook(() => {
      const save = useTimelineSave(queries, provider, interaction, store, data);
      const management = useTimelineTrackManagement({ dataRef: save.dataRef, resolvedConfig: save.data?.resolvedConfig ?? null,
        selectedClipId: save.selectedClipId, setSelectedTrackId: save.setSelectedTrackId, applyEdit: save.applyEdit });
      const drag = useDragCoordinator({ dataRef: save.dataRef, scale: 5, scaleWidth: 160, startLeft: 144, rowHeight: 36 });
      React.useLayoutEffect(() => {
        drag.editAreaRef.current = editArea;
        const state = store.getState();
        state.syncSlices({ data: { ...state.data, data: save.data, dataRef: save.dataRef, interactionStateRef: interaction,
          selectedClipIdsRef: selected, additiveSelectionRef: { current: false }, timelineWrapperRef: wrapperRef,
          deviceClass: 'desktop', interactionMode: 'select', gestureOwner: 'none', coordinator: drag.coordinator, scale: 5, scaleWidth: 160 },
          ops: { ...state.ops, ...management, applyEdit: save.applyEdit,
            setGestureOwner: () => {}, setInputModalityFromPointerType: () => 'mouse', selectClip: () => {}, selectClips: () => {} } });
        return publishTimelineRowLayout(editArea, buildTimelineRowLayout({ tracks: save.data!.tracks, mediaRowHeight: 36 }), save.dataRef.current);
      }, [save.data, management, drag.coordinator]);
      return save;
    }, { wrapper });
    const pointer = renderHook(() => useClipDrag(), { wrapper });
    // Default spy is call-through: observe authentic capture promises without replacing the seam.
    const captures = vi.spyOn(hook.result.current.localDocumentSave!, 'capture');
    const schedules: Array<{ gesture: string | undefined; changed: string[] }> = [];
    const unsubscribe = hook.result.current.eventBus.on('scheduleSave', (next, options) => {
      schedules.push({ gesture: options?.gestureBasis?.kind, changed: changedPaths(data.config, next.config) });
    });
    try {
      // Settle the genuine initial draft read before selecting the owner/read timing.
      await act(async () => { await loadTimelineDraft(timelineId); }); await drain();
      if (mode === 'ready') {
        await advance(100);
        expect(diagnostics.some(row => row.phase === 'handoff-ready')).toBe(true);
      } else if (mode === 'pending-identity') {
        expect(diagnostics.some(row => row.phase === 'basis-ready')).toBe(true);
        expect(diagnostics.some(row => row.phase === 'session-created')).toBe(false);
      }
      fireEvent.pointerDown(clipNode, { button: 0, pointerId: 77, pointerType: 'mouse', clientX: 181, clientY: 18 });
      fireEvent.pointerMove(window, { pointerId: 77, pointerType: 'mouse', clientX: 341, clientY: 18 });
      expect(pointer.result.current.dragSessionRef.current?.moveReadBasis?.kind).toBe('move');
      fireEvent.pointerUp(window, { pointerId: 77, pointerType: 'mouse', clientX: 341, clientY: 18 });
      await drain();
      expect(hook.result.current.dataRef.current?.config.clips.find(clip => clip.id === 'f2-app-clip')?.at).toBe(5);
      expect(diagnostics.some(row => row.phase === 'schedule' && row.gestureKind === 'move')).toBe(true);
      expect(diagnostics.some(row => row.phase === 'capture-called' && row.gestureKind === 'move')).toBe(true);
      const scope = { ...await readIdentity(), projectId, timelineId };
      if (mode !== 'ready') {
        expect(sends).toHaveLength(0);
        expect(await createCommitOutbox().list(scope)).toHaveLength(0);
        await act(async () => { originalRead.resolve(); identity.resolve(); }); await drain(); await advance(100);
      }
      await advance(6000);
      const records = await createCommitOutbox().list(scope);
      const captureResults = await Promise.allSettled(captures.mock.results.map(result => result.value));
      const captureFailures = captureResults.map(result => result.status === 'fulfilled' ? 'resolved'
        : result.reason?.message === 'Local document save retained: parent gesture changes more than its selected fields'
          ? 'parent-gesture-selected-fields' : result.reason?.message === 'Local document save retained: child ownership/fork mapping is unavailable'
            ? 'child-ownership-unavailable' : 'other-rejection');
      console.log('A2 outbox', JSON.stringify({ mode, sends: sends.length, owners: records.length,
        intents: records.map(row => row.intents.length), reserved: records.map(row => Boolean(row.pending)), schedules,
        captures: captures.mock.calls.map(([, basis]) => basis?.kind ?? 'absent'), captureFailures }));
      if (mode === 'pending-original-read') {
        expect(diagnostics.some(row => row.phase === 'owner-error' && row.errorCode === 'owner-original-read-invalidated')).toBe(true);
        expect(diagnostics.some(row => row.phase === 'capture-rejected' && row.errorCode === 'owner-original-read-invalidated')).toBe(true);
        expect(records).toHaveLength(0);
        expect(sends).toHaveLength(0);
      } else {
        // Keep the required save assertions RED; do not encode the refusal as the desired behavior.
        expect(diagnostics.some(row => row.phase === 'capture-resolved')).toBe(true);
        expect(sends).toHaveLength(1);
        expect(records).toHaveLength(1);
        expect(records[0].intents).toHaveLength(1);
        expect(records[0].pending?.request.key).toBe(sends[0].key);
        expect(JSON.parse(records[0].pending!.request.body)).toEqual(sends[0].request);
        expect(sends[0].request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId,
          base_revision_id: head.headRevisionId, base_publication_id: head.headPublicationId, dry_run: false,
          merge: 'fields', source: { via: 'app' }, label: 'Edit timeline',
          commands: [{ op: 'doc.patch', args: { changes: [expect.objectContaining({ op: 'set', ref: 'parent',
            path: ['clips', 'id:f2-app-clip', 'at'], before: { state: 'present', value: 0 }, value: 5 })] } }] });
        expect(sends[0].request.steps).toEqual([expect.objectContaining({ id: expect.any(String), label: 'Edit timeline',
          intent: 'Move f2-app-clip on V1', tags: [], command_ordinals: [0], patch: expect.any(Array), reads: expect.any(Array) })]);
        expect(sends[0].request.reads?.length).toBeGreaterThan(0);
        // rationale/group_id are optional; retain their actual presence without inventing values.
        console.log('A2 optional v2 fields', { rationale: Object.hasOwn(sends[0].request, 'rationale'),
          group_id: Object.hasOwn(sends[0].request, 'group_id') });
      }
      console.log('A2 boundary', JSON.stringify({ mode, localAt: 5, sends: sends.length,
        owners: records.length, intents: records.reduce((n, row) => n + row.intents.length, 0),
        reserved: records.some(row => Boolean(row.pending)), phases: diagnostics.map(row => ({ phase: row.phase,
          gesture: row.gestureKind, code: row.errorCode, generation: row.generation, session: row.sessionPresent })) }));
    } finally {
      console.log('A2 final state', JSON.stringify({ mode, basis: hook.result.current.originalLocalSaveBasis?.status,
        phases: diagnostics.map(row => ({ phase: row.phase, operation: row.operation, operationState: row.operationState,
          code: row.errorCode, session: row.sessionPresent })) }));
      pointer.unmount(); hook.unmount(); wrapperNode.remove(); queryClient.clear();
      unsubscribe();
      captures.mockRestore();
      window.removeEventListener('timeline:save-diagnostic', observe);
      Object.assign(window, { __timelineSaveDiagnosticsEnabled: false });
    }
  });
