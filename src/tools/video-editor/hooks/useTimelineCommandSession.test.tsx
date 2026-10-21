import { captureClipScalarEdit, submitClipScalarEdit, submitClipTransitionClears } from '../commands/clipScalarGesture.ts';
// @vitest-environment jsdom
import { act, fireEvent, render, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import React, { createElement, useEffect, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { createInteractionState } from '../lib/interaction-state.ts';
import { buildPendingDragSession, commitDraggingSession } from './useClipDrag.helpers.ts';
import { document as commandDocument, environment, scope } from '../commands/__tests__/commitSessionEnvironment.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createTimelineStore, TimelineStoreProvider } from './timelineStore.ts';
import { TimelineEditorCore } from '../components/TimelineEditor/TimelineEditorCore.tsx';
import { useTimelineSave } from './useTimelineSave.ts';
import { loadTimelineDraft } from '../data/timelineDraftIndexedDb.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';
import { useTimelineHistory } from './useTimelineHistory.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import * as timelineData from '../lib/timeline-data.ts';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { TimelineSchemaIncompatibleError, type DataProvider } from '../data/DataProvider.ts';
import type { MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipMove, submitClipMove } from '../commands/semanticGestures.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from '../commands/trackLabelGesture.ts';
import { createRecoveryConfig } from './useTimelineSave.draftConfig.ts';

import { useAssetManagement } from './useAssetManagement.ts';
import { useExternalDrop } from './useExternalDrop.ts';
import { useDragCoordinator } from './useDragCoordinator.ts';
import { bindPopupOccurrenceMediaPort } from '../commands/occurrenceMediaGesture.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { createShotTimelineInitialData } from '@/tools/travel-between-images/components/shotTimelineDataProvider.ts';
import duplicateFixture from '../commands/fixtures/recipe_m2_app_occurrence_duplicate.json';
import type { PreparedMediaImport } from '../data/AssetResolver.ts';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';

// These gallery observers do not participate in the file-drop command route.
vi.mock('./useStaleVariants.ts', () => ({ useStaleVariants: () => ({
  staleAssetKeys: new Set(), dismissedAssetKeys: new Set(), generationAssetKeys: new Set(),
}) }));
vi.mock('./useActiveTaskClips.ts', () => ({ useActiveTaskClips: () => ({ activeTaskAssetKeys: new Set() }) }));
vi.mock('./useAddVariantAsGeneration.ts', () => ({ useAddVariantAsGeneration: () => ({}) }));

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

function installStorage(env: Awaited<ReturnType<typeof environment>>) {
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
}

async function mounted(existingEnv?: Awaited<ReturnType<typeof environment>>, cold = false) {
  const env = existingEnv ?? await environment();
  installStorage(env);
  const snapshotSaves = vi.fn();
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const store = createTimelineStore();
  store.getState().setMounted(true);
  const initial = cold ? { ...env.current(), head: { ...env.current().head!, headPublicationId: null } } : env.current();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider: env.provider, timelineId: 'timeline-commit', shots: { canonicalDraft: null },
    project: { projectId: 'project-commit' }, toast: { error: vi.fn(), success: vi.fn() },
    assetResolver: { resolveAssetUrl: async (value: string) => value } } as unknown as VideoEditorRuntimeContextValue;
  const queries = { timelineQuery: { data: initial, isLoading: false }, assetRegistryQuery: { data: initial.registry } };
  const interactionStateRef = { current: createInteractionState() };
  const wrapper = ({ children }: { children: ReactNode }) => createElement(QueryClientProvider, { client: queryClient },
    createElement(VideoEditorRuntimeProvider, { value: runtime }, children));
  const readiness: { data: timelineData.TimelineData | null; isLoading: boolean }[] = [];
  const hook = renderHook(({ loaded }: { loaded: timelineData.TimelineData | undefined }) => {
    const save = useTimelineSave({ ...queries, timelineQuery: { data: loaded, isLoading: !loaded } },
      env.provider, interactionStateRef, store, cold ? undefined : initial);
    readiness.push({ data: save.data, isLoading: save.isLoading });
    const history = useTimelineHistory({ dataRef: save.dataRef, commitData: save.commitData,
      interactionStateRef, pendingOpsRef: save.pendingOpsRef });
    useEffect(() => save.eventBus.on('beforeCommit', history.onBeforeCommit), [save.eventBus, history.onBeforeCommit]);
    useEffect(() => save.eventBus.on('remoteCommit', history.onRemoteData), [save.eventBus, history.onRemoteData]);
    store.getState().syncSlices({
      data: { ...store.getState().data, data: save.data, resolvedConfig: save.data?.resolvedConfig ?? null, dataRef: save.dataRef },
      ops: { ...store.getState().ops, clipMove: save.commands.port },
    });
    return { commands: save.commands, commit: save, history };
  }, { wrapper, initialProps: { loaded: cold ? undefined : initial } });
  if (cold) {
    expect(hook.result.current.commands.trackLabelPort).toBeUndefined();
    expect(hook.result.current.commit.isLoading).toBe(true);
    act(() => hook.rerender({ loaded: initial }));
  }
  hook.result.current.commit.eventBus.on('scheduleSave', snapshotSaves);
  await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
  const service = createTimelineCommands(store);
  return { env, hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead, readiness };
}

async function scoped() {
  const env = await environment();
  installStorage(env);
  const initial = env.current();
  const snapshotWriteBlockedRef = { current: false };
  const headRevisionRef = { current: initial.head };
  const configVersionRef = { current: initial.configVersion };
  const lastSavedSignatureRef = { current: initial.stableSignature };
  const store = createTimelineStore();
  const eventBus = new TimelineEventBus();
  const recoveryConfig = createRecoveryConfig();
  let legacyClean = true;
  const hook = renderHook(({ provider, timelineId, loaded }: { provider: DataProvider; timelineId: string; loaded?: timelineData.TimelineData }) => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider, timelineId, commit, legacyClean: () => legacyClean,
      resolveAssetUrl: async (file) => file, loaded, snapshotWriteBlockedRef, headRevisionRef,
      configVersionRef, lastSavedSignatureRef, store, recoveryConfig, shots: { shots: undefined, isLoading: false, error: null,
        refetchShots: vi.fn(), finalVideoMap: new Map(), dismissFinalVideo: vi.fn(), canonicalDraft: null } });
    return { commit, commands };
  }, { initialProps: { provider: env.provider as DataProvider, timelineId: 'timeline-commit', loaded: undefined as timelineData.TimelineData | undefined } });
  await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
  const neutral: DataProvider = { persistenceEnabled: false, loadTimeline: vi.fn(), loadAssetRegistry: vi.fn(),
    saveTimeline: vi.fn(), resolveAssetUrl: async (file) => file };
  return { env, hook, neutral, snapshotWriteBlockedRef, headRevisionRef, configVersionRef, store, recoveryConfig,
    setLegacyClean: (clean: boolean) => { legacyClean = clean; } };
}

