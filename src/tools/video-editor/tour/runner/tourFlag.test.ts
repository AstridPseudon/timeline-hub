import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { exitEditorTour, getEditorTourState } from '@/shared/state/editorTourStore';
import { beginEditorTour, hasSeenEditorTour } from './tourFlag';
import { recordEditorTour } from './tourRecord';

vi.mock('./tourRecord', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./tourRecord')>()),
  recordEditorTour: vi.fn(async () => undefined),
}));

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
  vi.mocked(recordEditorTour).mockClear();
});

afterEach(() => {
  vi.restoreAllMocks();
  exitEditorTour();
  localStorage.clear();
});

describe('hasSeenEditorTour', () => {
  it('treats a localStorage read failure as seen so a blocked browser does not repeat the tour', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('storage blocked');
    });
    expect(hasSeenEditorTour()).toBe(true);
  });
});

describe('beginEditorTour (first run and Replay tour)', () => {
  it('starts the tour and records "started", even when the browser flag is already set', () => {
    localStorage.setItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, '1');

    beginEditorTour();

    expect(getEditorTourState()).toMatchObject({ status: 'running', act: 1, beat: 'welcome' });
    expect(recordEditorTour).toHaveBeenCalledWith(expect.objectContaining({ outcome: 'started', step: 'act1/welcome' }));
  });
});
