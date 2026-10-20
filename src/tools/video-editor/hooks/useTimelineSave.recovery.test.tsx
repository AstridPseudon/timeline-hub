// @vitest-environment jsdom
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { getStableConfigSignature } from '@/tools/video-editor/lib/config-utils.ts';
import { clearTimelineDraft, loadTimelineDraft, saveTimelineDraft } from '@/tools/video-editor/data/timelineDraftIndexedDb.ts';
import * as timelineDraftStore from '@/tools/video-editor/data/timelineDraftIndexedDb.ts';
import type { DataProvider } from '@/tools/video-editor/data/DataProvider.ts';
import type { TimelineConfig } from '@/tools/video-editor/types/index.ts';

const recovery = vi.hoisted(() => ({
  data: null as Record<string, unknown> | null,
  commitData: vi.fn(),
  persistence: null as Record<string, unknown> | null,
  persistenceOptions: null as { onCanonicalReloadStart?: () => void } | null,
  commandOptions: null as { initialReadReady?: boolean } | null,
}));

vi.stubGlobal('indexedDB', createFakeIndexedDB());
vi.mock('@/tools/video-editor/hooks/useTimelineCommit.ts', () => ({
  useTimelineCommit: () => recovery.data,
}));
vi.mock('@/tools/video-editor/hooks/useTimelinePersistence.ts', () => ({
  useTimelinePersistence: (options: { onCanonicalReloadStart?: () => void }) => {
    recovery.persistenceOptions = options;
    return recovery.persistence;
  },
}));
vi.mock('@/tools/video-editor/hooks/useTimelineCommandSession.ts', () => ({
  useTimelineCommandSession: (options: { initialReadReady?: boolean }) => {
    recovery.commandOptions = options;
    return {
      enabled: false,
      activeRef: { current: false },
      ownsHistoryRef: { current: false },
      flush: vi.fn(),
      state: { status: 'saved' },
      port: null,
    };
  },
}));
vi.mock('@/tools/video-editor/hooks/usePollSync.ts', () => ({ usePollSync: vi.fn() }));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => ({ timelineId: 'session-new', assetResolver: undefined, shots: {} }),
}));

import { useTimelineSave } from './useTimelineSave.ts';
import { createTimelineStore } from './timelineStore.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';

