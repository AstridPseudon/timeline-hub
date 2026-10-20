import { getClipTimelineDuration } from '@/tools/video-editor/lib/config-utils.ts';
import type { ResolvedTimelineClip, ResolvedTimelineConfig } from '@/tools/video-editor/types/index.ts';

type JsonRecord = Record<string, unknown>;
type OccurrenceDurationSource = 'effective' | 'stored';

function record(value: unknown): JsonRecord | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as JsonRecord
    : null;
}

/**
 * Bound a canonical projected clip to its occurrence's half-open interval.
 * This happens before preview/export sequence construction, so audio, visual,
 * effect, transition, overlap, and premount consumers share one boundary.
 */
export function boundCanonicalClipToOccurrence(
  clip: ResolvedTimelineClip,
  occurrenceDurationSource: OccurrenceDurationSource = 'effective',
): ResolvedTimelineClip | null {
  if (clip.enabled === false || clip.active === false || clip.disabled === true
    || clip.hidden === true || clip.deleted === true) return null;
  const app = record(clip.app);
  const timing = record(app?.canonicalTiming);
  const occurrenceStartMs = timing?.occurrenceStartMs;
  const storedOccurrenceDurationMs = timing?.storedOccurrenceDurationMs;
  const effectiveOccurrenceDurationMs = timing?.occurrenceDurationMs;
  const useStoredOccurrenceDuration = occurrenceDurationSource === 'stored'
    && typeof storedOccurrenceDurationMs === 'number'
    && Number.isFinite(storedOccurrenceDurationMs)
    && storedOccurrenceDurationMs >= 0
    && typeof effectiveOccurrenceDurationMs === 'number'
    && Number.isFinite(effectiveOccurrenceDurationMs)
    && storedOccurrenceDurationMs < effectiveOccurrenceDurationMs;
  const occurrenceDurationMs = useStoredOccurrenceDuration
    ? storedOccurrenceDurationMs
    : effectiveOccurrenceDurationMs;
  if (typeof occurrenceStartMs !== 'number' || !Number.isFinite(occurrenceStartMs)
    || typeof occurrenceDurationMs !== 'number' || !Number.isFinite(occurrenceDurationMs)) {
    return clip;
  }

  const occurrenceStart = Math.max(0, occurrenceStartMs / 1000);
  const occurrenceEnd = occurrenceStart + Math.max(0, occurrenceDurationMs / 1000);
  const start = Math.max(occurrenceStart, clip.at);
  if (start >= occurrenceEnd) return null;

  const duration = Math.min(getClipTimelineDuration(clip), occurrenceEnd - start);
  if (duration <= 0) return null;

  const speed = typeof clip.speed === 'number' && clip.speed > 0 ? clip.speed : 1;
  // Keep the editor/source clip untouched while carrying the selected render
  // boundary into the evaluator's private config copy.
  const nextApp = useStoredOccurrenceDuration
    ? { ...(app ?? {}), canonicalTiming: { ...timing, occurrenceDurationMs } }
    : null;
  const nextClip: ResolvedTimelineClip = {
    ...clip,
    ...(nextApp ? { app: nextApp as ResolvedTimelineClip['app'] } : {}),
    at: start,
    ...(typeof clip.hold === 'number'
      ? { hold: duration * speed }
      : typeof clip.from === 'number' && typeof clip.to === 'number'
        ? { to: clip.from + duration * speed }
        : { hold: duration }),
  };
  if (clip.transition) {
    const transitionDuration = Math.min(
      Math.max(0, clip.transition.duration),
      Math.max(0, start - occurrenceStart),
    );
    nextClip.transition = transitionDuration > 0
      ? { ...clip.transition, duration: transitionDuration }
      : undefined;
  }
  return nextClip;
}

export function boundCanonicalConfigClips(
  clips: readonly ResolvedTimelineClip[],
  occurrenceDurationSource: OccurrenceDurationSource = 'effective',
): ResolvedTimelineClip[] {
  return clips.flatMap((clip) => {
    const bounded = boundCanonicalClipToOccurrence(clip, occurrenceDurationSource);
    return bounded ? [bounded] : [];
  });
}

/** A render-only selection; editor rows keep their content-derived geometry. */
export function boundCanonicalRenderConfig<T extends ResolvedTimelineConfig>(config: T): T {
  const clips = config.clips.flatMap((clip) => {
    const timing = record(clip.app?.canonicalTiming);
    const stored = timing?.storedOccurrenceDurationMs;
    const effective = timing?.occurrenceDurationMs;
    // Only the explicit render selection consumes the stored cap. The popup's
    // live shot-local soft wall and ordinary editor bounds retain their policy.
    if (typeof stored !== 'number' || !Number.isFinite(stored) || stored < 0
      || typeof effective !== 'number' || !Number.isFinite(effective) || stored >= effective) return [clip];
    const bounded = boundCanonicalClipToOccurrence(clip, 'stored');
    return bounded ? [bounded] : [];
  });
  return clips.length === config.clips.length && clips.every((clip, index) => clip === config.clips[index])
    ? config : { ...config, clips };
}
