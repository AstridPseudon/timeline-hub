// @vitest-environment jsdom
import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AudioTrack } from '@/tools/video-editor/compositions/AudioTrack';
import { getClipDurationInFrames, secondsToFrames } from '@/tools/video-editor/lib/config-utils';
import type { ResolvedTimelineClip, TrackDefinition } from '@/tools/video-editor/types';
// Astrid's renderer component, vendored verbatim from @banodoco/timeline-composition.
import { AudioTrack as RendererAudioTrack } from '../../../../vendor/timeline-composition/typescript/src/AudioTrack';

const sequenceProps: Array<Record<string, unknown>> = [];
const html5AudioProps: Array<Record<string, unknown>> = [];
const mediaAudioProps: Array<Record<string, unknown>> = [];

let currentEnvironment = {
  isRendering: false,
  isClientSideRendering: false,
};

vi.mock('remotion', async () => {
  const React = await import('react');

  return {
    Sequence: ({ children, ...props }: React.PropsWithChildren<Record<string, unknown>>) => {
      sequenceProps.push(props);
      return <div data-testid="sequence">{children}</div>;
    },
    Audio: React.forwardRef<HTMLAudioElement, Record<string, unknown>>((props, ref) => {
      html5AudioProps.push(props);
      return (
        <audio
          data-testid="html5-audio"
          src={props.src as string}
          ref={ref}
          onErrorCapture={props.onErrorCapture as React.ReactEventHandler<HTMLAudioElement> | undefined}
        />
      );
    }),
    useRemotionEnvironment: () => currentEnvironment,
    staticFile: (file: string) => `/static/${file}`,
  };
});

vi.mock('@remotion/media', () => ({
  Audio: (props: Record<string, unknown>) => {
    mediaAudioProps.push(props);
    return <div data-testid="media-audio" />;
  },
}));

vi.mock('@/tools/video-editor/compositions/MediaErrorBoundary', () => ({
  MediaErrorBoundary: ({ children }: React.PropsWithChildren) => <>{children}</>,
}));

const track: TrackDefinition = {
  id: 'A1',
  kind: 'audio',
  label: 'A1',
};

const clip: ResolvedTimelineClip = {
  id: 'clip-1',
  at: 2,
  track: 'A1',
  clipType: 'media',
  asset: 'asset-1',
  from: 1,
  to: 4,
  speed: 1,
  volume: 0.8,
  assetEntry: {
    file: 'audio.mp3',
    src: 'https://example.com/audio.mp3',
    type: 'audio/mpeg',
  },
};

