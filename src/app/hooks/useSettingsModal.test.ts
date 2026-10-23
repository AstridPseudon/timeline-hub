import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useSettingsModal } from './useSettingsModal';
import { dispatchAppEvent } from '@/shared/lib/typedEvents';

describe('useSettingsModal', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('opens settings modal with explicit tab arguments', () => {
    const { result } = renderHook(() => useSettingsModal());

    act(() => {
      result.current.handleOpenSettings('extensions');
    });

    expect(result.current.isSettingsModalOpen).toBe(true);
    expect(result.current.settingsInitialTab).toBe('extensions');
  });

  it('responds to openSettings custom event', () => {
    const { result } = renderHook(() => useSettingsModal());

    act(() => {
      dispatchAppEvent('openSettings', { tab: 'extensions' });
    });

    expect(result.current.isSettingsModalOpen).toBe(true);
    expect(result.current.settingsInitialTab).toBe('extensions');
  });
});
