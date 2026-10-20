// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import type { CompiledCanonicalTransitions } from '@banodoco/timeline-composition';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment } from '../../commands/__tests__/commitSessionEnvironment.ts';
import type { CommandSessionState } from '../../commands/commitSession.ts';
import { captureClipMove, submitClipMove } from '../../commands/semanticGestures.ts';
import { compilePlayerTransitions } from '../../compositions/playerEvaluation.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import fixture from '../../data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { createTimelineStore, TimelineStoreProvider } from '../../hooks/timelineStore.ts';
import { useTimelineCommandSession } from '../../hooks/useTimelineCommandSession.ts';
import { useTimelineCommit } from '../../hooks/useTimelineCommit.ts';
import { TimelineEventBus } from '../../hooks/useTimelineEventBus.ts';
import type { TimelineData } from '../../lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';
import { useVideoEditorPreviewSurface } from './useVideoEditorPreviewSurface.tsx';

const player = vi.hoisted(() => ({
  config: null as ResolvedTimelineConfig | null,
  compiled: undefined as CompiledCanonicalTransitions | undefined,
}));

// Keep the command producers, runtime provider, surface and delivery mailbox real.
vi.mock('@remotion/player', async () => {
  const React = await import('react');
  return { Player: React.forwardRef(function Player(props: {
    inputProps: { config: ResolvedTimelineConfig; compiledTransitions?: CompiledCanonicalTransitions };
  }, ref) {
    player.config = props.inputProps.config;
    player.compiled = props.inputProps.compiledTransitions;
    React.useImperativeHandle(ref, () => ({
      addEventListener: vi.fn(), removeEventListener: vi.fn(), getCurrentFrame: () => 0,
      isPlaying: () => false, seekTo: vi.fn(), play: vi.fn(), pause: vi.fn(), toggle: vi.fn(),
    }), []);
    return <div data-testid="flat-command-player" />;
  }) };
});

function Surface() {
  const surface = useVideoEditorPreviewSurface();
  return <><div ref={surface.slotRef} />{surface.portal}</>;
}

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.useRealTimers(); });

