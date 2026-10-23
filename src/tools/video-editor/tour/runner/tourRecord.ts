import { AstridRuntimeClient } from '@/integrations/runtime/client';
import { EDITOR_TOUR_VERSION } from '@/shared/lib/editorTourVersion';

/**
 * The tour's outcome, kept per user in the workspace Runtime (actor-owned app state) so it follows the person across
 * browsers, origins and cleared storage. The browser flag in `tourFlag.ts` stays beside it as the offline fallback.
 */
export const EDITOR_TOUR_STATE_KEY = 'editor-tour';

export type EditorTourOutcome = 'started' | 'completed' | 'skipped';

export interface EditorTourRecord {
  version: number;
  outcome: EditorTourOutcome;
  /** `act<N>/<beat>` where the tour was when it began or ended. */
  step: string;
  at: string;
}

/** What the Runtime knows: `seen` (a record for this tour version), `unseen`, or `unavailable` (old Runtime, offline, error). */
export type RuntimeTourStatus = 'seen' | 'unseen' | 'unavailable';

export type EditorTourAutoStartInput = { localSeen: boolean; runtime: RuntimeTourStatus };

/** The one auto-start rule: start only when neither the Runtime nor this browser says the tour was seen. */
export function shouldAutoStartEditorTour({ localSeen, runtime }: EditorTourAutoStartInput): boolean {
  return !localSeen && runtime !== 'seen';
}

function isRecordForThisVersion(content: unknown): boolean {
  if (!content || typeof content !== 'object') return false;
  const { version } = content as { version?: unknown };
  return typeof version === 'number' && version >= EDITOR_TOUR_VERSION;
}

/** Never throws: a missing route (older Runtime), a failed read or no connection all read as `unavailable`. */
export async function readRuntimeTourStatus(): Promise<RuntimeTourStatus> {
  try {
    const state = await new AstridRuntimeClient().getUserAppState(EDITOR_TOUR_STATE_KEY);
    return isRecordForThisVersion(state.content) ? 'seen' : 'unseen';
  } catch {
    return 'unavailable';
  }
}

export function buildEditorTourRecord(outcome: EditorTourOutcome, act: number, beat: string, now = new Date()): EditorTourRecord {
  return { version: EDITOR_TOUR_VERSION, outcome, step: `act${act}/${beat}`, at: now.toISOString() };
}

async function writeRecord(record: EditorTourRecord): Promise<void> {
  const client = new AstridRuntimeClient();
  // A concurrent writer (another tab) moves the version under us once; read again and retry once.
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const current = await client.getUserAppState(EDITOR_TOUR_STATE_KEY);
    try {
      await client.updateUserAppState(EDITOR_TOUR_STATE_KEY, { ...record }, current.version);
      return;
    } catch (error) {
      if (!isVersionConflict(error)) throw error;
    }
  }
}

function isVersionConflict(error: unknown): boolean {
  return typeof error === 'object' && error !== null && (error as { status?: unknown }).status === 409;
}

let writes: Promise<void> = Promise.resolve();

/**
 * Best effort and in order (the "started" write lands before the outcome). Failures never reach the user: the tour
 * works the same without a Runtime that supports the record.
 */
export function recordEditorTour(record: EditorTourRecord): Promise<void> {
  writes = writes.then(() => writeRecord(record)).catch(() => undefined);
  return writes;
}
