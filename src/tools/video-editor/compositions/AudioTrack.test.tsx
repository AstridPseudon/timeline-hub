// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { audioEnvelopeAt, compileAudioEnvelope, type AudioCurve, type AudioEnvelope } from '@banodoco/timeline-composition/evaluation';
import {
  AUDIO_RETRY_DELAYS_MS,
  AUDIO_HOLD_LIMIT_MS,
  AudioTrack,
} from '@/tools/video-editor/compositions/AudioTrack';
import { PreviewAudioFailureProvider } from '@/tools/video-editor/compositions/PreviewMediaFailureContext';
import { PreviewAudioFailureNotice } from '@/tools/video-editor/components/PreviewPanel/PreviewAudioFailureNotice';
import { getClipDurationInFrames, secondsToFrames } from '@/tools/video-editor/lib/config-utils';
import type { ResolvedTimelineClip, TrackDefinition } from '@/tools/video-editor/types';

const sequenceProps: Array<Record<string, unknown>> = [];
const html5AudioProps: Array<Record<string, unknown>> = [];
const mediaAudioProps: Array<Record<string, unknown>> = [];
const playbackHolds = { active: 0, total: 0 };

let currentEnvironment = {
  isRendering: false,
  isClientSideRendering: false,
};
let premounting = false;

const bufferState = {
  delayPlayback: () => {
    playbackHolds.active += 1;
    playbackHolds.total += 1;
    let released = false;
    return {
      unblock: () => {
        if (released) return;
        released = true;
        playbackHolds.active -= 1;
      },
    };
  },
};

