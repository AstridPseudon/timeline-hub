import { memo, useContext, useEffect, useMemo, useReducer, useRef, type FC } from 'react';
import { Audio as Html5Audio, Internals, Sequence, useBufferState, useRemotionEnvironment } from 'remotion';
import { Audio as MediaAudio } from '@remotion/media';
import {
  getClipDurationInFrames,
  getSanitizedMediaSrc,
  getSanitizedMediaTrimProps,
  getSanitizedPlaybackRate,
  getSanitizedVolume,
  secondsToFrames,
} from '@/tools/video-editor/lib/config-utils.ts';
import { getAudioFade, getAudioVolumeProp, type AudioVolumeProp } from '@/tools/video-editor/lib/audioFade.ts';
import { MediaErrorBoundary } from '@/tools/video-editor/compositions/MediaErrorBoundary.tsx';
import { useOptionalPreviewAudioFailureReporter } from '@/tools/video-editor/compositions/PreviewMediaFailureContext.tsx';
import type { ResolvedTimelineClip, TrackDefinition } from '@/tools/video-editor/types/index.ts';
import { boundCanonicalClipToOccurrence } from '@/tools/video-editor/lib/canonicalRenderBounds.ts';

/**
 * Audio mounts this far ahead of its first frame. Remotion keeps a premounted
 * element paused and pre-seeked to the clip's first sample, so with
 * `preload="auto"` it is buffered and ready when the playhead arrives.
 */
export const AUDIO_PREMOUNT_SECONDS = 2;

/**
 * Delays before each automatic retry of a failed or stalled request. After the
 * last one the clip gives up, plays silently and reports to the editor chrome.
 */
export const AUDIO_RETRY_DELAYS_MS = [500, 1000, 2000] as const;

/**
 * A request that delivers no bytes for this long counts as failed, so a dead
 * connection cannot hold the Player forever. It is well above the slowest
 * healthy first byte measured under load (18 s), so slow is not taken for down.
 */
export const AUDIO_STALL_LIMIT_MS = 20_000;

type AttemptState = Readonly<{
  /** Each retry mounts a fresh <audio> element and so a fresh request. */
  mount: number;
  /** Consecutive failures since the clip last became playable. */
  failures: number;
  phase: 'mounted' | 'backoff' | 'gave-up';
}>;

type AttemptEvent = 'failed' | 'backoff-elapsed' | 'playable' | 'retry';

const INITIAL_ATTEMPT: AttemptState = { mount: 0, failures: 0, phase: 'mounted' };

function reduceAttempt(state: AttemptState, event: AttemptEvent): AttemptState {
  switch (event) {
    case 'failed': {
      if (state.phase !== 'mounted') return state;
      const failures = state.failures + 1;
      return { ...state, failures, phase: failures > AUDIO_RETRY_DELAYS_MS.length ? 'gave-up' : 'backoff' };
    }
    case 'backoff-elapsed':
      return state.phase === 'backoff' ? { ...state, mount: state.mount + 1, phase: 'mounted' } : state;
    case 'playable':
      return state.failures === 0 ? state : { ...state, failures: 0 };
    case 'retry':
      return state.phase === 'gave-up' ? { mount: state.mount + 1, failures: 0, phase: 'mounted' } : state;
  }
}

/** Stop an abandoned element's network activity (the standard media teardown). */
function releaseMediaRequest(element: HTMLAudioElement): void {
  element.removeAttribute('src');
  element.load();
}

type PreviewAudioProps = {
  clipId: string;
  src: string;
  trimBefore: number;
  trimAfter?: number;
  playbackRate: number;
  volume: AudioVolumeProp;
};

/**
 * Interactive-preview audio that plays like the render: buffered ahead, in
 * sync, and never drawn into the frame.
 *
 * - The Player waits (Remotion's buffer state) while an active clip cannot
 *   play yet, instead of running on silently and re-seeking a starved element.
 * - A failed or stalled request is retried on a fresh element with backoff.
 *   While an active clip waits to retry, it keeps holding the Player, so a
 *   transient failure costs time rather than sync.
 * - After the bounded retries the clip gives up, which releases the Player,
 *   and reports to the editor chrome. The composition itself renders nothing.
 */
