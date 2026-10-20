// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import fixture from '../../data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../../data/shotCompositionProjection.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from '../../hooks/timelineStore.ts';
import { assembleTimelineData, type TimelineData } from '../../lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';
import { useVideoEditorPreviewSurface } from './useVideoEditorPreviewSurface.tsx';

const player = vi.hoisted(() => ({
  config: null as ResolvedTimelineConfig | null,
  delivered: [] as ResolvedTimelineConfig[],
  listeners: new Map<string, Set<() => void>>(),
}));

// Only the external Player is replaced; the surface, providers, canonical
// adapter and RemotionPreview delivery mailbox are the production owners.
vi.mock('@remotion/player', async () => {
  const React = await import('react');
  return {
    Player: React.forwardRef(function Player(props: { inputProps: { config: ResolvedTimelineConfig } }, ref) {
      player.config = props.inputProps.config;
      player.delivered.push(props.inputProps.config);
      React.useImperativeHandle(ref, () => ({
        addEventListener: (name: string, listener: () => void) => {
          if (!player.listeners.has(name)) player.listeners.set(name, new Set());
          player.listeners.get(name)!.add(listener);
        },
        removeEventListener: (name: string, listener: () => void) => player.listeners.get(name)?.delete(listener),
        getCurrentFrame: () => 0,
        isPlaying: () => false,
        seekTo: vi.fn(),
        play: vi.fn(),
        pause: vi.fn(),
        toggle: vi.fn(),
      }), []);
      return <div data-testid="mounted-player" />;
    }),
  };
});

const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
function canonical(revisionId: string, atMs = 0) {
  const graph = structuredClone(fixture);
  graph.primary_timeline.head.revision_id = revisionId;
  // The general adapter fixture omits its selected audio asset row. Supply
  // the immutable binding so this lane exercises a complete media closure.
  const alpha = graph.shot_revisions.find((revision) => revision.shot_id === 'shot-alpha' && revision.revision_id === 'rev-a')!;
  alpha.assets.push({ ...alpha.assets[0]!, asset_id: 'alpha-audio', object_id: alpha.audio!.object_id,
    digest: alpha.audio!.digest, media_type: 'audio/mpeg' });
  graph.shot_revisions.find((revision) => revision.shot_id === 'shot-alpha' && revision.revision_id === 'rev-a')!
    .internal_timeline_revision.timeline.clips[0]!.at_ms = atMs;
  return adapter.prepare(graph);
}
function dataFor(config: ResolvedTimelineConfig): TimelineData {
  return assembleTimelineData({
    config,
    resolvedConfig: config,
    registry: { assets: config.registry },
    configVersion: 1,
    output: config.output,
    assetMap: {},
    head: { projectId: 'project-001', timelineId: 'document-primary', headRevisionId: 'R', headPublicationId: 'pub-R' },
  });
}
function local(config: ResolvedTimelineConfig, generation = 1) {
  return Object.assign(dataFor(config), {
    editProjection: { kind: 'local' as const, base: { revisionId: 'R', publicationId: 'pub-R' }, generation },
  });
}
function accepted(config: ResolvedTimelineConfig, revisionId = 'A', publicationId = `pub-${revisionId}`) {
  return Object.assign(dataFor(config), {
    editProjection: { kind: 'accepted' as const, head: { revisionId, publicationId } },
  });
}
function candidate(config: ResolvedTimelineConfig, at: number) {
  return { ...config, clips: config.clips.map((clip, index) => index === 0 ? { ...clip, at, x: 0.25 } : clip) };
}
function shotShell(config: ResolvedTimelineConfig): ResolvedTimelineConfig {
  return { ...config, clips: [{ id: 'unresolved-shot', at: 0, track: 'video', clipType: 'shot' }] };
}
function Surface() {
  const surface = useVideoEditorPreviewSurface();
  return <><div ref={surface.slotRef} />{surface.portal}
    {!surface.hasConfig && <div role="status">{surface.availability}: {surface.unavailableReason}</div>}
  </>;
}
function mount(initial: TimelineData, composition: ReturnType<typeof canonical> | null = canonical('R')) {
  const store = createTimelineStore();
  // Retain this slice config across updates, just as useDerivedTimeline does
  // for equal signatures. A command fact certifies data.resolvedConfig only.
  const memoizedConfig = initial.resolvedConfig;
  store.getState().syncDataSlice({ ...store.getState().data, data: initial, resolvedConfig: memoizedConfig });
  let runtime = {
    project: { projectId: 'project-001' }, timelineId: 'document-primary', userId: null,
    shots: { shotComposition: adapter, canonicalComposition: composition, canonicalDraft: null, canonicalCompositionError: null },
  } as VideoEditorRuntimeContextValue;
  const draw = () => <VideoEditorRuntimeProvider value={runtime}>
    <TimelineStoreProvider store={store}><Surface /></TimelineStoreProvider>
  </VideoEditorRuntimeProvider>;
  const view = render(draw());
  return {
    store,
    view,
    update(data: TimelineData, saveStatus: 'dirty' | 'saving' | 'saved' = 'saving') {
      act(() => {
        store.getState().syncDataSlice({ ...store.getState().data, data, resolvedConfig: memoizedConfig });
        store.getState().syncChromeSlice({ ...store.getState().chrome, saveStatus });
      });
    },
    runtime(change: Partial<VideoEditorRuntimeContextValue>) {
      runtime = { ...runtime, ...change };
      view.rerender(draw());
    },
    observe(composition: ReturnType<typeof canonical>, error: Error | null = null) {
      runtime = { ...runtime, shots: { ...runtime.shots, canonicalComposition: composition, canonicalCompositionError: error } };
      view.rerender(draw());
    },
    draft(composition: ReturnType<typeof canonical>) {
      runtime = { ...runtime, shots: { ...runtime.shots, canonicalDraft: {
        composition, generation: 1,
        scope: { projectId: 'project-001', parentDocumentId: 'document-primary', occurrenceId: 'occ-1', editorSessionId: 'editor' },
      } } };
      view.rerender(draw());
    },
  };
}
function advance(ms = 150) { act(() => { vi.advanceTimersByTime(ms); }); }
function label(text: string) { expect(screen.getByTestId('preview-revision-label').textContent).toBe(text); }
function flushFrame() {
  act(() => {
    const pending = [...raf.values()];
    raf.clear();
    pending.forEach((callback) => callback(1000));
  });
}
let raf = new Map<number, FrameRequestCallback>();
let nextFrame = 0;
beforeEach(() => {
  vi.useFakeTimers();
  player.config = null;
  player.delivered = [];
  player.listeners.clear();
  raf = new Map();
  nextFrame = 0;
  vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => { raf.set(++nextFrame, callback); return nextFrame; });
  vi.stubGlobal('cancelAnimationFrame', (id: number) => raf.delete(id));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.useRealTimers(); });

