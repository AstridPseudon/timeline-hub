import { describe, expect, it } from 'vitest';
import type { ResolvedTimelineClip } from '@/tools/video-editor/types/index.ts';
import { boundCanonicalClipToOccurrence, boundCanonicalConfigClips } from './canonicalRenderBounds.ts';
import { getClipTimelineDuration } from './config-utils.ts';

function canonicalClip(overrides: Partial<ResolvedTimelineClip> = {}): ResolvedTimelineClip {
  return {
    id: 'occ-1:clip',
    at: 12,
    track: 'video',
    clipType: 'media',
    hold: 5,
    transition: { type: 'fade', duration: 4 },
    app: {
      canonicalTiming: {
        occurrenceStartMs: 10_000,
        occurrenceDurationMs: 5_000,
      },
    },
    ...overrides,
  };
}

describe('canonical render bounds', () => {
  it('bounds visual/effect/transition content to the occurrence half-open interval', () => {
    const bounded = boundCanonicalClipToOccurrence(canonicalClip());

    expect(bounded).toMatchObject({
      at: 12,
      hold: 3,
      transition: { duration: 2 },
    });
    expect(boundCanonicalClipToOccurrence(canonicalClip({ at: 15 }))).toBeNull();
    expect(boundCanonicalConfigClips([
      canonicalClip({ id: 'occ-1:audio', track: 'audio', at: 14, hold: 4 }),
      canonicalClip({ id: 'occ-1:effect', track: 'effects', at: 15 }),
    ])).toMatchObject([
      { id: 'occ-1:audio', at: 14, hold: 1 },
    ]);
  });

  it('preserves trim semantics while clamping the rendered end', () => {
    const bounded = boundCanonicalClipToOccurrence(canonicalClip({
      from: 2,
      to: 8,
      hold: undefined,
      speed: 2,
    }));

    expect(bounded).toMatchObject({ at: 12, from: 2, to: 8 });
  });

  it.each([0.5, 2])('keeps source hold units while clipping at speed %s and can be applied repeatedly', (speed) => {
    const clip = canonicalClip({
      at: 10,
      hold: 5,
      speed,
      track: 'audio',
      app: { canonicalTiming: { occurrenceStartMs: 10_000, occurrenceDurationMs: 3_000 } },
    });
    const once = boundCanonicalClipToOccurrence(clip);
    const twice = once && boundCanonicalClipToOccurrence(once);
    const expectedDuration = Math.min(5 / speed, 3);

    expect(once?.hold).toBe(expectedDuration * speed);
    expect(twice?.hold).toBe(once?.hold);
    expect(once && getClipTimelineDuration(once)).toBe(expectedDuration);
    expect(twice && getClipTimelineDuration(twice)).toBe(expectedDuration);
  });

  it('uses only the private stored occurrence cap and keeps the editor clip unchanged', () => {
    const source = canonicalClip({
      at: 0,
      app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 5_000, storedOccurrenceDurationMs: 4_000 } },
    });
    const bounded = boundCanonicalClipToOccurrence(source, 'stored');

    expect(source).toMatchObject({ hold: 5, app: { canonicalTiming: { occurrenceDurationMs: 5_000 } } });
    expect(bounded).toMatchObject({ hold: 4, app: { canonicalTiming: {
      occurrenceDurationMs: 4_000, storedOccurrenceDurationMs: 4_000,
    } } });
  });

  it('uses the effective cap for missing and invalid stored metadata per clip', () => {
    const bounded = boundCanonicalConfigClips([
      canonicalClip({
        id: 'valid',
        at: 0,
        app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 5_000, storedOccurrenceDurationMs: 4_000 } },
      }),
      canonicalClip({ id: 'missing', at: 0 }),
      canonicalClip({
        id: 'negative',
        at: 0,
        app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 5_000, storedOccurrenceDurationMs: -1 } },
      }),
    ], 'stored');

    expect(bounded).toMatchObject([
      { id: 'valid', hold: 4, app: { canonicalTiming: { occurrenceDurationMs: 4_000 } } },
      { id: 'missing', hold: 5, app: { canonicalTiming: { occurrenceDurationMs: 5_000 } } },
      { id: 'negative', hold: 5, app: { canonicalTiming: { occurrenceDurationMs: 5_000, storedOccurrenceDurationMs: -1 } } },
    ]);
  });

  it.each([NaN, Infinity, -Infinity, '4000', null])('does not clamp malformed stored metadata to zero (%s)', (storedOccurrenceDurationMs) => {
    const bounded = boundCanonicalClipToOccurrence(canonicalClip({
      at: 0,
      app: { canonicalTiming: { occurrenceStartMs: 0, occurrenceDurationMs: 5_000, storedOccurrenceDurationMs } },
    }), 'stored');

    expect(bounded).toMatchObject({ hold: 5, app: { canonicalTiming: { occurrenceDurationMs: 5_000 } } });
  });
});
