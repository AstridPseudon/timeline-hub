// @vitest-environment jsdom
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import type { DataProvider, TimelineCommandBasis } from '../data/DataProvider.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { captureClipSplitEdit, submitClipSplitEdit } from '../commands/clipSplitGesture.ts';
import fixture from '../commands/fixtures/recipe_m2_clip_split.json';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { useClipEditing } from './useClipEditing.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { createTimelineStore } from './timelineStore.ts';

vi.mock('@/shared/components/ui/runtime/sonner.tsx', () => ({ toast: { error: vi.fn() } }));

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

async function mounted(database = createFakeIndexedDB(), changeDocument?: (document: TimelineCommandBasis['canonicalDocument']) => void) {
  vi.stubGlobal('indexedDB', database);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const canonicalDocument = structuredClone(fixture.input) as TimelineCommandBasis['canonicalDocument'];
  changeDocument?.(canonicalDocument);
  const basis = { canonicalDocument, head: { revisionId: 'parent-1', publicationId: 'pub-0' } };
  const parent = canonicalDocument.parent_revision.payload;
  const initial = await buildTimelineData(parent.config as never, parent.registry as never, undefined, 1, undefined,
    { projectId: 'project-1', timelineId: 'film', headRevisionId: 'parent-1', headPublicationId: 'pub-0' });
  const provider = {
    loadTimelineCommandBasis: vi.fn(async () => basis),
    getRecoverableIdentity: vi.fn(async () => ({ realmId: 'realm-1', actorId: 'actor-1' })),
    commitTimeline: vi.fn(async () => { throw new Error('lost acknowledgement'); }),
    saveTimeline: vi.fn(), saveTimelineAtHead: vi.fn(),
  } as unknown as DataProvider;
  const eventBus = new TimelineEventBus();
  const scheduled = vi.fn();
  eventBus.on('scheduleSave', scheduled);
  const snapshotWriteBlockedRef = { current: false };
  const headRevisionRef = { current: initial.head };
  const configVersionRef = { current: initial.configVersion };
  const lastSavedSignatureRef = { current: initial.stableSignature };
  const store = createTimelineStore();
  let clean = true;
  const applyEdit = vi.fn();
  const selectClip = vi.fn();
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider, timelineId: 'film', commit, legacyClean: () => clean,
      resolveAssetUrl: async (file) => file, loaded: undefined, snapshotWriteBlockedRef, headRevisionRef,
      configVersionRef, lastSavedSignatureRef, store, shots: { shots: undefined, isLoading: false, error: null,
        refetchShots: vi.fn(), finalVideoMap: new Map(), dismissFinalVideo: vi.fn(), canonicalDraft: null } });
    const editing = useClipEditing({ dataRef: commit.dataRef, resolvedConfig: commit.data?.resolvedConfig ?? null,
      selectedClipId: 'clip-a', selectedTrack: null, currentTime: 3, selectClip,
      setSelectedTrackId: vi.fn(), applyEdit, clipSplit: commands.clipSplitPort });
    return { commit, commands, editing };
  });
  await waitFor(() => expect(hook.result.current.commands.clipSplitPort).toBeDefined());
  return { hook, provider, scheduled, snapshotWriteBlockedRef, applyEdit, selectClip, store, setClean: (value: boolean) => { clean = value; } };
}

