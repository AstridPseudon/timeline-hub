/**
 * useTimelineOps — host adapter that produces a stable TimelineOps instance
 * wired to the existing commitData/history path.
 *
 * Extensions and proposal machinery receive this adapter through
 * CreativeContext.timeline.  It wraps the pure compiler functions
 * (validateTimelinePatch / compileTimelinePatch / previewTimelinePatch)
 * and delegates checkpoint/rollback to the host history module.
 *
 * @publicContract — only exposes the TimelineOps surface; never leaks
 *   raw TimelineData, applyEdit, provider handles, or store internals.
 */

import { useCallback, useMemo, useRef } from 'react';
import { bindProposalCorrelation, commandContext, freezeProposal, orderedPatchCommands, type ProposalCommandBinding, type ProposalTimelineOps } from '../lib/proposal-command-binding.ts';
import type { TimelineSaveTarget } from './useTimelinePersistence.ts';
import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import type {
  TimelineOps,
} from '@/sdk/index';
import type {
  TimelineDiff,
  TimelinePatch,
  TimelinePatchValidationResult,
  TimelinePreviewResult,
} from '@/sdk/video/timeline/patch.ts';
import {
  validateTimelinePatch,
  compileTimelinePatch,
  previewTimelinePatch,
} from '@/tools/video-editor/lib/timeline-patch';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data';
import type { TimelineEditability } from '@/tools/video-editor/lib/timeline-editability';
import type { CommitDataOptions } from '@/tools/video-editor/hooks/useTimelineCommit';
import type { Checkpoint } from '@/tools/video-editor/types/history';
import { TimelineVersionConflictError } from '@/sdk/video/timeline/errors.ts';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Generate a compact unique ID for checkpoint tracking. */
function uid(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `ckpt-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
}

// ---------------------------------------------------------------------------
// Argument types
// ---------------------------------------------------------------------------

export interface UseTimelineOpsArgs {
  /** Stable commitData from useTimelineCommit / useTimelineSave. */
  commitData: (nextData: TimelineData, options?: CommitDataOptions) => void;

  /** Enable captured proposals only for the current provider's command writer. */
  semanticCommandSaving?: boolean;
  /** Existing provider recovery scope, read only; never supplied by a proposal. */
  getProposalSourceContext?: () => string | null | undefined;
  getPendingProposalTransactionId?: () => string | undefined;
  recoverProposalSave?: (binding: ProposalCommandBinding) => Promise<void>;
  captureSaveTarget?: () => TimelineSaveTarget;
  flushSaveTarget?: (target: TimelineSaveTarget) => Promise<number>;

  /** Existing command-only editor path used by the admitted transcript consumer. */
  applyEdit?: (
    mutation: { readonly type: 'commands' },
    options: Readonly<{
      editCommands: readonly EditCommand[];
      transactionId: string;
      semantic: true;
      save: true;
    }>,
  ) => void;

  /** Mutable ref holding the current canonical TimelineData. */
  dataRef: { current: TimelineData | null };

  /**
   * Live source for the canonical timeline version (e.g. the store's
   * ack-tracked `configVersion` field, which advances on save acknowledgment
   * WITHOUT committing a new data object). Canonical-state comparisons
   * (stale-base-version checks) and patch versioning must use this channel.
   * When omitted, falls back to `dataRef.current.configVersion`.
   */
  getConfigVersion?: () => number;

  /** Normal host writer's edit-sequence acknowledgement barrier. */
  flushPendingSave?: () => Promise<number>;

  /** Host checkpoint creation (async fire-and-forget). */
  createManualCheckpoint: (label?: string) => Promise<void>;

  /** Host checkpoint restoration. */
  jumpToCheckpoint: (checkpointId: string) => void;

  /** Current checkpoint list (for existence checks). */
  checkpoints: Checkpoint[];

  /** Optional host-owned whole-timeline authoring guard. */
  editability?: TimelineEditability;
}

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

/**
 * Create a stable {@link TimelineOps} adapter wired to the host commit and
 * history pipeline.
 *
 * Every method that reads timeline state accesses `dataRef.current` at call
 * time so the adapter always operates on the latest canonical data without
 * re-creating the object on every render.
 *
 * ## Base-version semantics
 *
 * Every `apply()` call compares the patch's `version` field (the base version
 * the patch was built against) with the current canonical version — the live
 * `getConfigVersion()` channel when provided (it advances on save
 * acknowledgment without committing a new data object), else
 * `dataRef.current.configVersion`. If they differ the patch is stale and a
 * {@link TimelineVersionConflictError} is thrown before any mutation occurs.
 *
 * This is the **local monotonic invalidation** layer: it catches stale patches
 * before they reach the provider, which is essential when the provider does
 * not enforce strict compare-and-swap on save (e.g. AstridBridge).  When the
 * provider *does* enforce CAS the provider layer adds a second line of defence.
 *
 * Version 0 is treated as "no base-version expectation" (initial patches,
 * extensions that intentionally bypass version gating).
 */
export function useTimelineOps({
  commitData,
  applyEdit,
  semanticCommandSaving,
  getProposalSourceContext,
  getPendingProposalTransactionId,
  recoverProposalSave,
  captureSaveTarget,
  flushSaveTarget,
  dataRef,
  getConfigVersion,
  flushPendingSave,
  createManualCheckpoint,
  jumpToCheckpoint,
  checkpoints,
  editability,
}: UseTimelineOpsArgs): TimelineOps {
  const proposalSourceContextRef = useRef(getProposalSourceContext);
  proposalSourceContextRef.current = getProposalSourceContext;
  const proposalRecoveryRef = useRef({ getPendingProposalTransactionId, recoverProposalSave });
  proposalRecoveryRef.current = { getPendingProposalTransactionId, recoverProposalSave };

  // Keep checkpoints in a ref so synchronous rollback lookups are always
  // against the latest list without re-creating the adapter on every change.
  const checkpointsRef = useRef(checkpoints);
  checkpointsRef.current = checkpoints;

  // The canonical-version getter is deliberately read through a ref so the
  // stable adapter below does not re-create itself when the host's getter
  // identity changes between renders.
  const getConfigVersionRef = useRef(getConfigVersion);
  getConfigVersionRef.current = getConfigVersion;
  const flushPendingSaveRef = useRef(flushPendingSave);
  flushPendingSaveRef.current = flushPendingSave;
  const getCanonicalVersion = useCallback(
    () => getConfigVersionRef.current?.() ?? dataRef.current?.configVersion ?? 0,
    [dataRef],
  );

  // Map client-generated checkpoint IDs to labels so rollback can resolve
  // them against the backend-populated checkpoints list.
  const pendingLabels = useRef<Map<string, string>>(new Map());

  const assertTimelineEditable = useCallback((operation: string) => {
    const permission = editability?.checkTimeline?.();
    if (permission?.allowed === false) {
      throw new Error(
        `TimelineOps.${operation}: timeline edit denied (${permission.reason ?? 'read_only'}).`,
      );
    }
  }, [editability]);

  // ---- validate -----------------------------------------------------------

  const validate = useCallback(
    (patch: TimelinePatch): TimelinePatchValidationResult => {
      return validateTimelinePatch(patch);
    },
    [],
  );

  // ---- preview ------------------------------------------------------------

  const preview = useCallback(
    (patch: TimelinePatch): TimelinePreviewResult => {
      const current = dataRef.current;
      if (!current) {
        return {
          diff: { version: patch.version, entries: [], affectedObjectIds: [] },
          fullyPreviewable: false,
          diagnostics: [
            {
              severity: 'error',
              code: 'timeline-patch/no-data',
              message: 'Timeline data is not yet loaded.',
            },
          ],
        };
      }

      const result = previewTimelinePatch(patch, current);

      // Attach a stale-base-version warning when the patch was built against
      // a different version than the current canonical state.  Preview is
      // read-only, so we warn rather than block. The canonical version comes
      // from the live channel (which advances on receipt-only acks without a
      // new data object), not from `current.configVersion`.
      const canonicalVersion = getCanonicalVersion();
      if (
        patch.version !== 0 &&
        patch.version !== canonicalVersion &&
        result.fullyPreviewable
      ) {
        return {
          ...result,
          diagnostics: [
            ...result.diagnostics,
            {
              severity: 'warning' as const,
              code: 'timeline-patch/stale-base-version' as const,
              message:
                `Preview: patch baseVersion (${patch.version}) does not match ` +
                `current timeline version (${canonicalVersion}). ` +
                `The preview may not reflect the current state. Re-snapshot ` +
                `to get an accurate preview.`,
            },
          ],
        };
      }

      return result;
    },
    [dataRef, getCanonicalVersion],
  );

  // ---- apply --------------------------------------------------------------

  const apply = useCallback(
    (patch: TimelinePatch): TimelineDiff => {
      assertTimelineEditable('apply');

      // 0. Guard against no data
      const current = dataRef.current;
      if (!current) {
        throw new Error('TimelineOps.apply: timeline data is not yet loaded.');
      }

      // 0a. Base-version staleness check (local monotonic invalidation).
      //
      //     The patch.version is the base version the caller observed when
      //     building the patch.  If it doesn't match the current canonical
      //     version the timeline has been modified since the patch was
      //     created — the patch is stale and must be rejected. The canonical
      //     version comes from the live channel (which advances on
      //     receipt-only acks without a new data object), so a snapshot's
      //     baseVersion always compares against the same source.
      //
      //     Version 0 is treated as "no base-version expectation" (e.g.
      //     initial patches before the first provider load or patches from
      //     extensions that intentionally bypass version gating).
      const canonicalVersion = getCanonicalVersion();
      if (patch.version !== 0 && patch.version !== canonicalVersion) {
        throw new TimelineVersionConflictError(
          `TimelineOps.apply: stale baseVersion — ` +
          `patch created at version ${patch.version} but timeline is at ` +
          `version ${canonicalVersion}. ` +
          `Re-read the current snapshot and rebuild the patch.`,
        );
      }

      // 1. Validate the full batch
      const validation = validateTimelinePatch(patch);
      if (!validation.valid) {
        const messages = validation.diagnostics
          .filter((d) => d.severity === 'error')
          .map((d) => d.message)
          .join('; ');
        throw new Error(
          `TimelineOps.apply: patch validation failed. ${messages}`,
        );
      }

      // 2. Compile against current canonical data
      const compiled = compileTimelinePatch(patch, current);
      if (!compiled.valid || !compiled.nextData) {
        const messages = compiled.diagnostics
          .filter((d) => d.severity === 'error')
          .map((d) => d.message)
          .join('; ');
        throw new Error(
          `TimelineOps.apply: patch compilation failed. ${messages}`,
        );
      }

      // Adapt explicit patch intent, never a diff of its materialized document.
      // A mixed/unsupported batch stays entirely on the compatibility route.
      // Use the existing compiler for intermediate bases so repeated targets
      // carry sequential expectations without duplicating patch semantics.
      const commands = orderedPatchCommands(patch, current);
      // 3. Commit once through commitData with semantic transaction metadata.
      //    History recording is enabled by default (skipHistory defaults to false).
      commitData(compiled.nextData, {
        save: true,
        semantic: true,
        editCommands: commands,
      });

      // 4. Return the semantic diff
      return compiled.diff;
    },
    [assertTimelineEditable, commitData, dataRef, getCanonicalVersion],
  );

  // ---- checkpoint ---------------------------------------------------------

  const checkpoint = useCallback(
    (label?: string): string => {
      assertTimelineEditable('checkpoint');
      const id = uid();
      const effectiveLabel = label ?? `Patch checkpoint ${id.slice(0, 8)}`;
      pendingLabels.current.set(id, effectiveLabel);
      // Fire-and-forget: the host persists the checkpoint asynchronously.
      // The backend-generated ID will appear in the checkpoints list with
      // the same label, allowing rollback to resolve the client ID.
      void createManualCheckpoint(effectiveLabel);
      return id;
    },
    [assertTimelineEditable, createManualCheckpoint],
  );

  // ---- rollback -----------------------------------------------------------

  const rollback = useCallback(
    (checkpointId: string): TimelineDiff | null => {
      assertTimelineEditable('rollback');
      const currentCheckpoints = checkpointsRef.current;

      // Resolve the checkpoint: first try an exact ID match, then fall back
      // to label-based lookup for client-generated IDs.
      let resolvedId: string | null = null;

      const exactMatch = currentCheckpoints.find((c) => c.id === checkpointId);
      if (exactMatch) {
        resolvedId = exactMatch.id;
      } else {
        // Try label-based resolution for client-generated IDs.
        const label = pendingLabels.current.get(checkpointId);
        if (label) {
          const labelMatch = currentCheckpoints.find((c) => c.label === label);
          if (labelMatch) {
            resolvedId = labelMatch.id;
            pendingLabels.current.delete(checkpointId);
          }
        }
      }

      if (!resolvedId) {
        return null;
      }

      // Capture a snapshot of the pre-rollback state for the diff
      const beforeData = dataRef.current;

      jumpToCheckpoint(resolvedId);

      // Build a minimal rollback diff
      const afterData = dataRef.current;
      const affectedIds: string[] = [];
      if (beforeData) {
        for (const track of beforeData.tracks) {
          affectedIds.push(track.id);
        }
      }
      if (afterData) {
        for (const track of afterData.tracks) {
          if (!affectedIds.includes(track.id)) {
            affectedIds.push(track.id);
          }
        }
      }

      return {
        version: afterData?.configVersion ?? 0,
        entries: [
          {
            granularity: 'track',
            kind: 'modified',
            target: 'timeline',
            op: 'track.update',
            before: beforeData
              ? { configVersion: beforeData.configVersion }
              : undefined,
            after: afterData
              ? { configVersion: afterData.configVersion }
              : undefined,
          },
        ],
        affectedObjectIds: affectedIds,
      };
    },
    [assertTimelineEditable, dataRef, jumpToCheckpoint],
  );

  // ---- setAllTracksMuted --------------------------------------------------

  const setAllTracksMuted = useCallback(
    (muted: boolean): TimelineDiff => {
      const current = dataRef.current;
      if (!current) {
        throw new Error(
          'TimelineOps.setAllTracksMuted: timeline data is not yet loaded.',
        );
      }

      // Find all audio tracks
      const audioTracks = current.tracks.filter((t) => t.kind === 'audio');

      // The patch base version must match the CANONICAL version (the live
      // channel) or apply()'s stale-base check would reject it.
      const canonicalVersion = getCanonicalVersion();

      if (audioTracks.length === 0) {
        return {
          version: canonicalVersion,
          entries: [],
          affectedObjectIds: [],
        };
      }

      // Build a patch with track.update for each audio track.
      // The version is set to the canonical version so the base-version
      // check in apply() will pass.
      const patch: TimelinePatch = {
        version: canonicalVersion,
        operations: audioTracks.map((track) => ({
          op: 'track.update' as const,
          target: track.id,
          payload: { muted },
          mergeMode: 'merge' as const,
        })),
      };

      // Re-use apply which validates, compiles, and commits
      return apply(patch);
    },
    [apply, dataRef, getCanonicalVersion],
  );

  // Capture once at production proposal creation, before any user action.
  const submissions = useRef(new Map<string, { binding: ProposalCommandBinding; target: TimelineSaveTarget; before?: TimelineData; owner?: TimelineData; terminal?: unknown }>());
  const captureProposal = useCallback((patch: TimelinePatch, source: string, proposalId: string) => {
    if (!semanticCommandSaving) return undefined;
    if (proposalRecoveryRef.current.getPendingProposalTransactionId?.()) {
      throw new Error('A submitted proposal must be recovered before creating another proposal.');
    }
    const current = dataRef.current;
    if (!current) throw new Error('Proposal requires timeline data.');
    const commands = orderedPatchCommands(patch, current);
    // Other established patch families retain their compatibility behavior.
    if (!commands) return undefined;
    if (!current.head?.headRevisionId) throw new Error('Proposal requires an exact canonical base revision.');
    const baseVersion = getCanonicalVersion();
    if (patch.version !== 0 && patch.version !== baseVersion) throw new Error('Proposal has a stale base version.');
    const compiled = compileTimelinePatch(patch, current);
    if (!compiled.valid || !compiled.nextData) throw new Error('Proposal patch cannot be compiled.');
    const previewResult = previewTimelinePatch(patch, current);
    const occurrence = commandContext(current, commands);
    const providerContext = proposalSourceContextRef.current?.() ?? null;
    const detail = { proposalId, source, transactionId: 'proposal:' + proposalId,
      base: current.head, providerContext, baseVersion, occurrence };
    const preview = { ...previewResult, diagnostics: [...previewResult.diagnostics, {
      severity: 'info' as const, code: 'timeline-patch/proposal-command-binding' as const,
      message: 'Proposal commands are bound to this source and exact base revision.', detail,
    }] };
    return freezeProposal(JSON.parse(JSON.stringify({ proposalId, source, transactionId: `proposal:${proposalId}`,
      base: current.head, providerContext, baseVersion, signature: current.stableSignature, patch,
      commands, occurrence, preview }))) as ProposalCommandBinding;
  }, [semanticCommandSaving, dataRef, getCanonicalVersion]);

  const checkBinding = useCallback((binding: ProposalCommandBinding) => {
    const captured = captureProposal(binding.patch, binding.source, binding.proposalId);
    if (!captured || JSON.stringify(captured) !== JSON.stringify(binding)) {
      throw new Error('Proposal base, commands or source context changed.');
    }
    return binding.preview;
  }, [captureProposal]);

  const acceptProposal = useCallback((binding: ProposalCommandBinding): Promise<TimelineDiff> => {
    assertTimelineEditable('acceptProposal');
    const pending = proposalRecoveryRef.current.getPendingProposalTransactionId?.();
    if (pending) {
      if (pending !== binding.transactionId || !proposalRecoveryRef.current.recoverProposalSave) {
        throw new Error('An unresolved proposal COMMIT must be recovered before accepting another proposal.');
      }
      return proposalRecoveryRef.current.recoverProposalSave(binding).then(() => binding.preview.diff);
    }
    if (!semanticCommandSaving || !captureSaveTarget || !flushSaveTarget) throw new Error('Proposal command persistence is unavailable.');
    // Old provider/session closures must fail before scheduling any edit.
    captureSaveTarget();
    let submission = submissions.current.get(binding.proposalId);
    if (submission && JSON.stringify(submission.binding) !== JSON.stringify(binding)) throw new Error('Proposal retry changed its captured intent.');
    if (!submission) {
      checkBinding(binding);
      const before = dataRef.current!;
      const compiled = compileTimelinePatch(binding.patch, before);
      if (!compiled.valid || !compiled.nextData) throw new Error('Proposal cannot be compiled.');
      const owner = compiled.nextData;
      bindProposalCorrelation(owner, binding.transactionId);
      try {
        commitData(owner, { save: true, semantic: true, transactionId: binding.transactionId,
          editCommands: binding.commands.map((command) => validateEditCommand(command)), proposalBase: binding.base });
      } catch (error) {
        if (dataRef.current === owner) commitData(before, { save: false, skipHistory: true });
        throw error;
      }
      submission = { binding, before, owner, target: captureSaveTarget() };
      submissions.current.set(binding.proposalId, submission);
    }
    if (submission.terminal) throw submission.terminal;
    const attempt = submission;
    return flushSaveTarget(attempt.target).then(() => {
      attempt.before = undefined; attempt.owner = undefined;
      return binding.preview.diff;
    }, (error: unknown) => {
      // Ambiguous outcomes retain the original save owner/request for exact retry.
      if (error && typeof error === 'object' && 'certainty' in error && error.certainty === 'definitely-uncommitted') {
        attempt.terminal = error;
        if (attempt.before && dataRef.current === attempt.owner) commitData(attempt.before, { save: false, skipHistory: true });
        attempt.before = undefined; attempt.owner = undefined;
      }
      throw error;
    });
  }, [assertTimelineEditable, semanticCommandSaving, captureSaveTarget, flushSaveTarget, checkBinding, commitData, dataRef]);

  // ---- assemble stable adapter --------------------------------------------

  const flush = useCallback(async (): Promise<{ readonly version: number }> => {
    if (!dataRef.current) {
      throw new Error('TimelineOps.flush: timeline data is not yet loaded.');
    }
    const barrier = flushPendingSaveRef.current;
    if (!barrier) {
      throw new Error('TimelineOps.flush: durable persistence is unavailable.');
    }
    return Object.freeze({ version: await barrier() });
  }, [dataRef]);

  return useMemo<ProposalTimelineOps & {
    submitCommandTransaction: (
      commands: readonly EditCommand[],
      options: Readonly<{ transactionId: string; semantic: true }>,
    ) => void;
  }>(
    () => ({
      proposalContext: () => JSON.stringify([getCanonicalVersion(), dataRef.current?.head, dataRef.current?.stableSignature, proposalSourceContextRef.current?.() ?? null]),
      proposalSubmitted: () => Boolean(proposalRecoveryRef.current.getPendingProposalTransactionId?.()),
      captureProposal,
      previewProposal: checkBinding,
      acceptProposal,
      validate,
      preview,
      apply,
      submitCommandTransaction(commands, options) {
        assertTimelineEditable('submitCommandTransaction');
        if (!options.transactionId.trim() || commands.length === 0) {
          throw new Error('TimelineOps.submitCommandTransaction requires commands and a stable transaction ID.');
        }
        if (!applyEdit) throw new Error('TimelineOps.submitCommandTransaction is not wired to the editor command path.');
        const admittedCommands = commands.map((command) => validateEditCommand(command));
        applyEdit({ type: 'commands' }, {
          editCommands: admittedCommands,
          transactionId: options.transactionId,
          semantic: true,
          save: true,
        });
      },
      flush,
      checkpoint,
      rollback,
      setAllTracksMuted,
    }),
    [getCanonicalVersion, dataRef, captureProposal, checkBinding, acceptProposal, validate, preview, apply, applyEdit, assertTimelineEditable, flush, checkpoint, rollback, setAllTracksMuted],
  );
}
