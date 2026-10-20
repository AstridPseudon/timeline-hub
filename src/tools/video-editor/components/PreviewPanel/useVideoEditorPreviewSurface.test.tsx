// @vitest-environment jsdom
import React from 'react';
import { act, render, renderHook, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import fixture from '@/tools/video-editor/data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import { useVideoEditorPreviewSurface } from './useVideoEditorPreviewSurface.tsx';
import { PreviewPanel } from './PreviewPanel.tsx';

const mocks = vi.hoisted(() => ({
  runtime: null as unknown,
  timeline: null as unknown,
  playback: null as unknown,
  chrome: { saveStatus: 'saved' as const },
}));

vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineDataSelector: (selector: (timeline: unknown) => unknown) => selector(mocks.timeline),
  useTimelineChromeSelector: (selector: (chrome: unknown) => unknown) => selector(mocks.chrome),
  useTimelinePlaybackSelector: (selector: (playback: unknown) => unknown) => selector(mocks.playback),
  useTimelineOpsSelector: (selector: (ops: unknown) => unknown) => selector({}),
}));

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useOptionalVideoEditorRuntime: () => mocks.runtime,
}));

vi.mock('@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx', () => ({
  RemotionPreview: React.forwardRef(() => React.createElement('div')),
}));

function graphWithClipStart(atMs: number, head: string) {
  const graph = JSON.parse(JSON.stringify(fixture)) as typeof fixture;
  graph.primary_timeline.head.revision_id = head;
  graph.shot_revisions.find((revision) => revision.shot_id === 'shot-alpha' && revision.revision_id === 'rev-a')!
    .internal_timeline_revision.timeline.clips[0]!.at_ms = atMs;
  return graph;
}

