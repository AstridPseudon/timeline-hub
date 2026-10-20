// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import type { CompiledCanonicalTransitions } from '@banodoco/timeline-composition';
import { querySceneFrame } from '@banodoco/timeline-composition/evaluation';
import fixture from '../../data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../../data/shotCompositionProjection.ts';
import { compilePlayerTransitions, preparePlayerClipOpacity, preparePlayerTrack } from '../../compositions/playerEvaluation.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from '../../hooks/timelineStore.ts';
import { assembleTimelineData, type TimelineData } from '../../lib/timeline-data.ts';
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

function source(cap: number, revision: string): TimelineData {
  const prepared = createShotCompositionAdapter({ load: vi.fn() }).prepare(fixture);
  const original = prepared.occurrences[0];
  const internal = original.revision.internal_timeline_revision as Record<string, unknown>;
  const composition = { ...prepared, occurrences: [{ ...original, durationMs: cap,
    revision: { ...original.revision, internal_timeline_revision: { ...internal, timeline: {
      tracks: [{ id: 'video', kind: 'visual' }],
      clips: [{ id: 'image', track: 'video', at: 0, hold: 5, clipType: 'media', asset: 'alpha-image', effects: { fade_out: 1 } }],
    } } },
  }] };
  const config = projectCanonicalComposition(composition, {
    output: { fps: 30, resolution: '1920x1080', file: 'image.mp4' },
    tracks: [], clips: [], registry: {},
  }).config;
  return Object.assign(assembleTimelineData({ config, resolvedConfig: config,
    registry: { assets: config.registry }, output: config.output, assetMap: {}, configVersion: 1 }), {
    editProjection: { kind: 'accepted' as const, head: { revisionId: revision, publicationId: `pub-${revision}` } },
  });
}
function Surface() {
  const surface = useVideoEditorPreviewSurface();
  return <><div ref={surface.slotRef} />{surface.portal}</>;
}
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.useRealTimers(); });

it.each(['paused', 'playing'] as const)('delivers stored 4000/4500 config, vector, provenance and extent atomically while %s', (mode) => {
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
  const a = source(4000, 'A'), b = source(4500, 'B');
  expect(a.config.clips[0].hold).toBe(5);
  expect(b.config.clips[0].hold).toBe(5);
  const withoutCap = (data: TimelineData) => {
    const config = structuredClone(data.config);
    for (const clip of config.clips) Reflect.deleteProperty(clip.app!.canonicalTiming as object, 'storedOccurrenceDurationMs');
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
