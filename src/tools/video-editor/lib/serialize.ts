import type { PreparedShotComposition } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import type {
  ResolvedTimelineConfig,
  TimelineClip,
  TimelineConfig,
  TrackDefinition,
} from '@/tools/video-editor/types/index.ts';
import {
  assertValidTimelineConfigSnapshot,
  cloneAppExtension,
  cloneTimelineExtras,
  sanitizeTimelineClipSnapshot,
  sanitizeTrackDefinitionSnapshot,
} from './timeline-domain.ts';

export {
  TIMELINE_CLIP_FIELDS,
  TRACK_DEFINITION_FIELDS,
  type TimelineClipField,
  type TrackDefinitionField,
} from './timeline-domain.ts';

// Undefined means raw authored input; null means a derived caller lost its basis.
export const serializeClipForDisk = (
  clip: ResolvedTimelineConfig['clips'][number],
  rawClip?: Record<string, unknown> | null,
): TimelineClip => {
  if (rawClip === null) throw new Error('The projected clip has no verified raw serialization basis');
  return sanitizeTimelineClipSnapshot(rawClip === undefined ? clip : restoreStoredCap(clip, rawClip));
};

function restoreStoredCap<T extends TimelineClip>(serialized: T, rawClip: Record<string, unknown>): T {
  const timing = serialized.app?.canonicalTiming;
  if (!timing || typeof timing !== 'object' || Array.isArray(timing)) return serialized;
  const rawApp = rawClip.app as Record<string, unknown> | undefined;
  const restored = Object.fromEntries(Object.entries(timing)
    .filter(([key]) => key !== 'storedOccurrenceDurationMs'));
  // Projection overwrites these raw names. Restore authored collisions from
  // their counterpart; leave pre-existing view metadata alone otherwise.
  const app = { ...serialized.app, canonicalTiming: restored };
  for (const key of ['canonical', 'canonicalTiming']) {
    if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {
      Object.defineProperty(app, key, { value: structuredClone(rawApp[key]),
        enumerable: true, configurable: true, writable: true });
    }
  }
  return { ...serialized, app };
}

function hasDerivedStoredCap(config: ResolvedTimelineConfig): boolean {
  return config.clips.some((clip) => {
    const timing = clip.app?.canonicalTiming;
    return timing !== null && typeof timing === 'object' && !Array.isArray(timing)
      && Object.prototype.hasOwnProperty.call(timing, 'storedOccurrenceDurationMs');
  });
}

/** Resolve counterparts from the retained graph's identity map, never a display prefix. */
export function projectedClipCounterparts(composition: PreparedShotComposition, clips: readonly TimelineClip[] = []) {
  const { clipIdentities } = projectCanonicalComposition(composition, undefined, { clampToOccurrenceDuration: false });
  const counterparts = new Map([...clipIdentities].map(([id, identity]) => {
    const occurrence = composition.occurrences.find((item) => item.occurrenceId === identity.occurrenceId)!;
    const internal = occurrence.revision.internal_timeline_revision as Record<string, unknown>;
    const timeline = internal.timeline as { clips?: Record<string, unknown>[] };
    const matches = identity.rawClipId === null ? []
      : (timeline.clips ?? []).filter((clip) => clip.id === identity.rawClipId);
    return [id, matches.length === 1 ? matches[0] : null] as const;
  }));
  // A popup's copy-on-write ACK can remap the new child IDs while the editor
  // still displays its original pinned revision. That immutable revision is
  // already retained in the graph; use the existing full identity, not an ID
  // prefix or a canonicalTiming shape, to recover its raw counterpart.
  const parent = composition.contract.parent_composition as { clips?: TimelineClip[]; config?: { clips?: TimelineClip[] } };
  for (const clip of clips) {
    if (counterparts.has(clip.id) || (parent.clips ?? parent.config?.clips ?? []).some((raw) => raw.id === clip.id)) continue;
    const identity = clip.app?.canonical as { projectId?: string; parentDocumentId?: string;
      occurrenceId?: string; shotId?: string; revisionId?: string; rawClipId?: string; clipRef?: string } | undefined;
    if (identity?.projectId !== composition.projectId || identity.parentDocumentId !== composition.parentDocumentId
      || !composition.occurrences.some((item) => item.occurrenceId === identity.occurrenceId)
      || !identity.rawClipId || identity.clipRef !== `occurrence:${identity.occurrenceId}/clip:${identity.rawClipId}`) continue;
    const revision = composition.contract.shot_revisions.find((item) => item.shot_id === identity.shotId
      && item.revision_id === identity.revisionId);
    const internal = revision?.internal_timeline_revision as { timeline?: { clips?: Record<string, unknown>[] } } | undefined;
    const matches = (internal?.timeline?.clips ?? []).filter((raw) => raw.id === identity.rawClipId);
    if (matches.length === 1) counterparts.set(clip.id, matches[0]);
  }
  return counterparts;
}

