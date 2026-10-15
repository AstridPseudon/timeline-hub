// @vitest-environment jsdom
import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useEditorPreferences } from './useEditorPreferences';

describe('useEditorPreferences right panel state', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('migrates older timeline records and persists panel, slot, and lane choices', () => {
    localStorage.setItem('video-editor:preferences:legacy', JSON.stringify({
      scaleWidth: 190,
      activeClipTab: 'timing',
      assetPanel: { showAll: true, showHidden: false, hidden: [] },
    }));

    const { result } = renderHook(() => useEditorPreferences('legacy'));
    expect(result.current.preferences.selectedRightPanelId).toBe('host:properties');
    expect(result.current.preferences.rightPanelLayoutSlotsByPanelId).toEqual({});
    expect(result.current.preferences.showDataLanes).toBe(false);

    act(() => {
      result.current.setSelectedRightPanelId('com.reigh.transcript-lane:transcript-lane-panel');
      result.current.setRightPanelLayoutSlot('com.reigh.transcript-lane:transcript-lane-panel', 'compact');
      result.current.setShowDataLanes(true);
    });
    act(() => vi.advanceTimersByTime(250));

    const saved = JSON.parse(localStorage.getItem('video-editor:preferences:legacy') ?? '{}');
    expect(saved.selectedRightPanelId).toBe('com.reigh.transcript-lane:transcript-lane-panel');
    expect(saved.rightPanelLayoutSlotsByPanelId).toEqual({
      'com.reigh.transcript-lane:transcript-lane-panel': 'compact',
    });
    expect(saved.showDataLanes).toBe(true);
    expect(saved.scaleWidth).toBe(190);
  });

  it('keeps two timeline hosts isolated and persists an explicit closed panel', () => {
    const first = renderHook(() => useEditorPreferences('first'));
    const second = renderHook(() => useEditorPreferences('second'));

    act(() => {
      first.result.current.setSelectedRightPanelId(null);
      first.result.current.setRightPanelLayoutSlot('com.reigh.transcript-lane:transcript-lane-panel', 'compact');
      first.result.current.setShowDataLanes(true);
    });

    expect(first.result.current.preferences.selectedRightPanelId).toBeNull();
    expect(second.result.current.preferences.selectedRightPanelId).toBe('host:properties');
    expect(second.result.current.preferences.showDataLanes).toBe(false);
    expect(second.result.current.preferences.rightPanelLayoutSlotsByPanelId).toEqual({});
  });
});
