import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';

export type NewbornMediaKind = 'image' | 'video';
type MediaRow = Record<string, JSON>;

const own = (row: MediaRow, key: string): boolean => Object.prototype.hasOwnProperty.call(row, key);

/** Carry a source window into a detached newborn video row without touching the source row. */
export function addNewbornVideoHold(row: MediaRow): MediaRow {
  if (row.clipType !== 'media' || own(row, 'hold') || row.speed !== 1
    || typeof row.from !== 'number' || !Number.isFinite(row.from)
    || typeof row.to !== 'number' || !Number.isFinite(row.to)
    || row.to <= row.from) {
    return row;
  }
  return { ...row, hold: row.to - row.from };
}

/** Convert Main's detached birth shape to the raw Agent occurrence shape. */
export function adaptNewbornOccurrenceMediaRow(
  row: MediaRow,
  kind: NewbornMediaKind,
): MediaRow | null {
  const detached = structuredClone(row) as MediaRow;
  if (kind === 'image') {
    if (detached.clipType !== 'hold' || typeof detached.hold !== 'number'
      || !Number.isFinite(detached.hold) || detached.hold <= 0) {
      return null;
    }
    detached.clipType = 'image';
    return detached;
  }

  if (detached.clipType !== 'media' || own(detached, 'hold') || detached.speed !== 1
    || typeof detached.from !== 'number' || !Number.isFinite(detached.from)
    || typeof detached.to !== 'number' || !Number.isFinite(detached.to)
    || detached.to <= detached.from) {
    return null;
  }
  return addNewbornVideoHold(detached);
}
