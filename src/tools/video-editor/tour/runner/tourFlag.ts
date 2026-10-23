import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { readLocalStorageItem, writeLocalStorageItem } from '@/shared/lib/storage/localStorageSafe';
import { getEditorTourState, startEditorTour } from '@/shared/state/editorTourStore';
import { buildEditorTourRecord, recordEditorTour } from './tourRecord';

const CONTEXT = 'editorTour';

/** A read that throws (storage blocked) counts as seen: we could never record it, so the tour would restart on every load. */
export function hasSeenEditorTour(): boolean {
  return readLocalStorageItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, { context: CONTEXT, fallback: '1' }) !== null;
}

/**
 * "Seen" is stored at START, so a reload mid-tour never traps anyone: in this browser, and as a "started" record in the
 * Runtime (best effort). Settings' Replay tour starts here.
 */
export function beginEditorTour(): void {
  writeLocalStorageItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, '1', { context: CONTEXT, fallback: undefined });
  startEditorTour();
  const { act, beat } = getEditorTourState();
  void recordEditorTour(buildEditorTourRecord('started', act, beat));
}
