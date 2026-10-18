import type { TimelineOccurrenceContext, TimelineOccurrenceMediaContext, DataProvider } from '../data/DataProvider.ts';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import type { SelectedProjectMediaIdentity } from '@/shared/contracts/selectedProjectMedia.ts';

const selectedMediaFields = [
  'asset',
  'generation_id',
  'variant_id',
  'object_id',
  'catalog_digest',
] as const;

const isRecord = (value: unknown): value is Record<string, unknown> => (
  value !== null && typeof value === 'object' && !Array.isArray(value)
);

/** Validate a Runtime selection without deriving or repairing any identity. */
export function readSelectedProjectMediaIdentity(value: unknown): SelectedProjectMediaIdentity | null {
  if (!isRecord(value)) return null;
  const keys = Object.keys(value);
  if (keys.length !== selectedMediaFields.length
    || selectedMediaFields.some((field) => !Object.prototype.hasOwnProperty.call(value, field))) return null;
  if (selectedMediaFields.some((field) => typeof value[field] !== 'string' || value[field].length === 0)) return null;
  if (!/^sha256:[0-9a-f]{64}$/.test(value.object_id as string)
    || !/^sha256:[0-9a-f]{64}$/.test(value.catalog_digest as string)) return null;
  return value as unknown as SelectedProjectMediaIdentity;
}

/** Match the admitted SDK property-path grammar without splitting asset keys. */
export const selectedMediaRegistryExpectationPath = (asset: string, occurrenceId?: string): string => {
  const owner = occurrenceId ? `occurrence:${occurrenceId}/shot::internal_timeline.registry.assets` : 'parent::registry.assets';
  return /^[A-Za-z_][\w-]*$/.test(asset) ? `${owner}.${asset}` : `${owner}[${JSON.stringify(asset)}]`;
};

export function buildSelectedProjectMediaAddCommand({
  selection: selectionValue,
  assetKey,
  mediaType,
  trackId,
  trackKind,
  clipId,
  at,
  durationSeconds,
  intrinsicDurationSeconds,
  existingTrackIds,
  existingClipIds,
  existingRegistryEntry,
  occurrence,
}: {
  selection: unknown;
  assetKey: string;
  mediaType: 'image' | 'video' | 'audio';
  trackId: string;
  trackKind: 'audio' | 'visual';
  clipId: string;
  at: number;
  durationSeconds: number;
  intrinsicDurationSeconds: number | null;
  existingTrackIds: readonly string[];
  existingClipIds: readonly string[];
  existingRegistryEntry?: unknown;
  occurrence?: TimelineOccurrenceMediaContext;
}): EditCommand | undefined {
  const selection = readSelectedProjectMediaIdentity(selectionValue);
  if (!selection || selection.asset !== assetKey || !assetKey
    || !trackId || trackId.includes('/') || !clipId || clipId.includes('/')
    || existingTrackIds.filter((id) => id === trackId).length !== 1
    || existingClipIds.includes(clipId)
    || (trackKind === 'visual' && mediaType === 'audio')
    || (trackKind === 'audio' && mediaType === 'image')
    || !Number.isFinite(at) || at < 0
    || !Number.isFinite(durationSeconds) || durationSeconds <= 0
    || (mediaType === 'audio'
      && (!Number.isFinite(intrinsicDurationSeconds) || (intrinsicDurationSeconds ?? 0) <= 0))
    || (typeof intrinsicDurationSeconds === 'number' && durationSeconds > intrinsicDurationSeconds)) {
    return undefined;
  }

  const prefix = occurrence ? `occurrence:${occurrence.context.occurrenceId}` : 'parent';
  if (occurrence && (!validOccurrenceMediaContext(occurrence.context) || !Number.isSafeInteger(occurrence.atMs) || occurrence.atMs < 0)) return undefined;
  const scopedClipId = `${prefix}/clip:${clipId}`;
  return {
    op: 'timeline.add',
    select: `${prefix}/track:${trackId}`,
    ...(occurrence ? { resolved: [`${prefix}/track:${trackId}`] } : {}),
    args: {
      media: selection,
      clip_id: clipId,
      at: occurrence ? (Math.round(at * 1000) + occurrence.atMs) / 1000 : at,
      duration: durationSeconds,
    },
    created: [scopedClipId],
    expect: {
      [`${scopedClipId}::`]: { state: 'absent' },
      [selectedMediaRegistryExpectationPath(selection.asset, occurrence?.context.occurrenceId)]: existingRegistryEntry === undefined
        ? { state: 'absent' } : { state: 'present', value: structuredClone(existingRegistryEntry) },
    },
  };
}

