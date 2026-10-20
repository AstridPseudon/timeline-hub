import type { AstridRuntimeClient } from '@/integrations/runtime/client';
import type { MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types';
import type { TimelineCommandSession } from '@/tools/video-editor/commands/commitSession';
import { equal } from '@/tools/video-editor/commands/clipMovePrimitives';
import { asRecord } from '@/shared/lib/typeCoercion';
import {
  assertRuntimeRecoveryHead, assertRuntimeRecoverySource, freezeRecoveryValue,
  type RuntimeRecoveryPlacementDraft,
} from './runtimeRecoveryDestinations';

// Source staging: the official generated read must be exposed by the SAME
// authenticated App client. This is a local capability, never a replacement DTO.
export type RuntimeRecoveryPlacementClient = Pick<AstridRuntimeClient,
  'getTask' | 'getManagedOutput' | 'getProjectMediaSelection' | 'getProjectTimeline' | 'getRecoverableIdentity'> & {
  getProjectVerifiedMedia(projectId: string, selection: MediaSelection): Promise<VerifiedMedia>;
};

export interface RuntimeRecoveryCommandBinding {
  client: RuntimeRecoveryPlacementClient;
  session: TimelineCommandSession;
}

/** Binds one explicit chooser to the existing owner; never opens or steals an outbox. */
export function createRuntimeRecoveryPlacement(options: {
  client: RuntimeRecoveryPlacementClient;
  getBinding(): RuntimeRecoveryCommandBinding | null;
}) {
  let pending = false;
  let reserved: { key: string; childId: string; submitted: boolean } | undefined;
  return async (value: RuntimeRecoveryPlacementDraft, signal?: AbortSignal): Promise<void> => {
    if (pending) throw new Error('Manual placement is already pending; draft kept');
    const draft = freezeRecoveryValue(structuredClone(value));
    const binding = options.getBinding();
    if (!binding || binding.client !== options.client) throw new Error('Selected timeline command owner is unavailable; draft kept');
    const { session } = binding, { scope } = session;
    if (scope.projectId !== draft.projectId || scope.timelineId !== draft.timelineId) {
      throw new Error('Command owner does not match the explicit selected timeline; draft kept');
    }
    const current = () => {
      if (signal?.aborted || options.getBinding() !== binding) throw new Error('Manual placement cancelled or command owner changed; draft kept');
    };
    const identity = async () => {
      const actor = await options.client.getRecoverableIdentity();
      current();
      if (actor.actorId !== scope.actorId || actor.realmId !== scope.realmId) throw new Error('Manual placement actor changed; draft kept');
    };
    current();
    const key = JSON.stringify(draft);
    if (reserved?.submitted) throw new Error('Manual choice already submitted; use the command owner’s Retry or recovery, keeping the original request');
    if (reserved?.key !== key) reserved = { key, childId: crypto.randomUUID(), submitted: false };
    pending = true;
    try {
      await identity();
      await assertRuntimeRecoverySource(options.client, draft.projectId, draft.source);
      current();
      const pin = draft.source.mediaTuple;
      const verified = freezeRecoveryValue(structuredClone(await options.client.getProjectVerifiedMedia(draft.projectId, pin)));
      current();
      if (!equal(verified.selection, pin)) throw new Error('Verified media differs from the frozen selection; draft kept');
      const destination = draft.destination, document = draft.basis.canonicalDocument;
      const occurrences = document.parent_revision.payload.occurrences;
      const matches = Array.isArray(occurrences) ? occurrences.map(asRecord)
        .filter((row) => row?.occurrence_id === destination.owner.occurrenceId) : [];
      const occurrence = matches[0], placement = asRecord(occurrence?.placement);
      const shots = document.shot_revisions.filter((row) => row.shot_id === destination.shotId && row.revision_id === destination.shotRevisionId);
      const internals = document.internal_timeline_revisions.filter((row) => row.timeline_id === destination.internalTimelineId
        && row.revision_id === destination.internalRevisionId);
      const tracks = internals[0]?.payload.tracks;
      if (destination.owner.kind !== 'occurrence' || matches.length !== 1 || shots.length !== 1 || internals.length !== 1
        || occurrence?.shot_id !== destination.shotId || occurrence?.shot_revision_id !== destination.shotRevisionId
        || shots[0].internal_timeline_revision_id !== destination.internalRevisionId
        || (placement?.track ?? occurrence?.track) !== destination.parentTrackId
        || (placement?.track !== undefined && occurrence?.track !== undefined && placement.track !== occurrence.track)
        || !Array.isArray(tracks) || tracks.filter((row) => asRecord(row)?.id === destination.childTrackId).length !== 1) {
        throw new Error('Manual destination differs from its original raw ownership binding; draft kept');
      }
      const start = placement?.start_ms ?? occurrence?.at_ms;
      const { from, to } = draft.sourceWindow;
      if (typeof start !== 'number' || !Number.isFinite(start) || ![draft.on, from, to].every((n) => Number.isFinite(n) && n >= 0)
        || to <= from || draft.on < start / 1000) throw new Error('Manual timing is unsupported; draft kept');
      const kind = verified.media_type.split('/')[0];
      if (!['image', 'video'].includes(kind) || (kind === 'image' && from !== 0)) throw new Error('Manual source window is unsupported; draft kept');
      // The chooser labels parent timeline seconds. Native ADD owns child seconds;
      // its existing recipe refuses nontranslation maps, anchors and out-of-bounds intervals.
      const row = { id: reserved!.childId, clipType: kind, asset: pin.asset, track: destination.childTrackId,
        at: draft.on - start / 1000, hold: to - from, ...(kind === 'video' ? { from, to } : {}) };
      await Promise.all([
        assertRuntimeRecoverySource(options.client, draft.projectId, draft.source),
        assertRuntimeRecoveryHead(options.client, draft.projectId, draft.timelineId, draft.basis),
      ]);
      await identity();
      current();
      reserved!.submitted = true;
      await session.addOccurrenceMedia({ basis: draft.basis, ownerRef: `occurrence:${destination.owner.occurrenceId}`,
        row, media: pin, verifiedMedia: verified, assertCurrent: current });
      // No Placed notification. The session alone adopts the typed accepted closure.
    } finally { pending = false; }
  };
}
