// @vitest-environment jsdom
import { createElement, useEffect } from 'react';
import { render, renderHook, act } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { useTimelineSync } from './useTimelineSync.ts';

function PlayerFrameupdateEffect({ onTimeUpdate }: { onTimeUpdate: (time: number) => void }) {
  useEffect(() => {
    onTimeUpdate(1.001);
  }, [onTimeUpdate]);
  return null;
}

describe('useTimelineSync', () => {
  it('routes click and drag intent through the preview seek API while mirroring time', () => {
    const seek = vi.fn();
    const setCurrentTime = vi.fn();
    const timelineRef = { current: { setTime: vi.fn() } };
    const previewRef = { current: { seek } };
    const isSyncingFromPreview = { current: false };
    const isSyncingFromTimeline = { current: false };
    const { result } = renderHook(() => useTimelineSync({
      timelineRef,
      previewRef,
      setCurrentTime,
      isSyncingFromPreview,
      isSyncingFromTimeline,
    }));

    act(() => {
      result.current.onCursorDrag(1.25);
      result.current.onClickTimeArea(2.5);
    });

    expect(seek).toHaveBeenNthCalledWith(1, 1.25);
    expect(seek).toHaveBeenNthCalledWith(2, 2.5);
    expect(setCurrentTime).toHaveBeenNthCalledWith(1, 1.25);
    expect(setCurrentTime).toHaveBeenNthCalledWith(2, 2.5);
  });

  it("keeps an authored seek at 1 when the Player echoes its rational frame as 1.001", () => {
    const seek = vi.fn();
    const setCurrentTime = vi.fn();
    const setTime = vi.fn();
    const rafCallbacks: FrameRequestCallback[] = [];
    vi.spyOn(performance, 'now').mockReturnValueOnce(1000).mockReturnValueOnce(1300);
    vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => {
      rafCallbacks.push(callback);
      return rafCallbacks.length;
    });
    const { result } = renderHook(() => useTimelineSync({
      timelineRef: { current: { setTime } },
      previewRef: { current: { seek } },
      setCurrentTime,
      isSyncingFromPreview: { current: false },
      isSyncingFromTimeline: { current: false },
    }));

    act(() => {
      result.current.onClickTimeArea(1);
      // Remotion reports the rational-frame echo after the explicit seek.
      result.current.onPreviewTimeUpdate(1.001);
    });

    expect(seek).toHaveBeenCalledWith(1);
    expect(setCurrentTime).toHaveBeenCalledTimes(1);
    expect(setCurrentTime).toHaveBeenCalledWith(1);
    expect(setTime).not.toHaveBeenCalledWith(1.001);

    act(() => {
      for (const callback of rafCallbacks.splice(0)) callback(0);
      result.current.onPreviewTimeUpdate(1.5);
    });

    expect(setTime).toHaveBeenLastCalledWith(1.5);
    expect(setCurrentTime).toHaveBeenLastCalledWith(1.5);
  });

  it('keeps queued authored seek feedback suppressed until the Player effect runs', () => {
    const setCurrentTime = vi.fn();
    const setTime = vi.fn();
    const rafCallbacks: FrameRequestCallback[] = [];
    const requestAnimationFrame = globalThis.requestAnimationFrame;
    vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => {
      rafCallbacks.push(callback);
      return rafCallbacks.length;
    });
    vi.spyOn(performance, 'now').mockReturnValueOnce(1000).mockReturnValueOnce(1300);
    let seekCount = 0;
    const seek = vi.fn(() => {
      // The first seek owns the mailbox RAF; the second seek is its queued
      // latest target and is dispatched from that same mailbox flush.
      if (seekCount++ === 0) {
        rafCallbacks.push(() => undefined);
      }
    });
    const { result } = renderHook(() => useTimelineSync({
      timelineRef: { current: { setTime } },
      previewRef: { current: { seek } },
      setCurrentTime,
      isSyncingFromPreview: { current: false },
      isSyncingFromTimeline: { current: false },
    }));

    act(() => {
      result.current.onClickTimeArea(0.5);
      result.current.onClickTimeArea(1);
    });
    act(() => {
      for (const callback of rafCallbacks.splice(0)) callback(0);
    });

    render(createElement(PlayerFrameupdateEffect, { onTimeUpdate: result.current.onPreviewTimeUpdate }));

    expect(seek).toHaveBeenNthCalledWith(1, 0.5);
    expect(seek).toHaveBeenNthCalledWith(2, 1);
    expect(setCurrentTime).toHaveBeenCalledWith(0.5);
    expect(setCurrentTime).toHaveBeenCalledWith(1);
    expect(setTime).not.toHaveBeenCalledWith(1.001);

    act(() => {
      result.current.onPreviewTimeUpdate(1.5);
    });
    expect(setTime).toHaveBeenLastCalledWith(1.5);
    expect(setCurrentTime).toHaveBeenLastCalledWith(1.5);
    vi.stubGlobal('requestAnimationFrame', requestAnimationFrame);
  });
});
