import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { VideoEditSubMode } from '../model/editSettingsTypes';
import { useVideoEditModeHandlers } from './useVideoEditModeHandlers';

function setup(overrides: {
  persistedVideoEditSubMode?: VideoEditSubMode | null;
  canRegenerate?: boolean;
} = {}) {
  const setVideoEditSubMode = vi.fn();
  const setPersistedPanelMode = vi.fn();
  const videoEditingSetIsVideoEditMode = vi.fn();
  const { result } = renderHook(() => useVideoEditModeHandlers({
    setVideoEditSubMode,
    persistedVideoEditSubMode: overrides.persistedVideoEditSubMode ?? null,
    canRegenerate: overrides.canRegenerate ?? true,
    setPersistedPanelMode,
    videoEditingSetIsVideoEditMode,
  }));
  return { result, setVideoEditSubMode, setPersistedPanelMode, videoEditingSetIsVideoEditMode };
}

describe('useVideoEditModeHandlers', () => {
  it('enters replace mode when no sub-mode was persisted', () => {
    const { result, setVideoEditSubMode, setPersistedPanelMode, videoEditingSetIsVideoEditMode } = setup();

    act(() => result.current.handleEnterVideoEditMode());

    expect(setVideoEditSubMode).toHaveBeenCalledWith('replace');
    expect(setPersistedPanelMode).toHaveBeenCalledWith('edit');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenCalledWith(true);
  });

  it('restores the persisted enhance sub-mode without arming the replace editor', () => {
    const { result, setVideoEditSubMode, videoEditingSetIsVideoEditMode } = setup({
      persistedVideoEditSubMode: 'enhance',
    });

    act(() => result.current.handleEnterVideoEditMode());

    expect(setVideoEditSubMode).toHaveBeenCalledWith('enhance');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenCalledWith(false);
  });

  it('restores regenerate when it is available and falls back to replace when it is not', () => {
    const available = setup({ persistedVideoEditSubMode: 'regenerate', canRegenerate: true });
    act(() => available.result.current.handleEnterVideoEditMode());
    expect(available.setVideoEditSubMode).toHaveBeenCalledWith('regenerate');
    expect(available.videoEditingSetIsVideoEditMode).toHaveBeenCalledWith(false);

    const unavailable = setup({ persistedVideoEditSubMode: 'regenerate', canRegenerate: false });
    act(() => unavailable.result.current.handleEnterVideoEditMode());
    expect(unavailable.setVideoEditSubMode).toHaveBeenCalledWith('replace');
    expect(unavailable.videoEditingSetIsVideoEditMode).toHaveBeenCalledWith(true);
  });

  it('switches between the remaining sub-modes and toggles the replace editor with them', () => {
    const { result, setVideoEditSubMode, videoEditingSetIsVideoEditMode } = setup();

    act(() => result.current.handleEnterVideoRegenerateMode());
    expect(setVideoEditSubMode).toHaveBeenLastCalledWith('regenerate');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenLastCalledWith(false);

    act(() => result.current.handleEnterVideoEnhanceMode());
    expect(setVideoEditSubMode).toHaveBeenLastCalledWith('enhance');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenLastCalledWith(false);

    act(() => result.current.handleEnterVideoReplaceMode());
    expect(setVideoEditSubMode).toHaveBeenLastCalledWith('replace');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenLastCalledWith(true);
  });

  it('exits edit mode back to the info panel', () => {
    const { result, setVideoEditSubMode, setPersistedPanelMode, videoEditingSetIsVideoEditMode } = setup({
      persistedVideoEditSubMode: 'replace',
    });

    act(() => result.current.handleExitVideoEditMode());

    expect(setVideoEditSubMode).toHaveBeenCalledWith(null);
    expect(setPersistedPanelMode).toHaveBeenCalledWith('info');
    expect(videoEditingSetIsVideoEditMode).toHaveBeenCalledWith(false);
  });
});
