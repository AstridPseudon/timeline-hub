// @vitest-environment jsdom
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { createElement, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { createInteractionState } from '../lib/interaction-state.ts';
import { buildPendingDragSession, commitDraggingSession } from './useClipDrag.helpers.ts';
import { environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { createTimelineStore } from './timelineStore.ts';
import { useTimelineSave } from './useTimelineSave.ts';
import { loadTimelineDraft } from '../data/timelineDraftIndexedDb.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';

afterEach(() => { vi.unstubAllGlobals(); });

async function mounted() {
  const env = await environment();
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const snapshotSaves = vi.fn();
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const store = createTimelineStore();
  store.getState().setMounted(true);
  const initial = env.current();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider: env.provider, timelineId: 'timeline-commit', shots: { canonicalDraft: null },
    assetResolver: { resolveAssetUrl: async (value: string) => value } } as unknown as VideoEditorRuntimeContextValue;
  const queries = { timelineQuery: { data: initial, isLoading: false }, assetRegistryQuery: { data: initial.registry } };
  const interactionStateRef = { current: createInteractionState() };
  const wrapper = ({ children }: { children: ReactNode }) => createElement(QueryClientProvider, { client: queryClient },
    createElement(VideoEditorRuntimeProvider, { value: runtime }, children));
  const hook = renderHook(() => {
    const save = useTimelineSave(queries, env.provider, interactionStateRef, store, initial);
    store.getState().syncSlices({
      data: { ...store.getState().data, data: save.data, resolvedConfig: save.data?.resolvedConfig ?? null, dataRef: save.dataRef },
      ops: { ...store.getState().ops, clipMove: save.commands.port },
    });
    return { commands: save.commands, commit: save };
  }, { wrapper });
  hook.result.current.commit.eventBus.on('scheduleSave', snapshotSaves);
  await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
  const service = createTimelineCommands(store);
  return { env, hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead };
}

describe('mounted timeline command session', () => {
  it('moves through the actual command service with save:false and hydrates the accepted raw closure', async () => {
    const { hook, service, snapshotSaves, saveTimeline, saveTimelineAtHead } = await mounted();
    await act(async () => {
      expect(service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      await hook.result.current.commands.flush();
    });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data?.head?.headPublicationId).toBe('p1');
    expect(hook.result.current.commands.state.status).toBe('saved');
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    expect(await loadTimelineDraft('timeline-commit')).toBeNull();
    await act(async () => { await hook.result.current.commands.undo(); await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(1);
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
    expect(() => hook.result.current.commit.commitData(hook.result.current.commit.data!)).toThrow('pending timeline commands');
    expect(snapshotSaves).not.toHaveBeenCalled();
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    expect(hook.result.current.commit.data?.head?.headPublicationId).toBe('p2');
    hook.unmount();
  });
});