describe('useVideoEditorPreviewSurface', () => {
  it('keeps the draft base identity when the server head advances independently', () => {
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const canonical = adapter.prepare(graphWithClipStart(0, 'server-r2'));
    const draft = adapter.prepare(graphWithClipStart(700, 'draft-r1'));
    const advancedCanonical = adapter.prepare(graphWithClipStart(1200, 'server-r3'));
    const parentConfig = projectCanonicalComposition(canonical).config!;
    const expectedDraftConfig = projectCanonicalComposition(draft, parentConfig).config!;
    mocks.timeline = { resolvedConfig: parentConfig };
    mocks.playback = {
      currentTime: 0,
      previewRef: { current: null },
      playerContainerRef: { current: null },
      onPreviewTimeUpdate: vi.fn(),
    };
    mocks.runtime = {
      userId: null,
      shots: {
        shotComposition: adapter,
        canonicalComposition: canonical,
        canonicalDraft: { composition: draft },
        canonicalCompositionError: null,
      },
    };

    const { result, rerender } = renderHook(() => useVideoEditorPreviewSurface());
    const slot = document.createElement('div');
    act(() => result.current.slotRef(slot));
    const previewElement = (result.current.portal as unknown as { children: React.ReactElement }).children;

    expect(previewElement.props.config).toEqual(expectedDraftConfig);
    expect(previewElement.props.previewRevision).toMatchObject({
      kind: 'local',
      baseRevisionId: draft.headRevisionId,
    });
    expect(previewElement.props.currentTime).toBeUndefined();

    mocks.runtime = {
      userId: null,
      shots: {
        shotComposition: adapter,
        canonicalComposition: advancedCanonical,
        canonicalDraft: { composition: draft },
        canonicalCompositionError: null,
      },
    };
    rerender();
    const advancedPreviewElement = (result.current.portal as unknown as { children: React.ReactElement }).children;
    expect(advancedPreviewElement.props.config).toEqual(expectedDraftConfig);
    expect(advancedPreviewElement.props.previewRevision).toMatchObject({
      kind: 'local',
      baseRevisionId: draft.headRevisionId,
    });
  });

  it('pairs the current unavailable target with the actual canonical surface and clears it on recovery', () => {
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const canonical = adapter.prepare(graphWithClipStart(0, 'R1'));
    const config = projectCanonicalComposition(canonical).config!;
    const error = Object.assign(new Error('Runtime read failed'), { targetRevisionId: 'R2' });
    mocks.timeline = { data: { rows: [], meta: {} }, resolvedConfig: config };
    mocks.playback = {
      currentTime: 0,
      previewRef: { current: null },
      playerContainerRef: { current: null },
      onPreviewTimeUpdate: vi.fn(),
    };
    mocks.runtime = {
      userId: null,
      shots: {
        shotComposition: adapter,
        canonicalComposition: canonical,
        canonicalDraft: null,
        canonicalCompositionError: error,
      },
    };

    const { result, rerender } = renderHook(() => useVideoEditorPreviewSurface());
    act(() => result.current.slotRef(document.createElement('div')));
    let previewElement = (result.current.portal as unknown as { children: React.ReactElement }).children;
    const deliveredConfig = previewElement.props.config;
    expect(previewElement.props.previewRevision).toMatchObject({
      kind: 'committed',
      revisionId: 'R1',
      unavailableTarget: { targetRevisionId: 'R2' },
    });

    mocks.runtime = {
      userId: null,
      shots: {
        shotComposition: adapter,
        canonicalComposition: canonical,
        canonicalDraft: null,
        canonicalCompositionError: null,
      },
    };
    rerender();
    previewElement = (result.current.portal as unknown as { children: React.ReactElement }).children;
    expect(previewElement.props.config).toBe(deliveredConfig);
    expect(previewElement.props.previewRevision).toEqual({ kind: 'committed', revisionId: 'R1' });
  });

  it('shows an honest unavailable boundary without mounting a fake Player when no cache exists', () => {
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const config = projectCanonicalComposition(adapter.prepare(graphWithClipStart(0, 'R2'))).config!;
    const configWithShotShell = {
      ...config,
      clips: [{ id: 'shot-shell', at: 0, track: 'video', clipType: 'shot' as const }],
    };
    mocks.timeline = { data: { rows: [], meta: {} }, resolvedConfig: configWithShotShell };
    mocks.playback = {
      currentTime: 0,
      previewRef: { current: null },
      playerContainerRef: { current: null },
      onPreviewTimeUpdate: vi.fn(),
    };
    mocks.runtime = {
      userId: null,
      shots: {
        shotComposition: adapter,
        canonicalComposition: null,
        canonicalDraft: null,
        canonicalCompositionError: new Error('Canonical preview read failed'),
      },
    };

    function SurfacePreview() {
      return <PreviewPanel surface={useVideoEditorPreviewSurface()} showOverlayEditor={false} />;
    }

    render(<SurfacePreview />);
    expect(screen.getByRole('alert')).toHaveTextContent('Preview unavailable');
    expect(screen.getByRole('alert')).toHaveTextContent('Canonical preview read failed');
    expect(screen.queryByTestId('video-editor-preview-surface')).toBeNull();
  });

  it('does not turn a saved status without a pinned head into committed preview metadata', () => {
    mocks.timeline = {
      data: { head: undefined },
      resolvedConfig: {
        output: { resolution: '1280x720', fps: 30, file: 'legacy.mp4' },
        tracks: [],
        clips: [],
        registry: {},
      },
    };
    mocks.playback = {
      currentTime: 0,
      previewRef: { current: null },
      playerContainerRef: { current: null },
      onPreviewTimeUpdate: vi.fn(),
    };
    mocks.runtime = null;

    const { result } = renderHook(() => useVideoEditorPreviewSurface());
    act(() => result.current.slotRef(document.createElement('div')));
    const previewElement = (result.current.portal as unknown as { children: React.ReactElement }).children;

    expect(previewElement.props.previewRevision).toMatchObject({ kind: 'unknown' });
    expect(previewElement.props.previewRevision.revisionId).toBeUndefined();
  });

  it('retains the preview key across config updates and physical slot moves', () => {
    mocks.timeline = {
      resolvedConfig: {
        output: {resolution: '1280x720', fps: 30, file: 'preview.mp4'},
        tracks: [],
        clips: [],
        registry: {},
      },
    };
    mocks.playback = {
      currentTime: 4,
      previewRef: {current: null},
      playerContainerRef: {current: null},
      onPreviewTimeUpdate: vi.fn(),
    };
    mocks.runtime = null;

    const {result, rerender} = renderHook(() => useVideoEditorPreviewSurface());
    const firstSlot = document.createElement('div');
    act(() => result.current.slotRef(firstSlot));
    const firstPortal = result.current.portal as unknown as {children: React.ReactElement};
    const firstKey = firstPortal.children.key;

    mocks.timeline = {
      resolvedConfig: {
        output: {resolution: '1280x720', fps: 30, file: 'preview-edited.mp4'},
        tracks: [],
        clips: [],
        registry: {},
      },
    };
    rerender();
    const configPortal = result.current.portal as unknown as {children: React.ReactElement};
    expect(configPortal.children.key).toBe(firstKey);

    const secondSlot = document.createElement('div');
    act(() => result.current.slotRef(null));
    expect(result.current.portal).not.toBeNull();
    act(() => result.current.slotRef(secondSlot));
    const movedPortal = result.current.portal as unknown as {children: React.ReactElement};
    expect(movedPortal.children.key).toBe(firstKey);
    expect(firstSlot).toBeEmptyDOMElement();
    expect(secondSlot.childElementCount).toBe(1);
  });

  it('remounts the preview across project or timeline scopes so deferred footage cannot leak', () => {
    mocks.timeline={resolvedConfig:{output:{resolution:'1280x720',fps:30,file:'preview.mp4'},tracks:[],clips:[],registry:{}}};
    mocks.playback={currentTime:0,previewRef:{current:null},playerContainerRef:{current:null},onPreviewTimeUpdate:vi.fn()};
    mocks.runtime={project:{projectId:'one'},timelineId:'timeline-one'};
    const {result,rerender}=renderHook(()=>useVideoEditorPreviewSurface());
    act(()=>result.current.slotRef(document.createElement('div')));
    const key=()=> (result.current.portal as unknown as {children:React.ReactElement}).children.key;
    const first=key();
    mocks.runtime={project:{projectId:'two'},timelineId:'timeline-one'};
    rerender();
    expect(key()).not.toBe(first);
    const second=key();
    mocks.runtime={project:{projectId:'two'},timelineId:'timeline-two'};
    rerender();
    expect(key()).not.toBe(second);
  });
});
