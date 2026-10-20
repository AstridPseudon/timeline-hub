// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import fixture from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/data/shotCompositionProjection.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/hooks/timelineStore.ts';
import { assembleTimelineData, type TimelineData } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/types/index.ts';
import { useVideoEditorPreviewSurface } from '/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx';

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
// Test-only structural extension for the pending App producer field; product
// TimelineData remains unchanged until the shared producer branch lands.
type MountedTimelineData = TimelineData & { renderConfig?: ResolvedTimelineConfig };

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
function withRenderConfig(data: TimelineData, renderConfig?: ResolvedTimelineConfig): MountedTimelineData {
  return renderConfig ? { ...data, renderConfig } : data;
}
function local(config: ResolvedTimelineConfig, generation = 1, renderConfig?: ResolvedTimelineConfig) {
  return withRenderConfig(Object.assign(dataFor(config), {
    editProjection: { kind: 'local' as const, base: { revisionId: 'R', publicationId: 'pub-R' }, generation },
  }), renderConfig);
}
function accepted(config: ResolvedTimelineConfig, revisionId = 'A', publicationId = `pub-${revisionId}`, renderConfig?: ResolvedTimelineConfig) {
  return withRenderConfig(Object.assign(dataFor(config), {
    editProjection: { kind: 'accepted' as const, head: { revisionId, publicationId } },
  }), renderConfig);
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
function mount(initial: MountedTimelineData, composition: ReturnType<typeof canonical> | null = canonical('R')) {
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
    update(data: MountedTimelineData, saveStatus: 'dirty' | 'saving' | 'saved' = 'saving') {
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
  it('delivers an accepted prebuilt render config while preserving the clamped editor config and rows', () => {
    const editorConfig = projectCanonicalComposition(canonical('A')).config;
    const renderConfig = candidate(editorConfig, 2);
    const data = accepted(editorConfig, 'A', 'pub-A', renderConfig);
    const editorRows = data.rows;
    const h = mount(data);

    expect(player.config).toBe(renderConfig);
    expect(data.resolvedConfig).toBe(editorConfig);
    expect(data.rows).toBe(editorRows);
    expect(h.store.getState().data.data.resolvedConfig).toBe(editorConfig);
    expect(h.store.getState().data.data.rows).toBe(editorRows);
    label('Committed A');
  });

  it('uses the paired render config for local preview and recovery without changing editor data', () => {
    const editorConfig = projectCanonicalComposition(canonical('R')).config;
    const localRenderConfig = candidate(editorConfig, 2.5);
    const localData = local(editorConfig, 1, localRenderConfig);
    const editorRows = localData.rows;
    const h = mount(localData);

    expect(player.config).toBe(localRenderConfig);
    label('Unsaved local · based on R');

    const recoveredRenderConfig = candidate(editorConfig, 3.5);
    const recoveredData = accepted(editorConfig, 'A', 'pub-A', recoveredRenderConfig);
    h.update(recoveredData, 'saved');
    expect(player.config).toBe(localRenderConfig);
    label('Unsaved local · based on R');
    advance();
    expect(player.config).toBe(recoveredRenderConfig);
    expect(recoveredData.resolvedConfig).toBe(editorConfig);
    expect(recoveredData.rows).toEqual(editorRows);
    label('Committed A');
  });

  it('defers A to B config delivery and its label until B is delivered', () => {
    const editorConfig = projectCanonicalComposition(canonical('R')).config;
    const renderA = candidate(editorConfig, 1);
    const renderB = candidate(editorConfig, 2);
    const h = mount(accepted(editorConfig, 'A', 'pub-A', renderA));

    expect(player.config).toBe(renderA);
    h.update(accepted(editorConfig, 'B', 'pub-B', renderB), 'saved');
    expect(player.config).toBe(renderA);
    label('Committed A');
    advance();
    expect(player.config).toBe(renderB);
    label('Committed B');
  });

  it('keeps B local ahead of a stale A acknowledgement and an observed current head C', () => {
    const editorConfig = projectCanonicalComposition(canonical('R')).config;
    const renderB = candidate(editorConfig, 2);
    const renderC = candidate(editorConfig, 3);
    const h = mount(local(editorConfig, 2, renderB));

    expect(player.config).toBe(renderB);
    label('Unsaved local · based on R');

    // The stale A acknowledgement may refresh the host head metadata, but it
    // must not replace B's paired local fact or its delivered render config.
    h.update({ ...local(editorConfig, 2, renderB), head: { ...dataFor(editorConfig).head!, headRevisionId: 'A', headPublicationId: 'pub-A' } }, 'saved');
    h.observe(canonical('C', 700));
    expect(player.config).toBe(renderB);
    label('Unsaved local · based on R');

    // A late acknowledgement after the observed C head is still metadata-only.
    h.update(local(editorConfig, 2, renderB), 'saved');
    expect(player.config).toBe(renderB);
    label('Unsaved local · based on R');
    h.update(accepted(editorConfig, 'C', 'pub-C', renderC), 'saved');
    advance();
    expect(player.config).toBe(renderC);
    label('Committed C');
  });

  it('falls back conservatively to the existing resolved config when renderConfig is absent', () => {
    const editorConfig = projectCanonicalComposition(canonical('A')).config;
    const data = accepted(editorConfig);
    mount(data);

    expect(player.config).toBe(editorConfig);
    label('Committed A');
  });

  it('drops the paired render config with an invalidated fact, then rebuilds it with the next fact', () => {
    const editorConfig = projectCanonicalComposition(canonical('R')).config;
    const renderA = candidate(editorConfig, 1);
    const renderB = candidate(editorConfig, 2);
    const h = mount(accepted(editorConfig, 'A', 'pub-A', renderA));

    const invalidated = dataFor(editorConfig);
    h.update(invalidated, 'dirty');
    advance();
    expect(player.config).not.toBe(renderA);
    label('Committed R');

    h.update(local(editorConfig, 3, renderB), 'dirty');
    expect(player.config).not.toBe(renderB);
    advance();
    expect(player.config).toBe(renderB);
    label('Unsaved local · based on R');
  });

  it('delivers paired canonical-shot candidate geometry through project/saving, then the accepted pinned closure', () => {
    const base = projectCanonicalComposition(canonical('R')).config;
    const h = mount(dataFor(base));
    const edit = candidate(base, 1);
    h.update(local(edit), 'dirty');
    advance();
    expect(player.config).toBe(edit);
    expect(player.config!.clips[0]).toMatchObject({ at: 1, x: 0.25 });
    label('Unsaved local · based on R');
    h.update(local(edit), 'saving');
    advance();
    label('Unsaved local · based on R');

    const closure = projectCanonicalComposition(canonical('A', 500)).config;
    const pinnedMedia = closure.clips.find((clip) => clip.asset)!.assetEntry;
    h.update(accepted(closure), 'saved');
    expect(player.config).toBe(edit);
    label('Unsaved local · based on R');
    advance();
    expect(player.config).toBe(closure);
    expect(player.config!.clips.find((clip) => clip.asset)!.assetEntry).toBe(pinnedMedia);
    expect(player.config!.registry).toBe(closure.registry);
    label('Committed A');
  });

  it('keeps retained B local at its original base through prefix A acknowledgement and observed C', () => {
    const base = projectCanonicalComposition(canonical('R')).config;
    const b = candidate(base, 1.5);
    const h = mount(local(b, 2));
    label('Unsaved local · based on R');
    h.update({ ...local(b, 2), head: { ...dataFor(base).head!, headRevisionId: 'A', headPublicationId: 'pub-A' } }, 'saved');
    advance();
    expect(player.config).toBe(b);
    label('Unsaved local · based on R');
    h.observe(canonical('C', 700));
    h.update({ ...local(b, 2), head: { ...dataFor(base).head!, headRevisionId: 'C', headPublicationId: 'pub-C' } }, 'saved');
    advance();
    expect(player.config).toBe(b);
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
    expect(player.config).toBe(config);
    label('Unsaved local · based on R');
    advance(1);
    expect(player.config).toBe(nextConfig);
    label('Committed A');
  });

  it('refuses metadata-only certification of delivered frames and clears only target notices', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const h = mount(local(config));
    h.update(accepted(config), 'saved');
    advance();
    expect(player.config).toBe(config);
    label('Unsaved local · based on R');
    h.update(accepted(config, 'C'), 'saved');
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
    const h = mount(accepted(config));
    h.observe(canonical('C'), Object.assign(new Error('Cannot read D'), { targetRevisionId: 'D' }));
    expect(player.config).toBe(config);
    label('Committed A');
    expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of D unavailable');
    h.observe(canonical('C'));
    label('Committed A');
    expect(screen.queryByTestId('preview-revision-unavailable')).toBeNull();
  });

  it('cancels older paused command inputs and delivers the newest generation with its own label', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const h = mount(local(config));
    const a = candidate(config, 1);
    const b = candidate(config, 1.5);
    h.update(accepted(a));
    advance(100);
    h.update(local(b, 2));
    advance();
    expect(player.config).toBe(b);
    expect(player.delivered).not.toContain(a);
    label('Unsaved local · based on R');
  });

  it('coalesces playing command inputs on one frame without delivering the superseded acceptance', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const h = mount(local(config));
    act(() => { player.listeners.get('play')!.forEach((listener) => listener()); });
    flushFrame();
    const a = candidate(config, 1);
    const b = candidate(config, 1.5);
    h.update(accepted(a));
    h.update(local(b, 2));
    expect(player.config).toBe(config);
    flushFrame();
    expect(player.config).toBe(b);
    expect(player.delivered).not.toContain(a);
    label('Unsaved local · based on R');
  });

  it('remounts across project and timeline scopes while a command generation is queued', () => {
    const config = projectCanonicalComposition(canonical('R')).config;
    const h = mount(local(config));
    const pending = candidate(config, 1);
    h.update(accepted(pending));
    h.runtime({ timelineId: 'other-timeline' });
    expect(player.config).toBe(pending);
    advance();
    label('Committed A');
    expect(vi.getTimerCount()).toBe(0);
  });
});
