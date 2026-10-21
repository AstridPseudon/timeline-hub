import { createRef } from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { PANE_CONFIG } from '@/shared/config/panes';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  PanelPopoutFrame,
  POPOUT_SIZES_STORAGE_KEY,
  MIN_POPOUT_WIDTH,
  MIN_POPOUT_HEIGHT,
  clampRect,
  type PanelPopoutFrameProps,
} from './PanelPopoutFrame';

const BOUNDS = { width: 1000, height: 800 };
const DEFAULT_RECT = { x: 100, y: 50, width: 700, height: 500 };

function renderFrame(overrides: Partial<PanelPopoutFrameProps> = {}) {
  const onClose = vi.fn();
  const bodyRef = createRef<HTMLDivElement>();
  const props: PanelPopoutFrameProps = {
    title: 'Transcript',
    bounds: BOUNDS,
    defaultRect: DEFAULT_RECT,
    touch: false,
    onClose,
    ...overrides,
  };
  const utils = render(<PanelPopoutFrame ref={bodyRef} {...props} />);
  return { ...utils, onClose, bodyRef, props };
}

function frameStyle() {
  const frame = screen.getByRole('dialog');
  return {
    left: frame.style.left,
    top: frame.style.top,
    width: frame.style.width,
    height: frame.style.height,
  };
}

/** jsdom has no PointerEvent, so give pointer events the client coordinates the frame reads. */
class TestPointerEvent extends MouseEvent {
  constructor(type: string, init: MouseEventInit = {}) {
    super(type, init);
  }
}

beforeEach(() => {
  vi.useFakeTimers();
  window.localStorage.clear();
  Object.defineProperty(window, 'PointerEvent', { value: TestPointerEvent, configurable: true, writable: true });
});

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  window.localStorage.clear();
});

describe('clampRect', () => {
  it('keeps the rect inside the bounds', () => {
    expect(clampRect({ x: 900, y: 700, width: 640, height: 460 }, BOUNDS)).toEqual({ x: 360, y: 340, width: 640, height: 460 });
    expect(clampRect({ x: -20, y: -5, width: 640, height: 460 }, BOUNDS)).toEqual({ x: 0, y: 0, width: 640, height: 460 });
  });

  it('enforces the 640x460 minimum, and never exceeds the bounds', () => {
    expect(MIN_POPOUT_WIDTH).toBeGreaterThanOrEqual(640);
    // The body is the frame minus its 2px border, and must stay at least 608 wide.
    expect(MIN_POPOUT_WIDTH - 2).toBeGreaterThanOrEqual(608);
    expect(MIN_POPOUT_HEIGHT).toBe(460);
    expect(clampRect({ x: 0, y: 0, width: 100, height: 100 }, BOUNDS)).toMatchObject({ width: MIN_POPOUT_WIDTH, height: MIN_POPOUT_HEIGHT });
    expect(clampRect({ x: 0, y: 0, width: 2000, height: 2000 }, BOUNDS)).toEqual({ x: 0, y: 0, width: 1000, height: 800 });
    // A bounds smaller than the minimum wins over the minimum.
    expect(clampRect({ x: 0, y: 0, width: 100, height: 100 }, { width: 500, height: 300 })).toEqual({ x: 0, y: 0, width: 500, height: 300 });
  });
});

