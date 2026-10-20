import { getSanitizedPlaybackRate, computeMediaTrim } from '@banodoco/timeline-composition/evaluation';

type ClockClip = Parameters<typeof computeMediaTrim>[0] & { speed?: number };

/** Convert an already compiled clip to the public PCM source clock. */
export function compiledAudioSourceClock(clip: ClockClip, fps: number) {
  if (!Number.isFinite(fps) || fps <= 0) throw new Error('invalid audio source fps');
  return {
    source_from: computeMediaTrim(clip, fps).trimBefore / fps,
    playback_rate: getSanitizedPlaybackRate(clip.speed),
  };
}