/** Only explicitly projected callers use the verified graph to remove the new view hint. */
export function serializeProjectedTimelineConfig<T extends TimelineConfig>(
  config: T,
  composition: PreparedShotComposition | null,
): T {
  if (!composition) throw new Error('The projected timeline has no verified raw serialization basis; keep the draft');
  if (new Set(config.clips.map((clip) => clip.id)).size !== config.clips.length) {
    throw new Error('Projected serialization requires unambiguous clip identities; keep the draft');
  }
  const counterparts = projectedClipCounterparts(composition, config.clips);
  const parent = composition.contract.parent_composition as Record<string, unknown>;
  const parentConfig = parent.config as { clips?: TimelineClip[] } | undefined;
  const parentClips = (Array.isArray(parent.clips) ? parent.clips : parentConfig?.clips ?? []) as TimelineClip[];
  return { ...config, clips: config.clips.map((clip) => {
    if (!counterparts.has(clip.id)) {
      if (parentClips.filter((raw) => raw.id === clip.id).length === 1) return clip;
      throw new Error(`The projected clip ${clip.id} has no verified raw counterpart; keep the draft`);
    }
    const raw = counterparts.get(clip.id);
    if (!raw) throw new Error('The projected clip has no unambiguous raw counterpart');
    return restoreStoredCap(clip, raw);
  }) };
}

export const serializeTrackForDisk = (track: TrackDefinition): TrackDefinition => {
  return sanitizeTrackDefinitionSnapshot(track);
};

export const validateSerializedConfig = (config: TimelineConfig): void => {
  assertValidTimelineConfigSnapshot(config);
};

export const serializeForDisk = (
  resolved: ResolvedTimelineConfig,
  pinnedShotGroups?: TimelineConfig['pinnedShotGroups'],
  // Sprint 2: optional carry-through of schema-lift top-level fields. Callers
  // that don't pass these keep the prior behavior; existing timelines without
  // them stay unchanged.
  extras?: Pick<TimelineConfig, 'theme' | 'theme_overrides' | 'generation_defaults' | 'app'>,
  rawComposition?: PreparedShotComposition | null,
): TimelineConfig => {
  if (rawComposition === undefined && hasDerivedStoredCap(resolved)) {
    throw new Error('The projected timeline has no verified raw serialization basis; keep the draft');
  }
  const resolvedExtras = extras ?? resolved;
  const serialized: TimelineConfig = {
    // `output` is DERIVED (theme.visual.canvas), not persisted: the bridge
    // strips it on save and the editor re-materializes it on load. Keeping it
    // off the wire prevents editor/render settings from fighting the theme.
    output: resolved.output,
    tracks: resolved.tracks.map(serializeTrackForDisk),
    clips: (rawComposition === undefined ? resolved : serializeProjectedTimelineConfig(resolved, rawComposition))
      .clips.map((clip) => serializeClipForDisk(clip)),
  };

  if (pinnedShotGroups && pinnedShotGroups.length > 0) {
    serialized.pinnedShotGroups = pinnedShotGroups;
  }

  if (resolvedExtras.theme !== undefined) {
    serialized.theme = resolvedExtras.theme;
  }
  if (resolvedExtras.theme_overrides !== undefined) {
    serialized.theme_overrides = resolvedExtras.theme_overrides;
  }
  if (resolvedExtras.generation_defaults !== undefined) {
    serialized.generation_defaults = resolvedExtras.generation_defaults;
  }
  if (resolvedExtras.app !== undefined) {
    serialized.app = cloneAppExtension(resolvedExtras.app);
  }

  validateSerializedConfig(serialized);
  // Keep the static TimelineConfig return contract for existing callers while
  // honoring the wire contract: output is derived and must not be persisted.
  Reflect.deleteProperty(serialized, 'output');
  return serialized;
};

/** Editor edits keep opaque authored roots; strict disk serialization stays closed. */
export const serializeResolvedTimelineEdit = (
  resolved: ResolvedTimelineConfig,
  pinnedShotGroups?: TimelineConfig['pinnedShotGroups'],
  authoredConfig?: TimelineConfig,
  rawComposition?: PreparedShotComposition | null,
): TimelineConfig => {
  const { registry: _resolvedRegistry, ...authored } = resolved;
  return {
    ...cloneTimelineExtras(authored),
    // Resolution replaces this opaque authored root with preview assets.
    ...(authoredConfig && Object.prototype.hasOwnProperty.call(authoredConfig, 'registry')
      ? cloneAppExtension({ registry: Reflect.get(authoredConfig, 'registry') })
      : {}),
    ...serializeForDisk(resolved, pinnedShotGroups, undefined, rawComposition),
  };
};
