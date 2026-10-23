import type { SpotlightRect } from './useSpotlightRects';

const GAP = 16;
const EDGE = 16;

export interface CardPosition {
  left: number;
  top: number;
}

/**
 * Where the card goes: beside the spotlighted area on whichever side leaves the most room (right,
 * left, below, above), clamped to the viewport; centred when nothing is spotlighted. When no side
 * fits the card, it docks in the viewport's bottom-right corner.
 */
export function placeCard(
  rects: readonly SpotlightRect[],
  card: { width: number; height: number },
  viewport: { width: number; height: number },
): CardPosition {
  const clamp = (value: number, size: number, limit: number) => Math.max(EDGE, Math.min(value, limit - size - EDGE));
  if (rects.length === 0) {
    return { left: (viewport.width - card.width) / 2, top: (viewport.height - card.height) / 2 };
  }
  const left = Math.min(...rects.map((r) => r.x));
  const top = Math.min(...rects.map((r) => r.y));
  const right = Math.max(...rects.map((r) => r.x + r.width));
  const bottom = Math.max(...rects.map((r) => r.y + r.height));
  const midX = (left + right) / 2 - card.width / 2;
  const midY = (top + bottom) / 2 - card.height / 2;

  const sides = [
    { room: viewport.width - right - 2 * GAP, need: card.width, left: right + GAP, top: midY },
    { room: left - 2 * GAP, need: card.width, left: left - GAP - card.width, top: midY },
    { room: viewport.height - bottom - 2 * GAP, need: card.height, left: midX, top: bottom + GAP },
    { room: top - 2 * GAP, need: card.height, left: midX, top: top - GAP - card.height },
  ];
  const fitting = sides.filter((side) => side.room >= side.need).sort((a, b) => b.room - a.room)[0];
  if (!fitting) {
    return { left: viewport.width - card.width - EDGE, top: viewport.height - card.height - EDGE };
  }
  return { left: clamp(fitting.left, card.width, viewport.width), top: clamp(fitting.top, card.height, viewport.height) };
}