describe('mounted command projection delivery', () => {
  it('delivers paired canonical-shot candidate geometry through project/saving, then the accepted pinned closure', () => {
    const base = projectCanonicalComposition(canonical('R')).config;
    const h = mount(dataFor(base));
    const edit = candidate(base, 1);
    const localEdit = local(edit);
    h.update(localEdit, 'dirty');
    advance();
    expect(player.config).toBe(localEdit.resolvedConfig);
    expect(player.config!.clips[0]).toMatchObject({ at: 1, x: 0.25 });
    label('Unsaved local · based on R');
    const savingEdit = local(edit);
    h.update(savingEdit, 'saving');
    advance();
    label('Unsaved local · based on R');
    const deliveredEdit = player.config;

    const closure = projectCanonicalComposition(canonical('A', 500)).config;
    const pinnedMedia = closure.clips.find((clip) => clip.asset)!.assetEntry;
    const acceptedClosure = accepted(closure);
    h.update(acceptedClosure, 'saved');
    expect(player.config).toBe(deliveredEdit);
    label('Unsaved local · based on R');
    advance();
    expect(player.config).toBe(acceptedClosure.resolvedConfig);
    expect(player.config!.clips.find((clip) => clip.asset)!.assetEntry).toBe(pinnedMedia);
    expect(player.config!.registry).toBe(acceptedClosure.resolvedConfig.registry);
    label('Committed A');
  });

  it('keeps retained B local at its original base through prefix A acknowledgement and observed C', () => {
    const base = projectCanonicalComposition(canonical('R')).config;
    const b = candidate(base, 1.5);
    const initial = local(b, 2);
    const h = mount(initial);
    label('Unsaved local · based on R');
    const afterA = { ...local(b, 2), head: { ...dataFor(base).head!, headRevisionId: 'A', headPublicationId: 'pub-A' } };
    h.update(afterA, 'saved');
    advance();
    expect(player.config).toBe(afterA.resolvedConfig);
    label('Unsaved local · based on R');
    h.observe(canonical('C', 700));
    const afterC = { ...local(b, 2), head: { ...dataFor(base).head!, headRevisionId: 'C', headPublicationId: 'pub-C' } };
    h.update(afterC, 'saved');
    advance();
    expect(player.config).toBe(afterC.resolvedConfig);
    label('Unsaved local · based on R');
  });

  it('does not relabel observed C from an old A acknowledgement when A has no usable projection', () => {
    const c = canonical('C', 800);
    const config = projectCanonicalComposition(c).config;
    const h = mount(dataFor(shotShell(config)), c);
    const displayed = player.config;
    label('Committed C');
    h.update(accepted(shotShell(config)), 'saved');
    advance();
    expect(player.config).toBe(displayed);
    label('Committed C');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of A unavailable');
    h.update(accepted(shotShell(config), 'D'), 'saved');
    expect(player.config).toBe(displayed);
    label('Committed C');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of D unavailable');
    advance();
    expect(player.config).toBe(displayed);
    label('Committed C');
  });

  it('installs an accepted same-content config generation despite the unchanged editor signature', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = local(config);
    const h = mount(initial);
    const nextConfig = structuredClone(config);
    const next = accepted(nextConfig);
    expect(next.signature).toBe(initial.signature);
    h.update(next, 'saved');
    advance(149);
    expect(player.config).toBe(initial.resolvedConfig);
    label('Unsaved local · based on R');
    advance(1);
    expect(player.config).toBe(next.resolvedConfig);
    label('Committed A');
  });

  it('refuses metadata-only certification of delivered frames and clears only target notices', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = local(config);
    const h = mount(initial);
    const acceptedR = Object.assign({}, initial, {
      editProjection: { kind: 'accepted' as const, head: { revisionId: 'A', publicationId: 'pub-A' } },
    });
    h.update(acceptedR, 'saved');
    advance();
    expect(player.config).toBe(initial.resolvedConfig);
    label('Unsaved local · based on R');
    const acceptedC = Object.assign({}, initial, {
      editProjection: { kind: 'accepted' as const, head: { revisionId: 'C', publicationId: 'pub-C' } },
    });
    h.update(acceptedC, 'saved');
    advance();
    label('Unsaved local · based on R');
    h.update(accepted(shotShell(config), 'C'), 'saved');
    advance();
    label('Committed R');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of C unavailable');
    h.update(dataFor(config), 'saved');
    expect(screen.queryByTestId('preview-revision-unavailable')).toBeNull();
    label('Committed R');
  });

  it('keeps the true canonical identity when command media links are incomplete', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const incomplete = { ...config, clips: config.clips.map((clip) => ({ ...clip, assetEntry: undefined })) };
    mount(accepted(incomplete));
    expect(player.config).not.toBe(incomplete);
    label('Committed R');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of A unavailable');
  });

  it('does not mount incomplete shot shells when there is no canonical cache', () => {
    const config = projectCanonicalComposition(canonical('A')).config;
    mount(accepted(shotShell(config)), null);
    expect(screen.queryByTestId('mounted-player')).toBeNull();
    expect(screen.getByRole('status')).toHaveTextContent('unavailable');
    expect(screen.getByRole('status')).toHaveTextContent('Preview of A unavailable');
  });

  it('keeps a cached canonical draft at its own base when a local command projection is unavailable', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const h = mount(local(shotShell(config)));
    h.observe(canonical('C'));
    h.draft(canonical('draft-base', 500));
    advance();
    label('Unsaved local · based on draft-base');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview target unavailable');
  });

  it('keeps a complete paired config labelled while an independent canonical target read is unavailable', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = accepted(config);
    const h = mount(initial);
    const deliveredInitial = player.config;
    h.observe(canonical('C'), Object.assign(new Error('Cannot read D'), { targetRevisionId: 'D' }));
    expect(player.config).toBe(deliveredInitial);
    label('Committed A');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of D unavailable');
    h.observe(canonical('C'));
    label('Committed A');
    expect(screen.queryByTestId('preview-revision-unavailable')).toBeNull();
  });

  it('cancels older paused command inputs and delivers the newest generation with its own label', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = local(config);
    const h = mount(initial);
    const a = candidate(config, 1);
    const b = candidate(config, 1.5);
    const acceptedA = accepted(a);
    const localB = local(b, 2);
    h.update(acceptedA);
    advance(100);
    h.update(localB);
    advance();
    expect(player.config).toBe(localB.resolvedConfig);
    expect(player.delivered).not.toContain(a);
    label('Unsaved local · based on R');
  });

  it('coalesces playing command inputs on one frame without delivering the superseded acceptance', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = local(config);
    const h = mount(initial);
    act(() => { player.listeners.get('play')!.forEach((listener) => listener()); });
    flushFrame();
    const a = candidate(config, 1);
    const b = candidate(config, 1.5);
    const acceptedA = accepted(a);
    const localB = local(b, 2);
    h.update(acceptedA);
    h.update(localB);
    expect(player.config).toBe(initial.resolvedConfig);
    flushFrame();
    expect(player.config).toBe(localB.resolvedConfig);
    expect(player.delivered).not.toContain(a);
    label('Unsaved local · based on R');
  });

  it('remounts across project and timeline scopes while a command generation is queued', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const initial = local(config);
    const h = mount(initial);
    const pending = candidate(config, 1);
    const acceptedPending = accepted(pending);
    h.update(acceptedPending);
    h.runtime({ timelineId: 'other-timeline' });
    expect(player.config).toBe(acceptedPending.resolvedConfig);
    advance();
    label('Committed A');
    expect(vi.getTimerCount()).toBe(0);
  });
});
