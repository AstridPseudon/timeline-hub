import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';

const { mockGetUser, mockSingle, mockUpdateToolSettings } = vi.hoisted(() => ({
  mockGetUser: vi.fn(),
  mockSingle: vi.fn(),
  mockUpdateToolSettings: vi.fn().mockResolvedValue(undefined),
}));

vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    auth: {
      getUser: mockGetUser,
    },
    from: vi.fn(() => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => ({
          single: mockSingle,
        })),
      })),
    })),
  }),
}));

vi.mock('@/shared/hooks/settings/useToolSettings', () => ({
  updateToolSettingsSupabase: mockUpdateToolSettings,
}));

import {
  useUserUIState,
} from '../useUserUIState';

describe('useUserUIState', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    mockGetUser.mockResolvedValue({ data: { user: { id: 'user-1' } } });
    mockSingle.mockResolvedValue({
      data: {
        settings: {
          ui: {
            paneLocks: { shots: false, tasks: false, gens: false, editor: false },
            theme: { darkMode: true },
          },
        },
      },
      error: null,
    });
    window.history.replaceState({}, '', '/');
  });

  afterEach(() => {
    vi.useRealTimers();
    window.history.replaceState({}, '', '/');
  });

  it('keeps local-test preferences deterministic without initializing Supabase', async () => {
    window.history.replaceState({}, '', '/tools/video-editor?localTest=1');
    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    expect(result.current.isLoading).toBe(false);
    expect(result.current.value).toEqual(fallback);
    expect(mockGetUser).not.toHaveBeenCalled();

    act(() => {
      result.current.update({ darkMode: false });
    });
    await act(async () => {
      await vi.runAllTimersAsync();
    });

    expect(result.current.value).toEqual({ darkMode: false });
    expect(mockUpdateToolSettings).not.toHaveBeenCalled();
  });

  it('keeps Astrid-authority preferences local without loading or writing Supabase', async () => {
    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    expect(result.current.isLoading).toBe(false);
    expect(result.current.value).toEqual(fallback);
    expect(mockGetUser).not.toHaveBeenCalled();

    act(() => {
      result.current.update({ darkMode: false });
    });
    await act(async () => {
      await vi.runAllTimersAsync();
    });

    expect(result.current.value).toEqual({ darkMode: false });
    expect(mockUpdateToolSettings).not.toHaveBeenCalled();
  });

  it('returns fallback value initially', () => {
    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    expect(result.current.value).toEqual(fallback);
    expect(result.current.isLoading).toBe(false);
    expect(typeof result.current.update).toBe('function');
  });

  it('uses fallback when user is not authenticated', async () => {
    mockGetUser.mockResolvedValue({ data: { user: null } });

    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    await act(async () => {
      await vi.runAllTimersAsync();
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.value).toEqual(fallback);
  });

  it('is completely local and does not read or write Supabase in Astrid editor mode', async () => {
    window.history.replaceState({}, '', '/tools/video-editor?project=demo-project&timeline=demo-timeline');

    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    await act(async () => {
      await vi.runAllTimersAsync();
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.value).toEqual(fallback);
    expect(mockGetUser).not.toHaveBeenCalled();
    expect(mockSingle).not.toHaveBeenCalled();

    act(() => {
      result.current.update({ darkMode: false });
    });
    await act(async () => {
      await vi.runAllTimersAsync();
    });

    expect(result.current.value.darkMode).toBe(false);
    expect(mockGetUser).not.toHaveBeenCalled();
    expect(mockSingle).not.toHaveBeenCalled();
  });

  it('update changes local value immediately', async () => {
    const fallback = { darkMode: true };
    const { result } = renderHook(() => useUserUIState('theme', fallback));

    await act(async () => {
      await vi.runAllTimersAsync();
    });

    act(() => {
      result.current.update({ darkMode: false });
    });

    expect(result.current.value.darkMode).toBe(false);
  });
});
