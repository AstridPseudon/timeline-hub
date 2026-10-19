// @vitest-environment jsdom
import type { PropsWithChildren, CSSProperties } from 'react';
import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { declareAppTransition, prepareTrack, queryDrawFrame, queryTrackFrame } from '@banodoco/timeline-composition/evaluation';
import { VisualClipSequence } from './VisualClip.tsx';
import { preparePlayerTrack } from './playerEvaluation.ts';
import type { ResolvedTimelineClip, TrackDefinition } from '../types/index.ts';

let currentFrame = 0;
const videoProps = vi.hoisted(() => vi.fn());

vi.mock('remotion', async () => {
  const React = await import('react');
  const Frame = React.createContext<number | null>(null);
  const useFrame = () => React.useContext(Frame) ?? currentFrame;
  return {
    useCurrentFrame: useFrame,
    useVideoConfig: () => ({ fps: 30, width: 1920, height: 1080 }),
    useRemotionEnvironment: () => ({ isRendering: false, isClientSideRendering: false }),
    interpolate: (frame: number, [from, to]: number[]) => Math.min(1, Math.max(0, (frame - from) / (to - from))),
    AbsoluteFill: ({ children, style }: PropsWithChildren<{ style?: CSSProperties }>) => <div style={style}>{children}</div>,
    Sequence: ({ children, from = 0, durationInFrames = Infinity, premountFor = 0 }: PropsWithChildren<{
      from?: number; durationInFrames?: number; premountFor?: number;
    }>) => {
      const frame = useFrame();
      if (frame < from - premountFor || frame >= from + durationInFrames) return null;
      return (
        <div data-testid="sequence" data-from={from} data-duration={durationInFrames}
          data-premount={premountFor} data-active={frame >= from}>
          <Frame.Provider value={frame - from}>{children}</Frame.Provider>
        </div>
      );
    },
    Freeze: ({ frame, children }: PropsWithChildren<{ frame: number }>) => (
      <div data-testid="freeze"><Frame.Provider value={frame}>{children}</Frame.Provider></div>
    ),
  };
});

vi.mock('@astrid/packs/rendering/shared/readiness-image', async () => {
  const { useCurrentFrame } = await import('remotion');
  return { ReadinessImage: ({ mediaId }: { mediaId: string }) => (
    <div data-testid="picture" data-clip-id={mediaId} data-frame={useCurrentFrame()} />
  ) };
});
vi.mock('./ReadinessVideo.tsx', async () => {
  const { useCurrentFrame } = await import('remotion');
  return { ReadinessVideo: (props: Record<string, unknown>) => {
    videoProps({ ...props, frame: useCurrentFrame() });
    return <div data-testid="video" data-clip-id={props.clipId as string} />;
  } };
});

const track: TrackDefinition = { id: 'V1', kind: 'visual', label: 'Picture' };
const image = (id: string, at: number, overrides: Partial<ResolvedTimelineClip> = {}): ResolvedTimelineClip => ({
  id, at, track: 'V1', clipType: 'hold', hold: 1, asset: id,
  assetEntry: { type: 'image/png', src: `https://example.test/${id}.png` }, ...overrides,
});

beforeEach(() => {
  currentFrame = 0;
  videoProps.mockClear();
});