vi.mock('remotion', async () => {
  const React = await import('react');
  const SequenceContext = React.createContext<{ premounting: boolean } | null>(null);

  return {
    Internals: { SequenceContext },
    Sequence: ({ children, ...props }: React.PropsWithChildren<Record<string, unknown>>) => {
      sequenceProps.push(props);
      return (
        <SequenceContext.Provider value={{ premounting }}>
          <div data-testid="sequence">{children}</div>
        </SequenceContext.Provider>
      );
    },
    Audio: React.forwardRef<HTMLAudioElement, Record<string, unknown>>((props, ref) => {
      html5AudioProps.push(props);
      // Like Remotion's own (unshared) preview tag, native handlers reach the element.
      const nativeHandlers = Object.fromEntries(Object.entries(props).filter(([key]) => /^on[A-Z]/.test(key)));
      return <audio data-testid="html5-audio" src={props.src as string} ref={ref} {...nativeHandlers} />;
    }),
    // Like Remotion's, the buffer API is stable across renders.
    useBufferState: () => bufferState,
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

const canonicalClip: ResolvedTimelineClip = {
  ...clip,
  app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 160_334 } },
};

const canonicalAudioFailureCases = [
  ['an uncompiled duck', { app: { astrid: {}, duck: {} } }, 'DUCK_UNRENDERED'],
  ['an invalid authored envelope', { audio: { envelope: { keyframes: [] } } }, 'ENVELOPE_UNRENDERED'],
  ['an unknown authored fade curve', { params: { fadeIn: 1, fadeInCurve: 'unknown' } }, 'ENVELOPE_UNRENDERED'],
] as const;

function audioElement(): HTMLAudioElement {
  return screen.getByTestId('html5-audio') as HTMLAudioElement;
}

/** jsdom does not load media; stand in for the browser's loading state. */
function setLoadingState(element: HTMLAudioElement, state: { readyState: number; networkState?: number }) {
  Object.defineProperty(element, 'readyState', { configurable: true, get: () => state.readyState });
  if (state.networkState !== undefined) {
    Object.defineProperty(element, 'networkState', { configurable: true, get: () => state.networkState });
  }
}

function becomePlayable(element: HTMLAudioElement) {
  setLoadingState(element, { readyState: HTMLMediaElement.HAVE_ENOUGH_DATA });
  fireEvent.canPlay(element);
}

function renderPreview(clips: ResolvedTimelineClip[] = [clip]) {
  return render(
    <PreviewAudioFailureProvider>
      <div data-testid="composition">
        <AudioTrack track={track} clips={clips} fps={30} />
      </div>
      <PreviewAudioFailureNotice />
    </PreviewAudioFailureProvider>,
  );
}

describe('AudioTrack', () => {
  beforeEach(() => {
    sequenceProps.length = 0;
    html5AudioProps.length = 0;
    mediaAudioProps.length = 0;
    playbackHolds.active = 0;
    playbackHolds.total = 0;
    premounting = false;
    currentEnvironment = {
      isRendering: false,
      isClientSideRendering: false,
    };
    // jsdom does not implement media loading.
    vi.spyOn(HTMLMediaElement.prototype, 'load').mockImplementation(() => undefined);
  });

  afterEach(() => {
    // Unmount while load() is still stubbed: unmounting releases each element's request.
    cleanup();
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  describe('fades', () => {
    it.each([false, true])('compares trimmed, sped audio fades with the public envelope (rendering=%s)', isRendering => {
      currentEnvironment = { isRendering, isClientSideRendering: false };
      const fadeClip: ResolvedTimelineClip = { ...clip, at: 3, from: 3, to: 5, speed: 2, volume: 0.5,
        transition: { type: 'fade', duration: 0.4 }, params: { fadeIn: 0.4, fadeOut: 0.4 } };
      const fadeTrack = { ...track, volume: 0.8 };
      const envelope = compileAudioEnvelope(fadeClip, 30)!;
      const view = render(<AudioTrack track={fadeTrack} clips={[fadeClip]} fps={30} />);
      const props = (isRendering ? mediaAudioProps : html5AudioProps).at(-1)!;
      expect(sequenceProps.at(-1)).toMatchObject({ from: 90, durationInFrames: 30, premountFor: 60 });
      expect(props).toMatchObject({ trimBefore: 90, trimAfter: 150, playbackRate: 2 });
      const volume = props.volume as (frame: number) => number;
      // AudioTrack starts at authored at=3, independent of visual transition
      // pre-roll. The volume callback is in timeline frames, not source frames.
      for (const [frame, gain] of [[-1, 0], [0, 0], [6, 0.5], [12, 1], [18, 1], [24, 0.5], [29, 1 / 12], [30, 0]]) {
        expect(volume(frame)).toBeCloseTo(0.4 * gain, 12);
        expect(volume(frame)).toBeCloseTo(0.4 * audioEnvelopeAt(envelope, frame / 30), 12);
      }
      // Occurrence clipping moves the mount, while fades retain authored time.
      const bounded = { ...fadeClip, app: { canonicalTiming: { occurrenceStartMs: 3200, occurrenceDurationMs: 600 } } };
      view.rerender(<AudioTrack track={fadeTrack} clips={[bounded]} fps={30} />);
      expect(sequenceProps.at(-1)).toMatchObject({ from: 96, durationInFrames: 18 });
      const boundedVolume = (isRendering ? mediaAudioProps : html5AudioProps).at(-1)!.volume as (frame: number) => number;
      for (const frame of [0, 6, 12, 17]) {
        expect(boundedVolume(frame)).toBeCloseTo(0.4 * audioEnvelopeAt(envelope, (frame + 6) / 30), 12);
      }
      expect(boundedVolume(0)).toBeCloseTo(0.2, 12);
      expect(boundedVolume(6)).toBeCloseTo(0.4, 12);
      expect(boundedVolume(12)).toBeCloseTo(0.4, 12);
      expect(boundedVolume(17)).toBeCloseTo(0.4 * 7 / 12, 12);
      view.rerender(<AudioTrack track={{ ...fadeTrack, muted: true }} clips={[fadeClip]} fps={30} />);
      const mutedVolume = (isRendering ? mediaAudioProps : html5AudioProps).at(-1)!.volume as (frame: number) => number;
      expect(mutedVolume(6)).toBe(0);
    });

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

    it.each(fadeCases)('matches the public envelope at every frame: $name', ({ fps, clip: fadeClip, track: fadeTrack = track }) => {
      const envelope = compileAudioEnvelope(fadeClip, fps);
      render(<AudioTrack track={fadeTrack} clips={[fadeClip]} fps={fps} />);
      const previewVolume = html5AudioProps.at(-1)?.volume;
      const expectedBase = fadeTrack.muted ? 0 : (fadeTrack.volume ?? 1) * (fadeClip.volume ?? 1);
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();

      if (!envelope || typeof previewVolume !== 'function') {
        expect(previewVolume).toBe(expectedBase);
        return;
      }
      const durationFrames = getClipDurationInFrames(fadeClip, fps);
      for (let frame = 0; frame <= durationFrames; frame += 1) {
        expect(previewVolume(frame), `frame ${frame}`).toBeCloseTo(
          expectedBase * audioEnvelopeAt(envelope, frame / fps),
          12,
        );
      }
    });

    it('preserves fixed authored music fade boundaries and durations', () => {
      const cases = [
        {
          clip: { ...clip, at: 0, from: 0, to: 31.5, volume: 1, params: { fadeOut: 3 } },
          values: [[0, 1], [900, 0.5], [945, 0]],
        },
        {
          clip: { ...clip, at: 28.5, from: 28.5, to: 88.4, volume: 1, params: { fadeIn: 3, fadeOut: 4 } },
          values: [[0, 0], [45, 0.5], [90, 1], [1677, 1], [1737, 0.5], [1797, 0]],
        },
        {
          clip: { ...clip, at: 84.4, from: 123.46, to: 199.393331, volume: 1, params: { fadeIn: 4, fadeOut: 3 } },
          values: [[0, 0], [60, 0.5], [120, 1], [2232, 46 / 90], [2278, 0]],
        },
      ] as const;

      for (const { clip: fadeClip, values } of cases) {
        const view = render(<AudioTrack track={track} clips={[fadeClip]} fps={30} />);
        const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
        for (const [frame, expected] of values) {
          expect(volume(frame), `frame ${frame}`).toBeCloseTo(expected, 12);
        }
        view.unmount();
      }
    });

    it('multiplies overlapping ramps', () => {
      const overlapping = { ...clip, at: 0, from: 0, to: 1, volume: 1, params: { fadeIn: 1, fadeOut: 1 } };
      const view = render(<AudioTrack track={track} clips={[overlapping]} fps={30} />);
      const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;

      expect(volume(0)).toBe(0);
      expect(volume(15)).toBeCloseTo(0.25, 12);
      expect(volume(30)).toBe(0);
      view.unmount();
    });

    it.each([undefined, {}, { fadeIn: 0 }, { fadeIn: -1, fadeOut: Number.NaN },
      { fadeIn: '2' }, { fadeOut: Infinity }, { fadeIn: 0.001 }])(
      'keeps a finite plain gain for an unsupported fade value: %j', params => {
        const fadeClip = { ...clip, volume: 0.4, params: params as ResolvedTimelineClip['params'] };
        const view = render(<AudioTrack track={track} clips={[fadeClip]} fps={30} />);

        expect(html5AudioProps.at(-1)?.volume).toBe(0.4);
        view.unmount();
      },
    );

    it.each([0, -1, Number.NaN])('sanitizes an invalid authored speed before envelope compilation: %s', speed => {
      const malformedSpeed = { ...clip, from: 0, to: 2, speed, volume: 1, params: { fadeIn: 0.5 } };
      const view = render(<AudioTrack track={track} clips={[malformedSpeed]} fps={30} />);
      const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;

      expect(volume(7)).toBeCloseTo(7 / 15, 12);
      view.unmount();
    });

    it('honors a supported authored curve through the public envelope', () => {
      const curvedClip = { ...clip, params: { fadeIn: 1, fadeInCurve: 'equal-power' } };
      render(<AudioTrack track={track} clips={[curvedClip]} fps={30} />);

      const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(volume(15)).toBeCloseTo(0.8 * Math.sin(Math.PI / 4), 12);
    });

    it('uses an authored public envelope before legacy fade params', () => {
      const envelopeClip = {
        ...clip,
        volume: 1,
        params: { fadeIn: 1 },
        audio: { envelope: { keyframes: [{ at: 0, value: 0 }, { at: 2, value: 1 }] } },
      } as ResolvedTimelineClip & { audio: { envelope: { keyframes: Array<{ at: number; value: number }> } } };
      render(<AudioTrack track={track} clips={[envelopeClip]} fps={30} />);

      const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(volume(15)).toBeCloseTo(0.25, 12);
    });

    it('recompiles authored envelopes and curves when their semantic values change', () => {
      const envelopeClip = {
        ...clip,
        volume: 1,
        audio: { envelope: { keyframes: [{ at: 0, value: 0 }, { at: 2, value: 1 }] } },
      } as ResolvedTimelineClip & { audio: { envelope: { keyframes: Array<{ at: number; value: number }> } } };
      const view = render(<AudioTrack track={track} clips={[envelopeClip]} fps={30} />);
      const firstVolume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(firstVolume(15)).toBeCloseTo(0.25, 12);

      const changedEnvelope = {
        ...envelopeClip,
        audio: { envelope: { keyframes: [{ at: 0, value: 0 }, { at: 1, value: 1 }] } },
      };
      view.rerender(<AudioTrack track={track} clips={[changedEnvelope]} fps={30} />);
      const secondVolume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(secondVolume).not.toBe(firstVolume);
      expect(secondVolume(15)).toBeCloseTo(0.5, 12);

      const linearFade = { ...clip, volume: 1, params: { fadeIn: 1, fadeInCurve: 'linear' } };
      view.rerender(<AudioTrack track={track} clips={[linearFade]} fps={30} />);
      const linearVolume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      const curvedFade = { ...linearFade, params: { fadeIn: 1, fadeInCurve: 'equal-power' } };
      view.rerender(<AudioTrack track={track} clips={[curvedFade]} fps={30} />);
      const curvedVolume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(curvedVolume).not.toBe(linearVolume);
      expect(curvedVolume(15)).toBeCloseTo(Math.sin(Math.PI / 4), 12);
      view.unmount();
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
      rerender(<AudioTrack track={track} clips={[{ ...fadeClip, params: { ...fadeClip.params } }]} fps={30} />);

      expect(html5AudioProps).toHaveLength(2);
      expect(html5AudioProps[1]?.volume).toBe(html5AudioProps[0]?.volume);
    });
  });

  describe('preview amplification', () => {
    it('routes an authored envelope boost through Web Audio below unity base gain', () => {
      const boostedClip = { ...clip, audio: { envelope: { keyframes: [{ at: 0, value: 2 }] } } };
      const envelope = compileAudioEnvelope(boostedClip, 30)!;
      render(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);

      const props = html5AudioProps.at(-1)!;
      const volume = props.volume as (frame: number) => number;
      expect(volume(15)).toBe(1.6);
      expect(volume(15)).toBe(0.8 * audioEnvelopeAt(envelope, 0.5));
      expect(props.useWebAudioApi).toBe(true);
      expect(props.crossOrigin).toBe('anonymous');
    });

    const unityEnvelope: AudioEnvelope = { keyframes: [{ at: 0, value: 1 }] };
    const doubleEnvelope: AudioEnvelope = { keyframes: [{ at: 0, value: 2 }] };

    it.each([
      { name: 'multiply', envelope: { ...unityEnvelope, multiply: [doubleEnvelope] } },
      { name: 'minimum', envelope: { ...unityEnvelope, minimum: [doubleEnvelope, { keyframes: [{ at: 0, value: 3 }] }] } },
      { name: 'minimum inside multiply', envelope: { ...unityEnvelope, multiply: [{ ...unityEnvelope, minimum: [doubleEnvelope] }] } },
      { name: 'multiply inside minimum', envelope: { ...unityEnvelope, minimum: [{ ...unityEnvelope, multiply: [doubleEnvelope] }] } },
    ])('finds a declared boost in $name', ({ envelope }) => {
      const boostedClip = { ...clip, audio: { envelope } };
      const compiled = compileAudioEnvelope(boostedClip, 30)!;
      render(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);

      const props = html5AudioProps.at(-1)!;
      const volume = props.volume as (frame: number) => number;
      expect(volume(15)).toBe(1.6);
      expect(volume(15)).toBe(0.8 * audioEnvelopeAt(compiled, 0.5));
      expect(props.useWebAudioApi).toBe(true);
      expect(props.crossOrigin).toBe('anonymous');
    });

    it.each<AudioCurve>(['linear', 'equal-power', 'exponential-fast', 'exponential-moderate', 'exponential-slow', 's-curve'])(
      'keeps a nested envelope bounded by unity native with %s interpolation', (curve) => {
        const envelope: AudioEnvelope = {
          keyframes: [{ at: 0, value: 0, curve }, { at: 1, value: 1 }],
          multiply: [{ ...unityEnvelope, minimum: [unityEnvelope] }],
        };
        const envelopeClip = { ...clip, audio: { envelope } };
        render(<AudioTrack track={track} clips={[envelopeClip]} fps={30} />);

        const props = html5AudioProps.at(-1)!;
        const volume = props.volume as (frame: number) => number;
        expect(props.useWebAudioApi).toBeUndefined();
        expect(props.crossOrigin).toBeUndefined();
        for (const frame of [0, 15, 30, 60]) {
          expect(volume(frame)).toBe(0.8 * audioEnvelopeAt(compileAudioEnvelope(envelopeClip, 30)!, frame / 30));
        }
      },
    );

    it('conservatively admits a nested declared boost even when another node silences it', () => {
      const envelope = { ...unityEnvelope, multiply: [doubleEnvelope], minimum: [{ keyframes: [{ at: 0, value: 0 }] }] };
      const silentClip = { ...clip, audio: { envelope } };
      render(<AudioTrack track={track} clips={[silentClip]} fps={30} />);

      const props = html5AudioProps.at(-1)!;
      expect((props.volume as (frame: number) => number)(15)).toBe(0);
      expect(props.useWebAudioApi).toBe(true);
    });

    it.each([
      { name: 'muted track', audioTrack: { ...track, muted: true }, clipVolume: 0.8, gain: 0, amplify: undefined },
      { name: 'zero track gain', audioTrack: { ...track, volume: 0 }, clipVolume: 0.8, gain: 0, amplify: undefined },
      { name: 'zero clip gain', audioTrack: track, clipVolume: 0, gain: 0, amplify: undefined },
      { name: 'half track gain', audioTrack: { ...track, volume: 0.5 }, clipVolume: 0.8, gain: 0.8, amplify: true },
    ])('preserves $name with a boosted envelope', ({ audioTrack, clipVolume, gain, amplify }) => {
      const boostedClip = { ...clip, volume: clipVolume, audio: { envelope: doubleEnvelope } };
      render(<AudioTrack track={audioTrack} clips={[boostedClip]} fps={30} />);

      const props = html5AudioProps.at(-1)!;
      expect((props.volume as (frame: number) => number)(15)).toBe(gain);
      expect(props.useWebAudioApi).toBe(amplify);
      expect(props.crossOrigin).toBe(amplify ? 'anonymous' : undefined);
    });

    it('remounts on envelope backend changes in both directions and retains equivalent callbacks', () => {
      const nativeClip = { ...clip, audio: { envelope: unityEnvelope } };
      const boostedClip = { ...clip, audio: { envelope: doubleEnvelope } };
      const view = render(<AudioTrack track={track} clips={[nativeClip]} fps={30} />);
      const nativeElement = audioElement();
      act(() => becomePlayable(nativeElement));

      view.rerender(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);
      const boostedElement = audioElement();
      const boostedVolume = html5AudioProps.at(-1)?.volume;
      expect(boostedElement).not.toBe(nativeElement);
      expect(nativeElement).not.toHaveAttribute('src');
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBe(true);
      expect(html5AudioProps.at(-1)?.crossOrigin).toBe('anonymous');
      expect(playbackHolds.active).toBe(1);
      act(() => becomePlayable(boostedElement));
      expect(playbackHolds.active).toBe(0);

      const equivalentBoostedClip = { ...boostedClip, audio: { envelope: { keyframes: [{ at: 0, value: 2 }] } } };
      view.rerender(<AudioTrack track={track} clips={[equivalentBoostedClip]} fps={30} />);
      expect(audioElement()).toBe(boostedElement);
      expect(html5AudioProps.at(-1)?.volume).toBe(boostedVolume);

      view.rerender(<AudioTrack track={track} clips={[nativeClip]} fps={30} />);
      expect(audioElement()).not.toBe(boostedElement);
      expect(audioElement()).not.toBe(nativeElement);
      expect(boostedElement).not.toHaveAttribute('src');
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();
      expect(html5AudioProps.at(-1)?.crossOrigin).toBeUndefined();
      expect(playbackHolds.active).toBe(1);
      act(() => becomePlayable(audioElement()));
      expect(playbackHolds.active).toBe(0);
    });

    it('keeps boosted callbacks in authored time across occurrence bounds, trim and speed', () => {
      const boostedClip = { ...clip, at: 3, from: 3, to: 7, speed: 2,
        audio: { envelope: { keyframes: [{ at: 0, value: 1 }, { at: 1, value: 2 }] } },
        app: { canonicalTiming: { occurrenceStartMs: 3200, occurrenceDurationMs: 600 } } };
      const envelope = compileAudioEnvelope(boostedClip, 30)!;
      render(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);

      const props = html5AudioProps.at(-1)!;
      expect(sequenceProps.at(-1)).toMatchObject({ from: 96, durationInFrames: 18 });
      expect(props).toMatchObject({ trimBefore: 90, trimAfter: 126, playbackRate: 2, useWebAudioApi: true });
      const volume = props.volume as (frame: number) => number;
      for (const frame of [0, 6, 12, 17]) {
        expect(volume(frame)).toBe(0.8 * audioEnvelopeAt(envelope, (frame + 6) / 30));
      }
      expect(volume(17)).toBeGreaterThan(1);
    });

    it('remounts the preview audio when gain crosses the amplification threshold in either direction', () => {
      const { rerender } = render(<AudioTrack track={track} clips={[{ ...clip, volume: 1.2 }]} fps={30} />);
      const boostedElement = audioElement();
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBe(true);

      rerender(<AudioTrack track={track} clips={[{ ...clip, volume: 1 }]} fps={30} />);
      const ordinaryElement = audioElement();
      expect(ordinaryElement).not.toBe(boostedElement);
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();

      rerender(<AudioTrack track={track} clips={[{ ...clip, volume: 1.2 }]} fps={30} />);
      expect(audioElement()).not.toBe(ordinaryElement);
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBe(true);
    });

    it('routes boosted gain through Web Audio, including fade frames below unity', () => {
      const voiceOver = { ...clip, volume: 1.2589, params: { fadeIn: 1 } };
      render(<AudioTrack track={track} clips={[voiceOver]} fps={30} />);

      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBe(true);
      expect(html5AudioProps.at(-1)?.crossOrigin).toBe('anonymous');
      const volume = html5AudioProps.at(-1)?.volume as (frame: number) => number;
      expect(volume(0)).toBe(0);
      expect(volume(30)).toBeCloseTo(1.2589, 12);
      expect(playbackHolds.active).toBe(1);
      act(() => becomePlayable(audioElement()));
      expect(playbackHolds.active).toBe(0);
    });

    it.each([0, 0.8, 1])('keeps gain %s on the ordinary preview path', (gain) => {
      render(<AudioTrack track={track} clips={[{ ...clip, volume: gain }]} fps={30} />);

      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();
      expect(html5AudioProps.at(-1)?.crossOrigin).toBeUndefined();
      expect(html5AudioProps.at(-1)?.volume).toBe(gain);
    });
  });

  describe('loading ahead and buffering', () => {
    it.each([
      ['an ordinary clip', clip],
      ['a canonical clip', canonicalClip],
    ])('premounts %s at least two seconds ahead', (_name, premountClip) => {
      render(<AudioTrack track={track} clips={[premountClip]} fps={30} />);

      expect(sequenceProps[0]?.premountFor).toBeGreaterThanOrEqual(2 * 30);
    });

    it('buffers the whole premount window', () => {
      render(<AudioTrack track={track} clips={[clip]} fps={30} />);

      expect(html5AudioProps[0]?.preload).toBe('auto');
    });

    it('makes the Player wait while an active clip cannot play, and resume once it can', () => {
      render(<AudioTrack track={track} clips={[clip]} fps={30} />);
      expect(playbackHolds.active).toBe(1);

      act(() => becomePlayable(audioElement()));
      expect(playbackHolds.active).toBe(0);

      // An underrun mid-play holds again until data arrives.
      act(() => {
        setLoadingState(audioElement(), { readyState: HTMLMediaElement.HAVE_CURRENT_DATA });
        fireEvent.waiting(audioElement());
      });
      expect(playbackHolds.active).toBe(1);
      act(() => becomePlayable(audioElement()));
      expect(playbackHolds.active).toBe(0);
    });

    it('lets a premounted clip load without holding, then holds on arrival without restarting its request', () => {
      premounting = true;
      const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
      const element = audioElement();
      setLoadingState(element, { readyState: HTMLMediaElement.HAVE_METADATA, networkState: HTMLMediaElement.NETWORK_LOADING });
      expect(playbackHolds.total).toBe(0);
      // Remotion's own pauseWhenBuffering calls load() here, aborting the request in flight.
      expect(html5AudioProps.every((props) => props.pauseWhenBuffering === false)).toBe(true);

      premounting = false;
      view.rerender(<AudioTrack track={track} clips={[{ ...clip }]} fps={30} />);

      expect(audioElement()).toBe(element);
      expect(playbackHolds.active).toBe(1);
      expect(HTMLMediaElement.prototype.load).not.toHaveBeenCalled();
      act(() => becomePlayable(element));
      expect(playbackHolds.active).toBe(0);
    });

    it('starts an element the browser left idle (no preload) once its clip is due', () => {
      premounting = true;
      const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
      setLoadingState(audioElement(), { readyState: HTMLMediaElement.HAVE_NOTHING, networkState: HTMLMediaElement.NETWORK_IDLE });

      premounting = false;
      view.rerender(<AudioTrack track={track} clips={[{ ...clip }]} fps={30} />);

      expect(HTMLMediaElement.prototype.load).toHaveBeenCalledTimes(1);
    });
  });

  describe('failures', () => {
    it.each(canonicalAudioFailureCases)('reports %s in preview and clears after readiness on correction', (_name, invalidFields, code) => {
      const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined);
      const validClip = { ...clip, app: { astrid: {} } };
      const view = renderPreview([validClip]);
      expect(screen.getByTestId('html5-audio')).toBeInTheDocument();

      const invalidClip = { ...validClip, ...invalidFields };
      view.rerender(
        <PreviewAudioFailureProvider>
          <div data-testid="composition">
            <AudioTrack track={track} clips={[invalidClip]} fps={30} />
          </div>
          <PreviewAudioFailureNotice />
        </PreviewAudioFailureProvider>,
      );
      expect(screen.queryByTestId('html5-audio')).toBeNull();
      expect(consoleError).toHaveBeenCalledWith(expect.stringContaining('MediaErrorBoundary'));
      expect(consoleError).toHaveBeenCalledWith(expect.stringContaining(code));
      expect(screen.getByTestId('preview-audio-failure')).toHaveTextContent('Audio unavailable for 1 clip');

      view.rerender(
        <PreviewAudioFailureProvider>
          <div data-testid="composition">
            <AudioTrack track={track} clips={[validClip]} fps={30} />
          </div>
          <PreviewAudioFailureNotice />
        </PreviewAudioFailureProvider>,
      );
      expect(screen.getByTestId('html5-audio')).toBeInTheDocument();
      act(() => becomePlayable(audioElement()));
      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();
      consoleError.mockRestore();
    });

    it.each(canonicalAudioFailureCases)('propagates %s during rendering', (_name, invalidFields, code) => {
      currentEnvironment = { isRendering: true, isClientSideRendering: false };
      const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined);
      const invalidClip = { ...clip, app: { astrid: {} }, ...invalidFields };

      expect(() => render(<AudioTrack track={track} clips={[invalidClip]} fps={30} />)).toThrow(code);
      expect(consoleError).toHaveBeenCalledWith(expect.stringContaining('The above error occurred in the <ClipAudio> component'));
      consoleError.mockRestore();
    });

    it('recovers from a transient failure without drawing anything into the frame', () => {
      vi.useFakeTimers();
      renderPreview();
      const failedElement = audioElement();

      act(() => {
        fireEvent.error(failedElement);
      });

      const composition = screen.getByTestId('composition');
      expect(composition.textContent).toBe('');
      expect(within(composition).queryByRole('alert')).toBeNull();
      expect(within(composition).queryByRole('button')).toBeNull();
      expect(screen.queryByTestId('html5-audio')).toBeNull();
      // The abandoned request is released, and the Player holds while the active clip waits to retry.
      expect(failedElement).not.toHaveAttribute('src');
      expect(playbackHolds.active).toBe(1);

      act(() => {
        vi.advanceTimersByTime(AUDIO_RETRY_DELAYS_MS[0]);
      });

      const retried = audioElement();
      expect(retried).not.toBe(failedElement);
      expect(retried).toHaveAttribute('src', clip.assetEntry?.src);
      // One continuous hold from the failure until the retried element can play.
      expect(playbackHolds).toEqual({ active: 1, total: 1 });

      act(() => becomePlayable(retried));
      expect(playbackHolds.active).toBe(0);
      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();
      expect(composition.textContent).toBe('');
    });

    it('does not hold the Player for a clip that is still premounting', () => {
      vi.useFakeTimers();
      premounting = true;
      renderPreview();

      act(() => {
        fireEvent.error(audioElement());
      });

      expect(playbackHolds.total).toBe(0);
    });

    it('backs off between bounded retries, then gives up, releases the Player and reports in the editor chrome', () => {
      vi.useFakeTimers();
      renderPreview();

      for (const delay of AUDIO_RETRY_DELAYS_MS) {
        act(() => {
          fireEvent.error(audioElement());
        });
        act(() => {
          vi.advanceTimersByTime(delay - 1);
        });
        expect(screen.queryByTestId('html5-audio')).toBeNull();
        act(() => {
          vi.advanceTimersByTime(1);
        });
        expect(screen.getByTestId('html5-audio')).toBeInTheDocument();
      }
      act(() => {
        fireEvent.error(audioElement());
      });
      act(() => {
        vi.runOnlyPendingTimers();
      });

      expect(screen.queryByTestId('html5-audio')).toBeNull();
      expect(playbackHolds.active).toBe(0);
      const composition = screen.getByTestId('composition');
      expect(composition.textContent).toBe('');
      const notice = screen.getByTestId('preview-audio-failure');
      expect(composition).not.toContainElement(notice);
      expect(notice).toHaveTextContent('Audio unavailable for 1 clip');

      act(() => {
        fireEvent.click(within(notice).getByRole('button', { name: 'Retry audio' }));
      });

      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();
      act(() => {
        fireEvent.canPlay(audioElement());
      });
      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();
      expect(html5AudioProps.at(-1)?.src).toBe(clip.assetEntry?.src);
    });

    it('holds the Player while bytes arrive, then lets playback go on without restarting a request that delivers nothing', () => {
      vi.useFakeTimers();
      renderPreview();
      const slow = audioElement();

      for (let elapsed = 0; elapsed < 3 * AUDIO_HOLD_LIMIT_MS; elapsed += AUDIO_HOLD_LIMIT_MS / 2) {
        act(() => {
          vi.advanceTimersByTime(AUDIO_HOLD_LIMIT_MS / 2);
          fireEvent.progress(slow);
        });
      }
      expect(playbackHolds.active).toBe(1);

      act(() => {
        vi.advanceTimersByTime(AUDIO_HOLD_LIMIT_MS);
      });
      expect(playbackHolds.active).toBe(0);
      // Slow is not down: the same request carries on, and nothing is reported.
      expect(audioElement()).toBe(slow);
      expect(slow).toHaveAttribute('src', clip.assetEntry?.src);
      expect(HTMLMediaElement.prototype.load).not.toHaveBeenCalled();
      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();

      // When it can play it joins; a later underrun may hold the Player again.
      act(() => becomePlayable(slow));
      act(() => {
        setLoadingState(slow, { readyState: HTMLMediaElement.HAVE_CURRENT_DATA });
        fireEvent.waiting(slow);
      });
      expect(playbackHolds.active).toBe(1);
    });

    it('clears a reported failure when the clip later plays', () => {
      vi.useFakeTimers();
      const view = renderPreview();
      for (let attempt = 0; attempt <= AUDIO_RETRY_DELAYS_MS.length; attempt += 1) {
        act(() => {
          fireEvent.error(audioElement());
        });
        act(() => {
          vi.runOnlyPendingTimers();
        });
      }
      expect(screen.getByTestId('preview-audio-failure')).toBeInTheDocument();

      // Seeking away and back remounts the clip with a fresh retry budget.
      view.rerender(
        <PreviewAudioFailureProvider>
          <div data-testid="composition">
            <AudioTrack track={track} clips={[{ ...clip, at: 3 }]} fps={30} />
          </div>
          <PreviewAudioFailureNotice />
        </PreviewAudioFailureProvider>,
      );
      act(() => {
        fireEvent.canPlay(audioElement());
      });

      expect(screen.queryByTestId('preview-audio-failure')).toBeNull();
    });
  });

  it('uses the media audio component while rendering', () => {
    currentEnvironment = {
      isRendering: true,
      isClientSideRendering: false,
    };

    render(<AudioTrack track={track} clips={[clip]} fps={24} />);

    expect(screen.getByTestId('media-audio')).toBeInTheDocument();
    expect(sequenceProps[0]?.premountFor).toBeGreaterThanOrEqual(2 * 24);
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

  it('starts a fresh element when the source identity changes', () => {
    const { rerender } = render(<AudioTrack track={track} clips={[clip]} fps={30} />);

    const nextClip: ResolvedTimelineClip = {
      ...clip,
      assetEntry: { ...clip.assetEntry!, src: 'https://example.com/replacement.mp3' },
    };
    rerender(<AudioTrack track={track} clips={[nextClip]} fps={30} />);

    expect(screen.getByTestId('html5-audio')).toHaveAttribute('src', nextClip.assetEntry?.src);
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
