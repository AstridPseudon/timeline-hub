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

  it('holds timeline feedback through queued completion and suppresses its quantized echo', () => {
    const fps = 30000 / 1001;
    const seek = vi.fn();
    const setCurrentTime = vi.fn();
    const setTime = vi.fn();
    const isSyncingFromPreview = { current: false };
    const isSyncingFromTimeline = { current: false };
    const { result } = renderHook(() => useTimelineSync({
      timelineRef: { current: { setTime } },
      previewRef: { current: { seek } },
      setCurrentTime,
      isSyncingFromPreview,
      isSyncingFromTimeline,
    }));

    act(() => {
      result.current.onClickTimeArea(0.5);
      result.current.onClickTimeArea(1);
      result.current.onPreviewTimeUpdate(15 / fps);
      result.current.onPreviewTimeUpdate(30 / fps, true);
      result.current.onPreviewTimeUpdate(45 / fps);
    });

    expect(seek).toHaveBeenNthCalledWith(1, 0.5);
    expect(seek).toHaveBeenNthCalledWith(2, 1);
    expect(setCurrentTime).toHaveBeenNthCalledWith(1, 0.5);
    expect(setCurrentTime).toHaveBeenNthCalledWith(2, 1);
    expect(setCurrentTime).not.toHaveBeenCalledWith(30 / fps);
    expect(setTime).toHaveBeenCalledWith(45 / fps);
    expect(isSyncingFromTimeline.current).toBe(false);
  });
});