describe('VisualClip shared draw plans', () => {
  it.each(['crossfade', 'cross-fade'])('mounts the image before its %s boundary with shared opacity and the correct own clock', type => {
    const previous = image('a', 2);
    const clip = image('b', 3, { transition: { type, duration: 0.4 } });
    const plan = preparePlayerTrack(track, [previous, clip], 30, 1920, 1080).plans.get('b')!;
    currentFrame = 87;
    const { rerender } = render(<VisualClipSequence clip={clip} track={track} fps={30} drawPlan={plan} />);
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-from', '78');
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-duration', '42');
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-premount', '30');
    expect(screen.getByTestId('picture')).toHaveAttribute('data-frame', '0');
    expect(screen.getByTestId('freeze').parentElement).toHaveStyle({ opacity: 0.75 });
    currentFrame = 95;
    rerender(<VisualClipSequence clip={clip} track={track} fps={30} drawPlan={plan} />);
    expect(screen.getByTestId('picture')).toHaveAttribute('data-frame', '5');
    expect(screen.getByTestId('freeze').parentElement).toHaveStyle({ opacity: 1 });
    currentFrame = 120;
    rerender(<VisualClipSequence clip={clip} track={track} fps={30} drawPlan={plan} />);
    expect(screen.queryByTestId('picture')).not.toBeInTheDocument();
  });

  it('preserves the mounted image fade pair with outgoing opacity one and the legacy incoming clock', () => {
    const previous = image('outgoing', 2);
    const incoming = image('incoming', 3, { transition: { type: 'fade', duration: 0.4 } });
    const player = preparePlayerTrack(track, [previous, incoming], 30, 1920, 1080);
    const renderPair = () => <>
      <VisualClipSequence clip={previous} track={track} fps={30}
        drawPlan={player.plans.get(previous.id) ?? null} />
      <VisualClipSequence clip={incoming} predecessor={previous} track={track} fps={30}
        drawPlan={player.plans.get(incoming.id) ?? null} />
    </>;
    const view = render(renderPair());
    // App fade is incoming-only. Public DIP would darken the outgoing image
    // and freeze the incoming clock, changing existing films.
    for (const [frame, local, opacity] of [[77, -1, 0], [78, 0, 0], [84, 6, 0.5], [90, 12, 1]]) {
      currentFrame = frame;
      view.rerender(renderPair());
      const outgoing = view.container.querySelector('[data-clip-id="outgoing"]')!;
      const picture = view.container.querySelector('[data-clip-id="incoming"]')!;
      expect(outgoing).toHaveAttribute('data-frame', String(frame - 60));
      expect(picture).toHaveAttribute('data-frame', String(local));
      const outgoingSequence = outgoing.closest('[data-testid="sequence"]')!;
      const incomingSequence = picture.closest('[data-testid="sequence"]')!;
      expect(outgoingSequence).toHaveAttribute('data-from', '60');
      expect(outgoingSequence).toHaveAttribute('data-duration', '31');
      expect(outgoingSequence.querySelector<HTMLElement>('[style*="opacity"]')?.style.opacity ?? '1').toBe('1');
      expect(incomingSequence).toHaveAttribute('data-from', '78');
      expect(incomingSequence).toHaveAttribute('data-duration', '43');
      expect(incomingSequence).toHaveAttribute('data-active', String(frame >= 78));
      expect(incomingSequence).toHaveAttribute('data-premount', '30');
      expect(picture.parentElement).toHaveStyle({ opacity });
      expect(screen.queryByTestId('freeze')).not.toBeInTheDocument();
    }
    currentFrame = 91;
    view.rerender(renderPair());
    expect(view.container.querySelector('[data-clip-id="outgoing"]')).not.toBeInTheDocument();
    expect(view.container.querySelector('[data-clip-id="incoming"]')).toHaveAttribute('data-frame', '13');
  });

  it('keeps trimmed video on its playing own clock with unchanged premount, speed and audio controls', () => {
    const clip = image('video', 2, { clipType: 'media', hold: undefined, from: 3, to: 5, speed: 2, volume: 0.5,
      assetEntry: { type: 'video/mp4', src: 'https://example.test/clip.mp4' } });
    const renderClip = (muted = false) => <VisualClipSequence clip={clip} track={{ ...track, volume: 0.8, muted }} fps={30} />;
    currentFrame = 35;
    const { rerender } = render(renderClip());
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-active', 'false');
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-premount', '30');
    expect(screen.queryByTestId('freeze')).not.toBeInTheDocument();
    currentFrame = 64;
    rerender(renderClip());
    expect(videoProps).toHaveBeenLastCalledWith(expect.objectContaining({
      frame: 4, trimBefore: 90, trimAfter: 150, playbackRate: 2, volume: 0.4, muted: false,
    }));
    rerender(renderClip(true));
    expect(videoProps).toHaveBeenLastCalledWith(expect.objectContaining({ volume: 0, muted: true }));
    currentFrame = 90;
    rerender(renderClip());
    expect(screen.queryByTestId('video')).not.toBeInTheDocument();
  });

  it('retains the host path for video transitions without freezing or extracting its audio', () => {
    const clip = image('video', 1, { transition: { type: 'crossfade', duration: 0.5 },
      assetEntry: { type: 'video/mp4', src: 'https://example.test/clip.mp4' }, volume: 0.7 });
    currentFrame = 20;
    render(<VisualClipSequence clip={clip} predecessor={image('a', 0)} track={track} fps={30} />);
    expect(screen.getByTestId('sequence')).toHaveAttribute('data-from', '15');
    expect(screen.queryByTestId('freeze')).not.toBeInTheDocument();
    expect(videoProps).toHaveBeenLastCalledWith(expect.objectContaining({ frame: 5, volume: 0.7, muted: false }));
  });

  it.each(['crossfade', 'cross-fade', 'fade'])('measures native %s clocks and opacity against the public planner', type => {
    const previous = image('outgoing', 2, { clipType: 'media', hold: undefined, from: 1, to: 3, speed: 2,
      assetEntry: { type: 'video/mp4', src: 'https://example.test/outgoing.mp4' } });
    const clip = image('incoming', 3, { clipType: 'media', hold: undefined, from: 3, to: 5, speed: 2,
      volume: 0.5, params: { fadeIn: 0.4, fadeOut: 0.4 }, transition: { type, duration: 0.4 },
      assetEntry: { type: 'video/mp4', src: 'https://example.test/incoming.mp4' } });
    const prepared = prepareTrack([{ start: 60, duration: 30 }, { start: 90, duration: 30 }],
      [declareAppTransition(track.id, previous.id, clip.transition!, 30, 'timeline-composition').spec]);
    const incomingPlan = prepared.plans[1];
    expect(incomingPlan).toMatchObject({ drawStart: 78, drawDuration: 42, ownOffset: 12 });
    const player = preparePlayerTrack(track, [previous, clip], 30, 1920, 1080);
    const renderPair = (muted = false) => <>
      <VisualClipSequence clip={previous} track={{ ...track, volume: 0.8, muted }} fps={30}
        drawPlan={player.plans.get(previous.id) ?? null} />
      <VisualClipSequence clip={clip} predecessor={previous} track={{ ...track, volume: 0.8, muted }} fps={30}
        drawPlan={player.plans.get(clip.id) ?? null} />
    </>;
    const view = render(renderPair());
    // Source frames below are media-clock inputs, not decoded samples. Frame 77
    // is premounted/inactive; the mock does not claim it produces audible output.
    for (const [frame, local, canonicalOwn, hostOpacity, canonicalOpacity, outgoingOpacity] of [
      [77, -1, 0, 0, 0, 1], // before the draw window
      [78, 0, 0, 0, 0, 1], // transition start
      [84, 6, 0, 0.5, type === 'fade' ? 0 : 0.5, type === 'fade' ? 0 : 1], // midpoint
      [90, 12, 0, 1, 1, 0], // transition end; outgoing canonical span is excluded
    ]) {
      currentFrame = frame;
      videoProps.mockClear();
      view.rerender(renderPair());
      const media = videoProps.mock.calls.map(([props]) => props).find(props => props.clipId === clip.id)!;
      expect(media).toMatchObject({ frame: local, trimBefore: 90, trimAfter: 150,
        playbackRate: 2, volume: 0.4, muted: false });
      expect(media.trimBefore + media.frame * media.playbackRate).toBe(90 + local * 2);
      const evaluated = queryDrawFrame(incomingPlan, frame - incomingPlan.drawStart);
      expect(evaluated).toMatchObject({ drawLocalFrame: local, ownFrame: canonicalOwn, opacity: canonicalOpacity });
      expect(90 + evaluated.ownFrame * 2).toBe(90);
      const incoming = view.container.querySelector('[data-clip-id="incoming"]')!;
      expect(incoming.parentElement).toHaveStyle({ opacity: hostOpacity });
      expect(incoming.closest('[data-testid="sequence"]')).toHaveAttribute('data-active', String(frame >= 78));
      expect(incoming.closest('[data-testid="sequence"]')).toHaveAttribute('data-duration', '43');
      const outgoing = view.container.querySelector('[data-clip-id="outgoing"]')!;
      expect(outgoing.parentElement?.style.opacity).toBe('');
      const outgoingLayer = queryTrackFrame(prepared, frame).layers.find(layer => layer.clipIndex === 0);
      if (frame < 90) expect(outgoingLayer?.opacity).toBe(outgoingOpacity);
      else expect(outgoingLayer).toBeUndefined();
      expect(screen.queryByTestId('freeze')).not.toBeInTheDocument();
    }
    view.rerender(renderPair(true));
    expect(videoProps).toHaveBeenLastCalledWith(expect.objectContaining({ clipId: clip.id, volume: 0, muted: true }));
    // The legacy host has one extra mount frame; canonical planning is half-open.
    currentFrame = 120;
    view.rerender(renderPair());
    expect(view.container.querySelector('[data-clip-id="incoming"]')).toBeInTheDocument();
    expect(queryTrackFrame(prepared, 120).layers).toEqual([]);
    currentFrame = 121;
    view.rerender(renderPair());
    expect(screen.queryByTestId('video')).not.toBeInTheDocument();
    currentFrame = 120;
    view.rerender(<VisualClipSequence clip={{ ...clip,
      app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 4000 } } }}
      predecessor={previous} track={track} fps={30} drawPlan={null} />);
    expect(screen.queryByTestId('video')).not.toBeInTheDocument();
  });
});
