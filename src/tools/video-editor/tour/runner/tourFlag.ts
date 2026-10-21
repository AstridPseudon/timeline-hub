import { STORAGE_KEYS } from '@/shared/lib/storage/storageKeys';
import { readLocalStorageItem, writeLocalStorageItem } from '@/shared/lib/storage/localStorageSafe';
import { getEditorTourState, startEditorTour } from '@/shared/state/editorTourStore';
import { buildEditorTourRecord, readRuntimeTourStatus, recordEditorTour, shouldAutoStartEditorTour } from './tourRecord';

const CONTEXT = 'editorTour';

/** A read that throws (storage blocked) counts as seen: we could never record it, so the tour would restart on every load. */
export function hasSeenEditorTour(): boolean {
  return readLocalStorageItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, { context: CONTEXT, fallback: '1' }) !== null;
}

/**
 * "Seen" is stored at START, so a reload mid-tour never traps anyone: in this browser, and as a "started" record in the
 * Runtime (best effort). The first-run trigger and Settings' Replay tour both start here.
 */
export function beginEditorTour(): void {
  writeLocalStorageItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, '1', { context: CONTEXT, fallback: undefined });
  startEditorTour();
  const { act, beat } = getEditorTourState();
  void recordEditorTour(buildEditorTourRecord('started', act, beat));
}

/**
 * First-run trigger: starts once, ever, when the editor is ready for it. Resolves to whether it started.
 * The browser flag is checked first (no request); otherwise the Runtime record decides, and an old or unreachable
 * Runtime leaves the browser flag as the only rule. `stillEligible` is asked again once the Runtime has answered.
 */
export async function startEditorTourIfFirstRun(eligible: boolean, stillEligible: () => boolean = () => true): Promise<boolean> {
  if (!eligible || getEditorTourState().status === 'running' || hasSeenEditorTour()) return false;
  const runtime = await readRuntimeTourStatus();
  if (!stillEligible() || getEditorTourState().status === 'running' || hasSeenEditorTour()) return false;
  if (!shouldAutoStartEditorTour({ localSeen: false, runtime })) {
    // Seen elsewhere: remember it here too, so the next load needs no request.
    writeLocalStorageItem(STORAGE_KEYS.EDITOR_TOUR_SEEN, '1', { context: CONTEXT, fallback: undefined });
    return false;
  }
  beginEditorTour();
  return true;
}
