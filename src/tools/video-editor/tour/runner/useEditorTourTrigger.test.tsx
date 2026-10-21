// @vitest-environment jsdom

import { renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { exitEditorTour, getEditorTourState, startEditorTour } from '@/shared/state/editorTourStore';
import { readRuntimeTourStatus } from './tourRecord';
import { useEditorTourTrigger } from './useEditorTourTrigger';

vi.mock('./tourRecord', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./tourRecord')>()),
  readRuntimeTourStatus: vi.fn(async () => 'unseen'),
  recordEditorTour: vi.fn(async () => undefined),
}));

const mocks = vi.hoisted(() => ({
  isMobile: false,
  isTablet: false,
  viewportWidth: 1440,
  tabletHardware: false,
}));

vi.mock('@/shared/hooks/mobile', () => ({
  useIsMobile: () => mocks.isMobile,
  useIsTablet: () => mocks.isTablet,
  useViewportWidth: () => mocks.viewportWidth,
  isTabletHardware: () => mocks.tabletHardware,
}));

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
  mocks.isMobile = false;
  mocks.isTablet = false;
  mocks.viewportWidth = 1440;
  mocks.tabletHardware = false;
});

afterEach(() => {
  vi.restoreAllMocks();
  exitEditorTour();
  localStorage.clear();
});

describe('useEditorTourTrigger', () => {
  it('starts once on desktop with a selection, and not again on rerender or remount', async () => {
    const runIdBefore = getEditorTourState().runId;

    const first = renderHook(({ hasSelection }) => useEditorTourTrigger(hasSelection), {
      initialProps: { hasSelection: true },
    });
    await waitFor(() => expect(getEditorTourState()).toMatchObject({ status: 'running', runId: runIdBefore + 1 }));
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).not.toBeNull();

    first.rerender({ hasSelection: true });
    first.unmount();
    exitEditorTour();

    // Remount after the tour was dismissed: the seen flag keeps it from starting again.
    const second = renderHook(() => useEditorTourTrigger(true));
    expect(getEditorTourState()).toMatchObject({ status: 'idle', runId: runIdBefore + 1 });
    second.unmount();
  });

  it('never starts without a selection', () => {
    const runIdBefore = getEditorTourState().runId;

    const { unmount } = renderHook(() => useEditorTourTrigger(false));

    expect(getEditorTourState()).toMatchObject({ status: 'idle', runId: runIdBefore });
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
    unmount();
  });

  it('never starts on a phone-width viewport and writes nothing to localStorage', () => {
    mocks.isMobile = true;
    mocks.viewportWidth = 800;
    const setItem = vi.spyOn(Storage.prototype, 'setItem');
    const runIdBefore = getEditorTourState().runId;

    const { unmount } = renderHook(() => useEditorTourTrigger(true));

    expect(getEditorTourState()).toMatchObject({ status: 'idle', runId: runIdBefore });
    expect(setItem).not.toHaveBeenCalled();
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
    unmount();
  });

  it('waits for the Runtime before deciding, and does not start when the Runtime says it was seen', async () => {
    vi.mocked(readRuntimeTourStatus).mockResolvedValueOnce('seen');

    const { unmount } = renderHook(() => useEditorTourTrigger(true));
    expect(getEditorTourState().status).toBe('idle');
    await waitFor(() => expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).not.toBeNull());

    expect(getEditorTourState().status).toBe('idle');
    unmount();
  });

  it('does not start if the editor unmounts while the Runtime is still answering', async () => {
    let answer: (status: 'unseen') => void = () => undefined;
    vi.mocked(readRuntimeTourStatus).mockReturnValueOnce(new Promise((resolve) => { answer = resolve; }));

    const { unmount } = renderHook(() => useEditorTourTrigger(true));
    unmount();
    answer('unseen');
    await Promise.resolve();
    await Promise.resolve();

    expect(getEditorTourState().status).toBe('idle');
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });
});