it('compiles actual flat local and accepted command projections without a graph, retaining their config/vector pair through a late graph read', async () => {
  const raw = document();
  const parent = raw.parent_revision.payload;
  const clips = [
    { id: 'a', track: 'V1', at: 0, hold: 1, clipType: 'hold' },
    { id: 'x', track: 'V1', at: 1, hold: 1, clipType: 'hold', transition: { type: 'fade', duration: 0.4 } },
    { id: 'c', track: 'V1', at: 2, hold: 1, clipType: 'hold' },
  ];
  parent.clips = clips;
  parent.config = { ...parent.config as object, clips };
  raw.parent_revision.content_digest = fixtureDigest(parent);
  const env = await environment(raw);
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const initial = env.current();
  const store = createTimelineStore();
  const eventBus = new TimelineEventBus();
  const lastSavedSignatureRef = { current: initial.stableSignature };
  const configVersionRef = { current: initial.configVersion };
  const headRevisionRef = { current: initial.head };
  const snapshotWriteBlockedRef = { current: false };
  const installed: { data: TimelineData; status: CommandSessionState['status'] }[] = [];
  let status: CommandSessionState['status'] = 'loading';
  const producer = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider: env.provider, timelineId: 'timeline-commit',
      commit: { ...commit, commitData: (data, options) => {
        commit.commitData(data, options);
        installed.push({ data: commit.dataRef.current!, status });
      } }, legacyClean: () => true, snapshotWriteBlockedRef,
      resolveAssetUrl: async (file) => file, loaded: initial, configVersionRef, headRevisionRef,
      lastSavedSignatureRef, store, shots: { canonicalDraft: null, shots: [], isLoading: false,
        error: null, refetchShots: vi.fn(), finalVideoMap: new Map(), dismissFinalVideo: vi.fn() } });
    status = commands.state.status;
    return { commit, commands };
  });
  await waitFor(() => expect(producer.result.current.commands.port).toBeDefined());
  const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
  let runtime = {
    project: { projectId: 'project-commit' }, timelineId: 'timeline-commit', userId: null,
    shots: { shotComposition: adapter, canonicalComposition: null, canonicalDraft: null, canonicalCompositionError: null },
  } as VideoEditorRuntimeContextValue;
  // Deliberately retain the older derived slice config: the fact certifies only
  // data.resolvedConfig, including when the editor signature has not changed.
  const install = (data: TimelineData, saveStatus: 'dirty' | 'saving' | 'saved', config = initial.resolvedConfig) => act(() => {
    store.getState().syncDataSlice({ ...store.getState().data, data, resolvedConfig: config });
    store.getState().syncChromeSlice({ ...store.getState().chrome, saveStatus });
  });
  install(initial, 'saved');
  const draw = () => <VideoEditorRuntimeProvider value={runtime}>
    <TimelineStoreProvider store={store}><Surface /></TimelineStoreProvider>
  </VideoEditorRuntimeProvider>;
  const surface = render(draw());
  expect(player.config).toBe(initial.resolvedConfig);
  expect(player.compiled).toBeUndefined();

  const gate = env.pause();
  act(() => { submitClipMove(captureClipMove(producer.result.current.commands.port,
    producer.result.current.commit.dataRef.current!, 'x'), 1.25); });
  await waitFor(() => expect(producer.result.current.commands.state.status).toBe('saving'));
  const local = producer.result.current.commit.data!;
  expect(local.editProjection).toMatchObject({ kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' } });
  install(local, 'dirty');
  await waitFor(() => expect(player.config).toBe(local.resolvedConfig));
  expect(player.compiled).toBeDefined();
  expect(player.compiled).toEqual(compilePlayerTransitions(local.resolvedConfig));
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on r0');
  install(local, 'saving');
  const localVector = player.compiled;
  expect(player.config).toBe(local.resolvedConfig);
  expect(player.compiled).toBe(localVector);

  await act(async () => { gate.resolve(); await producer.result.current.commands.flush(); });
  const accepted = installed.find(({ data }) => data.editProjection?.kind === 'accepted'
    && data.editProjection.head.publicationId === 'p1')!;
  expect(accepted.status).toBe('saving');
  expect(accepted.data.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r1', publicationId: 'p1' } });
  install(accepted.data, 'saving');
  await waitFor(() => expect(player.config).toBe(accepted.data.resolvedConfig));
  expect(player.compiled).toBeDefined();
  expect(player.compiled).toEqual(compilePlayerTransitions(accepted.data.resolvedConfig));
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed r1');
  const acceptedVector = player.compiled;
  vi.useFakeTimers();
  runtime = { ...runtime, shots: { ...runtime.shots, canonicalComposition: adapter.prepare(structuredClone(fixture)) } };
  surface.rerender(draw());
  act(() => { vi.advanceTimersByTime(150); });
  expect(player.config).toBe(accepted.data.resolvedConfig);
  expect(player.compiled).toBe(acceptedVector);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed r1');
  vi.useRealTimers();

  act(() => { producer.result.current.commit.applyEdit({ type: 'config', resolvedConfig: {
    ...accepted.data.resolvedConfig, clips: accepted.data.resolvedConfig.clips.map(clip => ({ ...clip, label: 'ordinary edit' })),
  } }); });
  const native = producer.result.current.commit.data!;
  expect(native.editProjection).toBeUndefined();
  runtime = { ...runtime, shots: { ...runtime.shots, canonicalComposition: null } };
  surface.rerender(draw());
  install(native, 'saved', native.resolvedConfig);
  await waitFor(() => expect(player.config).toBe(native.resolvedConfig));
  expect(player.compiled).toBeUndefined();
  expect(player.config!.clips.find(clip => clip.id === 'x')!.transition).toEqual({ type: 'fade', duration: 0.4 });
  install(native, 'saving', native.resolvedConfig);
  expect(player.compiled).toBeUndefined();
});
