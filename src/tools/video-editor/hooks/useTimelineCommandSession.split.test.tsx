// @vitest-environment jsdom
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import type { DataProvider, TimelineCommandBasis } from '../data/DataProvider.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { captureClipSplitEdit, submitClipSplitEdit } from '../commands/clipSplitGesture.ts';
import fixture from '../commands/fixtures/recipe_m2_clip_split.json';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { createTimelineStore } from './timelineStore.ts';

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

async function mounted() {
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const canonicalDocument = structuredClone(fixture.input) as TimelineCommandBasis['canonicalDocument'];
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
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider, timelineId: 'film', commit, legacyClean: () => clean,
      resolveAssetUrl: async (file) => file, loaded: undefined, snapshotWriteBlockedRef, headRevisionRef,
      configVersionRef, lastSavedSignatureRef, store, shots: { shots: undefined, isLoading: false, error: null,
        refetchShots: vi.fn(), finalVideoMap: new Map(), dismissFinalVideo: vi.fn(), canonicalDraft: null } });
    return { commit, commands };
  });
  await waitFor(() => expect(hook.result.current.commands.clipSplitPort).toBeDefined());
  return { hook, provider, scheduled, snapshotWriteBlockedRef, setClean: (value: boolean) => { clean = value; } };
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
