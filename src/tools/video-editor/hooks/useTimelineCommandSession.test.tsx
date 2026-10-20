// @vitest-environment jsdom
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { createElement, useEffect, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { createInteractionState } from '../lib/interaction-state.ts';
import { buildPendingDragSession, commitDraggingSession } from './useClipDrag.helpers.ts';
import { document as commandDocument, environment, scope } from '../commands/__tests__/commitSessionEnvironment.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createTimelineStore } from './timelineStore.ts';
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
import { captureClipMove, submitClipMove } from '../commands/semanticGestures.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from '../commands/trackLabelGesture.ts';
import { createRecoveryConfig } from './useTimelineSave.draftConfig.ts';

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

async function mounted(existingEnv?: Awaited<ReturnType<typeof environment>>) {
  const env = existingEnv ?? await environment();
  installStorage(env);
  const snapshotSaves = vi.fn();
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const store = createTimelineStore();
  store.getState().setMounted(true);
  const initial = env.current();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider: env.provider, timelineId: 'timeline-commit', shots: { canonicalDraft: null },
    project: { projectId: 'project-commit' }, toast: { error: vi.fn(), success: vi.fn() },
    assetResolver: { resolveAssetUrl: async (value: string) => value } } as unknown as VideoEditorRuntimeContextValue;
  const queries = { timelineQuery: { data: initial, isLoading: false }, assetRegistryQuery: { data: initial.registry } };
  const interactionStateRef = { current: createInteractionState() };
  const wrapper = ({ children }: { children: ReactNode }) => createElement(QueryClientProvider, { client: queryClient },
    createElement(VideoEditorRuntimeProvider, { value: runtime }, children));
  const hook = renderHook(() => {
    const save = useTimelineSave(queries, env.provider, interactionStateRef, store, initial);
    const history = useTimelineHistory({ dataRef: save.dataRef, commitData: save.commitData,
      interactionStateRef, pendingOpsRef: save.pendingOpsRef });
    useEffect(() => save.eventBus.on('beforeCommit', history.onBeforeCommit), [save.eventBus, history.onBeforeCommit]);
    useEffect(() => save.eventBus.on('remoteCommit', history.onRemoteData), [save.eventBus, history.onRemoteData]);
    store.getState().syncSlices({
      data: { ...store.getState().data, data: save.data, resolvedConfig: save.data?.resolvedConfig ?? null, dataRef: save.dataRef },
      ops: { ...store.getState().ops, clipMove: save.commands.port },
    });
    return { commands: save.commands, commit: save, history };
  }, { wrapper });
  hook.result.current.commit.eventBus.on('scheduleSave', snapshotSaves);
  await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
  const service = createTimelineCommands(store);
  return { env, hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead };
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
});