describe('PanelPopoutFrame', () => {
  it('opens as a non-modal dialog on the default rect, clamped to the bounds', () => {
    renderFrame({ defaultRect: { x: 900, y: 700, width: 100, height: 100 } });
    const frame = screen.getByRole('dialog');
    expect(frame.getAttribute('aria-modal')).toBe('false');
    expect(frameStyle()).toEqual({ left: `${BOUNDS.width - MIN_POPOUT_WIDTH}px`, top: `${BOUNDS.height - MIN_POPOUT_HEIGHT}px`, width: `${MIN_POPOUT_WIDTH}px`, height: `${MIN_POPOUT_HEIGHT}px` });
  });

  it('remembers the size per panel key and reopens with it', () => {
    const first = renderFrame({ panelKey: 'host:transcript' });
    const handle = document.querySelector('[data-panel-popout-handle="se"]') as HTMLElement;
    fireEvent.pointerDown(handle, { clientX: 0, clientY: 0, button: 0 });
    fireEvent.pointerMove(window, { clientX: 120, clientY: 60 });
    fireEvent.pointerUp(window, { clientX: 120, clientY: 60 });
    expect(frameStyle()).toMatchObject({ width: '820px', height: '560px' });
    act(() => { vi.advanceTimersByTime(500); });
    first.unmount();

    const stored = JSON.parse(window.localStorage.getItem(POPOUT_SIZES_STORAGE_KEY) ?? '{}');
    expect(stored['host:transcript']).toEqual({ width: 820, height: 560 });

    renderFrame({ panelKey: 'host:transcript', defaultRect: { x: 0, y: 0, width: 800, height: 600 } });
    expect(frameStyle()).toMatchObject({ width: '820px', height: '560px' });
  });

  it('keeps sizes for other panel keys separate', () => {
    window.localStorage.setItem(POPOUT_SIZES_STORAGE_KEY, JSON.stringify({ 'host:other': { width: 900, height: 700 } }));
    renderFrame({ panelKey: 'host:transcript' });
    expect(frameStyle()).toMatchObject({ width: '700px', height: '500px' });
  });

  it('closes on Esc only when focus is inside and the key was not consumed', () => {
    const { onClose, bodyRef } = renderFrame();
    const inner = document.createElement('button');
    inner.textContent = 'inside';
    bodyRef.current!.appendChild(inner);
    inner.focus();

    fireEvent.keyDown(inner, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('ignores Esc that an inner handler already prevented', () => {
    const { onClose, bodyRef } = renderFrame();
    const inner = document.createElement('div');
    inner.tabIndex = 0;
    inner.addEventListener('keydown', (event) => event.preventDefault());
    bodyRef.current!.appendChild(inner);
    inner.focus();

    fireEvent.keyDown(inner, { key: 'Escape' });
    expect(onClose).not.toHaveBeenCalled();
  });

  it('ignores Esc when focus is outside the frame', () => {
    const outside = document.createElement('button');
    document.body.appendChild(outside);
    const { onClose } = renderFrame();
    outside.focus();

    fireEvent.keyDown(outside, { key: 'Escape' });
    expect(onClose).not.toHaveBeenCalled();
    outside.remove();
  });

  it('focuses the data-autofocus element when content arrives, and returns focus to the opener on close', () => {
    const opener = document.createElement('button');
    document.body.appendChild(opener);
    opener.focus();
    const { bodyRef, unmount } = renderFrame();

    const first = document.createElement('button');
    const target = document.createElement('input');
    target.setAttribute('data-autofocus', '');
    bodyRef.current!.append(first, target);
    // The observer runs as a microtask; flush it.
    return Promise.resolve().then(() => {
      expect(document.activeElement).toBe(target);
      unmount();
      expect(document.activeElement).toBe(opener);
      opener.remove();
    });
  });

  it('fills the bounds with the fill toggle and restores the last size', () => {
    renderFrame();
    const fill = screen.getByRole('button', { name: 'Fill editor' });
    fireEvent.click(fill);
    expect(frameStyle()).toEqual({ left: '0px', top: '0px', width: '1000px', height: '800px' });
    expect(screen.getByRole('button', { name: 'Restore size' }).getAttribute('aria-pressed')).toBe('true');

    fireEvent.click(screen.getByRole('button', { name: 'Restore size' }));
    expect(frameStyle()).toEqual({ left: '100px', top: '50px', width: '700px', height: '500px' });
  });

  it('touch mode fills the bounds with no move or resize, and a Done button', () => {
    const { onClose } = renderFrame({ touch: true });
    const frame = screen.getByRole('dialog');
    expect(frame.className).toContain('inset-0');
    expect(frame.style.width).toBe('');
    expect(frame.style.height).toBe('');
    expect(document.querySelector('[data-panel-popout-handle]')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Fill editor' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Return to panel' })).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Done' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('stacks the floating frame above the pane handles, and the touch frame does not use that layer', () => {
    const paneZ = Number(/\d+/.exec(PANE_CONFIG.zIndex.CONTROL_UNLOCKED)![0]);
    expect(paneZ).toBe(100016);
    const frameZ = Number(/z-\[(\d+)\]/.exec(screen.queryByRole('dialog')?.className ?? '')?.[1] ?? 0);
    cleanup();

    renderFrame();
    const frame = screen.getByRole('dialog');
    expect(frame.className).toContain('z-[100017]');
    expect(Number(/z-\[(\d+)\]/.exec(frame.className)![1])).toBeGreaterThan(paneZ);
    expect(frameZ).toBe(0);
    cleanup();

    renderFrame({ touch: true });
    expect(screen.getByRole('dialog').className).not.toContain('z-[100017]');
  });

  it('draws a grip svg in the south-east resize handle', () => {
    renderFrame();
    const handle = document.querySelector('[data-panel-popout-handle="se"]') as HTMLElement;
    expect(handle.querySelector('svg')).not.toBeNull();
  });

  it('closes from the Return to panel button', () => {
    const { onClose } = renderFrame();
    fireEvent.click(screen.getByRole('button', { name: 'Return to panel' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('clamps a move to the bounds', () => {
    renderFrame();
    const titlebar = document.querySelector('[data-panel-popout-titlebar]') as HTMLElement;
    fireEvent.pointerDown(titlebar, { clientX: 0, clientY: 0, button: 0 });
    fireEvent.pointerMove(window, { clientX: 5000, clientY: -5000 });
    fireEvent.pointerUp(window, { clientX: 5000, clientY: -5000 });
    expect(frameStyle()).toMatchObject({ left: '300px', top: '0px', width: '700px', height: '500px' });
  });
});