describe('useTimelineSave stable occurrence recovery', () => {
  const recoveryKey = 'parent:shot:occurrence';
  const config: TimelineConfig = {
    ...createDefaultTimelineConfig(),
    clips: [{ id: 'recovered-clip', track: 'V1', clipType: 'hold', at: 0, hold: 2 }],
  };
  const registry = { assets: {} };

  beforeEach(async () => {
    resetFakeIndexedDB();
    recovery.commitData.mockReset();
    recovery.data = null;
    recovery.persistence = null;
    recovery.persistenceOptions = null;
    recovery.commandOptions = null;
    await clearTimelineDraft(recoveryKey);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('retries the initial check for the reloaded generation after its read goes stale', async () => {
    const initialData = await buildTimelineData(config, registry, undefined, 1);
    const canonicalData = await buildTimelineData({
      ...config,
      clips: [{ id: 'canonical-clip', track: 'V1', clipType: 'hold', at: 0, hold: 3 }],
    }, registry, undefined, 2);
    recovery.data = {
      data: initialData,
      dataRef: { current: initialData },
      selectedClipId: null,
      selectedTrackId: null,
      setSelectedTrackId: vi.fn(),
      applyEdit: vi.fn(),
      patchRegistry: vi.fn(),
      unpatchRegistry: vi.fn(),
      commitData: recovery.commitData,
      editSeqRef: { current: 0 },
      pendingOpsRef: { current: 0 },
      selectedClipIdRef: { current: null },
      selectedTrackIdRef: { current: null },
    };
    const resumeDeferredRecoverySave = vi.fn();
    recovery.persistence = {
      scheduleSave: vi.fn(),
      resumeDeferredRecoverySave,
      clearDeferredRecoverySave: vi.fn(),
      flushPendingSave: vi.fn(async () => 1),
      saveStatus: 'saved',
      isConflictExhausted: false,
      isConflictExhaustedRef: { current: false },
      schemaIncompatible: null,
      isSavingRef: { current: false },
      canonicalReloadInProgressRef: { current: false },
      reloadFromServer: vi.fn(),
      retrySaveAfterConflict: vi.fn(),
      watchdogTripped: false,
      watchdogReason: null,
      retryWatchdog: vi.fn(),
      retryPendingSave: vi.fn(),
      loadedBundleRef: { current: null },
    };

    let releaseInitialRead!: (record: null) => void;
    const initialRead = new Promise<null>((resolve) => { releaseInitialRead = resolve; });
    let releaseCurrentRead!: (record: null) => void;
    const currentRead = new Promise<null>((resolve) => { releaseCurrentRead = resolve; });
    const loadDraft = vi.spyOn(timelineDraftStore, 'loadTimelineDraft')
      .mockReturnValueOnce(initialRead)
      .mockReturnValueOnce(currentRead);
    const provider = { resolveAssetUrl: async (file: string) => file } as unknown as DataProvider;
    const hook = renderHook(() => useTimelineSave({ timelineQuery: { isLoading: false } } as never,
      provider, { current: createInteractionState() }, createTimelineStore()));

    expect(recovery.commandOptions?.initialReadReady).toBe(false);
    expect(loadDraft).toHaveBeenCalledTimes(1);

    await act(async () => {
      recovery.persistenceOptions?.onCanonicalReloadStart?.();
      recovery.data = { ...recovery.data!, data: canonicalData, dataRef: { current: canonicalData } };
      hook.rerender();
    });
    expect(recovery.commandOptions?.initialReadReady).toBe(false);

    await act(async () => { releaseInitialRead(null); await Promise.resolve(); });
    await waitFor(() => expect(loadDraft).toHaveBeenCalledTimes(2));
    expect(recovery.commandOptions?.initialReadReady).toBe(false);
    await act(async () => { releaseCurrentRead(null); await Promise.resolve(); });
    await waitFor(() => expect(recovery.commandOptions?.initialReadReady).toBe(true));
    expect(resumeDeferredRecoverySave).toHaveBeenCalledTimes(1);

    hook.unmount();
    loadDraft.mockRestore();
  });

  it.each([true, false])('compares source-inclusive recovery with its server snapshot (same source: %s)', async (sameSource) => {
    const items = [{
      id: 'source:segment', shape: 'interval' as const, domain: 'source_seconds' as const,
      extent: { start: 0, end: 1 }, schemaRef: 'astrid.transcript_segment/v1',
      sourceArtifactRef: { assetId: 'asset-1' }, provenance: { adapterId: 'test', adapterVersion: '1' },
      payload: { sourceId: 'source', segmentId: 'segment', text: 'Saved source' },
    }];
    const sourceItemsBySchemaRef = { 'astrid.transcript_segment/v1': items };
    const loaded = await buildTimelineData(config, registry, undefined, 1, sourceItemsBySchemaRef);
    recovery.data = {
      data: loaded, dataRef: { current: loaded }, selectedClipId: null, selectedTrackId: null,
      setSelectedTrackId: vi.fn(), applyEdit: vi.fn(), patchRegistry: vi.fn(), unpatchRegistry: vi.fn(),
      commitData: recovery.commitData, editSeqRef: { current: 0 }, pendingOpsRef: { current: 0 },
      selectedClipIdRef: { current: null }, selectedTrackIdRef: { current: null },
    };
    recovery.persistence = {
      scheduleSave: vi.fn(), resumeDeferredRecoverySave: vi.fn(), clearDeferredRecoverySave: vi.fn(),
      flushPendingSave: vi.fn(async () => 1), saveStatus: 'saved', isConflictExhausted: false,
      schemaIncompatible: null, isSavingRef: { current: false }, reloadFromServer: vi.fn(),
      retrySaveAfterConflict: vi.fn(), watchdogTripped: false, watchdogReason: null,
      retryWatchdog: vi.fn(), loadedBundleRef: { current: null },
    };
    const draftItems = sameSource ? items : items.map((item) => ({ ...item, payload: { ...item.payload, text: 'Unsaved correction' } }));
    const bundle = { schema_version: 1, itemsBySchemaRef: { 'astrid.transcript_segment/v1': draftItems } };
    await saveTimelineDraft('session-new', { config: loaded.config, registry, bundle }, 1);
    const provider = { resolveAssetUrl: async (file: string) => file } as unknown as DataProvider;
    const hook = renderHook(() => useTimelineSave({ timelineQuery: { isLoading: false } } as never,
      provider, { current: createInteractionState() }, createTimelineStore()));
    if (sameSource) {
      await waitFor(async () => expect(await loadTimelineDraft('session-new')).toBeNull());
      expect(hook.result.current.recoveryDraft).toBeNull();
    } else {
      await waitFor(() => expect(hook.result.current.recoveryDraft).not.toBeNull());
      expect((await loadTimelineDraft('session-new'))?.draft.bundle).toEqual(bundle);
    }
    hook.unmount();
  });

  it('shows a hydrated draft as dirty/retryable and retries it without another edit', async () => {
    const stableSignature = getStableConfigSignature(config, registry);
    recovery.data = {
      data: {
        config,
        registry,
        stableSignature,
        dataRef: { current: { config, registry, stableSignature } },
      },
      dataRef: { current: { config, registry, stableSignature } },
      selectedClipId: null,
      selectedTrackId: null,
      setSelectedTrackId: vi.fn(),
      applyEdit: vi.fn(),
      patchRegistry: vi.fn(),
      unpatchRegistry: vi.fn(),
      commitData: recovery.commitData,
      editSeqRef: { current: 0 },
      pendingOpsRef: { current: 0 },
      selectedClipIdRef: { current: null },
      selectedTrackIdRef: { current: null },
    };
    const reloadFromServer = vi.fn(async () => { await clearTimelineDraft(recoveryKey); });
    reloadFromServer.mockRejectedValueOnce(new Error('canonical reload failed'));
    recovery.persistence = {
      scheduleSave: vi.fn(),
      resumeDeferredRecoverySave: vi.fn(),
      clearDeferredRecoverySave: vi.fn(),
      flushPendingSave: vi.fn(async () => 1),
      saveStatus: 'saved',
      isConflictExhausted: false,
      schemaIncompatible: null,
      isSavingRef: { current: false },
      reloadFromServer,
      retrySaveAfterConflict: vi.fn(),
      watchdogTripped: false,
      watchdogReason: null,
      retryWatchdog: vi.fn(),
      loadedBundleRef: { current: null },
    };
    const provider = {
      getTimelineDraftRecoveryMetadata: () => ({ recoveryKey }),
      resolveAssetUrl: async (file: string) => file,
    } as unknown as DataProvider;
    await saveTimelineDraft('old-session', { config, registry }, 7, {
      recoveryKey,
      draftIdentity: 'pending-publication',
    });
    const store = createTimelineStore();
    const queries = { timelineQuery: { isLoading: false } } as never;
    const hook = renderHook(() => useTimelineSave(queries, provider, {
      current: createInteractionState(),
    }, store));

    await waitFor(() => expect(hook.result.current.recoveryDraft).toMatchObject({ baseVersion: 7 }));
    expect(hook.result.current.saveStatus).toBe('dirty');
    expect(await loadTimelineDraft(recoveryKey)).not.toBeNull();

    await act(async () => { await hook.result.current.retryRecoveredDraft(); });
    expect(recovery.commitData).toHaveBeenCalledWith(
      expect.objectContaining({ config: expect.objectContaining({ clips: config.clips }) }),
      { save: true },
    );
    // Recovery stays visible until the save-success acknowledgement.
    expect(hook.result.current.recoveryDraft).toMatchObject({ baseVersion: 7 });
    expect(await loadTimelineDraft(recoveryKey)).not.toBeNull();

    await act(async () => {
      await expect(hook.result.current.reloadFromServer()).rejects.toThrow('canonical reload failed');
    });
    expect(hook.result.current.recoveryDraft).toMatchObject({ baseVersion: 7 });
    expect(hook.result.current.saveStatus).toBe('dirty');
    expect(await loadTimelineDraft(recoveryKey)).not.toBeNull();

    await act(async () => { await hook.result.current.discardRecoveredDraft(); });
    expect(reloadFromServer).toHaveBeenLastCalledWith({ clearDraft: true });
    expect(hook.result.current.recoveryDraft).toBeNull();
    expect(hook.result.current.saveStatus).toBe('saved');
    expect(await loadTimelineDraft(recoveryKey)).toBeNull();
  });
});
