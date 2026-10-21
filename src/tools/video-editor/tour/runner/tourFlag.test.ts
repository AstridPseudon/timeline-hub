import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { exitEditorTour, getEditorTourState, startEditorTour } from '@/shared/state/editorTourStore';
import { hasSeenEditorTour, startEditorTourIfFirstRun } from './tourFlag';

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
});

afterEach(() => {
  vi.restoreAllMocks();
  exitEditorTour();
  localStorage.clear();
});

describe('startEditorTourIfFirstRun', () => {
  it('starts on the first eligible run and stores the seen flag', () => {
    expect(startEditorTourIfFirstRun(true)).toBe(true);

    expect(getEditorTourState()).toMatchObject({ status: 'running', act: 1, beat: 'welcome' });
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).not.toBeNull();
  });

  it('never starts a second time, even after the tour exits', () => {
    expect(startEditorTourIfFirstRun(true)).toBe(true);
    exitEditorTour();

    expect(startEditorTourIfFirstRun(true)).toBe(false);
    expect(getEditorTourState().status).toBe('idle');
  });

  it('when not eligible, never starts and does not write the flag', () => {
    expect(startEditorTourIfFirstRun(false)).toBe(false);

    expect(getEditorTourState().status).toBe('idle');
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });

  it('does not start or write the flag while a tour is already running', () => {
    startEditorTour();
    const runId = getEditorTourState().runId;

    expect(startEditorTourIfFirstRun(true)).toBe(false);

    expect(getEditorTourState().runId).toBe(runId);
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });

  it('treats a localStorage read failure as seen, so a storage-blocked browser never restarts the tour', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('storage blocked');
    });

    expect(hasSeenEditorTour()).toBe(true);
    expect(startEditorTourIfFirstRun(true)).toBe(false);
    expect(getEditorTourState().status).toBe('idle');
  });

  it('still starts, without throwing, when only the write fails', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('quota exceeded');
    });

    expect(() => startEditorTourIfFirstRun(true)).not.toThrow();
    expect(getEditorTourState().status).toBe('running');
  });
});
