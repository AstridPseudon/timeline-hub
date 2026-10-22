// @vitest-environment jsdom

import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useSettledCardPosition, useSettledRects } from './useSettledCardPosition';
import type { SpotlightRect } from './useSpotlightRects';

const SIZE = { width: 300, height: 100 };
const rect = (x: number, y = 100): SpotlightRect => ({ x, y, width: 100, height: 50 });

beforeEach(() => {
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'requestAnimationFrame', 'cancelAnimationFrame'] });
  Object.defineProperty(window, 'innerWidth', { value: 1400, configurable: true });
  Object.defineProperty(window, 'innerHeight', { value: 900, configurable: true });
});
afterEach(() => {
  vi.useRealTimers();
  
});

const frames = (n: number) => act(() => { vi.advanceTimersByTime(16 * n); });

function mount(initial: { beatKey: string; rects: SpotlightRect[]; size?: { width: number; height: number } }) {
  return renderHook((props) => useSettledCardPosition(props.beatKey, props.rects, props.size ?? SIZE), { initialProps: initial });
}

describe('useSettledCardPosition', () => {
  it('places the first aim without animating', () => {
    const { result } = mount({ beatKey: '1:1:welcome', rects: [] });
    expect(result.current.animate).toBe(false);
    expect(result.current.value).toEqual({ left: 550, top: 400 });
  });

  it('holds still on a beat change until the targets settle, then travels once', () => {
    const { result, rerender } = mount({ beatKey: '1:1:welcome', rects: [] });
    frames(3);
    const start = result.current.value;
    rerender({ beatKey: '1:1:compose', rects: [rect(100)] });
    expect(result.current.value).toEqual(start);
    // The target keeps sliding for a few frames; the card does not follow.
    for (const x of [140, 180, 220]) {
      frames(1);
      rerender({ beatKey: '1:1:compose', rects: [rect(x)] });
      expect(result.current.value).toEqual(start);
    }
    frames(2);
    const settled = result.current.value;
    expect(settled).not.toEqual(start);
    expect(result.current.animate).toBe(true);
    expect(settled.left).toBe(220 + 100 + 16); // right of the final rect, not an intermediate one
    frames(10);
    expect(result.current.value).toEqual(settled);
  });

  it('commits after the cap even if the target never stops moving', () => {
    const { result, rerender } = mount({ beatKey: '1:1:welcome', rects: [] });
    frames(3);
    const start = result.current.value;
    rerender({ beatKey: '1:1:compose', rects: [rect(100)] });
    for (let i = 0; i < 30; i += 1) {
      frames(1);
      rerender({ beatKey: '1:1:compose', rects: [rect(100 + i * 10)] });
    }
    expect(result.current.value).not.toEqual(start);
  });

  it('ignores small drift within a beat and re-aims once after a big move', () => {
    const { result, rerender } = mount({ beatKey: '1:1:compose', rects: [rect(100)] });
    frames(3);
    const first = result.current.value;
    rerender({ beatKey: '1:1:compose', rects: [rect(110)] });
    frames(5);
    expect(result.current.value).toEqual(first);
    rerender({ beatKey: '1:1:compose', rects: [rect(300)] });
    frames(1);
    expect(result.current.value).toEqual(first);
    frames(2);
    expect(result.current.value.left).toBe(300 + 100 + 16);
  });

  it('re-aims at once, unanimated, when the viewport resizes', () => {
    const { result } = mount({ beatKey: '1:1:welcome', rects: [] });
    frames(3);
    act(() => {
      Object.defineProperty(window, 'innerWidth', { value: 1000, configurable: true });
      window.dispatchEvent(new Event('resize'));
    });
    frames(0);
    expect(result.current.animate).toBe(false);
    expect(result.current.value.left).toBe(350);
  });
});

describe('useSettledRects', () => {
  it('keeps the old cutouts until the new targets hold still', () => {
    const { result, rerender } = renderHook((p) => useSettledRects(p.beatKey, p.rects), { initialProps: { beatKey: 'a', rects: [rect(10)] } });
    frames(3);
    expect(result.current).toEqual([rect(10)]);
    rerender({ beatKey: 'b', rects: [rect(500)] });
    expect(result.current).toEqual([rect(10)]);
    frames(2);
    expect(result.current).toEqual([rect(500)]);
  });
});