describe('staged single-parent split at the mounted command-session boundary', () => {
  it('installs one full-row preview through the UI adapter and retains it for exact pending retry', async () => {
    const { hook, provider, scheduled, snapshotWriteBlockedRef } = await mounted();
    const current = hook.result.current.commit.data!;
    const captured = captureClipSplitEdit(hook.result.current.commands.clipSplitPort, current, 'clip-a', 3, 'right');
    const original = structuredClone(captured.basis);
    expect(hook.result.current.commit.data).toBe(current);
    const commitData = vi.spyOn(hook.result.current.commit, 'commitData');
    act(() => { submitClipSplitEdit(captured); });
    expect(commitData).toHaveBeenCalledOnce();
    expect(commitData.mock.calls[0][1]).toEqual({ save: false, skipHistory: true });
    const draft = hook.result.current.commit.data!;
    expect(draft.config.clips).toEqual(fixture.output.parent_revision.payload.clips);
    expect(draft.registry).toBe(current.registry);
    expect(draft.config.output).toEqual(current.config.output);
    expect(draft.editProjection?.kind).toBe('local');
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    expect(snapshotWriteBlockedRef.current).toBe(true);
    expect(provider.commitTimeline).toHaveBeenCalledOnce();
    const first = structuredClone(vi.mocked(provider.commitTimeline!).mock.calls[0]);
    expect(first[0].commands).toEqual(fixture.commands);
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(vi.mocked(provider.commitTimeline!).mock.calls[1]).toEqual(first);
    expect(hook.result.current.commit.data).toBe(draft);
    expect(captured.basis).toEqual(original);
    expect(commitData).toHaveBeenCalledOnce();
    expect(scheduled).not.toHaveBeenCalled();
    expect(provider.saveTimeline).not.toHaveBeenCalled();
    expect(provider.saveTimelineAtHead).not.toHaveBeenCalled();
    hook.unmount();
  });

  it('fences capture, finish and submit behind earlier snapshot work and permits abandoning capture', async () => {
    const { hook, provider, scheduled, setClean } = await mounted();
    const port = hook.result.current.commands.clipSplitPort!;
    const current = hook.result.current.commit.data!;
    const input = { clipId: 'clip-a', on: 3, rightId: 'right', current };
    setClean(false);
    expect(() => port.capture(input)).toThrow('earlier timeline saves');
    setClean(true);
    const basis = port.capture(input);
    setClean(false);
    expect(() => port.finish(basis)).toThrow('earlier timeline saves');
    setClean(true);
    const prepared = port.finish(basis);
    setClean(false);
    expect(() => port.submit(prepared)).toThrow('earlier timeline saves');
    expect(hook.result.current.commit.data).toBe(current);
    expect(provider.commitTimeline).not.toHaveBeenCalled();
    expect(scheduled).not.toHaveBeenCalled();
    hook.unmount();
  });
});