const PreviewAudio: FC<PreviewAudioProps> = ({ clipId, src, ...media }) => {
  const reporter = useOptionalPreviewAudioFailureReporter();
  const premounting = useContext(Internals.SequenceContext)?.premounting ?? false;
  const buffer = useBufferState();
  const [attempt, dispatch] = useReducer(reduceAttempt, INITIAL_ATTEMPT);
  const elementRef = useRef<HTMLAudioElement | null>(null);
  const isMounted = attempt.phase === 'mounted';

  useEffect(() => {
    if (attempt.phase !== 'backoff') return undefined;
    const timer = window.setTimeout(() => dispatch('backoff-elapsed'), AUDIO_RETRY_DELAYS_MS[attempt.failures - 1]);
    return () => window.clearTimeout(timer);
  }, [attempt.phase, attempt.failures]);

  useEffect(() => {
    if (attempt.phase !== 'backoff' || premounting) return undefined;
    return buffer.delayPlayback().unblock;
  }, [attempt.phase, buffer, premounting]);

  // The callbacks are stable; only `retryGeneration` changes on Retry.
  const reportFailure = reporter?.reportFailure;
  const clearFailure = reporter?.clearFailure;
  useEffect(() => {
    if (attempt.phase === 'gave-up') reportFailure?.({ clipId, source: src });
  }, [attempt.phase, clipId, reportFailure, src]);

  const retryGeneration = reporter?.retryGeneration ?? 0;
  const seenRetryGeneration = useRef(retryGeneration);
  useEffect(() => {
    if (retryGeneration === seenRetryGeneration.current) return;
    seenRetryGeneration.current = retryGeneration;
    dispatch('retry');
  }, [retryGeneration]);

  // An element abandoned by a retry, or unmounted with its clip, stops
  // downloading; `preload="auto"` would otherwise keep fetching in the background.
  useEffect(() => {
    const element = elementRef.current;
    if (!isMounted || !element) return undefined;
    return () => releaseMediaRequest(element);
  }, [attempt.mount, isMounted]);

  useEffect(() => {
    const element = elementRef.current;
    if (!isMounted || !element) return undefined;
    const onError = () => dispatch('failed');
    const onPlayable = () => {
      dispatch('playable');
      clearFailure?.(clipId);
    };
    element.addEventListener('error', onError);
    element.addEventListener('canplay', onPlayable);
    return () => {
      element.removeEventListener('error', onError);
      element.removeEventListener('canplay', onPlayable);
    };
  }, [attempt.mount, clearFailure, clipId, isMounted]);

  // Stall watchdog: runs only while an active clip is starved of data, i.e.
  // while it holds the Player. Every received chunk restarts it.
  useEffect(() => {
    const element = elementRef.current;
    if (!isMounted || premounting || !element) return undefined;
    let timer: number | null = null;
    const disarm = () => {
      if (timer !== null) window.clearTimeout(timer);
      timer = null;
    };
    const arm = () => {
      disarm();
      if (element.readyState >= element.HAVE_FUTURE_DATA) return;
      timer = window.setTimeout(() => dispatch('failed'), AUDIO_STALL_LIMIT_MS);
    };
    const onWaiting = () => {
      if (timer === null) arm();
    };
    const onProgress = () => {
      if (timer !== null) arm();
    };
    arm();
    element.addEventListener('waiting', onWaiting);
    element.addEventListener('progress', onProgress);
    element.addEventListener('canplay', disarm);
    return () => {
      disarm();
      element.removeEventListener('waiting', onWaiting);
      element.removeEventListener('progress', onProgress);
      element.removeEventListener('canplay', disarm);
    };
  }, [attempt.mount, isMounted, premounting]);

  if (!isMounted) return null;

  return (
    <Html5Audio
      key={attempt.mount}
      ref={elementRef}
      src={src}
      {...media}
      // Buffer the whole premount window, not just metadata.
      preload="auto"
      pauseWhenBuffering
    />
  );
};

