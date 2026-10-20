// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import type { CompiledCanonicalTransitions } from '@banodoco/timeline-composition';
import { querySceneFrame } from '@banodoco/timeline-composition/evaluation';
import closure from '../../data/mainImageCap.fixture.json';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata.ts';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../../data/shotCompositionProjection.ts';
import { compilePlayerTransitions, preparePlayerClipOpacity, preparePlayerTrack } from '../../compositions/playerEvaluation.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from '../../hooks/timelineStore.ts';
import { buildTimelineData, type TimelineData } from '../../lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';
import { useVideoEditorPreviewSurface } from './useVideoEditorPreviewSurface.tsx';

const player = vi.hoisted(() => ({
  config: null as ResolvedTimelineConfig | null,
  vector: undefined as CompiledCanonicalTransitions | undefined,
  extent: 0,
  frame: 0,
  listeners: new Map<string, Set<() => void>>(),
}));
vi.mock('@remotion/player', async () => {
  const React = await import('react');
  return { Player: React.forwardRef(function Player(props: {
    inputProps: { config: ResolvedTimelineConfig; compiledTransitions?: CompiledCanonicalTransitions };
    durationInFrames: number;
  }, ref) {
    player.config = props.inputProps.config;
    player.vector = props.inputProps.compiledTransitions;
    player.extent = props.durationInFrames;
    React.useImperativeHandle(ref, () => ({
      addEventListener: (name: string, fn: () => void) => {
        if (!player.listeners.has(name)) player.listeners.set(name, new Set());
        player.listeners.get(name)!.add(fn);
      },
      removeEventListener: (name: string, fn: () => void) => player.listeners.get(name)?.delete(fn),
      getCurrentFrame: () => player.frame, isPlaying: () => false,
      seekTo: (frame: number) => { player.frame = frame; },
      play: vi.fn(), pause: vi.fn(), toggle: vi.fn(),
    }), []);
    return <div />;
  }) };
});

async function source(cap: number, revision: string): Promise<TimelineData> {
  const raw = structuredClone(closure);
  const parent = raw.parent_revision;
  parent.revision_id = revision;
  parent.payload.occurrences[0].duration_ms = cap;
  parent.content_digest = fixtureDigest(parent.payload);
  const prefix = `/v1/projects/${parent.project_id}`;
  const responses: Record<string, unknown> = {
    '/v1/health': { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_instance_id: 'stored-cap-instance', runtime_epoch: 1 },
    '/v1/handshake': { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      actor_id: 'actor-1', realm_id: 'realm-1', scopes: [...RUNTIME_CLIENT_SCOPES],
      capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] },
    '/v1/realm': { realm_id: 'realm-1' },
    [`${prefix}/timelines/${parent.timeline_id}/composition-revisions/${revision}`]: parent,
    ...Object.fromEntries(raw.shot_revisions.map(shot =>
      [`${prefix}/shots/${shot.shot_id}/revisions/${shot.revision_id}`, shot])),
    ...Object.fromEntries(raw.internal_timeline_revisions.map(internal =>
      [`${prefix}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`, internal])),
  };
  const provider = new RuntimeDataProvider({ projectId: parent.project_id,
    baseUrl: 'http://stored-cap.test', token: 'token', transport: async (method, path) => {
      expect(method).toBe(path === '/v1/handshake' ? 'POST' : 'GET');
      expect(responses).toHaveProperty(path);
      return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(responses[path])) };
    } });
  const graph = await provider.shotComposition.loadAtHead!({ projectId: parent.project_id,
    parentDocumentId: parent.timeline_id, headRevisionId: revision });
  const composition = createShotCompositionAdapter(provider.shotComposition).prepare(graph);
  const config = projectCanonicalComposition(composition).config;
  const data = await buildTimelineData(config, { assets: config.registry }, async () => 'https://example.test/image.png');
  expect(data.config.app?.canonicalComposition).toMatchObject({ headRevisionId: revision });
  expect(raw.parent_revision.payload.occurrences[0].duration_ms).toBe(cap);
  expect(raw.internal_timeline_revisions[0].payload.clips[0].hold).toBe(5);
  data.editProjection = { kind: 'accepted', head: { revisionId: revision, publicationId: `pub-${revision}` } };
  return data;
}
function Surface() {
  const surface = useVideoEditorPreviewSurface();
  return <><div ref={surface.slotRef} />{surface.portal}</>;
}
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.useRealTimers(); });

