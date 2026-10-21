// @vitest-environment jsdom
import { createElement, type ReactNode } from 'react';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { document as commandDocument, environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { PUBLIC_TIMELINE_SERVICE_HOOKS } from '../runtime/timelineHostServiceHooks.ts';
import type { TimelineHostServiceHooks } from '../runtime/timelineHostServiceHooks.ts';
import { useTimelineState } from './useTimelineState.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';
import { useKeyboardShortcuts } from './useKeyboardShortcuts.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { TimelineSchemaIncompatibleError } from '../data/DataProvider.ts';
import { loadTimelineDraft } from '../data/timelineDraftIndexedDb.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';

// Query delivery is controlled; save, history, command session, provider and
// store assembly remain real. No renderer is needed for history ingress.
vi.mock('./useTimelineQueries.ts', () => ({
  useTimelineQueries: (_provider: unknown, _id: string, _resolver: unknown, initial: unknown) => ({
    timelineQuery: { data: initial, isLoading: false, error: null, refetch: vi.fn() },
    assetRegistryQuery: { data: (initial as { registry: unknown }).registry },
  }),
}));
vi.mock('./useRenderState.ts', () => ({ useRenderState: () => ({ setRenderDirty: vi.fn() }) }));

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

async function mounted(
  raw = commandDocument(),
  existing?: Awaited<ReturnType<typeof environment>>,
  timelineServices: TimelineHostServiceHooks = PUBLIC_TIMELINE_SERVICE_HOOKS,
) {
  const env = existing ?? await environment(raw);
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const error = vi.fn();
  const runtime = { provider: env.provider, timelineId: 'timeline-commit', userId: 'actor-1',
    project: { projectId: 'project-commit' }, shots: { canonicalDraft: null, shots: [], isLoading: false },
    toast: { error, success: vi.fn() }, assetResolver: { resolveAssetUrl: async (file: string) => file },
  } as unknown as VideoEditorRuntimeContextValue;
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const loaded = existing ? await latestData(env) : env.current();
  const wrapper = ({ children }: { children: ReactNode }) => createElement(QueryClientProvider, { client },
    createElement(VideoEditorRuntimeProvider, { value: runtime }, children));
  const hook = renderHook(({ loaded }) => {
    const state = useTimelineState(timelineServices, loaded);
    useKeyboardShortcuts({ hasSelectedClip: false, canMoveSelectedClipToTrack: false,
      precisionEnabled: false, selectedClipIds: new Set(), timelineFps: 30,
      undo: state.chrome.undo, redo: state.chrome.redo,
      moveSelectedClipsToTrack: vi.fn(), nudgeSelectedClipsInTime: vi.fn(), selectAllClips: vi.fn(),
      togglePlayPause: vi.fn(), seekRelative: vi.fn(), toggleMute: vi.fn(), splitSelectedClip: vi.fn(),
      deleteSelectedClip: vi.fn(), clearSelection: vi.fn() });
    return state;
  }, { wrapper, initialProps: { loaded } });
  act(() => { hook.result.current.store.getState().setMounted(true); });
  await waitFor(() => expect(hook.result.current.editorOps.clipMove).toBeDefined());
  const commands = createTimelineCommands(hook.result.current.store);
  return { env, hook, commands, error, saveTimeline, saveTimelineAtHead, held };
}

async function latestData(env: Awaited<ReturnType<typeof environment>>) {
  const basis = await env.provider.loadTimelineCommandBasis('timeline-commit');
  const parent = basis.canonicalDocument.parent_revision.payload;
  return buildTimelineData({ ...parent.config as object, clips: parent.clips } as never,
    parent.registry as never, undefined, 2, undefined, { projectId: 'project-commit', timelineId: 'timeline-commit',
      headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
}

describe('mounted editor history authority', () => {
  it('passes the provider-bound native addClip facade into the mounted asset consumer', async () => {
    const env = await environment();
    const selection = {
      asset: 'prepared-asset',
      generation_id: 'prepared-generation',
      variant_id: 'prepared-variant',
      object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
      catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
    } as const;
    const verifiedRead = vi.spyOn(env.provider, 'getProjectVerifiedMedia').mockResolvedValue({
      selection: { ...selection },
      media_type: 'video/mp4',
      size: 1,
      duration_seconds: 1,
    });
    const legacySave = vi.spyOn(env.provider, 'saveTimeline');
    let received: { commands?: { addClip: (...args: never[]) => unknown } } | undefined;
    const timelineServices: TimelineHostServiceHooks = {
      ...PUBLIC_TIMELINE_SERVICE_HOOKS,
      useAssetManagement(args) {
        received = args as typeof received;
        const fallback = PUBLIC_TIMELINE_SERVICE_HOOKS.useAssetManagement(args);
        return {
          ...fallback,
          // This is the row-local consumer contract supplied by App2's exact
          // restore patch: prepared video rows call the injected native facade.
          handleAssetDrop: (...input: Parameters<typeof fallback.handleAssetDrop>) => {
            const prepared = input[5];
            if (!prepared || !received?.commands) return false;
            return Promise.resolve(received.commands.addClip({
              preparedAsset: prepared,
              ...(input[1] !== undefined ? { trackId: input[1] } : {}),
              time: input[2],
            } as never)).then((result) => Boolean((result as { ok?: unknown })?.ok));
          },
        } as never;
      },
    };
    const { hook } = await mounted(undefined, env, timelineServices);
    await waitFor(() => expect(received?.commands?.addClip).toBeTypeOf('function'));
    const nativePort = {
      capture: vi.fn(() => ({ media: selection }) as never),
      finish: vi.fn(() => ({
        command: { op: 'clip.add-media' },
        preview: { version: 1, source: 'test', operations: [] },
      }) as never),
      submit: vi.fn(),
    };
    hook.result.current.store.getState().syncOpsSlice({
      ...hook.result.current.store.getState().ops,
      parentClipAddMedia: nativePort as never,
    });

    const preparedAsset = {
      assetKey: selection.asset,
      mediaType: 'video' as const,
      durationSeconds: 1,
      source: 'registered' as const,
      entry: { file: 'https://runtime.test/prepared.mp4', type: 'video/mp4', duration: 1 },
      mediaSelection: selection,
    };
    await expect(hook.result.current.editor.handleAssetDrop(
      selection.asset, 'V1', 3, false, false, preparedAsset,
    )).resolves.toBe(true);
    expect(verifiedRead).toHaveBeenCalledWith('project-commit', selection);
    expect(nativePort.capture).toHaveBeenCalledOnce();
    expect(nativePort.finish).toHaveBeenCalledOnce();
    expect(nativePort.submit).toHaveBeenCalledOnce();
    expect(legacySave).not.toHaveBeenCalled();
  });

  it.each(['undo', 'redo'] as const)('does not rewind an accepted echo through local %s', async (direction) => {
    const raw = commandDocument();
    // Already normalized authored data lets two producers write identical
    // bytes; no digest, closure, acceptance or head is fabricated.
    Object.assign(raw.parent_revision.payload.config, { output: { background: null, background_scale: null,
      file: 'output.mp4', fps: 30, resolution: '1280x720' } });
    const clip = raw.parent_revision.payload.clips[0] as Record<string, unknown>;
    clip.app = { opaque: null, astrid: { fixed_start: true, for: 1 } };
    (raw.parent_revision.payload.config as Record<string, unknown>).clips = structuredClone(raw.parent_revision.payload.clips);
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const { env, hook, commands, saveTimelineAtHead } = await mounted(raw);
    const events = vi.spyOn(TimelineEventBus.prototype, 'emit');
    // Same explicit 410 setup as useTimelineCommandSession.test.tsx. The
    // provider/transport fixture covers commits and immutable reads, not the
    // retired snapshot endpoint; never make that endpoint succeed here.
    saveTimelineAtHead.mockRejectedValue(new TimelineSchemaIncompatibleError('timeline_commit_required', []));
    act(() => { expect(commands.updateClip({ clipId: 'x', patch: { at: 5 } }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.chrome.schemaIncompatible).toEqual([]));
    expect(hook.result.current.chrome.canUndo).toBe(true);
    expect(hook.result.current.editorData.data?.editProjection).toBeUndefined();
    expect((await loadTimelineDraft('timeline-commit'))?.draft.config.clips[0].at).toBe(5);
    const local = hook.result.current.editorData.data!;
    if (direction === 'redo') {
      act(() => { hook.result.current.chrome.undo(); });
      expect(hook.result.current.editorData.data?.config.clips[0].at).toBe(1);
      expect(hook.result.current.chrome.canRedo).toBe(true);
    }
    await waitFor(async () => expect((await loadTimelineDraft('timeline-commit'))?.draft.config.clips[0].at)
      .toBe(direction === 'undo' ? 5 : 1));
    const kept = await loadTimelineDraft('timeline-commit');

    // Another editor accepts the same authored bytes through real command
    // capture, the raw-closure provider and its guarded HTTP fixture.
    const remote = await env.mount();
    env.move(remote, direction === 'undo' ? 5 : 1);
    await remote.flush();
    await remote.dispose();
    const accepted = await latestData(env);
    expect(accepted.head).toMatchObject({ headRevisionId: direction === 'undo' ? 'r1' : 'r0', headPublicationId: 'p1' });
    expect(accepted.stableSignature).toBe(direction === 'undo' ? local.stableSignature : hook.result.current.editorData.data?.stableSignature);
    act(() => { hook.rerender({ loaded: accepted }); });
    await waitFor(() => expect(hook.result.current.editorData.data?.editProjection).toEqual({
      kind: 'accepted', head: { revisionId: accepted.head!.headRevisionId, publicationId: accepted.head!.headPublicationId },
    }));
    const savesBefore = events.mock.calls.filter(([name]) => name === 'scheduleSave').length;
    const commitsBefore = env.commits().length;
    act(() => { hook.result.current.chrome[direction](); });
    // Accepted history may only change through a Runtime inverse. Local
    // snapshot undo must not replace this accepted projection or save it.
    expect.soft(hook.result.current.editorData.data?.config.clips[0].at).toBe(direction === 'undo' ? 5 : 1);
    expect.soft(hook.result.current.editorData.data?.editProjection).toEqual({
      kind: 'accepted', head: { revisionId: accepted.head!.headRevisionId, publicationId: accepted.head!.headPublicationId },
    });
    expect.soft(events.mock.calls.filter(([name]) => name === 'scheduleSave')).toHaveLength(savesBefore);
    expect(env.commits()).toHaveLength(commitsBefore);
    expect(hook.result.current.chrome.canUndo).toBe(false);
    expect(hook.result.current.chrome.canRedo).toBe(false);
    expect(await loadTimelineDraft('timeline-commit')).toEqual(kept);
    // Reload the immutable accepted closure: local history did not change it.
    const server = await latestData(env);
    expect(server.config.clips[0].at).toBe(direction === 'undo' ? 5 : 1);
  });

  it.each(['undo', 'redo'] as const)('keeps unsent %s through a same-head URL refresh', async (direction) => {
    const raw = commandDocument();
    raw.parent_revision.payload.registry = { assets: { image: { file: 'image.png', type: 'image/png' } } };
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const { env, hook, commands, saveTimelineAtHead } = await mounted(raw, await environment(raw));
    saveTimelineAtHead.mockRejectedValue(new TimelineSchemaIncompatibleError('timeline_commit_required', []));
    act(() => { expect(commands.updateClip({ clipId: 'x', patch: { at: 5 } }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.chrome.schemaIncompatible).toEqual([]));
    if (direction === 'redo') act(() => { hook.result.current.chrome.undo(); });
    await waitFor(async () => expect((await loadTimelineDraft('timeline-commit'))?.draft.config.clips[0].at)
      .toBe(direction === 'undo' ? 5 : 1));
    const current = hook.result.current.editorData.data!;
    const kept = await loadTimelineDraft('timeline-commit');
    const basisReads = vi.spyOn(env.provider, 'loadTimelineCommandBasis');
    const echo = await buildTimelineData(current.config, current.registry,
      async (file) => `${file}?refreshed`, current.configVersion, undefined, current.head);
    expect(echo.stableSignature).toBe(current.stableSignature);
    expect(echo.head).toEqual(current.head);
    expect(echo.resolvedConfig.registry.image.src).toBe('image.png?refreshed');
    expect(echo.resolvedConfig.registry.image.src).not.toBe(current.resolvedConfig.registry.image.src);
    act(() => { hook.rerender({ loaded: echo }); });
    await waitFor(() => expect(basisReads).toHaveResolved());
    expect(hook.result.current.chrome[direction === 'undo' ? 'canUndo' : 'canRedo']).toBe(true);
    expect(await loadTimelineDraft('timeline-commit')).toEqual(kept);
    act(() => { hook.result.current.chrome[direction](); });
    expect(hook.result.current.editorData.data?.config.clips[0].at).toBe(direction === 'undo' ? 1 : 5);
    expect(env.commits()).toHaveLength(0);
  });

  it.each(['bad', 'delayed', 'superseded'] as const)('retains unsent history while a remote closure is %s', async (mode) => {
    const env = await environment();
    let checkReads = false;
    let release!: () => void;
    const gate = new Promise<void>((resolve) => { release = resolve; });
    const reading = vi.fn();
    const provider = new RuntimeDataProvider({ projectId: 'project-commit',
      baseUrl: `http://history-${crypto.randomUUID()}.test`, token: 'token',
      transport: async (...args) => {
        const response = await env.transport(...args);
        if (checkReads && args[1].includes('/composition-revisions/')) {
          reading();
          if (mode === 'bad') {
            const body = JSON.parse(new TextDecoder().decode(response.body));
            body.content_digest = 'sha256:broken';
            return { ...response, body: new TextEncoder().encode(JSON.stringify(body)) };
          }
          await gate;
        }
        return response;
      } });
    const { hook, commands, saveTimelineAtHead } = await mounted(commandDocument(), { ...env, provider });
    saveTimelineAtHead.mockRejectedValue(new TimelineSchemaIncompatibleError('timeline_commit_required', []));
    act(() => { expect(commands.updateClip({ clipId: 'x', patch: { at: 5 } }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.chrome.schemaIncompatible).toEqual([]));
    const kept = await loadTimelineDraft('timeline-commit');
    const remote = await env.mount();
    env.move(remote, 5);
    await remote.flush();
    await remote.dispose();
    // A query stamp can match the local authored bytes without having passed
    // the separate immutable-closure read used by the command session.
    const current = hook.result.current.editorData.data!;
    const query = { ...current, head: (await latestData(env)).head };
    checkReads = true;
    const reads = vi.spyOn(provider, 'loadTimelineCommandBasis');
    act(() => { hook.rerender({ loaded: query }); });
    await waitFor(() => expect(reading).toHaveBeenCalled());
    if (mode === 'bad') {
      await waitFor(() => expect(hook.result.current.chrome.commandSession?.state.error).toMatch(/digest/i));
    }
    expect(hook.result.current.editorData.data).toBe(current);
    expect(hook.result.current.chrome.canUndo).toBe(true);
    expect(await loadTimelineDraft('timeline-commit')).toEqual(kept);
    if (mode === 'superseded') {
      // Supersede the delayed read. The newer attempt fails verification;
      // neither that query stamp nor the cancelled earlier result is authority.
      checkReads = false;
      reads.mockRejectedValueOnce(new Error('newer closure unavailable'));
      act(() => { hook.rerender({ loaded: { ...query } }); });
      await waitFor(() => expect(hook.result.current.chrome.commandSession?.state.error).toBe('newer closure unavailable'));
    }
    await act(async () => {
      release();
      await Promise.allSettled(reads.mock.results.map((result) => result.value));
    });
    if (mode === 'delayed') {
      await waitFor(() => expect(hook.result.current.editorData.data?.editProjection).toEqual({
        kind: 'accepted', head: { revisionId: query.head!.headRevisionId, publicationId: query.head!.headPublicationId },
      }));
      expect(hook.result.current.chrome.canUndo).toBe(false);
    } else {
      expect(hook.result.current.editorData.data).toBe(current);
      act(() => { hook.result.current.chrome.undo(); });
      expect(hook.result.current.editorData.data?.config.clips[0].at).toBe(1);
    }
    expect(env.commits()).toHaveLength(1);
  });

  it('keeps dependent B local through A acceptance, remote C, refused undo/reload and recovery', async () => {
    const first = await mounted();
    const { env, hook, commands, error, saveTimeline, saveTimelineAtHead } = first;
    env.setFault('lost');
    act(() => {
      expect(commands.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      expect(commands.moveClip({ clipId: 'x', time: 7 }).ok).toBe(true);
    });
    await waitFor(() => expect(hook.result.current.chrome.commandSession?.state.status).toBe('retry'));
    const b = hook.result.current.editorData.data!;
    expect(b.config.clips[0].at).toBe(7);
    expect(b.editProjection).toEqual({ kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' }, generation: 2 });
    await env.provider.undoTimeline({ projectId: 'project-commit', timelineId: 'timeline-commit',
      headRevisionId: 'r1', headPublicationId: 'p1' }, ['p1'], 'remote-c');
    act(() => { hook.result.current.chrome.undo(); });
    await waitFor(() => expect(error).toHaveBeenCalled());
    await expect(hook.result.current.chrome.reloadFromServer()).rejects.toThrow('pending timeline commands');
    await act(async () => { await hook.result.current.chrome.commandSession!.retry(); });
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    expect(env.commits()[3].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ expect: { 'parent/clip:x::at': { state: 'present', value: 5 } } }] });
    expect(hook.result.current.chrome.commandSession?.state.status).toBe('conflict');
    expect(hook.result.current.editorData.data).toBe(b);
    expect(hook.result.current.chrome.canUndo).toBe(false);
    expect(hook.result.current.chrome.canRedo).toBe(false);
    const owner = hook.result.current.chrome.commandSession!.state.ownerId!;
    hook.unmount();
    await waitFor(() => expect(first.held.size).toBe(0));
    const recovered = await mounted(commandDocument(), env);
    await waitFor(() => expect(recovered.hook.result.current.chrome.commandSession?.state.status).toBe('recovery'));
    await act(async () => { await recovered.hook.result.current.chrome.commandSession!.recover(owner); });
    expect(recovered.hook.result.current.chrome.commandSession?.state.status).toBe('conflict');
    expect(recovered.hook.result.current.editorData.data?.config.clips[0].at).toBe(7);
    expect(recovered.hook.result.current.editorData.data?.editProjection).toMatchObject({ kind: 'local',
      base: { revisionId: 'r0', publicationId: 'p0' } });
    await expect(recovered.hook.result.current.chrome.reloadFromServer()).rejects.toThrow('pending timeline commands');
    expect(env.commits()).toHaveLength(4);
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
  });

  it('uses Runtime undo after accepted A while retaining a refused ordinary draft separately', async () => {
    const { env, hook, commands, saveTimelineAtHead, saveTimeline } = await mounted();
    const events = vi.spyOn(TimelineEventBus.prototype, 'emit');
    act(() => { expect(commands.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.editorData.data?.editProjection?.kind).toBe('accepted'));
    saveTimelineAtHead.mockRejectedValue(new TimelineSchemaIncompatibleError('timeline_commit_required', []));
    act(() => { expect(commands.updateClip({ clipId: 'x', patch: { label: 'kept draft' } }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.chrome.schemaIncompatible).toEqual([]));
    expect(hook.result.current.editorData.data?.editProjection).toBeUndefined();
    const kept = await loadTimelineDraft('timeline-commit');
    expect(kept).toMatchObject({ baseHeadRevisionId: 'r1', draft: { config: {
      clips: [expect.objectContaining({ at: 5, label: 'kept draft' })],
    } } });
    const savesBefore = events.mock.calls.filter(([name]) => name === 'scheduleSave').length;
    act(() => { hook.result.current.chrome.undo(); });
    await waitFor(() => expect(hook.result.current.editorData.data?.editProjection).toEqual({
      kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' },
    }));
    expect(env.commits()[1].body?.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p1'] } });
    expect(await loadTimelineDraft('timeline-commit')).toEqual(kept);
    expect(events.mock.calls.filter(([name]) => name === 'scheduleSave')).toHaveLength(savesBefore);
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).toHaveBeenCalledOnce();
  });

  it.each(['chrome', 'keyboard'] as const)('routes %s undo of an accepted move through Runtime inverse', async (ingress) => {
    const { env, hook, commands, saveTimeline, saveTimelineAtHead } = await mounted();
    act(() => { expect(commands.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true); });
    await waitFor(() => expect(hook.result.current.editorData.data?.editProjection).toEqual({
      kind: 'accepted', head: { revisionId: 'r1', publicationId: 'p1' },
    }));
    expect(hook.result.current.chrome.canUndo).toBe(true);
    expect(hook.result.current.chrome.canRedo).toBe(false);
    act(() => {
      if (ingress === 'chrome') hook.result.current.chrome.undo();
      else window.dispatchEvent(new KeyboardEvent('keydown', { key: 'z', ctrlKey: true, cancelable: true }));
    });
    await waitFor(() => expect(hook.result.current.editorData.data?.editProjection).toEqual({
      kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' },
    }));
    expect(env.commits()).toHaveLength(2);
    expect(env.commits()[1].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'timeline.inverse', args: { publications: ['p1'] } }] });
    expect(hook.result.current.editorData.data?.config.clips[0].at).toBe(1);
    act(() => { hook.result.current.chrome.redo(); });
    expect(env.commits()).toHaveLength(2);
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
  });
});