const AudioTrackComponent: FC<{
  track: TrackDefinition;
  clips: ResolvedTimelineClip[];
  fps: number;
}> = ({ track, clips, fps }) => {
  const environment = useRemotionEnvironment();
  const isRendering = environment.isRendering || environment.isClientSideRendering;

  return (
    <>
      {clips.map((clip) => {
        const boundedClip = boundCanonicalClipToOccurrence(clip);
        if (!boundedClip) return null;
        const renderClip = boundedClip;
        const mediaSrc = getSanitizedMediaSrc(renderClip.assetEntry?.src);
        const assetType = renderClip.assetEntry?.type?.toLowerCase() ?? '';
        // Astrid's registry uses both MIME types (for example audio/mpeg) and
        // the canonical media-family values (audio/video). Treat both forms
        // as playable here; otherwise generic `audio` entries silently vanish
        // while later clips with MIME metadata still play.
        const isPlayableAudio = assetType === 'audio'
          || assetType === 'video'
          || assetType.startsWith('audio/')
          || assetType.startsWith('video/');
        const effectiveVolume = track.muted ? 0 : getSanitizedVolume(track.volume) * getSanitizedVolume(renderClip.volume);
        const playbackRate = getSanitizedPlaybackRate(renderClip.speed);
        const trimProps = getSanitizedMediaTrimProps(renderClip, fps);

        return (
          <Sequence
            // Remotion's Sequence + Audio timing is not fully updated by prop changes during playback,
            // so audio clips need a remount whenever timing or playback-rate inputs change.
            key={`${renderClip.id}-${renderClip.at}-${renderClip.from ?? 0}-${renderClip.to ?? ''}-${renderClip.speed ?? 1}`}
            from={secondsToFrames(renderClip.at, fps)}
            durationInFrames={getClipDurationInFrames(renderClip, fps)}
            premountFor={Math.ceil(fps * AUDIO_PREMOUNT_SECONDS)}
          >
            {mediaSrc && isPlayableAudio ? (
              <MediaErrorBoundary
                clipId={renderClip.id}
                resetKey={`${renderClip.id}:${mediaSrc}:${trimProps.trimBefore}:${trimProps.trimAfter ?? 'none'}:${playbackRate}:${effectiveVolume}:audio`}
                fallback={null}
              >
                <ClipAudio
                  clip={clip}
                  renderClip={renderClip}
                  fps={fps}
                  baseVolume={effectiveVolume}
                  isRendering={isRendering}
                  src={mediaSrc}
                  trimBefore={trimProps.trimBefore}
                  trimAfter={trimProps.trimAfter}
                  playbackRate={playbackRate}
                />
              </MediaErrorBoundary>
            ) : null}
          </Sequence>
        );
      })}
    </>
  );
};

const ClipAudio: FC<{
  /** The clip as authored; its fades are anchored to it, as in the render. */
  clip: ResolvedTimelineClip;
  /** The clip as played, after canonical occurrence bounds. */
  renderClip: ResolvedTimelineClip;
  fps: number;
  baseVolume: number;
  isRendering: boolean;
  src: string;
  trimBefore: number;
  trimAfter?: number;
  playbackRate: number;
}> = ({ clip, renderClip, fps, baseVolume, isRendering, src, trimBefore, trimAfter, playbackRate }) => {
  const fade = getAudioFade(clip, fps);
  const fadeInFrames = fade?.fadeInFrames ?? 0;
  const fadeOutFrames = fade?.fadeOutFrames ?? 0;
  const durationFrames = fade?.durationFrames ?? 0;
  const frameOffset = secondsToFrames(renderClip.at, fps) - secondsToFrames(clip.at, fps);
  // A stable function identity matters: Remotion re-derives a per-frame
  // volume table whenever the `volume` prop changes.
  const volume = useMemo(
    () => getAudioVolumeProp(
      baseVolume,
      fadeInFrames > 0 || fadeOutFrames > 0 ? { fadeInFrames, fadeOutFrames, durationFrames } : null,
      frameOffset,
    ),
    [baseVolume, durationFrames, fadeInFrames, fadeOutFrames, frameOffset],
  );

  if (isRendering) {
    return (
      <MediaAudio
        src={src}
        trimBefore={trimBefore}
        trimAfter={trimAfter}
        playbackRate={playbackRate}
        volume={volume}
      />
    );
  }

  return (
    <PreviewAudio
      key={JSON.stringify([
        renderClip.id,
        src,
        renderClip.at,
        trimBefore,
        trimAfter,
        playbackRate,
        getClipDurationInFrames(renderClip, fps),
        fps,
      ])}
      clipId={renderClip.id}
      src={src}
      trimBefore={trimBefore}
      trimAfter={trimAfter}
      playbackRate={playbackRate}
      volume={volume}
    />
  );
};

export const AudioTrack = memo(AudioTrackComponent);
AudioTrack.displayName = 'AudioTrack';