describe('mounted timeline command session', () => {
  it.each(['open', 'closed during import', 'closed during verification', 'changed during verification'] as const)(
    'routes a mounted Runtime file drop through the live occurrence session: %s', async (lifetime) => {
      const selection = { asset: 'sha256:asset', generation_id: 'generation-1', variant_id: 'variant-1',
        object_id: `sha256:${'a'.repeat(64)}`, catalog_digest: `sha256:${'b'.repeat(64)}` };
      let completeImport!: (value: PreparedMediaImport) => void;
      const prepareMediaImport = vi.fn(() => new Promise<PreparedMediaImport>(resolve => { completeImport = resolve; }));
      const raw = structuredClone(duplicateFixture.bundle.source_mapping._runtime_document) as unknown as CanonicalDocument;
      raw.project_id = scope.projectId;
      raw.timeline_id = scope.timelineId;
      raw.parent_revision.revision_id = 'r0';
      const internal = raw.internal_timeline_revisions[0];
      delete internal.payload.source_window; // Media ADD uses the literal child timeline, without a source window.
      internal.payload.tracks = [{ id: 'V1', kind: 'visual' }, { id: 'V2', kind: 'visual' }];
      for (const clip of internal.payload.clips as Array<Record<string, string>>) clip.track = 'V1';
      internal.content_digest = fixtureDigest(internal.payload);
      raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
      const env = await environment(raw);
      let finishVerification!: () => void;
      const verification = new Promise<void>(resolve => { finishVerification = resolve; });
      const verifiedRead = vi.spyOn(env.provider, 'getProjectVerifiedMedia').mockImplementation(async () => {
        await verification;
        return { selection, media_type: 'image/png', size: 5 };
      });
      env.setFault('unavailable');
      const runtime = { provider: env.provider, project: { projectId: scope.projectId }, toast: { error: vi.fn() } } as unknown as VideoEditorRuntimeContextValue;
      const preparedComposition = createShotCompositionAdapter(env.provider.shotComposition).prepare(env.initial.graph);
      const projected = projectCanonicalComposition({ ...preparedComposition,
        occurrences: preparedComposition.occurrences.filter(occurrence => occurrence.occurrenceId === 'occ-0') }).config;
      const initial = createShotTimelineInitialData(projected);
      vi.spyOn(env.provider, 'prepareMediaImport').mockImplementation(prepareMediaImport);
      const dataRef = { current: initial };
      const pendingOpsRef = { current: 0 };
      const applyEdit = vi.fn();
      const patchRegistry = vi.fn();
      const { hook, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted(env);
      const parent = hook.result.current.commit.dataRef.current!;
      const native = hook.result.current.commands.occurrenceMediaPort!;
      const capture = vi.spyOn(native, 'capture');
      let popupOpen = true;
      const port = bindPopupOccurrenceMediaPort(native, 'occ-0', () => popupOpen ? hook.result.current.commit.dataRef.current : null);
      const childStore = createTimelineStore();
      function MountedDrop() {
        const assets = useAssetManagement({ dataRef, selectedTrackId: 'V2', selectedProjectId: scope.projectId, applyEdit,
          selectClip: vi.fn(), setSelectedTrackId: vi.fn(), patchRegistry,
          invalidateAssetRegistry: vi.fn(), resolveAssetUrl: async file => file,
          occurrenceId: 'occ-0', occurrenceMediaPort: port });
        const { coordinator, editAreaRef, indicatorRef } = useDragCoordinator({ dataRef, scale: 5, scaleWidth: 100,
          startLeft: 0, rowHeight: 36 });
        const handlers = useExternalDrop({ occurrenceId: 'occ-0', dataRef, pendingOpsRef, selectedTrackId: 'V2', applyEdit,
          scale: 5, scaleWidth: 100,
          invalidateAssetRegistry: vi.fn(), resolveAssetUrl: async file => file,
          coordinator, ...assets, finalVideoMap: new Map() });
        const state = childStore.getState();
        state.syncSlices({ data: { ...state.data, data: initial, resolvedConfig: initial.resolvedConfig,
          dataRef, pendingOpsRef, coordinator, editAreaRef, indicatorRef, selectedTrackId: 'V2', scale: 5, scaleWidth: 100 },
        ops: { ...state.ops, ...handlers, applyEdit, isClipSelected: () => false } });
        return <TimelineStoreProvider store={childStore}><TimelineEditorCore /></TimelineStoreProvider>;
      }
      const view = render(<VideoEditorRuntimeProvider value={runtime}><MountedDrop /></VideoEditorRuntimeProvider>);
      const wrapper = view.container.querySelector('.timeline-wrapper')!;
      const file = new File(['image'], 'popup-add.png', { type: 'image/png' });
      const dataTransfer = { types: ['Files'], files: [file], items: [{ type: 'image/png' }], getData: () => '' };
      for (const type of ['dragover', 'drop']) {
        fireEvent(wrapper, Object.assign(new Event(type, { bubbles: true, cancelable: true }),
          { dataTransfer, clientX: 50, clientY: 54 }));
      }
      await waitFor(() => expect(prepareMediaImport).toHaveBeenCalledTimes(1));
      if (lifetime === 'closed during import') popupOpen = false;
      await act(async () => completeImport({ provider: 'runtime', project: scope.projectId,
        importOperationId: 'operation-1', generationId: selection.generation_id, variantId: selection.variant_id,
        assetId: selection.asset, entry: { file: 'https://runtime.test/image', type: 'image/png' }, mediaSelection: selection }));
      if (lifetime !== 'closed during import') {
        expect(runtime.toast.error).not.toHaveBeenCalled();
        await waitFor(() => expect(verifiedRead).toHaveBeenCalledTimes(1));
        if (lifetime === 'closed during verification') popupOpen = false;
        if (lifetime === 'changed during verification') {
          act(() => hook.result.current.commit.commitData({ ...parent }, { save: false }));
        }
      }
      await act(async () => finishVerification());
      if (lifetime !== 'open') {
        await waitFor(() => expect(runtime.toast.error).toHaveBeenCalledWith(expect.stringMatching(/popup media|Displayed timeline changed/)));
        expect(env.commits()).toEqual([]);
        expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
        expect(applyEdit).not.toHaveBeenCalled();
        expect(patchRegistry).not.toHaveBeenCalled();
        expect(dataRef.current).toBe(initial);
        expect(snapshotSaves).not.toHaveBeenCalled();
        expect(saveTimeline).not.toHaveBeenCalled();
        expect(saveTimelineAtHead).not.toHaveBeenCalled();
        view.unmount();
        hook.unmount();
        return;
      }
      expect(runtime.toast.error).not.toHaveBeenCalled();
      await waitFor(() => expect(env.commits()).toHaveLength(1));
      expect(capture).toHaveBeenCalledWith({ current: parent, request: {
        kind: 'add', ownerRef: 'occurrence:occ-0', trackRef: 'occurrence:occ-0/track:V2', media: selection,
        row: { id: expect.stringMatching(/^popup-child-/), clipType: 'image', track: 'V2', at: expect.any(Number),
          asset: selection.asset, hold: 5 },
      } });
      expect(verifiedRead).toHaveBeenCalledExactlyOnceWith(scope.projectId, selection);
      const post = env.commits()[0];
      expect(post.body!.commands).toMatchObject([{ op: 'occurrence.add-media', select: 'occurrence:occ-0',
        intent: { ownership: 'occurrence' }, args: { media: selection, row: { track: 'V2', asset: selection.asset } } }]);
      expect(post.body).not.toHaveProperty('parent_composition');
      await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
      const [owner] = await env.outboxes.list(scope);
      expect(owner.pending!.request.body).toBe(post.bodyText);
      expect(owner.pending!.request.key).toBe(post.key);
      expect(snapshotSaves).not.toHaveBeenCalled();
      expect(saveTimeline).not.toHaveBeenCalled();
      expect(saveTimelineAtHead).not.toHaveBeenCalled();
      expect(applyEdit).not.toHaveBeenCalled();
      expect(patchRegistry).not.toHaveBeenCalled();
      expect(dataRef.current).toBe(initial);
      expect(runtime.toast.error).not.toHaveBeenCalled();
      view.unmount();
      hook.unmount();
    });

  it('initializes a clean mounted save hook with a verified accepted projection', async () => {
    const { env, hook, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    expect(hook.result.current.commit.data!.editProjection).toEqual({ kind: 'accepted', head: env.initial.head });
    expect(hook.result.current.commit.data!.config.clips[0].at).toBe(1);
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    expect(env.commits()).toHaveLength(0);
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });
  it('keeps command history ownership when an accepted publication is present on reload', async () => {
    const first = await mounted();
    const current = first.hook.result.current.commit.data!;
    act(() => {
      submitTrackLabelEdit(captureTrackLabelEdit(first.hook.result.current.commands.trackLabelPort, current, 'V1'),
        { values: { label: 'accepted before reload' }, clear: [] });
    });
    await act(async () => { await first.hook.result.current.commands.flush(); });
    first.hook.unmount();

    const accepted = await first.env.provider.loadTimelineCommandBasis('timeline-commit');
    vi.spyOn(first.env.provider, 'loadTimelineCommandBasis').mockResolvedValue({
      ...accepted,
      history: {
        ...accepted.history,
        items: [{
          publication_id: accepted.head.publicationId,
          revision_id: accepted.head.revisionId,
          previous: null,
          receipt: {} as never,
          intent: 'recorded',
          records: {} as never,
          provider_version: null,
          compiler_version: null,
          publisher: scope.actorId,
        }],
      },
    });
    const reopened = await mounted(first.env);
    expect(reopened.hook.result.current.commands.state).toMatchObject({ status: 'saved', canUndo: true });
    expect(reopened.hook.result.current.commands.ownsHistoryRef.current).toBe(true);
    reopened.hook.unmount();
  });
  it('projects Use latest as a normal accepted read pin only after durable explicit discard', async () => {
    const { env, hook, snapshotWriteBlockedRef, headRevisionRef } = await scoped();
    env.setFault('conflict');
    act(() => { submitTrackLabelEdit(captureTrackLabelEdit(hook.result.current.commands.trackLabelPort,
      hook.result.current.commit.data!, 'V1'), { values: { label: 'Mine' }, clear: [] }); });
    await waitFor(() => expect(hook.result.current.commands.state.canDiscardRejected).toBe(true));
    const [original] = await env.outboxes.list(scope);
    const fresh = await env.external((raw) => {
      (raw.parent_revision.payload.config as { tracks: Array<{ label: string }> }).tracks[0].label = 'Theirs';
    });
    const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis');
    await act(async () => { await hook.result.current.commands.useLatest(); });
    expect(load).toHaveBeenCalledWith('timeline-commit');
    expect(hook.result.current.commands.state.status).toBe('saved');
    expect(snapshotWriteBlockedRef.current).toBe(false);
    expect(hook.result.current.commands.activeRef.current).toBe(false);
    expect(headRevisionRef.current).toMatchObject({ headRevisionId: fresh.head.revisionId,
      headPublicationId: fresh.head.publicationId });
    expect(hook.result.current.commit.data!.config.tracks[0].label).toBe('Theirs');
    expect(hook.result.current.commit.data!.editProjection).toEqual({ kind: 'accepted', head: fresh.head });
    const [cleared] = await env.outboxes.list(scope);
    expect(cleared.ownerId).toBe(original.ownerId);
    expect(cleared.intents).toEqual([]);
    expect(cleared.pending).toBeUndefined();
    expect(env.commits()).toHaveLength(1);
    hook.unmount();
  });

  it('fences a late poll across explicit Keep so old pixels cannot acquire the new accepted pin', async () => {
    const { env, hook, headRevisionRef } = await scoped();
    env.setFault('conflict');
    act(() => { submitTrackLabelEdit(captureTrackLabelEdit(hook.result.current.commands.trackLabelPort,
      hook.result.current.commit.data!, 'V1'), { values: { label: 'Mine' }, clear: [] }); });
    await waitFor(() => expect(hook.result.current.commands.state.canReapplyLabel).toBe(true));
    const stale = await env.external((raw) => {
      (raw.parent_revision.payload.config as { tracks: Array<{ label: string }> }).tracks[0].label = 'Earlier remote';
    });
    let finishPoll!: (basis: typeof env.initial) => void;
    const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockImplementationOnce(() =>
      new Promise((resolve) => { finishPoll = resolve; }));
    hook.rerender({ provider: env.provider, timelineId: 'timeline-commit', loaded: { ...env.current() } });
    await waitFor(() => expect(load).toHaveBeenCalledOnce());
    await env.external((raw) => {
      (raw.parent_revision.payload.config as { tracks: Array<{ label: string }> }).tracks[0].label = 'Fresh remote';
    });
    env.setFault(null);
    await act(async () => { await hook.result.current.commands.keepLabelChanges(); });
    const accepted = hook.result.current.commit.data!;
    const acceptedHead = headRevisionRef.current;
    expect(accepted.config.tracks[0].label).toBe('Mine');
    expect(env.commits()[1].body!.commands[0].expect?.['parent/track:V1::label'])
      .toEqual({ state: 'present', value: 'Fresh remote' });
    await act(async () => { finishPoll(stale); });
    expect(hook.result.current.commit.data).toBe(accepted);
    expect(headRevisionRef.current).toBe(acceptedHead);
    expect(hook.result.current.commit.data!.editProjection).toEqual({ kind: 'accepted',
      head: { revisionId: acceptedHead!.headRevisionId, publicationId: acceptedHead!.headPublicationId } });
    hook.unmount();
  });

  it('preserves the original rejected owner when a project switch races Keep', async () => {
    const { env, hook, neutral, headRevisionRef, snapshotWriteBlockedRef } = await scoped();
    env.setFault('conflict');
    act(() => { submitTrackLabelEdit(captureTrackLabelEdit(hook.result.current.commands.trackLabelPort,
      hook.result.current.commit.data!, 'V1'), { values: { label: 'Mine' }, clear: [] }); });
    await waitFor(() => expect(hook.result.current.commands.state.canReapplyLabel).toBe(true));
    const [original] = await env.outboxes.list(scope);
    let finish!: (basis: typeof env.initial) => void;
    const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockImplementationOnce(() =>
      new Promise((resolve) => { finish = resolve; }));
    const keeping = hook.result.current.commands.keepLabelChanges();
    const refused = expect(keeping).rejects.toThrow('closed');
    await waitFor(() => expect(load).toHaveBeenCalledOnce());
    hook.rerender({ provider: neutral, timelineId: 'other', loaded: undefined });
    const next = compileTimelinePatch({ version: 1, operations: [{ op: 'track.update', target: 'V1',
      payload: { label: 'New project pixels' } }] }, hook.result.current.commit.data!).nextData!;
    const nextHead = { projectId: 'other-project', timelineId: 'other', headRevisionId: 'next-r', headPublicationId: 'next-p' };
    act(() => { hook.result.current.commit.commitData(next); headRevisionRef.current = nextHead; });
    await act(async () => { finish(env.initial); await refused; });
    expect(hook.result.current.commit.dataRef.current).toBe(next);
    expect(headRevisionRef.current).toBe(nextHead);
    expect(snapshotWriteBlockedRef.current).toBe(false);
    expect((await env.outboxes.list(scope))[0]).toEqual(original);
    expect(env.commits()).toHaveLength(1);
    hook.unmount();
  });

  it('fences track-label capture, completion and submission behind earlier legacy saves', async () => {
    const { env, hook, setLegacyClean } = await scoped();
    const port = hook.result.current.commands.trackLabelPort!;
    const current = hook.result.current.commit.data!;
    const args = { values: { label: 'kept typing' }, clear: [] } as const;
    setLegacyClean(false);
    expect(() => captureTrackLabelEdit(port, current, 'V1')).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const captured = captureTrackLabelEdit(port, current, 'V1');
    setLegacyClean(false);
    expect(() => submitTrackLabelEdit(captured, { values: args.values, clear: [] })).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const prepared = port.finish(captured.basis, { values: args.values, clear: [] });
    setLegacyClean(false);
    expect(() => port.submit({ command: prepared.command,
      preview: { version: 1, operations: [{ op: 'track.update', target: 'V1', payload: args.values }] } })).toThrow('earlier timeline saves');
    expect(args.values.label).toBe('kept typing');
    expect(hook.result.current.commit.data).toBe(current);
    expect(env.commits()).toHaveLength(0);
    hook.unmount();
  });
  it('fences parent media capture, completion and submission behind an intervening legacy save', async () => {
    const { env, hook, setLegacyClean } = await scoped();
    const port = hook.result.current.commands.parentClipAddMediaPort!;
    const swapPort = hook.result.current.commands.parentClipSwapMediaPort!;
    const current = hook.result.current.commit.data!;
    const media: MediaSelection = {
      asset: 'reserved-media',
      generation_id: 'generation-media',
      variant_id: 'variant-media',
      object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
      catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
    };
    const row = { id: 'native-clip', track: 'V1', at: 2, clipType: 'video', asset: 'reserved-media',
      from: 0, to: 1, hold: 1, speed: 1 };
    const verified: VerifiedMedia = { selection: { ...media }, media_type: 'video/mp4', size: 1, duration_seconds: 1 };

    setLegacyClean(false);
    expect(() => port.prepare()).toThrow('earlier timeline saves');
    expect(() => swapPort.prepare()).toThrow('earlier timeline saves');
    expect(() => port.capture({ row, media, current })).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const addPreparation = port.prepare();
    const swapPreparation = swapPort.prepare();
    const basis = port.capture({ row, media, current });
    let releaseVerification!: (value: VerifiedMedia) => void;
    const verification = new Promise<VerifiedMedia>((resolve) => { releaseVerification = resolve; });
    const finishing = verification.then((value) => port.finish(basis, value));
    setLegacyClean(false);
    releaseVerification(verified);
    await expect(finishing).rejects.toThrow('earlier timeline saves');
    expect(() => port.assertPreparationCurrent(addPreparation)).toThrow('earlier timeline saves');
    expect(() => swapPort.assertPreparationCurrent(swapPreparation)).toThrow('earlier timeline saves');
    expect((await env.outboxes.list(scope))[0]?.intents).toEqual([]);
    setLegacyClean(true);
    const captured = port.finish(basis, verified);
    setLegacyClean(false);
    expect(() => port.submit(captured)).toThrow('earlier timeline saves');
    expect(env.commits()).toHaveLength(0);
    hook.unmount();
  });
  it('cold seed hydration projects the verified initial head before the first Unicode track rename', async () => {
    const raw = commandDocument();
    // seedThreeProducts' fresh parent/shot shape, before any App move (referenceAt=15).
    const tracks = [{ id: 'V1', kind: 'visual', label: 'V1' }, { id: 'S1', kind: 'visual', label: 'S1' }];
    const imageDigest = fixtureDigest('cold-image'), videoDigest = fixtureDigest('cold-video');
    const image = (name: string) => ({ file: `${name}.png`, type: 'image/png',
      media_id: imageDigest, content_sha256: imageDigest });
    const clips = [
      { id: 'f2-app-clip', at: 0, track: 'V1', clipType: 'media', asset: 'f2-app', from: 0, to: 3, speed: 1 },
      { id: 'f2-transition-clip', at: 15, track: 'V1', clipType: 'media', asset: 'f2-video', from: 0, to: 3,
        speed: 1, transition: { type: 'crossfade', duration: 0.5 } },
    ];
    const parent = raw.parent_revision.payload;
    parent.config = { output: { file: 'out.mp4', fps: 30, resolution: '1280x720' }, tracks, clips,
      x_f2_opaque: { flag: true, nested: [1, { k: 'v' }], owner: 'f2' } };
    delete parent.tracks;
    parent.clips = clips;
    parent.registry = { assets: { 'f2-app': image('f2-app'), 'f2-video': { file: 'f2-video.webm',
      type: 'video/webm', duration: 12, media_id: videoDigest, content_sha256: videoDigest } } };
    parent.occurrences = [{ occurrence_id: 'f2-occurrence', shot_id: 'f2-shot', shot_revision_id: 'shot-r0',
      placement: { start_ms: 0 }, source_offset: 0, duration_ms: 12000, speed: 1, track: 'S1',
      transform: {}, gain: 1, muted: false, provenance: {} }];
    const internal = { tracks: [{ id: 'plate', kind: 'visual', label: 'plate' }, { id: 'V2', kind: 'visual', label: 'V2' }],
      clips: [{ id: 'f2-plate', at: 0, track: 'plate', clipType: 'media', asset: 'f2-plate', hold: 12 },
        { id: 'f2-agent-clip', at: 3, track: 'V2', clipType: 'media', asset: 'f2-placeholder', hold: 3,
          app: { f2Opaque: { owner: 'f2', nested: [1, { k: 'v' }] } } },
        { id: 'f2-agent-clear-clip', at: 6, track: 'V2', clipType: 'media', asset: 'f2-clear', hold: 3 }],
      effects: [], audio: [], layout: {}, assets: [], registry: { assets: Object.fromEntries(
        ['f2-plate', 'f2-placeholder', 'f2-clear'].map(name => [name, image(name)])) } };
    const shot = { internal_timeline_revision_id: 'internal-r0', metadata: { title: 'F2 agent shot' }, items: [], pools: [], selected_variants: {},
      provenance: {}, generation_inputs: {}, audio_bindings: [], text_bindings: [] };
    raw.internal_timeline_revisions = [{ timeline_id: scope.timelineId, revision_id: 'internal-r0',
      content_digest: fixtureDigest(internal), payload: internal }];
    raw.shot_revisions = [{ shot_id: 'f2-shot', revision_id: 'shot-r0', internal_timeline_revision_id: 'internal-r0',
      content_digest: fixtureDigest(shot), payload: shot }];
    raw.dependency_manifest = { documents: [], media: [imageDigest, videoDigest].map(digest =>
      ({ media_id: digest, content_digest: digest })), shots: raw.shot_revisions.map(({ payload, ...pin }) => pin),
      internal_timelines: raw.internal_timeline_revisions.map(({ payload, ...pin }) => pin) };
    raw.parent_revision.content_digest = fixtureDigest(parent);
    const env = await environment(raw);
    const { hook, snapshotSaves, saveTimeline, saveTimelineAtHead, readiness } = await mounted(env, true);
    const initial = hook.result.current.commit.data!;
    const captured = captureTrackLabelEdit(hook.result.current.commands.trackLabelPort, initial, 'V1');
    const rawDisplays = readiness.filter(({ data }) => data && !data.editProjection);
    expect(rawDisplays.length).toBeGreaterThan(0);
    expect(rawDisplays.every(({ isLoading }) => isLoading)).toBe(true);
    expect(initial.head).toEqual({ projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: 'r0', headPublicationId: 'p0' });
    expect(initial.editProjection).toEqual({ kind: 'accepted', head: env.initial.head });
    expect(initial.config.clips).toHaveLength(5);
    expect(initial.config.clips.some(clip => clip.id.includes('f2-occurrence'))).toBe(true);
    expect(hook.result.current.commit.isLoading).toBe(false);
    const label = '映像 🎬 — café';
    act(() => submitTrackLabelEdit(captured, { values: { label }, clear: [] }));
    await act(async () => { await hook.result.current.commands.flush(); });
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0',
      commands: [{ op: 'track.set', select: 'parent/track:V1', args: { values: { label }, clear: [] },
        expect: { 'parent/track:V1::label': { state: 'present', value: 'V1' } },
        reads: [{ ref: 'parent/track:V1', path: ['id'], state: { state: 'present', value: 'V1' } }],
        bindings: { 'scalar.target': 'parent/track:V1' } }] });
    expect(hook.result.current.commit.data!.config.tracks[0].label).toBe(label);
    expect(hook.result.current.commit.data!.config).toMatchObject({ x_f2_opaque: parent.config.x_f2_opaque });
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
  });

  it('shares move → label projection and guarded undo without any snapshot save', async () => {
    const { env, hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    await act(async () => {
      expect(service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      await hook.result.current.commands.flush();
    });
    const captured = captureTrackLabelEdit(hook.result.current.commands.trackLabelPort, hook.result.current.commit.data!, 'V1');
    await act(async () => {
      submitTrackLabelEdit(captured, { values: { label: '' }, clear: [] });
      expect(hook.result.current.commit.dataRef.current!.config.tracks[0].label).toBe('');
      await hook.result.current.commands.flush();
    });
    expect(hook.result.current.commit.data!.config.tracks[0].label).toBe('');
    expect(hook.result.current.commit.data!.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data!.head?.headPublicationId).toBe('p2');
    expect(env.commits()[1].body!.commands[0]).toMatchObject({ op: 'track.set',
      args: { values: { label: '' }, clear: [] }, expect: { 'parent/track:V1::label': { state: 'absent' } } });
    await act(async () => { await hook.result.current.commands.undo(); await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data!.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data!.config.tracks[0]).not.toHaveProperty('label');
    expect(env.commits()[2].body!.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p2'] } });
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });
  it('recovers move → clear with the original pending request and a display-only label fallback', async () => {
    const env = await environment();
    const first = await mounted(env);
    env.setFault('lost');
    act(() => {
      expect(first.service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      submitTrackLabelEdit(captureTrackLabelEdit(first.hook.result.current.commands.trackLabelPort,
        first.hook.result.current.commit.dataRef.current!, 'V1'), { values: {}, clear: ['label'] });
    });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    const owner = first.hook.result.current.commands.state.ownerId!;
    expect(first.hook.result.current.commands.activeRef.current).toBe(true);
    expect(first.hook.result.current.commit.data!.config.tracks[0].label).toBe('V1');
    first.hook.unmount();
    const second = await mounted(env);
    await waitFor(() => expect(second.hook.result.current.commands.state.status).toBe('recovery'));
    await act(async () => { await second.hook.result.current.commands.recover(owner); });
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'track.set',
      args: { values: {}, clear: ['label'] }, expect: { 'parent/track:V1::label': { state: 'absent' } } }] });
    expect(second.hook.result.current.commit.data!.config.clips[0].at).toBe(5);
    expect(second.hook.result.current.commands.state.status).toBe('saved');
    expect(first.snapshotSaves).not.toHaveBeenCalled();
    expect(second.snapshotSaves).not.toHaveBeenCalled();
    expect(first.saveTimeline).not.toHaveBeenCalled();
    expect(first.saveTimelineAtHead).not.toHaveBeenCalled();
    second.hook.unmount();
  });
  it('clears command ownership and the snapshot block on provider cleanup, fencing an old ACK', async () => {
    const { env, hook, neutral, snapshotWriteBlockedRef } = await scoped();
    const gate = env.pause();
    act(() => { submitClipMove(captureClipMove(hook.result.current.commands.port, hook.result.current.commit.data!, 'x'), 5); });
    await waitFor(() => expect(env.commits()).toHaveLength(1));
    expect(snapshotWriteBlockedRef.current).toBe(true);
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(true);
    const old = hook.result.current.commands;
    const finished = expect(old.flush()).rejects.toThrow('not acknowledged');
    hook.rerender({ provider: neutral, timelineId: 'other' });
    expect(snapshotWriteBlockedRef.current).toBe(false);
    expect(hook.result.current.commands.activeRef.current).toBe(false);
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    const next = compileTimelinePatch({ version: 1,
      operations: [{ op: 'clip.move', target: 'x', payload: { at: 9 } }] }, hook.result.current.commit.data!).nextData!;
    act(() => { hook.result.current.commit.commitData(next); });
    await act(async () => { gate.resolve(); await finished; });
    expect(hook.result.current.commit.dataRef.current).toBe(next);
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    hook.unmount();
  });
  it('fences an in-progress async projection across a timeline switch', async () => {
    const { env, hook, headRevisionRef, configVersionRef, store, snapshotWriteBlockedRef, recoveryConfig } = await scoped();
    let finishProjection!: () => void;
    const gate = new Promise<void>((resolve) => { finishProjection = resolve; });
    const build = timelineData.buildTimelineData;
    const projecting = vi.fn();
    vi.spyOn(timelineData, 'buildTimelineData').mockImplementation(async (...args) => {
      projecting();
      await gate;
      return build(...args);
    });
    act(() => { submitClipMove(captureClipMove(hook.result.current.commands.port, hook.result.current.commit.data!, 'x'), 5); });
    const finished = expect(hook.result.current.commands.flush()).rejects.toThrow('not acknowledged');
    await waitFor(() => expect(projecting).toHaveBeenCalledOnce());
    vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockResolvedValue({ ...env.initial,
      canonicalDocument: { ...env.initial.canonicalDocument, timeline_id: 'other' } });
    hook.rerender({ provider: env.provider, timelineId: 'other' });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('saved'));
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    expect(snapshotWriteBlockedRef.current).toBe(false);
    const next = compileTimelinePatch({ version: 1,
      operations: [{ op: 'clip.move', target: 'x', payload: { at: 9 } }] }, hook.result.current.commit.data!).nextData!;
    const nextHead = { projectId: 'other-project', timelineId: 'other', headRevisionId: 'new-r', headPublicationId: 'new-p' };
    act(() => {
      hook.result.current.commit.commitData(next);
      headRevisionRef.current = nextHead;
      recoveryConfig.remember(nextHead, { x_next: null });
      configVersionRef.current = 42;
      store.getState().setConfigVersion(42);
    });
    await act(async () => { finishProjection(); await finished; });
    expect(hook.result.current.commit.dataRef.current).toBe(next);
    expect(headRevisionRef.current).toBe(nextHead);
    expect(configVersionRef.current).toBe(42);
    expect(store.getState().configVersion).toBe(42);
    expect(recoveryConfig.snapshot(nextHead, next.config)).toEqual({ ...next.config, x_next: null });
    expect(hook.result.current.commands.state.status).toBe('saved');
    hook.unmount();
  });
  it.each([false, true])('stores raw opaque roots with an ordinary rename (after accepted move: %s)', async (moveFirst) => {
    const raw = commandDocument();
    const opaque = { x_null: null, x_false: false, x_zero: 0, x_empty: [],
      x_nested: { unknown: [null, false, 0, [], { value: 'keep' }] } };
    Object.assign(raw.parent_revision.payload.config, opaque);
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const { env, hook, service, saveTimelineAtHead } = await mounted(await environment(raw));
    saveTimelineAtHead.mockRejectedValue(new TimelineSchemaIncompatibleError('timeline_commit_required', []));
    // The raw basis load has completed before capture becomes available.
    if (moveFirst) {
      await act(async () => {
        expect(service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
        await hook.result.current.commands.flush();
      });
    }
    const base = { ...hook.result.current.commit.data!.head! };
    const next = compileTimelinePatch({ version: 1, operations: [
      { op: 'track.update', target: 'V1', payload: { label: 'retained rename' } },
    ] }, hook.result.current.commit.data!).nextData!;
    act(() => { hook.result.current.commit.commitData(next); });
    await waitFor(() => expect(hook.result.current.commit.schemaIncompatible).toEqual([]));
    const kept = await loadTimelineDraft('timeline-commit');
    expect(kept).toMatchObject({ baseHeadProjectId: base.projectId, baseHeadTimelineId: base.timelineId,
      baseHeadRevisionId: base.headRevisionId, draft: { config: { ...opaque,
        tracks: [{ id: 'V1', kind: 'visual', label: 'retained rename' }],
        clips: [expect.objectContaining({ id: 'x', at: moveFirst ? 5 : 1 })] } } });
    expect(kept!.draft.config).not.toHaveProperty('x_absent');
    expect(hook.result.current.commit.data!.config).toMatchObject(opaque);
    expect(hook.result.current.commit.data!.resolvedConfig).toMatchObject(opaque);
    expect(saveTimelineAtHead).toHaveBeenCalledWith('timeline-commit', next.config, base, next.registry, undefined);
    expect(env.commits()).toHaveLength(moveFirst ? 1 : 0);
    hook.unmount();
  });
  it('leaves clean legacy undo available until an actual command owns history', async () => {
    const { env, hook, snapshotSaves } = await mounted();
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    const original = hook.result.current.commit.data!;
    const edited = compileTimelinePatch({ version: 1,
      operations: [{ op: 'clip.move', target: 'x', payload: { at: 3 } }] }, original).nextData!;
    act(() => {
      hook.result.current.history.onBeforeCommit(original, {});
      // An existing, clean legacy edit has no command intent to recover.
      hook.result.current.commit.commitData(edited, { save: false });
    });
    expect(hook.result.current.history.canUndo).toBe(true);
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(false);
    act(() => { hook.result.current.history.undo(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(1);
    expect(snapshotSaves).toHaveBeenCalledOnce();
    expect(env.commits()).toHaveLength(0);
    hook.unmount();
  });
  it('moves through the actual command service with save:false and hydrates the accepted raw closure', async () => {
    const { hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    await act(async () => {
      expect(service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      await hook.result.current.commands.flush();
    });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data?.head?.headPublicationId).toBe('p1');
    expect(hook.result.current.commands.state.status).toBe('saved');
    expect(hook.result.current.commands.ownsHistoryRef.current).toBe(true);
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    expect(await loadTimelineDraft('timeline-commit')).toBeNull();
    await act(async () => { await hook.result.current.commands.undo(); await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(1);
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    expect(snapshotSaves).not.toHaveBeenCalled();
    hook.unmount();
  });
  it('uses the real pointerdown capture and drag release path with the mounted port', async () => {
    const { hook, env, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    const current = hook.result.current.commit.data!;
    const pending = buildPendingDragSession({ clipId: 'x', rowId: 'V1', sourceKind: 'visual',
      sourceAction: current.rows[0].actions[0], current, clipTarget: document.createElement('div'), labelTarget: null,
      event: { pointerId: 1, clientX: 100, clientY: 20, ctrlKey: false, metaKey: false } as PointerEvent,
      selectedClipIds: new Set(['x']), additiveSelection: false, dragAllowed: true,
      inputModality: 'mouse', pixelsPerSecond: 100, clipMove: hook.result.current.commands.port });
    expect(pending.session.moveCaptureError).toBeUndefined();
    await act(async () => {
      expect(commitDraggingSession({ session: pending.session, nextStart: 5, dropPosition: null,
        crossTrackActive: false }).refusal).toBeUndefined();
      await hook.result.current.commands.flush();
    });
    expect(env.commits()[0].body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 1 });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(5);
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });
  it('keeps A5/B7 visible after a lost ACK and blocks snapshot history from saving the move', async () => {
    const { env, hook, service, snapshotSaves } = await mounted();
    env.setFault('lost');
    act(() => {
      expect(service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      expect(service.moveClip({ clipId: 'x', time: 7 }).ok).toBe(true);
    });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    const before = hook.result.current.commit.dataRef.current;
    const overlap = compileTimelinePatch({ version: 1,
      operations: [{ op: 'clip.move', target: 'x', payload: { at: 9 } }] }, before!).nextData!;
    expect(() => hook.result.current.commit.commitData(overlap)).toThrow('pending timeline commands');
    expect(hook.result.current.commit.dataRef.current).toBe(before);
    expect(snapshotSaves).not.toHaveBeenCalled();
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    expect(hook.result.current.commit.data?.head?.headPublicationId).toBe('p2');
    hook.unmount();
  });
  it('exposes the scalar port and fences capture, finish and submit behind earlier legacy saves', async () => {
    const { env, hook, setLegacyClean } = await scoped();
    const port = hook.result.current.commands.clipScalarPort!;
    const current = hook.result.current.commit.data!;
    const args = { values: {}, clear: ['asset'] } as const;
    setLegacyClean(false);
    expect(() => captureClipScalarEdit(port, current, 'x', 'parent')).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const captured = captureClipScalarEdit(port, current, 'x', 'parent');
    setLegacyClean(false);
    expect(() => submitClipScalarEdit(captured, { values: {}, clear: ['asset'] })).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const prepared = port.finish(captured.basis, { values: {}, clear: ['asset'] });
    setLegacyClean(false);
    expect(() => port.submit({ command: prepared.command,
      preview: { version: 1, operations: [{ op: 'clip.update', target: 'x', payload: {}, clear: ['asset'] }] } })).toThrow('earlier timeline saves');
    expect(args.clear).toEqual(['asset']);
    expect(hook.result.current.commit.data).toBe(current);
    expect(env.commits()).toHaveLength(0);
    hook.unmount();
  });
  it('fences atomic transition clear finish and submit behind earlier legacy saves', async () => {
    const { env, hook, setLegacyClean } = await scoped();
    const port = hook.result.current.commands.clipScalarPort!;
    const current = hook.result.current.commit.data!;
    const captured = captureClipScalarEdit(port, current, 'x', 'parent');
    setLegacyClean(false);
    expect(() => submitClipTransitionClears([captured])).toThrow('earlier timeline saves');
    setLegacyClean(true);
    const prepared = port.finishBatch!([captured.basis], { values: {}, clear: ['transition'] });
    setLegacyClean(false);
    expect(() => port.submitBatch!({ commands: prepared.commands,
      preview: { version: 1, operations: [{ op: 'clip.update', target: 'x', payload: {}, clear: ['transition'] }] } }))
      .toThrow('earlier timeline saves');
    expect(hook.result.current.commit.data).toBe(current);
    expect(env.commits()).toHaveLength(0);
    hook.unmount();
  });
  it('previews scalar ABSENT through the mounted hook and keeps the draft on command refusal without snapshot traffic', async () => {
    const { env, hook, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    env.setFault('conflict');
    act(() => submitClipScalarEdit(captureClipScalarEdit(hook.result.current.commands.clipScalarPort!,
      hook.result.current.commit.data!, 'x', 'parent'), { values: {}, clear: ['asset'] }));
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('conflict'));
    expect(hook.result.current.commit.data!.config.clips[0]).not.toHaveProperty('asset');
    expect(hook.result.current.commit.data!.resolvedConfig.clips[0]).not.toHaveProperty('asset');
    expect(env.commits()[0].body!.commands[0]).toMatchObject({ op: 'clip.set', select: 'parent/clip:x',
      args: { values: {}, clear: ['asset'] }, expect: { 'parent/clip:x::asset': { state: 'absent' } } });
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')
      .every((call) => call.path.endsWith('/commit'))).toBe(true);
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });

  it.each([false, true])('queues new None (bulk=%s) after uncertain A until exact retry, preserving an ordinary suffix', async (bulk) => {
    const raw = commandDocument();
    const parent = raw.parent_revision.payload;
    const clips = [
      { id: 'x', track: 'V1', at: 1, hold: 4, clipType: 'hold', transition: { type: 'crossfade', duration: 0.5, revision: 'x-revision', params: { opaque: null } } },
      { id: 'y', track: 'V1', at: 9, hold: 4, clipType: 'hold', transition: { type: 'crossfade', duration: 0.75, revision: 'y-revision', params: { opaque: [false, null] } } },
    ];
    parent.clips = structuredClone(clips);
    parent.config = { ...parent.config as object, clips: structuredClone(clips) };
    raw.parent_revision.content_digest = fixtureDigest(parent);
    const { env, hook, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted(await environment(raw));
    env.setFault('lost');
    act(() => submitClipMove(captureClipMove(hook.result.current.commands.port,
      hook.result.current.commit.dataRef.current!, 'x'), 5));
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    const [original] = await env.outboxes.list(scope);
    const requestA = original.pending!.request;
    const wireA = structuredClone(env.commits()[0]);
    expect((await env.provider.loadTimelineCommandBasis(scope.timelineId)).head)
      .toEqual({ revisionId: 'r1', publicationId: 'p1' });
    const displayed = hook.result.current.commit.dataRef.current!;
    expect(displayed.head).toMatchObject({ headRevisionId: 'r0', headPublicationId: 'p0' });
    expect(displayed.editProjection).toMatchObject({ kind: 'local', base: env.initial.head });
    const port = hook.result.current.commands.clipScalarPort!;
    const capture = vi.spyOn(port, 'capture');
    const finish = vi.spyOn(port, bulk ? 'finishBatch' : 'finish');
    const captured = (bulk ? ['x', 'y'] : ['x']).map((id) => captureClipScalarEdit(port, displayed, id));
    const bases = structuredClone(captured.map((edit) => edit.basis));
    act(() => {
      if (bulk) submitClipTransitionClears(captured);
      else submitClipScalarEdit(captured[0], { values: {}, clear: ['transition'] });
    });
    await waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [withB] = await env.outboxes.list(scope);
    const intentB = structuredClone(withB.intents[1]);
    const commandsB = (intentB.payload as { commands: unknown[] }).commands;
    expect(commandsB).toHaveLength(bulk ? 2 : 1);
    for (const [index, command] of commandsB.entries()) {
      expect(command).toMatchObject({ op: 'clip.set', version: '1', select: `parent/clip:${clips[index].id}`,
        args: { values: {}, clear: ['transition'] },
        expect: { [`parent/clip:${clips[index].id}::transition`]: { state: 'present', value: clips[index].transition } } });
    }
    expect(intentB).toMatchObject({ basis: { after: original.intents[0].id }, payload: { displayBasis: env.initial } });
    expect(intentB.readyBase).toBeUndefined();
    // Both scalar removal and the ordinary move preview use compileTimelinePatch in the mounted hook.
    act(() => submitClipMove(captureClipMove(hook.result.current.commands.port,
      hook.result.current.commit.dataRef.current!, 'x'), 7));
    await waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(3));
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    const [queued] = await env.outboxes.list(scope);
    const commandsC = (queued.intents[2].payload as { commands: unknown[] }).commands;
    expect(queued.pending).toEqual(original.pending);
    expect(queued.intents.slice(0, 2)).toEqual(withB.intents);
    expect(queued.intents[2]).toMatchObject({ basis: { after: intentB.id } });
    expect(commandsC).toMatchObject([{ op: 'clip.move', args: { on: 7 },
      expect: { 'parent/clip:x::at': { state: 'present', value: 5 } } }]);
    expect(env.commits()).toEqual([wireA]);
    const expected = clips.map((clip, index) => {
      const moved = index ? clip : { ...clip, at: 7 };
      if (!bulk && index) return moved;
      const { transition: _transition, ...cleared } = moved;
      return cleared;
    });
    for (const config of [hook.result.current.commit.data!.config, hook.result.current.commit.data!.resolvedConfig]) {
      expect([...config.clips].sort((a, b) => a.id.localeCompare(b.id))).toEqual(expected);
    }
    expect(hook.result.current.commit.data!.head).toMatchObject({ headRevisionId: 'r0', headPublicationId: 'p0' });
    expect(hook.result.current.commit.data!.editProjection).toMatchObject({ kind: 'local', base: env.initial.head });
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(env.commits()).toHaveLength(4);
    expect(env.commits()[1]).toEqual(wireA);
    expect(env.commits()[1]).toMatchObject({ bodyText: requestA.body, key: requestA.key });
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: commandsB });
    expect(env.commits()[2].body!.commands).toEqual(commandsB);
    expect(env.commits()[3].body).toMatchObject({ base_revision_id: 'r2', base_publication_id: 'p2', commands: commandsC });
    expect(new Set(env.commits().map((call) => call.key)).size).toBe(3);
    expect(captured.map((edit) => edit.basis)).toEqual(bases);
    expect(capture).toHaveBeenCalledTimes(bulk ? 2 : 1);
    expect(finish).toHaveBeenCalledOnce();
    expect(hook.result.current.commands.state.status).toBe('saved');
    const accepted = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect(accepted.head).toEqual({ revisionId: 'r3', publicationId: 'p3' });
    expect(hook.result.current.commit.data!.editProjection).toEqual({ kind: 'accepted', head: accepted.head });
    const expectedAccepted = expected.map((clip) => clip.id === 'x'
      ? { ...clip, app: { astrid: { fixed_start: true, for: 4 } } } : clip);
    for (const config of [hook.result.current.commit.data!.config, hook.result.current.commit.data!.resolvedConfig]) {
      expect(config.clips).toEqual(expectedAccepted);
    }
    expect(accepted.canonicalDocument.parent_revision.payload.clips).toEqual(expectedAccepted);
    expect((accepted.canonicalDocument.parent_revision.payload.config as { clips: unknown }).clips).toEqual(expectedAccepted);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake'))
      .toEqual(env.commits());
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });

});
