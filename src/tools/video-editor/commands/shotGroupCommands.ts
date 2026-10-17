import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { occurrenceIdentityFor } from './semanticGestures.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import type { ShotFinalVideo } from '@/tools/video-editor/hooks/useFinalVideoAvailable.ts';
import { readSelectedProjectMediaIdentity } from './selectedProjectMedia.ts';

export type ShotGroupIdentity = { shotId: string; trackId: string };
export type ShotGroupSelection = ShotGroupIdentity & { clipIds: string[] };

function storedGroup(data: TimelineData | null, group: ShotGroupIdentity) {
  const matches = data?.config.pinnedShotGroups?.filter((candidate) => (
    candidate.shotId === group.shotId && candidate.trackId === group.trackId
  )) ?? [];
  return matches.length === 1 ? matches[0] : undefined;
}

const nonempty = (value: unknown): value is string => typeof value === 'string' && value.length > 0;

function scopedMember(data: TimelineData, clipId: string, trackId: string): string | null {
  if (!nonempty(clipId) || clipId.includes('/')) return null;
  const matches = data.config.clips.filter((clip) => clip.id === clipId);
  if (matches.length !== 1) return null;
  const clip = matches[0];
  if (clip.track !== trackId) return null;
  const identity = occurrenceIdentityFor(data, clipId);
  if (clip.app?.canonical && !identity) return null;
  return identity
    ? `occurrence:${identity.occurrenceId}/clip:${identity.sourceClipId}`
    : `parent/clip:${clipId}`;
}

function groupCommand(op: string, group: ShotGroupIdentity, args: Record<string, unknown>): EditCommand | null {
  if (!nonempty(group.shotId) || !nonempty(group.trackId) || group.shotId.includes('/') || group.trackId.includes('/')) {
    return null;
  }
  return { op, select: null, args: { group: { shotId: group.shotId, trackId: group.trackId }, ...args } };
}

export function buildPinShotGroupCommand(
  data: TimelineData | null,
  group: ShotGroupSelection,
  name?: string,
): EditCommand | null {
  if (!data || !Array.isArray(group.clipIds) || group.clipIds.length === 0) return null;
  const members = group.clipIds.map((clipId) => scopedMember(data, clipId, group.trackId));
  if (members.some((member) => member === null) || new Set(members).size !== members.length) return null;
  const scopes = new Set(members.map((member) => member!.split('/clip:', 1)[0]));
  if (scopes.size !== 1) return null;
  const args = {
    intent: 'pin',
    members: members as string[],
    ...(typeof name === 'string' && name.length > 0 ? { name } : {}),
  };
  return groupCommand('shot-group.set', group, args);
}

export function buildUnpinShotGroupCommand(data: TimelineData | null, group: ShotGroupIdentity): EditCommand | null {
  if (!storedGroup(data, group)) return null;
  return groupCommand('shot-group.remove', group, { remove_clip_ids: [] });
}

/** Transfer the complete stored group. Display IDs supply lookup only; canonical
 * identities and the stored member selectors supply occurrence ownership.
 */
