import { useEffect, useState } from 'react';

export interface SpotlightRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

const PADDING = 6;

/** The part of an element its scrolling or clipping ancestors actually show (a timeline row is wider than the timeline). */
function visibleBox(element: Element): { left: number; top: number; right: number; bottom: number } {
  const box = element.getBoundingClientRect();
  const visible = { left: box.left, top: box.top, right: box.right, bottom: box.bottom };
  for (let parent = element.parentElement; parent && parent !== document.body; parent = parent.parentElement) {
    const { overflowX, overflowY } = getComputedStyle(parent);
    if (overflowX === 'visible' && overflowY === 'visible') continue;
    const clip = parent.getBoundingClientRect();
    if (overflowX !== 'visible') {
      visible.left = Math.max(visible.left, clip.left);
      visible.right = Math.min(visible.right, clip.right);
    }
    if (overflowY !== 'visible') {
      visible.top = Math.max(visible.top, clip.top);
      visible.bottom = Math.min(visible.bottom, clip.bottom);
    }
  }
  return visible;
}

function measure(selectors: readonly string[]): SpotlightRect[] {
  const rects: SpotlightRect[] = [];
  for (const selector of selectors) {
    const element = document.querySelector(selector);
    if (!element) continue;
    const box = visibleBox(element);
    const width = box.right - box.left;
    const height = box.bottom - box.top;
    if (width <= 0 || height <= 0) continue;
    rects.push({ x: box.left - PADDING, y: box.top - PADDING, width: width + 2 * PADDING, height: height + 2 * PADDING });
  }
  return rects;
}

function sameRects(a: readonly SpotlightRect[], b: readonly SpotlightRect[]): boolean {
  return a.length === b.length
    && a.every((r, i) => r.x === b[i].x && r.y === b[i].y && r.width === b[i].width && r.height === b[i].height);
}

/**
 * Viewport rects of the first element matching each selector. Re-measured (one frame at a time) when a
 * target resizes, when the page scrolls or resizes, and when elements mount or unmount, so the Tasks
 * pane opening or a row sliding in keeps the spotlight on its target.
 */
export function useSpotlightRects(selectors: readonly string[]): SpotlightRect[] {
  const [rects, setRects] = useState<SpotlightRect[]>([]);
  const key = selectors.join('|');

  useEffect(() => {
    const targets = key ? key.split('|') : [];
    const resizeObserver = new ResizeObserver(() => schedule());
    let observed = new Set<Element>();
    let frame = 0;

    function update() {
      frame = 0;
      const elements = new Set(targets.map((selector) => document.querySelector(selector)).filter((el): el is Element => !!el));
      observed.forEach((el) => { if (!elements.has(el)) resizeObserver.unobserve(el); });
      elements.forEach((el) => { if (!observed.has(el)) resizeObserver.observe(el); });
      observed = elements;
      const next = measure(targets);
      setRects((previous) => (sameRects(previous, next) ? previous : next));
    }
    function schedule() {
      if (!frame) frame = requestAnimationFrame(update);
    }

    const mutationObserver = new MutationObserver(schedule);
    mutationObserver.observe(document.body, { childList: true, subtree: true });
    window.addEventListener('resize', schedule);
    window.addEventListener('scroll', schedule, { capture: true, passive: true });
    update();

    return () => {
      if (frame) cancelAnimationFrame(frame);
      resizeObserver.disconnect();
      mutationObserver.disconnect();
      window.removeEventListener('resize', schedule);
      window.removeEventListener('scroll', schedule, { capture: true });
    };
  }, [key]);

  return rects;
}
