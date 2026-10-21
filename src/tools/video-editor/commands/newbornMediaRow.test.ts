import { describe, expect, it } from 'vitest';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { adaptNewbornOccurrenceMediaRow, addNewbornVideoHold } from './newbornMediaRow.ts';

const imageRow: Record<string, JSON> = {
  id: 'reserved-image-child', at: 2, track: 'picture', asset: 'reserved-image', clipType: 'hold', hold: 5,
  opacity: 1, opaque: { keep: [null, false, 0] }, nullable: null,
};
const videoRow: Record<string, JSON> = {
  id: 'reserved-video-child', at: 2, track: 'picture', asset: 'reserved-video', clipType: 'media',
  from: 0, to: 6, speed: 1, opacity: 1, opaque: { keep: [null, false, 0] }, nullable: null,
};

describe('newborn occurrence media row adapter', () => {
  it('maps Main image holds to native image without changing timing or opaque fields', () => {
    const source = structuredClone(imageRow);
    const adapted = adaptNewbornOccurrenceMediaRow(source, 'image');

    expect(adapted).toEqual({ ...imageRow, clipType: 'image' });
    expect(source).toEqual(imageRow);
    expect(Object.keys(adapted!)).toEqual(Object.keys(imageRow));
  });

  it('reuses the newborn video hold carrier for an absent hold', () => {
    const source = structuredClone(videoRow);
    const adapted = adaptNewbornOccurrenceMediaRow(source, 'video');

    expect(adapted).toEqual({ ...videoRow, hold: 6 });
    expect(source).toEqual(videoRow);
    expect(addNewbornVideoHold(source)).toEqual({ ...videoRow, hold: 6 });
  });

  it.each([
    ['present-null hold', { hold: null }],
    ['other speed', { speed: 2 }],
    ['nonfinite from', { from: Number.POSITIVE_INFINITY }],
    ['nonfinite to', { to: Number.POSITIVE_INFINITY }],
    ['zero-length window', { from: 0, to: 0 }],
    ['negative window', { from: 2, to: 1 }],
  ])('refuses unsafe video newborn %s and leaves the source unchanged', (_label, patch) => {
    const source = { ...videoRow, ...patch } as Record<string, JSON>;

    expect(adaptNewbornOccurrenceMediaRow(source, 'video')).toBeNull();
    expect(source).toEqual({ ...videoRow, ...patch });
  });

  it('refuses a non-newborn image shape instead of rewriting an accepted row', () => {
    const source = { ...imageRow, clipType: 'image' } as Record<string, JSON>;

    expect(adaptNewbornOccurrenceMediaRow(source, 'image')).toBeNull();
    expect(source).toEqual({ ...imageRow, clipType: 'image' });
  });
});