describe('production single-parent split ingress', () => {
  it.each(['selected', 'context menu', 'keyboard'] as const)('routes %s through actual hook capture/finish/submit exactly once', async (ingress) => {
    const env = await mounted();
    const port = env.hook.result.current.commands.clipSplitPort!;
    const capture = vi.spyOn(port, 'capture');
    const finish = vi.spyOn(port, 'finish');
    const submit = vi.spyOn(port, 'submit');
    const run = () => {
      const editing = env.hook.result.current.editing;
      if (ingress === 'selected') editing.handleSplitSelectedClip();
      else if (ingress === 'context menu') editing.handleSplitClipAtTime('clip-a', 3);
      else editing.handleSplitClipsAtPlayhead(['clip-a', 'clip-a']);
    };
    act(() => { run(); run(); });
    await waitFor(() => expect(env.hook.result.current.commands.state.status).toBe('retry'));
    expect(capture).toHaveBeenCalledOnce();
    expect(finish).toHaveBeenCalledOnce();
    expect(submit).toHaveBeenCalledOnce();
    const reserved = capture.mock.calls[0][0].rightId;
    expect(finish.mock.calls[0][0]).toEqual(capture.mock.results[0].value);
    const request = vi.mocked(env.provider.commitTimeline!).mock.calls[0];
    expect(request[0].commands[0]).toMatchObject({ op: 'clip.split', select: 'parent/clip:clip-a',
      args: { on: 3, right_id: reserved }, created: [`parent/clip:${reserved}`] });
    expect(env.selectClip).toHaveBeenCalledExactlyOnceWith(reserved);
    const draft = env.hook.result.current.commit.data;
    await act(async () => { await env.hook.result.current.commands.retry(); });
    expect(vi.mocked(env.provider.commitTimeline!).mock.calls[1]).toEqual(request);
    expect(env.hook.result.current.commit.data).toBe(draft);
    expect(env.applyEdit).not.toHaveBeenCalled();
    expect(env.scheduled).not.toHaveBeenCalled();
    expect(env.provider.saveTimeline).not.toHaveBeenCalled();
    expect(env.provider.saveTimelineAtHead).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('recovers an unknown-ACK UI split after remount with the original reserved ID and request bytes', async () => {
    const database = createFakeIndexedDB();
    const first = await mounted(database);
    act(() => { first.hook.result.current.editing.handleSplitSelectedClip(); });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    const request = structuredClone(vi.mocked(first.provider.commitTimeline!).mock.calls[0]);
    const owner = first.hook.result.current.commands.state.ownerId!;
    const rightId = request[0].commands[0].args.right_id;
    first.hook.unmount();

    const second = await mounted(database);
    expect(second.hook.result.current.commands.state.status).toBe('recovery');
    expect(second.provider.commitTimeline).not.toHaveBeenCalled();
    const capture = vi.spyOn(second.hook.result.current.commands.clipSplitPort!, 'capture');
    await act(async () => { await second.hook.result.current.commands.recover(owner); });
    await waitFor(() => expect(second.hook.result.current.commands.state.status).toBe('retry'));
    expect(vi.mocked(second.provider.commitTimeline!).mock.calls[0]).toEqual(request);
    expect(second.hook.result.current.commit.data!.config.clips.map((clip) => clip.id))
      .toEqual(['clip-a', rightId, 'clip-b']);
    expect(capture).not.toHaveBeenCalled();
    expect(second.applyEdit).not.toHaveBeenCalled();
    expect(second.scheduled).not.toHaveBeenCalled();
    expect(second.provider.saveTimeline).not.toHaveBeenCalled();
    expect(second.provider.saveTimelineAtHead).not.toHaveBeenCalled();
    second.hook.unmount();
  });

  it('routes the SDK command facade to the same raw session and selects its reserved right ID', async () => {
    const env = await mounted();
    const state = env.store.getState();
    state.syncSlices({ data: { ...state.data, dataRef: env.hook.result.current.commit.dataRef },
      ops: { ...state.ops, clipSplit: env.hook.result.current.commands.clipSplitPort,
        applyEdit: env.applyEdit, selectClip: env.selectClip } });
    const service = createTimelineCommands(env.store);
    let result: ReturnType<typeof service.splitClip>;
    act(() => { result = service.splitClip({ clipId: 'clip-a', time: 3 }); });
    expect(result!).toMatchObject({ ok: true, data: { clipId: 'clip-a' } });
    await waitFor(() => expect(env.provider.commitTimeline).toHaveBeenCalledOnce());
    const command = vi.mocked(env.provider.commitTimeline!).mock.calls[0][0].commands[0];
    expect(result!).toEqual({ ok: true, data: { clipId: 'clip-a', nextClipId: command.args.right_id } });
    expect(env.selectClip).toHaveBeenCalledExactlyOnceWith(command.args.right_id);
    expect(env.applyEdit).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('visibly retains the draft on a valid native capture refusal without an alternate write', async () => {
    const env = await mounted();
    const before = env.hook.result.current.commit.data;
    env.setClean(false);
    act(() => { env.hook.result.current.editing.handleSplitClipAtTime('clip-a', 3); });
    expect(toast.error).toHaveBeenCalledWith('Wait for earlier timeline saves before splitting');
    expect(env.hook.result.current.commit.data).toBe(before);
    expect(env.applyEdit).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    expect(env.scheduled).not.toHaveBeenCalled();
    env.setClean(true);
    act(() => { env.hook.result.current.editing.handleSplitClipAtTime('clip-a', 3); });
    await waitFor(() => expect(env.provider.commitTimeline).toHaveBeenCalledOnce());
    env.hook.unmount();
  });

  it.each(['selected', 'context menu', 'keyboard', 'SDK'] as const)('keeps a positive %s split on the existing writer when a non-target mirror diverges', async (ingress) => {
    const env = await mounted(undefined, (document) => {
      const config = document.parent_revision.payload.config as Record<string, unknown>;
      (config.clips as Array<Record<string, unknown>>)[1].at = 99;
    });
    const port = env.hook.result.current.commands.clipSplitPort!;
    const capture = vi.spyOn(port, 'capture');
    const current = env.hook.result.current.commit.data!;
    expect(port.supports!({ clipId: 'clip-a', current })).toBe(false);
    act(() => {
      const editing = env.hook.result.current.editing;
      if (ingress === 'selected') editing.handleSplitSelectedClip();
      else if (ingress === 'context menu') editing.handleSplitClipAtTime('clip-a', 3);
      else if (ingress === 'keyboard') editing.handleSplitClipsAtPlayhead(['clip-a']);
      else {
        const state = env.store.getState();
        state.syncSlices({ data: { ...state.data, dataRef: env.hook.result.current.commit.dataRef },
          ops: { ...state.ops, clipSplit: port, applyEdit: env.applyEdit, selectClip: env.selectClip } });
        expect(createTimelineCommands(env.store).splitClip({ clipId: 'clip-a', time: 3 }).ok).toBe(true);
      }
    });
    expect(env.applyEdit).toHaveBeenCalledOnce();
    const clips = env.applyEdit.mock.calls[0][0].resolvedConfig.clips;
    expect(clips).toHaveLength(3);
    expect(clips[2]).toEqual(current.resolvedConfig.clips[1]);
    expect(capture).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it.each(['unsupported', 'multi', 'group'] as const)('preserves the existing %s path with the real native port available', async (kind) => {
    const env = await mounted();
    const current = env.hook.result.current.commit.data!;
    const capture = vi.spyOn(env.hook.result.current.commands.clipSplitPort!, 'capture');
    if (kind === 'unsupported') {
      // The native raw basis excludes clip-b's missing moving-media source window.
      act(() => { env.hook.result.current.editing.handleSplitClipAtTime('clip-b', 6); });
      expect(env.applyEdit).toHaveBeenCalledOnce();
    } else if (kind === 'multi') {
      act(() => { env.hook.result.current.editing.handleSplitClipsAtPlayhead(['clip-a', 'clip-b']); });
      expect(env.applyEdit).toHaveBeenCalledOnce();
    } else {
      current.config.pinnedShotGroups = [{ shotId: 'shot', trackId: 'picture', clipIds: ['clip-a'] }] as never;
      act(() => { env.hook.result.current.editing.handleSplitClipAtTime('clip-a', 3); });
      expect(toast.error).toHaveBeenCalledWith('Use Delete shot from the shot menu');
    }
    expect(capture).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    env.hook.unmount();
  });
  it.each(['text', 'animation', 'relation', 'transition'] as const)('keeps a successful %s split on its established writer', async (kind) => {
    const env = await mounted(undefined, (document) => {
      const rows = document.parent_revision.payload.clips as Array<Record<string, unknown>>;
      if (kind === 'text') rows[0].clipType = 'text';
      if (kind === 'animation') rows[0].params = { animation: { opacity: [0, 1] } };
      if (kind === 'relation') rows[0].app = { on: 'literal-anchor' };
      if (kind === 'transition') rows[1].transition = { type: 'fade', duration: 0.1 };
      (document.parent_revision.payload.config as Record<string, unknown>).clips = structuredClone(rows);
    });
    const port = env.hook.result.current.commands.clipSplitPort!;
    const capture = vi.spyOn(port, 'capture');
    expect(port.supports!({ clipId: 'clip-a', current: env.hook.result.current.commit.data! })).toBe(false);
    act(() => { env.hook.result.current.editing.handleSplitClipAtTime('clip-a', 3); });
    expect(env.applyEdit).toHaveBeenCalledOnce();
    expect(env.applyEdit.mock.calls[0][0].resolvedConfig.clips).toHaveLength(3);
    expect(capture).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('keeps an occurrence display without a raw parent binding on its successful existing writer', async () => {
    const env = await mounted();
    const current = env.hook.result.current.commit.data!;
    current.config.clips[0].id = 'literal-occurrence';
    current.resolvedConfig.clips[0].id = 'literal-occurrence';
    const capture = vi.spyOn(env.hook.result.current.commands.clipSplitPort!, 'capture');
    act(() => { env.hook.result.current.editing.handleSplitClipAtTime('literal-occurrence', 3); });
    expect(env.applyEdit).toHaveBeenCalledOnce();
    expect(env.applyEdit.mock.calls[0][0].resolvedConfig.clips).toHaveLength(3);
    expect(capture).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('returns SDK capture refusal without publishing a snapshot or losing the draft', async () => {
    const env = await mounted();
    const state = env.store.getState();
    state.syncSlices({ data: { ...state.data, dataRef: env.hook.result.current.commit.dataRef },
      ops: { ...state.ops, clipSplit: env.hook.result.current.commands.clipSplitPort,
        applyEdit: env.applyEdit, selectClip: env.selectClip } });
    const before = env.hook.result.current.commit.data;
    env.setClean(false);
    const result = createTimelineCommands(env.store).splitClip({ clipId: 'clip-a', time: 3 });
    expect(result).toMatchObject({ ok: false, error: { code: 'mutation_failed',
      message: 'Wait for earlier timeline saves before splitting' } });
    expect(env.hook.result.current.commit.data).toBe(before);
    expect(env.applyEdit).not.toHaveBeenCalled();
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    expect(env.scheduled).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('routes opaque canonical metadata through the raw parent binding without treating it as authority', async () => {
    const opaque = { ownerRef: 'opaque-owner', clipRef: 'literal', rawClipId: 'literal' };
    const env = await mounted(undefined, (document) => {
      const rows = document.parent_revision.payload.clips as Array<Record<string, unknown>>;
      rows[0].app = { ...rows[0].app as object, canonical: opaque };
      (document.parent_revision.payload.config as Record<string, unknown>).clips = structuredClone(rows);
    });
    act(() => { env.hook.result.current.editing.handleSplitSelectedClip(); });
    await waitFor(() => expect(env.provider.commitTimeline).toHaveBeenCalledOnce());
    const draft = env.hook.result.current.commit.data!;
    expect(draft.config.clips[0].app!.canonical).toEqual(opaque);
    expect(draft.config.clips[1].app!.canonical).toEqual(opaque);
    expect(vi.mocked(env.provider.commitTimeline!).mock.calls[0][0].commands[0].select).toBe('parent/clip:clip-a');
    expect(env.applyEdit).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('keeps the SDK legacy split positive when no native port is supplied', async () => {
    const env = await mounted();
    const state = env.store.getState();
    state.syncSlices({ data: { ...state.data, dataRef: env.hook.result.current.commit.dataRef },
      ops: { ...state.ops, clipSplit: undefined, applyEdit: env.applyEdit } });
    const result = createTimelineCommands(env.store).splitClip({ clipId: 'clip-a', time: 3 });
    expect(result.ok).toBe(true);
    expect(env.applyEdit).toHaveBeenCalledOnce();
    expect(env.applyEdit.mock.calls[0][0].resolvedConfig.clips).toHaveLength(3);
    expect(env.provider.commitTimeline).not.toHaveBeenCalled();
    env.hook.unmount();
  });

});
