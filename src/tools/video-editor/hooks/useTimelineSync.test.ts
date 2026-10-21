// @vitest-environment jsdom
import { renderHook, act } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { useTimelineSync } from './useTimelineSync.ts';

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
});
