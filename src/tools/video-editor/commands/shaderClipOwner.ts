import { occurrenceIdentityFor } from './semanticGestures.ts';
import type { ShaderOwner } from './shaderSlots.ts';
import type { TimelineData } from '../lib/timeline-data.ts';

/** Reuse the editor's captured occurrence identity; never retarget a projected ID. */
export function shaderClipOwner(data: Pick<TimelineData, 'config' | 'head'>, id: string): ShaderOwner | undefined {
  const clips = data.config.clips.filter(clip => clip.id === id);
  if (clips.length !== 1) return;
  if (!clips[0].app?.canonical) return id.includes('/') ? undefined : { id: `parent/clip:${id}`, value: clips[0] };
  const identity = occurrenceIdentityFor(data, id);
  if (!identity?.sourceClip || identity.projectId !== data.head?.projectId || identity.parentDocumentId !== data.head?.timelineId
    || identity.headRevisionId !== data.head?.headRevisionId) return;
  return { id: `occurrence:${identity.occurrenceId}/clip:${identity.sourceClipId}`, value: identity.sourceClip };
}
