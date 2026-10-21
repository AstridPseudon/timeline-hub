import { ASTRID_EFFECT_CATALOG } from '@/tools/video-editor/runtime/astrid-element-catalog.ts';
import type { ResolvedTimelineClip } from '@/tools/video-editor/types/index.ts';

const finite = (value: unknown): value is number => typeof value === 'number' && Number.isFinite(value);

const ELEMENT_DEFAULT_VOLUME = new Map<string, number>(
  ASTRID_EFFECT_CATALOG.flatMap((element) => (
    finite(element.defaults.volume) ? [[element.id, element.defaults.volume] as [string, number]] : []
  )),
);

/**
 * The one definition of a clip's sound level, shared by everything in the
 * editor that plays, draws, analyses or displays it (and mirrored by the
 * render, e.g. Astrid's am-footage `footageVolume`):
 *   1. the explicit `clip.volume` (finite, >= 0);
 *   2. else the element's declared default (its manifest `defaults.volume`,
 *      or the legacy `volume` param that carries it);
 *   3. else 1, a plain media clip at full level.
 */
export const getEffectiveClipVolume = (
  clip: Pick<ResolvedTimelineClip, 'volume' | 'elementRef' | 'clipType' | 'params'>,
): number => {
  if (finite(clip.volume) && clip.volume >= 0) return clip.volume;
  const paramVolume = clip.params?.volume;
  if (finite(paramVolume)) return paramVolume;
  const id = clip.elementRef?.id ?? clip.clipType;
  return (id !== undefined ? ELEMENT_DEFAULT_VOLUME.get(id) : undefined) ?? 1;
};