export function validOccurrenceMediaContext(context: TimelineOccurrenceContext): boolean {
  return ['projectId', 'parentDocumentId', 'headRevisionId', 'occurrenceId', 'shotId', 'shotRevisionId', 'internalRevisionId'].every(key => typeof context[key as keyof TimelineOccurrenceContext] === 'string' && context[key as keyof TimelineOccurrenceContext].length > 0)
    && !context.occurrenceId.includes('/');
}

/** Exact selected-media forms admitted by the occurrence import/placement path. */
export function isOccurrenceMediaCommand(command: EditCommand, context: TimelineOccurrenceContext): boolean {
  const media = readSelectedProjectMediaIdentity(command.args.media);
  const prefix = `occurrence:${context.occurrenceId}`;
  if (!validOccurrenceMediaContext(context) || !media || command.resolved?.length !== 1
    || command.resolved[0] !== command.select) return false;
  const registry = command.expect?.[selectedMediaRegistryExpectationPath(media.asset, context.occurrenceId)];
  if (!registry || !['absent', 'present'].includes(registry.state)) return false;
  if (command.op === 'timeline.add') {
    const child = `${prefix}/clip:${command.args.clip_id}`;
    return typeof command.select === 'string' && command.select.startsWith(`${prefix}/track:`)
      && command.select.slice(`${prefix}/track:`.length).length > 0
      && !command.select.slice(`${prefix}/track:`.length).includes('/')
      && Object.keys(command.args).length === 4 && typeof command.args.clip_id === 'string'
      && command.args.clip_id.length > 0 && !command.args.clip_id.includes('/')
      && command.created?.length === 1 && command.created[0] === child
      && command.expect?.[`${child}::`]?.state === 'absent'
      && typeof command.args.at === 'number' && Number.isFinite(command.args.at) && command.args.at >= 0
      && typeof command.args.duration === 'number' && Number.isFinite(command.args.duration) && command.args.duration > 0;
  }
  return command.op === 'clip.swap-asset' && typeof command.select === 'string'
    && command.select.startsWith(`${prefix}/clip:`) && !command.select.slice(`${prefix}/clip:`.length).includes('/')
    && Object.keys(command.args).length === 1 && !command.created?.length
    && command.expect?.[`${command.select}::`]?.state === 'present';
}

export function buildSelectedProjectMediaSwapCommand({ selection, sourceClipId, sourceClip, existingRegistryEntry, occurrence }: {
  selection: unknown; sourceClipId: string; sourceClip: Record<string, unknown>; existingRegistryEntry?: unknown;
  occurrence: TimelineOccurrenceMediaContext;
}): EditCommand | undefined {
  const media = readSelectedProjectMediaIdentity(selection);
  if (!media || !validOccurrenceMediaContext(occurrence.context) || !sourceClipId || sourceClipId.includes('/') || sourceClip.id !== sourceClipId) return undefined;
  const select = `occurrence:${occurrence.context.occurrenceId}/clip:${sourceClipId}`;
  return { op: 'clip.swap-asset', select, resolved: [select], args: { media }, expect: {
    [`${select}::`]: { state: 'present', value: structuredClone(sourceClip) },
    [selectedMediaRegistryExpectationPath(media.asset, occurrence.context.occurrenceId)]: existingRegistryEntry === undefined
      ? { state: 'absent' } : { state: 'present', value: structuredClone(existingRegistryEntry) },
  } };
}

/**
 * Resolve the current Runtime selection for a staged Gallery item. Providers
 * without this capability retain their legacy prepared-media behavior; a
 * present selector is authoritative and any malformed or mismatched response
 * is a refusal.
 */
export async function readGalleryGenerationSelection(
  provider: Pick<DataProvider, 'getProjectMediaSelection'>,
  request: { projectId: string; asset: string; generationId: string; variantId: string },
): Promise<SelectedProjectMediaIdentity | null | undefined> {
  if (!provider.getProjectMediaSelection) return undefined;
  let response: unknown;
  try {
    response = await provider.getProjectMediaSelection.call(provider, request);
  } catch {
    return null;
  }
  const identity = readSelectedProjectMediaIdentity(response);
  if (!identity || identity.asset !== request.asset
    || identity.generation_id !== request.generationId
    || identity.variant_id !== request.variantId
    || identity.object_id !== request.asset) {
    return null;
  }
  // Keep the exact helper response object. Do not reconstruct its identity.
  return identity;
}