it.each(['paused', 'playing'] as const)('delivers stored 4000/4500 config, vector, provenance and extent atomically while %s', async (mode) => {
  const a = await source(4000, 'A'), b = await source(4500, 'B');
  vi.useFakeTimers();
  let nextFrame = 0;
  const frames = new Map<number, FrameRequestCallback>();
  vi.stubGlobal('requestAnimationFrame', (fn: FrameRequestCallback) => { frames.set(++nextFrame, fn); return nextFrame; });
  vi.stubGlobal('cancelAnimationFrame', (id: number) => frames.delete(id));
  const flushFrame = () => act(() => {
    const pending = [...frames.values()]; frames.clear(); pending.forEach((fn) => fn(1000));
  });
  const advance = (ms = 150) => act(() => { vi.advanceTimersByTime(ms); });
  player.listeners.clear(); player.frame = 0;
  expect(a.config.clips[0].hold).toBe(5);
  expect(b.config.clips[0].hold).toBe(5);
  const withoutCap = (data: TimelineData) => {
    const config = structuredClone(data.config);
    for (const clip of config.clips) Reflect.deleteProperty(clip.app!.canonicalTiming as object, 'storedOccurrenceDurationMs');
    // The verified revision differs; all other flattened inputs except the cap agree.
    Reflect.deleteProperty(config.app!.canonicalComposition as object, 'headRevisionId');
    return config;
  };
  expect(withoutCap(a)).toStrictEqual(withoutCap(b));
  const store = createTimelineStore();
  const install = (data: TimelineData) => act(() => {
    // An unchanged editor slice cannot supply the selected command's cap.
    store.getState().syncDataSlice({ ...store.getState().data, data, resolvedConfig: a.resolvedConfig });
  });
  install(a);
  const runtime = { userId: null, project: { projectId: 'project' }, timelineId: 'timeline',
    shots: { canonicalComposition: null, canonicalDraft: null } } as VideoEditorRuntimeContextValue;
  const view = render(<VideoEditorRuntimeProvider value={runtime}>
    <TimelineStoreProvider store={store}><Surface /></TimelineStoreProvider>
  </VideoEditorRuntimeProvider>);
  const assertDelivery = (cap: number, revision: string) => {
    expect(player.config!.clips[0].hold).toBe(cap / 1000);
    expect(player.extent).toBe(cap * 30 / 1000);
    expect(player.vector).toEqual(compilePlayerTransitions(player.config!));
    expect(screen.getByTestId('preview-revision-label')).toHaveTextContent(`Committed ${revision}`);
    const config = player.config!;
    expect(preparePlayerClipOpacity(config.clips[0], 30)(105)).toBe(cap === 4000 ? 0.5 : 1);
    const evaluation = preparePlayerTrack(config.tracks[0], config.clips, 30, 1920, 1080, undefined, player.vector);
    expect(querySceneFrame(evaluation.scene, 105).layers).toHaveLength(1);
    expect(querySceneFrame(evaluation.scene, 119).layers).toHaveLength(1);
    expect(querySceneFrame(evaluation.scene, 120).layers).toHaveLength(cap === 4000 ? 0 : 1);
    expect(querySceneFrame(evaluation.scene, cap * 30 / 1000).layers).toEqual([]);
  };
  advance(); assertDelivery(4000, 'A');
  if (mode === 'playing') {
    act(() => player.listeners.get('play')?.forEach((fn) => fn())); flushFrame();
  }
  const originalVector = player.vector;
  install(b);
  assertDelivery(4000, 'A'); expect(player.vector).toBe(originalVector);
  if (mode === 'playing') flushFrame(); else { advance(149); assertDelivery(4000, 'A'); advance(1); }
  assertDelivery(4500, 'B');
  // An end seek is clamped on delivery of the shorter selected unit.
  player.frame = 134;
  install(a);
  assertDelivery(4500, 'B');
  if (mode === 'playing') flushFrame(); else advance();
  flushFrame(); assertDelivery(4000, 'A'); expect(player.frame).toBeLessThan(120);
  install(b); install(a);
  advance(); flushFrame(); assertDelivery(4000, 'A');
  view.unmount();
  advance(500); flushFrame();
  expect(frames.size).toBe(0);
});
