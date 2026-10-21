// @vitest-environment jsdom
import { createElement } from 'react';
import { cleanup, createEvent, fireEvent, render } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { TimeBar } from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/TimeBar';

afterEach(() => {
  cleanup();
});

// A 10 s bar: the step is span / 50 = 0.2 s, Shift steps five times that.
function bar(props: Partial<Parameters<typeof TimeBar>[0]> = {}) {
  const onSeek = vi.fn();
  const onJump = vi.fn();
  const onRange = vi.fn();
  const view = render(createElement(TimeBar, {
    start: 0, end: 10, time: 2, label: 'Travel position', valueText: '0:02.0',
    onSeek, onJump, onRange, ...props,
  }));
  return { ...view, onSeek, onJump, onRange };
}

/** Dispatches a key on the element and returns the event, so its defaultPrevented can be read. */
function press(element: HTMLElement, key: string, init: KeyboardEventInit = {}) {
  const event = createEvent.keyDown(element, { key, ...init });
  fireEvent(element, event);
  return event;
}

describe('TimeBar', () => {
  it('is a slider named by its label, with its value', () => {
    const view = bar({ time: 2.5 });
    const slider = view.getByRole('slider', { name: 'Travel position' });
    expect(slider).toHaveAttribute('aria-valuemin', '0');
    expect(slider).toHaveAttribute('aria-valuemax', '10');
    expect(slider).toHaveAttribute('aria-valuenow', '2.5');
    expect(slider).toHaveAttribute('aria-valuetext', '0:02.0');
  });

  it('ArrowRight and ArrowLeft seek one step from the current time', () => {
    const view = bar();
    const slider = view.getByRole('slider', { name: 'Travel position' });
    fireEvent.keyDown(slider, { key: 'ArrowRight' });
    expect(view.onSeek).toHaveBeenCalledTimes(1);
    expect(view.onSeek.mock.calls[0][0]).toBeCloseTo(2.2);

    fireEvent.keyDown(slider, { key: 'ArrowLeft' });
    expect(view.onSeek.mock.calls[1][0]).toBeCloseTo(1.8);
  });

  it('Shift with an arrow seeks five steps', () => {
    const view = bar();
    const slider = view.getByRole('slider', { name: 'Travel position' });
    fireEvent.keyDown(slider, { key: 'ArrowRight', shiftKey: true });
    expect(view.onSeek.mock.calls[0][0]).toBeCloseTo(3);
  });

  it('clamps stepping to the bounds', () => {
    const view = bar({ time: 9.9 });
    fireEvent.keyDown(view.getByRole('slider', { name: 'Travel position' }), { key: 'ArrowRight', shiftKey: true });
    expect(view.onSeek).toHaveBeenCalledWith(10);
  });

  it('Home seeks to the start and End to the end', () => {
    const view = bar();
    const slider = view.getByRole('slider', { name: 'Travel position' });
    fireEvent.keyDown(slider, { key: 'Home' });
    expect(view.onSeek).toHaveBeenLastCalledWith(0);
    fireEvent.keyDown(slider, { key: 'End' });
    expect(view.onSeek).toHaveBeenLastCalledWith(10);
  });

  it('prevents the default of a handled key and does not propagate it to a parent', () => {
    const parentKeyDown = vi.fn();
    const view = render(createElement('div', { onKeyDown: parentKeyDown },
      createElement(TimeBar, { start: 0, end: 10, time: 2, label: 'Travel position', valueText: '0:02.0', onSeek: vi.fn() })));
    const slider = view.getByRole('slider', { name: 'Travel position' });

    const event = press(slider, 'ArrowRight');
    expect(event.defaultPrevented).toBe(true);
    expect(parentKeyDown).not.toHaveBeenCalled();
  });

  it('leaves keys it does not handle to the page', () => {
    const parentKeyDown = vi.fn();
    const onSeek = vi.fn();
    const view = render(createElement('div', { onKeyDown: parentKeyDown },
      createElement(TimeBar, { start: 0, end: 10, time: 2, label: 'Travel position', valueText: '0:02.0', onSeek })));
    const event = press(view.getByRole('slider', { name: 'Travel position' }), 'a');
    expect(event.defaultPrevented).toBe(false);
    expect(parentKeyDown).toHaveBeenCalledTimes(1);
    expect(onSeek).not.toHaveBeenCalled();
  });

  it('renders event markers as buttons named by title and time, and a click jumps to the marker', () => {
    const view = bar({
      markers: [
        { key: 'dawn', from: 2, to: 2, title: 'Dawn', time: '0:02' },
        { key: 'lanterns', from: 4, to: 6, title: 'Lanterns' },
      ],
    });
    const dawn = view.getByRole('button', { name: 'Dawn, 0:02' });
    expect(dawn).toHaveAttribute('aria-label', 'Dawn, 0:02');
    expect(dawn).toHaveAttribute('data-event-marker', 'tick');
    const lanterns = view.getByRole('button', { name: 'Lanterns' });
    expect(lanterns).toHaveAttribute('data-event-marker', 'band');

    fireEvent.click(dawn);
    expect(view.onJump).toHaveBeenCalledWith(2);
    fireEvent.click(lanterns);
    expect(view.onJump).toHaveBeenLastCalledWith(4);
    expect(view.onSeek).not.toHaveBeenCalled();
  });

  it('a marker click seeks when there is no onJump', () => {
    const view = bar({ markers: [{ key: 'dawn', from: 2, to: 2, title: 'Dawn' }], onJump: undefined });
    fireEvent.click(view.getByRole('button', { name: 'Dawn' }));
    expect(view.onSeek).toHaveBeenCalledWith(2);
  });

  it('with a range, shows two handles that move the range, not the playhead', () => {
    const view = bar({ range: { from: 2, to: 6 } });
    const sliders = view.getAllByRole('slider');
    expect(sliders).toHaveLength(3);
    const end = view.getByRole('slider', { name: 'Range end' });
    const start = view.getByRole('slider', { name: 'Range start' });
    expect(end).toHaveAttribute('data-range-handle', 'to');
    expect(start).toHaveAttribute('data-range-handle', 'from');

    const event = press(end, 'ArrowRight');
    expect(event.defaultPrevented).toBe(true);
    expect(view.onRange).toHaveBeenCalledTimes(1);
    const moved = view.onRange.mock.calls[0][0];
    expect(moved.from).toBe(2);
    expect(moved.to).toBeCloseTo(6.1);
    expect(view.onSeek).not.toHaveBeenCalled();
  });

  it('the start handle cannot pass the end handle, which keeps 0.1 s of stretch', () => {
    const view = bar({ range: { from: 5, to: 6 } });
    // End sends the start handle as far right as it can go; it must stop 0.1 s short of the end handle.
    fireEvent.keyDown(view.getByRole('slider', { name: 'Range start' }), { key: 'End' });
    expect(view.onRange).toHaveBeenCalledTimes(1);
    const moved = view.onRange.mock.calls[0][0];
    expect(moved.from).toBeCloseTo(5.9);
    expect(moved.to).toBe(6);
  });

  it('a disabled bar renders no markers or range handles and ignores keys', () => {
    const view = bar({
      disabled: true,
      range: { from: 2, to: 6 },
      markers: [{ key: 'dawn', from: 2, to: 2, title: 'Dawn', time: '0:02' }],
    });
    expect(view.queryByRole('button', { name: 'Dawn, 0:02' })).toBeNull();
    expect(view.queryByRole('slider', { name: 'Range start' })).toBeNull();
    expect(view.queryByRole('slider', { name: 'Range end' })).toBeNull();

    const slider = view.getByRole('slider', { name: 'Travel position' });
    expect(slider).toHaveAttribute('aria-disabled', 'true');
    const event = press(slider, 'ArrowRight');
    expect(event.defaultPrevented).toBe(false);
    fireEvent.keyDown(slider, { key: 'Home' });
    expect(view.onSeek).not.toHaveBeenCalled();
  });
});
