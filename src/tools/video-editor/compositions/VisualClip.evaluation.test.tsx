// @vitest-environment jsdom
import type { PropsWithChildren, CSSProperties } from 'react';
import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
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
  return { ReadinessImage: () => <div data-testid="picture" data-frame={useCurrentFrame()} /> };
});
vi.mock('./ReadinessVideo.tsx', async () => {
  const { useCurrentFrame } = await import('remotion');
  return { ReadinessVideo: (props: Record<string, unknown>) => {
    videoProps({ ...props, frame: useCurrentFrame() });
    return <div data-testid="video" />;
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
  it('mounts the image before its boundary and renders shared opacity with the correct own clock', () => {
    const previous = image('a', 2);
    const clip = image('b', 3, { transition: { type: 'crossfade', duration: 0.4 } });
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

  it('applies the outgoing half of a shared fade through background', () => {
    const clip = image('a', 0);
    const incoming = image('b', 1, { transition: { type: 'fade', duration: 0.4 } });
    const plan = preparePlayerTrack(track, [clip, incoming], 30, 1920, 1080).plans.get('a')!;
    currentFrame = 21;
    const { container } = render(<VisualClipSequence clip={clip} track={track} fps={30} drawPlan={plan} />);
    expect(container.querySelector('[style*="opacity"]')).toHaveStyle({ opacity: 0.5 });
    expect(screen.getByTestId('picture')).toHaveAttribute('data-frame', '21');
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
});
