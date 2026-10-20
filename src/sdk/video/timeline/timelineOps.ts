/**
 * TimelineOps — atomic mutation interface for timeline operations.
 *
 * TimelineOps is the only public mutation surface available to extensions
 * and host proposal machinery. It validates full batches, delegates to the
 * existing commitData/history path for undo/persistence, and does not expose
 * internal mutation APIs, provider handles, or raw timeline stores.
 *
 * @publicContract
 */

import type {
  TimelinePatch,
  TimelinePatchValidationResult,
  TimelinePreviewResult,
  TimelineDiff,
} from './patch';
import type { ClipSetParamsArgs } from '@/integrations/runtime/timeline-commit-types.ts';

/**
 * Stable host adapter for atomic timeline mutations.
 *
 * TimelineOps is the only public mutation surface available to extensions
 * and host proposal machinery. It validates full batches, delegates to the
 * existing commitData/history path for undo/persistence, and does not expose
 * internal mutation APIs, provider handles, or raw timeline stores.
 */
export interface SubmittedClipParamsInput {
  readonly id: string;
  readonly args: ClipSetParamsArgs;
  readonly basis?: Readonly<Record<string, unknown>>;
  readonly accepted: boolean;
}

export interface TimelineOps {
  /** Read the existing session's submitted input without capturing or queuing an edit. */
  getSubmittedClipParams?(clipId: string): SubmittedClipParamsInput | undefined;

  /**
   * Stage one selected-pack clip command at its original basis and retained
   * schema pin. Resolution means queued, not accepted; the command session
   * owns pending/error/retry and projects only the provider's accepted closure.
   */
  setClipParams?(clipId: string, args: ClipSetParamsArgs, signal?: AbortSignal): Promise<void>;

  /**
   * Validate a patch batch without mutating timeline state.
   * Returns structured diagnostics for every invalid operation.
   */
  validate(patch: TimelinePatch): TimelinePatchValidationResult;

  /**
   * Preview a patch batch against a snapshot of current timeline state.
   * Returns the projected timeline diff and affected object IDs without
   * committing any changes.
   */
  preview(patch: TimelinePatch): TimelinePreviewResult;

  /**
   * Validate and apply a patch batch atomically through the existing
   * commitData/history path. Returns the applied diff.
   *
   * Throws if validation fails — always call validate() first when
   * the caller cannot guarantee validity.
   */
  apply(patch: TimelinePatch): TimelineDiff;

  /**
   * Await durable acknowledgement of the host edit sequence current at this
   * call, including edits made through synchronous apply(). Later edits may
   * be coalesced into the same save. The receipt is an acknowledged editor
   * timeline version, not a Runtime revision ID.
   *
   * Rejects when durable persistence is unavailable, data is unloaded, the
   * host cannot save during an interaction, a save fails or conflicts, or the
   * timeline session is closed/replaced/reloaded. A transport rejection does
   * not prove that the server did not commit. Hosts own retries and conflict UX.
   */
  flush(): Promise<{ readonly version: number }>;

  /**
   * Take a checkpoint of the current timeline state for later rollback.
   * Returns the checkpoint identifier.
   */
  checkpoint(label?: string): string;

  /**
   * Rollback to a previously taken checkpoint, discarding all mutations
   * applied after it.
   *
   * Returns the diff that was undone, or null if the checkpoint is not found.
   */
  rollback(checkpointId: string): TimelineDiff | null;

  /**
   * Convenience: set all audio tracks to the given muted state and commit.
   * Returns the diff describing which tracks were affected.
   */
  setAllTracksMuted(muted: boolean): TimelineDiff;
}
