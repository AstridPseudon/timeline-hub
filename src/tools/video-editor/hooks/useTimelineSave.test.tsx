// @vitest-environment jsdom
import React from 'react';
import { act, renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { useTimelineSave } from './useTimelineSave';
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
    result: { current: ReturnType<typeof useTimelineSave> };
    unmount: () => void;
  };
  saveTimeline: ReturnType<typeof vi.fn>;
}

function setup(
  saveTimelineImpl: DataProvider['saveTimeline'],
  timelineEditability?: TimelineEditability,
  original?: { data: TimelineData; loadBasis: DataProvider['loadTimelineCommandBasis'] },
): SetupResult {
  const saveTimeline = vi.fn(saveTimelineImpl);
  const provider: DataProvider = {
    persistenceEnabled: true,
    loadTimeline: vi.fn(async () => ({ config: createDefaultTimelineConfig(), configVersion: 1 })),
    loadAssetRegistry: vi.fn(async () => ({ assets: {} })),
    saveTimeline,
    resolveAssetUrl: vi.fn(async (file: string) => file),
    ...(original ? { loadTimelineCommandBasis: original.loadBasis } : {}),
  };
  const queries = {
    timelineQuery: { data: undefined, isLoading: false },
    assetRegistryQuery: { data: undefined },
  };
  const interactionStateRef: InteractionStateRef = { current: createInteractionState() };
  const store = createTimelineStore();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = {
    provider,
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
      <VideoEditorRuntimeProvider value={runtime}>{children}</VideoEditorRuntimeProvider>
    </QueryClientProvider>
  );
  const hook = renderHook(
    () => useTimelineSave(queries, provider, interactionStateRef, store, original?.data),
    { wrapper },
  );
  return { hook, saveTimeline };
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
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.useRealTimers();
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