describe('AudioTrack', () => {
  beforeEach(() => {
    sequenceProps.length = 0;
    html5AudioProps.length = 0;
    mediaAudioProps.length = 0;
    currentEnvironment = {
      isRendering: false,
      isClientSideRendering: false,
    };
  });

  describe('fades', () => {
    const fadeCases: Array<{ name: string; fps: number; clip: ResolvedTimelineClip; track?: TrackDefinition }> = [
      { name: 'fade-out only (music-chip)', fps: 30, clip: { ...clip, at: 0, from: 0, to: 31.5, volume: 0.5129, params: { fadeOut: 3 } } },
      { name: 'fade-in and fade-out (music-piano)', fps: 30, clip: { ...clip, at: 28.5, from: 28.5, to: 88.4, volume: 0.7674, params: { fadeIn: 3, fadeOut: 4 } } },
      { name: 'trimmed source (music-orch)', fps: 30, clip: { ...clip, at: 84.4, from: 123.46, to: 199.393331, volume: 0.263, params: { fadeIn: 4, fadeOut: 3 } } },
      { name: 'overlapping ramps at 24 fps', fps: 24, clip: { ...clip, params: { fadeIn: 2, fadeOut: 2.5 } } },
      { name: 'fractional fade lengths at 60 fps', fps: 60, clip: { ...clip, speed: 1.5, params: { fadeIn: 0.41, fadeOut: 0.77 } } },
      { name: 'track gain applies under the ramp', fps: 30, clip: { ...clip, params: { fadeIn: 1 } }, track: { ...track, volume: 0.5 } },
      { name: 'muted track stays silent', fps: 30, clip: { ...clip, params: { fadeOut: 1 } }, track: { ...track, muted: true } },
      { name: 'no fade keeps a plain gain', fps: 30, clip: { ...clip, params: { fadeIn: 0, fadeOut: -1 } } },
    ];

    it.each(fadeCases)('matches the renderer\'s gain envelope at every frame: $name', ({ fps, clip: fadeClip, track: fadeTrack = track }) => {
      render(<RendererAudioTrack clip={fadeClip} track={fadeTrack} assetEntry={{ file: 'https://example.com/audio.mp3' }} fps={fps} />);
      const rendererVolume = html5AudioProps.at(-1)?.volume;
      html5AudioProps.length = 0;
      render(<AudioTrack track={fadeTrack} clips={[fadeClip]} fps={fps} />);
      const previewVolume = html5AudioProps.at(-1)?.volume;

      expect(typeof previewVolume).toBe(typeof rendererVolume);
      if (typeof rendererVolume !== 'function' || typeof previewVolume !== 'function') {
        expect(previewVolume).toBe(rendererVolume);
        return;
      }
      const durationFrames = getClipDurationInFrames(fadeClip, fps);
      for (let frame = 0; frame <= durationFrames; frame += 1) {
        expect(previewVolume(frame), `frame ${frame}`).toBeCloseTo(rendererVolume(frame), 12);
      }
    });

    it('applies the same fades when the editor renders an export', () => {
      currentEnvironment = { isRendering: true, isClientSideRendering: false };
      const fadeClip = { ...clip, params: { fadeIn: 1 } };
      render(<AudioTrack track={track} clips={[fadeClip]} fps={30} />);

      const volume = mediaAudioProps[0]?.volume as (frame: number) => number;
      expect(volume(0)).toBe(0);
      expect(volume(15)).toBeCloseTo(0.4, 12);
      expect(volume(30)).toBeCloseTo(0.8, 12);
    });

    it('keeps the volume function identity across re-renders', () => {
      const fadeClip = { ...clip, params: { fadeIn: 1 } };
      const { rerender } = render(<AudioTrack track={track} clips={[fadeClip]} fps={30} />);
      rerender(<AudioTrack track={track} clips={[{ ...fadeClip }]} fps={30} />);

      expect(html5AudioProps).toHaveLength(2);
      expect(html5AudioProps[1]?.volume).toBe(html5AudioProps[0]?.volume);
    });
  });

  it('premounts preview audio and keeps buffering non-blocking in the player', () => {
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);

    expect(screen.getByTestId('html5-audio')).toBeInTheDocument();
    expect(sequenceProps[0]?.premountFor).toBe(30);
    expect(html5AudioProps[0]?.pauseWhenBuffering).toBe(false);
  });

  it('uses the media audio component while rendering', () => {
    currentEnvironment = {
      isRendering: true,
      isClientSideRendering: false,
    };

    render(<AudioTrack track={track} clips={[clip]} fps={24} />);

    expect(screen.getByTestId('media-audio')).toBeInTheDocument();
    expect(sequenceProps[0]?.premountFor).toBe(24);
    expect(mediaAudioProps[0]?.pauseWhenBuffering).toBe(false);
  });

  it('captures terminal preview failure and retries only after an explicit click', () => {
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);

    fireEvent.error(screen.getByTestId('html5-audio'));

    expect(screen.getByRole('alert')).toHaveTextContent('Audio unavailable.');
    expect(screen.queryByTestId('html5-audio')).toBeNull();
    expect(html5AudioProps).toHaveLength(1);

    fireEvent.click(screen.getByRole('button', { name: 'Retry audio' }));

    expect(screen.queryByRole('alert')).toBeNull();
    expect(screen.getByTestId('html5-audio')).toHaveAttribute('src', clip.assetEntry?.src);
    expect(html5AudioProps).toHaveLength(2);
    expect(html5AudioProps.at(-1)?.pauseWhenBuffering).toBe(false);
  });

  it('clears terminal preview failure when the source identity changes', () => {
    const { rerender } = render(<AudioTrack track={track} clips={[clip]} fps={30} />);

    fireEvent.error(screen.getByTestId('html5-audio'));
    expect(screen.getByRole('alert')).toBeInTheDocument();

    const nextClip: ResolvedTimelineClip = {
      ...clip,
      assetEntry: { ...clip.assetEntry!, src: 'https://example.com/replacement.mp3' },
    };
    rerender(<AudioTrack track={track} clips={[nextClip]} fps={30} />);

    expect(screen.queryByRole('alert')).toBeNull();
    expect(screen.getByTestId('html5-audio')).toHaveAttribute('src', nextClip.assetEntry?.src);
    expect(html5AudioProps.at(-1)?.pauseWhenBuffering).toBe(false);
  });

  it('plays Astrid registry entries that use the generic audio family type', () => {
    const genericAudioClip: ResolvedTimelineClip = {
      ...clip,
      assetEntry: {
        ...clip.assetEntry!,
        type: 'audio',
      },
    };

    render(<AudioTrack track={track} clips={[genericAudioClip]} fps={30} />);

    expect(screen.getByTestId('html5-audio')).toBeInTheDocument();
  });

  it('remounts the audio sequence when a clip moves mid-playback (keyed on at)', () => {
    const { rerender } = render(<AudioTrack track={track} clips={[clip]} fps={30} />);

    const firstSequenceNode = screen.getByTestId('sequence');
    const firstAudioMounters = html5AudioProps.length;

    const movedClip: ResolvedTimelineClip = { ...clip, at: 5 };
    rerender(<AudioTrack track={track} clips={[movedClip]} fps={30} />);

    // The Sequence key includes `at`, so a move remounts the subtree — the only
    // path that re-times Remotion audio during playback.
    expect(screen.getByTestId('sequence')).not.toBe(firstSequenceNode);
    expect(html5AudioProps.length).toBe(firstAudioMounters + 1);
    expect(sequenceProps.at(-1)?.from).toBe(secondsToFrames(5, 30));
  });
});
