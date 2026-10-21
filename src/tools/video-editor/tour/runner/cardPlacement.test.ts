import { describe, expect, it } from 'vitest';
import { placeCard } from './cardPlacement';
import type { SpotlightRect } from './useSpotlightRects';

const VIEWPORT = { width: 1440, height: 900 };
const CARD = { width: 300, height: 200 };
const EDGE = 16;

function expectInViewport(position: { left: number; top: number }, card = CARD) {
  expect(position.left).toBeGreaterThanOrEqual(EDGE);
  expect(position.top).toBeGreaterThanOrEqual(EDGE);
  expect(position.left + card.width).toBeLessThanOrEqual(VIEWPORT.width - EDGE);
  expect(position.top + card.height).toBeLessThanOrEqual(VIEWPORT.height - EDGE);
}

describe('placeCard', () => {
  it('centres the card when nothing is spotlighted', () => {
    expect(placeCard([], CARD, VIEWPORT)).toEqual({ left: 570, top: 350 });
  });

  it('puts the card to the right of a rect on the left', () => {
    const rect: SpotlightRect = { x: 20, y: 300, width: 200, height: 300 };

    const position = placeCard([rect], CARD, VIEWPORT);

    expect(position.left).toBeGreaterThanOrEqual(rect.x + rect.width);
    expect(position.top).toBeLessThan(rect.y + rect.height);
    expectInViewport(position);
  });

  it('puts the card to the left of a rect on the far right', () => {
    const rect: SpotlightRect = { x: 1200, y: 300, width: 220, height: 300 };

    const position = placeCard([rect], CARD, VIEWPORT);

    expect(position.left + CARD.width).toBeLessThanOrEqual(rect.x);
    expectInViewport(position);
  });

  it('puts the card below a full-width rect near the top', () => {
    const rect: SpotlightRect = { x: 0, y: 20, width: 1440, height: 100 };

    const position = placeCard([rect], CARD, VIEWPORT);

    expect(position.top).toBeGreaterThanOrEqual(rect.y + rect.height);
    expectInViewport(position);
  });

  it('docks bottom-right when the rects cover the whole viewport', () => {
    const rect: SpotlightRect = { x: 0, y: 0, width: 1440, height: 900 };

    expect(placeCard([rect], CARD, VIEWPORT)).toEqual({
      left: VIEWPORT.width - CARD.width - EDGE,
      top: VIEWPORT.height - CARD.height - EDGE,
    });
  });

  it('always keeps the card inside the viewport', () => {
    const layouts: SpotlightRect[][] = [
      [{ x: 0, y: 0, width: 10, height: 10 }],
      [{ x: 1430, y: 890, width: 10, height: 10 }],
      [{ x: 700, y: 400, width: 40, height: 40 }],
      [{ x: 0, y: 0, width: 720, height: 900 }],
      [{ x: 720, y: 0, width: 720, height: 900 }],
      [{ x: 100, y: 100, width: 1200, height: 700 }],
      [
        { x: 10, y: 10, width: 300, height: 300 },
        { x: 1100, y: 500, width: 300, height: 300 },
      ],
    ];
    for (const rects of layouts) {
      expectInViewport(placeCard(rects, CARD, VIEWPORT));
    }
  });
});
