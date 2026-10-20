import { object } from '../../commands/clipMovePrimitives.ts';

type SplitClipShape = Record<string, unknown>;

const UNSUPPORTED_CLIP_KEYS = [
  'clip_type', 'asset_id', 'media_id', 'object_id', 'at_ms', 'from_ms', 'to_ms',
  'duration', 'duration_ms', 'time_map', 'timeMap', 'clips', 'children', 'transition', 'effects',
  'animation', 'animations', 'keyframes', 'enter', 'exit', 'continuous',
] as const;
const UNSUPPORTED_PARAM_KEYS = [
  'keyframes', 'animation', 'animations', 'effects', 'fade_in', 'fade_out',
  'volume_curve', 'fadeIn', 'fadeOut', 'fadeInCurve', 'fadeOutCurve',
] as const;
const RELATIONAL_KEYS = [
  'on', 'until', 'until_film_end', 'cut', 'sequence', 'sequence_index', 'sequence_fit',
  'orphan', 'formulas', 'anchor', 'standin', 'standin_intent', 'words', 'beats',
] as const;

function hasValue(row: SplitClipShape, keys: readonly string[]): boolean {
  return keys.some((key) => row[key] != null);
}

function hasUnsupportedTimingOrRelation(row: SplitClipShape): boolean {
  if (hasValue(row, UNSUPPORTED_CLIP_KEYS)) return true;

  const params = object(row.params) ? row.params : undefined;
  if (params && hasValue(params, UNSUPPORTED_PARAM_KEYS)) return true;

  const app = object(row.app) ? row.app : undefined;
  for (const container of [row, app, object(app?.astrid) ? app.astrid : undefined]) {
    if (!container) continue;
    if (container.fixed_start != null && container.fixed_start !== true) return true;
    if (container.for != null && typeof container.for !== 'number') return true;
    if (hasValue(container, RELATIONAL_KEYS)) return true;
  }
  return false;
}

function mediaKind(clip: SplitClipShape): string | undefined {
  const source = object(clip.assetEntry) ? clip.assetEntry : undefined;
  if (typeof source?.type !== 'string') return undefined;
  return source.type.trim().toLowerCase().split(';', 1)[0].split('/', 1)[0].split('-', 1)[0];
}

/**
 * Select the old single-split ingress before native capture for an authored
 * shape that the current native contract does not cover. A missing or
 * ambiguous raw target deliberately returns false so native ownership checks
 * remain authoritative instead of turning into a legacy write.
 */
export function shouldUseLegacySingleSplit(
  resolvedClip: SplitClipShape,
  rawClips: readonly SplitClipShape[],
): boolean {
  const rawMatches = rawClips.filter((clip) => clip.id === resolvedClip.id);
  if (rawMatches.length !== 1) return false;

  const rawTarget = rawMatches[0];
  if (resolvedClip.clipType !== 'media' || typeof resolvedClip.asset !== 'string'
    || rawTarget.clipType !== 'media' || typeof rawTarget.asset !== 'string') {
    return true;
  }
  if (hasUnsupportedTimingOrRelation(rawTarget)) return true;
  if (rawClips.some((clip) => clip.transition != null)) return true;

  const kind = mediaKind(resolvedClip);
  return (!kind || !['image', 'video', 'audio'].includes(kind))
    || (rawTarget.from == null && rawTarget.to == null && kind !== 'image');
}
