import {
  declareAppTransition,
  prepareScene,
  type DrawPlan,
  type TransitionSpec,
} from '@banodoco/timeline-composition/evaluation';
import { getClipTimelineDuration, getSanitizedPlaybackRate } from '../lib/config-utils.ts';
import type { ResolvedTimelineClip, TrackDefinition } from '../types/index.ts';

type EvaluationClip = Parameters<typeof prepareScene>[0][number]['clips'][number];

/** Adapt the host's sanitized source clock without changing the authored clip. */
export const playerEvaluationClip = (clip: ResolvedTimelineClip): EvaluationClip => ({
  ...clip,
  speed: getSanitizedPlaybackRate(clip.speed),
  hold: getClipTimelineDuration(clip) * getSanitizedPlaybackRate(clip.speed),
});

const isNativeMedia = (clip: ResolvedTimelineClip): boolean => (
  (!clip.elementRef || clip.elementRef.kind === 'transition')
  && (!clip.clipType || ['media', 'image', 'hold'].includes(clip.clipType))
);

// Only a plain image has a known silent subtree. Freezing video or injected
// effects would also freeze their sound; those boundaries retain the host path.
const isSilentImage = (clip: ResolvedTimelineClip): boolean => (
  isNativeMedia(clip) && !!clip.assetEntry?.type?.startsWith('image')
  && !clip.entrance && !clip.exit && !clip.continuous
  && (!clip.effects || Object.keys(clip.effects).length === 0)
);

/** App transitions belong to the incoming clip; Composition owns the outgoing boundary. */
export const preparePlayerTrack = (
  track: TrackDefinition,
  clips: readonly ResolvedTimelineClip[],
  fps: number,
  width: number,
  height: number,
  usesNativeMedia: (clip: ResolvedTimelineClip) => boolean = () => true,
) => {
  const sorted = [...clips].sort((left, right) => left.at - right.at);
  const evaluatedMedia = (clip: ResolvedTimelineClip) => isNativeMedia(clip) && usesNativeMedia(clip);
  const transitions: (TransitionSpec | null)[] = sorted.slice(1).map(() => null);
  const hostTiming = new Set<number>();
  sorted.forEach((incoming, index) => {
    if (!incoming.transition) return;
    const outgoing = sorted[index - 1];
    const { type, duration } = incoming.transition;
    if (outgoing && evaluatedMedia(outgoing) && evaluatedMedia(incoming)
      && isSilentImage(outgoing) && isSilentImage(incoming)
      // App fade is incoming-only; the public DIP policy changes its picture.
      && ['crossfade', 'cross-fade'].includes(type)
      && Number.isFinite(duration) && duration > 0 && Math.round(duration * fps) > 0) {
      transitions[index - 1] = declareAppTransition(track.id, outgoing.id,
        { ...incoming.transition, params: incoming.transition.params ?? undefined },
        fps, 'timeline-composition').spec;
    } else {
      hostTiming.add(index);
      if (outgoing) hostTiming.add(index - 1);
    }
  });
  const assets = { assets: Object.fromEntries(sorted.flatMap(clip => clip.asset && clip.assetEntry
    ? [[clip.asset, { ...clip.assetEntry, file: clip.assetEntry.src }]] : [])) };
  const inputs = [{ track, clips: sorted.map(playerEvaluationClip), transitions }];
  // Undeclared component internals remain unknown. Scene visibility is never
  // used to cull host components or their diagnostic placeholders.
  const options = { elements: new Set(sorted.filter(clip => !evaluatedMedia(clip))
    .map(clip => clip.clipType ?? 'media')) };
  let scene = prepareScene(inputs, assets, fps, width, height, options);
  scene.tracks[0].prepared.plans.forEach((plan, index) => {
    if (index > 0 && transitions[index - 1] && !plan.fadeIn) {
      // Gaps, overlaps and oversized transitions have an existing host contract.
      hostTiming.add(index - 1);
      hostTiming.add(index);
    }
  });
  // A shared boundary cannot partly execute across a host-timed endpoint.
  let changed = true;
  while (changed) {
    changed = false;
    transitions.forEach((transition, index) => {
      if (transition && (hostTiming.has(index) || hostTiming.has(index + 1))) {
        transitions[index] = null;
        hostTiming.add(index);
        hostTiming.add(index + 1);
        changed = true;
      }
    });
  }
  if (hostTiming.size > 0) scene = prepareScene(inputs, assets, fps, width, height, options);
  const plans = new Map<string, DrawPlan>();
  sorted.forEach((clip, index) => {
    if (evaluatedMedia(clip) && !hostTiming.has(index)) {
      plans.set(clip.id, scene.tracks[0].prepared.plans[index]);
    }
  });
  return { clips: sorted, scene, plans };
};
