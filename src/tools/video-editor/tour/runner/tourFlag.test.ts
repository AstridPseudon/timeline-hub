import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { exitEditorTour, getEditorTourState, startEditorTour } from '@/shared/state/editorTourStore';
import { beginEditorTour, hasSeenEditorTour, startEditorTourIfFirstRun } from './tourFlag';
import { readRuntimeTourStatus, recordEditorTour, type RuntimeTourStatus } from './tourRecord';

vi.mock('./tourRecord', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./tourRecord')>()),
  readRuntimeTourStatus: vi.fn(),
  recordEditorTour: vi.fn(async () => undefined),
}));

const runtimeStatus = (status: RuntimeTourStatus) => vi.mocked(readRuntimeTourStatus).mockResolvedValue(status);

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
  vi.mocked(recordEditorTour).mockClear();
  vi.mocked(readRuntimeTourStatus).mockReset();
  runtimeStatus('unseen');
});

afterEach(() => {
  vi.restoreAllMocks();
  exitEditorTour();
  localStorage.clear();
});

describe('startEditorTourIfFirstRun: the auto-start rule', () => {
  const cases: Array<[RuntimeTourStatus, boolean, boolean]> = [
    // runtime, local flag set, starts
    ['unseen', false, true],
    ['unseen', true, false],
    ['seen', false, false],
    ['seen', true, false],
    ['unavailable', false, true], // an older Runtime or a failed read: the local flag alone decides
    ['unavailable', true, false],
  ];
  it.each(cases)('Runtime %s, local flag set %s: starts %s', async (runtime, localSet, starts) => {
    runtimeStatus(runtime);
    if (localSet) localStorage.setItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, '1');

    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(starts);

    expect(getEditorTourState().status).toBe(starts ? 'running' : 'idle');
    // A local flag needs no request at all.
    expect(vi.mocked(readRuntimeTourStatus)).toHaveBeenCalledTimes(localSet ? 0 : 1);
  });

  it('records the start in the Runtime and the browser when it starts', async () => {
    await startEditorTourIfFirstRun(true);

    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).not.toBeNull();
    expect(recordEditorTour).toHaveBeenCalledWith(expect.objectContaining({ version: 1, outcome: 'started', step: 'act1/welcome' }));
  });

  it('remembers a Runtime "seen" in the browser too, so the next load makes no request', async () => {
    runtimeStatus('seen');

    await startEditorTourIfFirstRun(true);

    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).not.toBeNull();
    expect(recordEditorTour).not.toHaveBeenCalled();
  });

  it('never starts a second time, even after the tour exits', async () => {
    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(true);
    exitEditorTour();

    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(false);
    expect(getEditorTourState().status).toBe('idle');
  });

  it('when not eligible, never starts, asks nothing and does not write the flag', async () => {
    await expect(startEditorTourIfFirstRun(false)).resolves.toBe(false);

    expect(getEditorTourState().status).toBe('idle');
    expect(readRuntimeTourStatus).not.toHaveBeenCalled();
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });

  it('does not start if eligibility lapsed while the Runtime was answering', async () => {
    let eligible = true;
    const pending = startEditorTourIfFirstRun(true, () => eligible);
    eligible = false;

    await expect(pending).resolves.toBe(false);
    expect(getEditorTourState().status).toBe('idle');
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });

  it('does not start or write the flag while a tour is already running', async () => {
    startEditorTour();
    const runId = getEditorTourState().runId;

    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(false);

    expect(getEditorTourState().runId).toBe(runId);
    expect(localStorage.getItem(STORAGE_KEYS.EDITOR_TOUR_SEEN)).toBeNull();
  });

  it('treats a localStorage read failure as seen, so a storage-blocked browser never restarts the tour', async () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('storage blocked');
    });

    expect(hasSeenEditorTour()).toBe(true);
    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(false);
    expect(getEditorTourState().status).toBe('idle');
  });

  it('still starts, without throwing, when only the write fails', async () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('quota exceeded');
    });

    await expect(startEditorTourIfFirstRun(true)).resolves.toBe(true);
    expect(getEditorTourState().status).toBe('running');
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
