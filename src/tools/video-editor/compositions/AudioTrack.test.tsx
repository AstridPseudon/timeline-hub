// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  compileAudioEnvelope,
  computeMediaTrim,
  getSanitizedPlaybackRate,
  type AudioCurve,
  type AudioEnvelope,
} from '@banodoco/timeline-composition/evaluation';
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
const NativeURL = URL;

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

const flushPreview = () => act(async () => {
  await Promise.resolve();
  await Promise.resolve();
});

function preparedSource(clip: ResolvedTimelineClip, fps: number) {
  const envelope = compileAudioEnvelope(clip, fps)!;
  return {
    file: 'https://example.com/prepared-envelope.wav',
    envelope_key: JSON.stringify(envelope),
    source_from: computeMediaTrim(clip, fps).trimBefore / fps,
    playback_rate: getSanitizedPlaybackRate(clip.speed),
  };
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
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, arrayBuffer: async () => new ArrayBuffer(8) }));
    vi.stubGlobal('AudioContext', class {
      close = vi.fn().mockResolvedValue(undefined);
      decodeAudioData = vi.fn().mockResolvedValue({
        numberOfChannels: 1,
        sampleRate: 48_000,
        getChannelData: () => new Float32Array(48_000),
      });
    });
    vi.stubGlobal('URL', class extends NativeURL {
      static createObjectURL = vi.fn(() => 'blob:test');
      static revokeObjectURL = vi.fn();
    });
  });

  afterEach(() => {
    // Unmount while load() is still stubbed: unmounting releases each element's request.
    cleanup();
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  describe('fades', () => {
    it('bakes preview fades into continuous PCM and leaves native playback at constant gain', async () => {
      const fadeClip = { ...clip, at: 3, from: 3, to: 5, speed: 2, volume: 0.5,
        params: { fadeIn: 0.4, fadeOut: 0.4 } };
      render(<AudioTrack track={{ ...track, volume: 0.8 }} clips={[fadeClip]} fps={30} />);
      expect(screen.queryByTestId('html5-audio')).toBeNull();
      await flushPreview();
      expect(html5AudioProps.at(-1)).toMatchObject({
        src: 'blob:test', trimBefore: 90, trimAfter: 150, playbackRate: 2, volume: 0.4,
      });
      expect(typeof html5AudioProps.at(-1)?.volume).toBe('number');
      expect(vi.mocked(fetch)).toHaveBeenCalledTimes(1);
    });

    it('uses a matching prepared source for rendering with one constant gain', () => {
      currentEnvironment = { isRendering: true, isClientSideRendering: false };
      const fadeClip = {
        ...clip, at: 3, from: 3, to: 5, speed: 2, volume: 0.5,
        params: { fadeIn: 1 },
        audio: { render_source: preparedSource({ ...clip, at: 3, from: 3, to: 5, speed: 2, volume: 0.5, params: { fadeIn: 1 } }, 30) },
      };
      render(<AudioTrack track={{ ...track, volume: 0.8 }} clips={[fadeClip]} fps={30} />);
      expect(mediaAudioProps.at(-1)).toMatchObject({
        src: 'https://example.com/prepared-envelope.wav',
        trimBefore: 90, trimAfter: 150, playbackRate: 2, volume: 0.4,
      });
      expect(typeof mediaAudioProps.at(-1)?.volume).toBe('number');
    });

    it('re-bakes after authored envelope semantics change', async () => {
      const first = { ...clip, volume: 1, audio: { envelope: { keyframes: [{ at: 0, value: 0 }, { at: 2, value: 1 }] } } };
      const view = render(<AudioTrack track={track} clips={[first]} fps={30} />);
      await flushPreview();
      const firstProps = html5AudioProps.at(-1)!;
      const changed = { ...first, audio: { envelope: { keyframes: [{ at: 0, value: 0 }, { at: 1, value: 1 }] } } };
      view.rerender(<AudioTrack track={track} clips={[changed]} fps={30} />);
      await flushPreview();
      expect(html5AudioProps.at(-1)?.volume).toBe(1);
      expect(html5AudioProps.at(-1)).not.toBe(firstProps);
      expect(vi.mocked(fetch)).toHaveBeenCalledTimes(2);
    });

    it.each([undefined, {}, { fadeIn: 0 }, { fadeIn: -1, fadeOut: Number.NaN },
      { fadeIn: '2' }, { fadeOut: Infinity }, { fadeIn: 0.001 }, { fadeIn: 0, fadeOut: -1 }])(
      'keeps unsupported fade values on the ordinary native path: %j', params => {
      const malformed = { ...clip, volume: 0.4, params: params as ResolvedTimelineClip['params'] };
      render(<AudioTrack track={track} clips={[malformed]} fps={30} />);
      expect(html5AudioProps.at(-1)).toMatchObject({ src: clip.assetEntry?.src, volume: 0.4 });
      expect(typeof html5AudioProps.at(-1)?.volume).toBe('number');
      },
    );

    it('keeps authored timing and native playback gain when the track is muted', () => {
      const muted = { ...clip, params: undefined };
      render(<AudioTrack track={{ ...track, muted: true }} clips={[muted]} fps={30} />);
      expect(html5AudioProps.at(-1)).toMatchObject({
        src: clip.assetEntry?.src, trimBefore: 30, trimAfter: 120, playbackRate: 1, volume: 0,
      });
    });
  });

  describe('preview amplification', () => {
    it('routes an authored envelope boost through Web Audio after PCM preparation', async () => {
      const boostedClip = { ...clip, audio: { envelope: { keyframes: [{ at: 0, value: 2 }] } } };
      render(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);
      await flushPreview();
      const props = html5AudioProps.at(-1)!;
      expect(props).toMatchObject({ volume: 0.8, useWebAudioApi: true, crossOrigin: 'anonymous', src: 'blob:test' });
      expect(typeof props.volume).toBe('number');
    });

    it.each(['linear', 'equal-power', 's-curve'] as const)(
      'keeps a bounded nested envelope on native gain with %s interpolation', async curve => {
        const envelope: AudioEnvelope = {
          keyframes: [{ at: 0, value: 0, curve }, { at: 1, value: 1 }],
          multiply: [{ keyframes: [{ at: 0, value: 1 }] }],
        };
        render(<AudioTrack track={track} clips={[{ ...clip, audio: { envelope } }]} fps={30} />);
        await flushPreview();
        expect(html5AudioProps.at(-1)).toMatchObject({ volume: 0.8, src: 'blob:test' });
        expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();
        expect(html5AudioProps.at(-1)?.crossOrigin).toBeUndefined();
      },
    );

    it.each([
      { name: 'muted track', audioTrack: { ...track, muted: true }, clipVolume: 0.8, gain: 0 },
      { name: 'zero track gain', audioTrack: { ...track, volume: 0 }, clipVolume: 0.8, gain: 0 },
      { name: 'zero clip gain', audioTrack: track, clipVolume: 0, gain: 0 },
      { name: 'half track gain', audioTrack: { ...track, volume: 0.5 }, clipVolume: 0.8, gain: 0.4 },
    ])('preserves $name with a boosted envelope', async ({ audioTrack, clipVolume, gain }) => {
      const boostedClip = { ...clip, volume: clipVolume, audio: { envelope: { keyframes: [{ at: 0, value: 2 }] } } };
      render(<AudioTrack track={audioTrack} clips={[boostedClip]} fps={30} />);
      await flushPreview();
      expect(html5AudioProps.at(-1)?.volume).toBe(gain);
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBe(gain > 0 ? true : undefined);
    });

    it('keeps occurrence bounds on the native window while baking against authored time', async () => {
      const boostedClip = { ...clip, at: 3, from: 3, to: 7, speed: 2,
        audio: { envelope: { keyframes: [{ at: 0, value: 1 }, { at: 1, value: 2 }] } },
        app: { canonicalTiming: { occurrenceStartMs: 3200, occurrenceDurationMs: 600 } } };
      render(<AudioTrack track={track} clips={[boostedClip]} fps={30} />);
      await flushPreview();
      expect(sequenceProps.at(-1)).toMatchObject({ from: 96, durationInFrames: 18 });
      expect(html5AudioProps.at(-1)).toMatchObject({
        trimBefore: 90, trimAfter: 126, playbackRate: 2, volume: 0.8, useWebAudioApi: true, src: 'blob:test',
      });
    });

    it('remounts ordinary preview audio when gain crosses the Web Audio threshold', () => {
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

    it.each([0, 0.8, 1])('keeps gain %s on the ordinary preview path', gain => {
      render(<AudioTrack track={track} clips={[{ ...clip, volume: gain }]} fps={30} />);
      expect(html5AudioProps.at(-1)).toMatchObject({ src: clip.assetEntry?.src, volume: gain });
      expect(html5AudioProps.at(-1)?.useWebAudioApi).toBeUndefined();
      expect(html5AudioProps.at(-1)?.crossOrigin).toBeUndefined();
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