export function buildTransferShotGroupCommand(
  data: TimelineData,
  group: ShotGroupSelection,
  targetTrackId: string,
): EditCommand | null {
  const stored = storedGroup(data, group);
  if (!stored || !nonempty(targetTrackId) || targetTrackId.includes('/') || targetTrackId === group.trackId
    || !['images', 'video'].includes(stored.mode ?? 'images')
    || (stored.mode === 'video' && stored.clipIds.length !== 1)
    || group.clipIds.length !== stored.clipIds.length || new Set(group.clipIds).size !== group.clipIds.length
    || group.clipIds.some((id) => !stored.clipIds.includes(id))
    || data.config.pinnedShotGroups?.some((row) => row !== stored && row.clipIds.some((id) => group.clipIds.includes(id)))
    || data.config.pinnedShotGroups?.some((row) => row.shotId === group.shotId && row.trackId === targetTrackId)
    || [group.trackId, targetTrackId].some((id) => {
      const tracks = data.config.tracks?.filter((track) => track.id === id) ?? [];
      return tracks.length !== 1 || tracks[0].kind !== 'visual';
    })) return null;
  const members = group.clipIds.map((id) => scopedMember(data, id, group.trackId));
  if (members.some((id) => id === null) || new Set(members).size !== members.length) return null;
  const scopes = new Set(members.map((id) => id!.split('/clip:')[0]));
  if (scopes.size !== 1) return null;
  const scope = [...scopes][0];
  if (stored.ownerOccurrenceId != null && scope !== `occurrence:${stored.ownerOccurrenceId}`) return null;
  if (scope !== 'parent' && (!stored.memberSelectors || stored.ownerOccurrenceId == null)) return null;
  if (stored.memberSelectors && (stored.memberSelectors.length !== members.length
    || new Set(stored.memberSelectors).size !== members.length
    || members.some((id) => !stored.memberSelectors!.includes(id!)))) return null;
  let capturedIdentity: ReturnType<typeof occurrenceIdentityFor>;
  for (const id of group.clipIds) {
    const identity = occurrenceIdentityFor(data, id);
    const source = identity?.sourceClip ?? data.config.clips.find((clip) => clip.id === id)!;
    if (identity && (identity.projectId !== data.head?.projectId || identity.parentDocumentId !== data.head?.timelineId
      || identity.headRevisionId !== data.head?.headRevisionId)) return null;
    if (identity && capturedIdentity && ['projectId', 'parentDocumentId', 'headRevisionId', 'occurrenceId', 'shotId',
      'revisionId', 'internalTimelineRevisionId', 'outputIdentity'].some((key) =>
        Reflect.get(identity, key) !== Reflect.get(capturedIdentity!, key))) return null;
    capturedIdentity = identity;
    const app = source.app as Record<string, unknown> | undefined;
    const intent = app?.astrid as Record<string, unknown> | undefined;
    // Relation/sequence/bed and source-edge choices remain with their existing
    // producers. A literal transfer must not normalize authored relationships.
    if (source.track !== group.trackId || typeof source.at !== 'number' || !Number.isFinite(source.at)
      || ['on', 'until', 'for', 'cut', 'sequence', 'sequence_fit', 'segment', 'formulas', 'loop', 'orphan']
        .some((key) => Object.prototype.hasOwnProperty.call(app ?? {}, key) || Object.prototype.hasOwnProperty.call(intent ?? {}, key))
      || ['keyframes', 'modifiers', 'keyframeOrigin'].some((key) => Object.prototype.hasOwnProperty.call(source, key))) return null;
  }
  if ((data.config.app?.astrid as Record<string, unknown> | undefined)?.music_beds != null) return null;
  return groupCommand('shot-group.set', group, { intent: 'transfer', target: `${scope}/track:${targetTrackId}`, members });
}

export function buildDeleteShotGroupCommand(
  data: TimelineData | null,
  group: ShotGroupSelection,
): EditCommand | null {
  if (!data || !Array.isArray(group.clipIds) || group.clipIds.length === 0) return null;
  const removeClipIds = group.clipIds.map((clipId) => scopedMember(data, clipId, group.trackId));
  if (removeClipIds.some((clipId) => clipId === null) || new Set(removeClipIds).size !== removeClipIds.length) return null;
  const stored = storedGroup(data, group);
  if (!stored || group.clipIds.some((clipId) => !stored.clipIds.includes(clipId))) return null;
  return groupCommand('shot-group.remove', group, { remove_clip_ids: removeClipIds as string[] });
}

export function buildRestoreShotGroupImagesCommand(data: TimelineData | null, group: ShotGroupIdentity): EditCommand | null {
  if (storedGroup(data, group)?.mode !== 'video') return null;
  return groupCommand('shot-group.set', group, { intent: 'images' });
}

function selectedVideoMedia(finalVideo: ShotFinalVideo | undefined) {
  const media = readSelectedProjectMediaIdentity(
    (finalVideo as (ShotFinalVideo & { selectedMedia?: unknown }) | undefined)?.selectedMedia,
  );
  // Runtime final-video rows are keyed by their immutable object identity.
  // Refuse a selection captured for a different output instead of silently
  // replacing the user's latest output with stale media.
  return media && media.object_id === finalVideo?.id ? media : null;
}

export function buildSetShotGroupVideoCommand(
  data: TimelineData | null,
  group: ShotGroupIdentity,
  finalVideo: ShotFinalVideo | undefined,
  reservedLocalId: string,
): EditCommand | null {
  if (storedGroup(data, group)?.mode !== 'images') return null;
  const media = selectedVideoMedia(finalVideo);
  if (!media || !nonempty(reservedLocalId) || reservedLocalId.includes('/')) return null;
  return groupCommand('shot-group.set', group, {
    intent: 'video',
    media,
    identities: { clip_id: reservedLocalId },
  });
}

export function buildReplaceShotGroupVideoCommand(
  data: TimelineData | null,
  group: ShotGroupIdentity,
  finalVideo: ShotFinalVideo | undefined,
): EditCommand | null {
  if (storedGroup(data, group)?.mode !== 'video') return null;
  const media = selectedVideoMedia(finalVideo);
  if (!media) return null;
  return groupCommand('shot-group.set', group, { intent: 'replace-video', media });
}
