import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useOnboardingFlow } from './useOnboardingFlow';

const {
  navigateMock,
  closeOnboardingModalMock,
  handleErrorMock,
  checkAstridDoctorAvailabilityMock,
  useUserUIStateMock,
} = vi.hoisted(() => ({
  navigateMock: vi.fn(),
  closeOnboardingModalMock: vi.fn(),
  handleErrorMock: vi.fn(),
  checkAstridDoctorAvailabilityMock: vi.fn(),
  useUserUIStateMock: vi.fn(),
}));
const mode = vi.hoisted(() => ({ current: 'first-run' as 'first-run' | 'reconnect' }));

vi.mock('react-router-dom', () => ({
  useNavigate: () => navigateMock,
}));

vi.mock('@/integrations/astrid/doctorAvailability.ts', () => ({
  checkAstridDoctorAvailability: checkAstridDoctorAvailabilityMock,
}));

vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({
  normalizeAndPresentError: handleErrorMock,
}));

vi.mock('@/shared/hooks/useOnboarding', () => ({
  useOnboarding: () => ({
    showOnboardingModal: false,
    onboardingMode: mode.current,
    closeOnboardingModal: closeOnboardingModalMock,
  }),
}));

vi.mock('@/shared/hooks/useUserUIState', () => ({
  useUserUIState: useUserUIStateMock,
}));

describe('useOnboardingFlow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mode.current = 'first-run';
    vi.useFakeTimers();
    checkAstridDoctorAvailabilityMock.mockResolvedValue({ status: 'available' });
  });

  it('closes, checks Astrid, and returns to the editor entry', async () => {
    const { result, unmount } = renderHook(() => useOnboardingFlow());

    await act(async () => {
      await result.current.handleOnboardingClose();
    });

    expect(closeOnboardingModalMock).toHaveBeenCalledTimes(1);
    expect(checkAstridDoctorAvailabilityMock).toHaveBeenCalledTimes(1);
    expect(result.current.doctorAvailability).toEqual({ status: 'available' });
    expect(navigateMock).toHaveBeenCalledWith('/tools/video-editor');

    expect(handleErrorMock).not.toHaveBeenCalled();

    unmount();
    vi.useRealTimers();
  });

  it('returns directly from reconnect without navigating away from the current editor route', async () => {
    mode.current = 'reconnect';
    const { result, unmount } = renderHook(() => useOnboardingFlow());

    await act(async () => {
      await result.current.handleOnboardingClose();
    });

    expect(closeOnboardingModalMock).toHaveBeenCalledOnce();
    expect(checkAstridDoctorAvailabilityMock).not.toHaveBeenCalled();
    expect(navigateMock).not.toHaveBeenCalled();

    unmount();
    mode.current = 'first-run';
    vi.useRealTimers();
  });

  it('surfaces the doctor recovery action and does not enter the tool when unavailable', async () => {
    checkAstridDoctorAvailabilityMock.mockResolvedValue({
      status: 'unavailable',
      reason: 'connection refused',
    });
    const { result, unmount } = renderHook(() => useOnboardingFlow());

    await act(async () => {
      await result.current.handleOnboardingClose();
    });

    expect(result.current.doctorAvailability).toEqual({
      status: 'unavailable',
      reason: 'connection refused',
    });
    expect(handleErrorMock).toHaveBeenCalledWith(
      expect.objectContaining({
        message: expect.stringContaining('python3 -m astrid doctor --json'),
      }),
      {
        context: 'useOnboardingFlow.doctorUnavailable',
        showToast: true,
      },
    );
    expect(closeOnboardingModalMock).not.toHaveBeenCalled();
    expect(navigateMock).not.toHaveBeenCalled();

    unmount();
    vi.useRealTimers();
  });

  it('keeps a local editor link open after first-run setup completes', async () => {
    window.history.replaceState({}, '', '/tools/video-editor?project=demo-project&timeline=demo-timeline');
    const { result, unmount } = renderHook(() => useOnboardingFlow());

    await act(async () => {
      await result.current.handleOnboardingClose();
    });

    expect(closeOnboardingModalMock).toHaveBeenCalledTimes(1);
    expect(checkAstridDoctorAvailabilityMock).not.toHaveBeenCalled();
    expect(navigateMock).not.toHaveBeenCalled();

    unmount();
    window.history.replaceState({}, '', '/');
    vi.useRealTimers();
  });

  it('cancels a pending tour start on unmount', async () => {
    const { result, unmount } = renderHook(() => useOnboardingFlow());

    await act(async () => {
      await result.current.handleOnboardingClose();
    });
    unmount();

    vi.useRealTimers();
  });
});
