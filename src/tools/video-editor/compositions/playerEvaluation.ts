import { compileCanonicalTransitions, prepareCompositionScene, toRuntimeTheme } from '@banodoco/timeline-composition';
import {
  declareAppTransition,
  prepareScene,
  querySceneFrame,
  type DrawPlan,
  type CompiledCanonicalTransitions,
  type TransitionSpec,
} from '@banodoco/timeline-composition/evaluation';
import { getClipTimelineDuration, getSanitizedPlaybackRate } from '../lib/config-utils.ts';
import { resolveTimelineRenderTheme } from './installed-themes.ts';
import { projectOutputTimelineConfig } from '../data/timelineOutputProjection.ts';
import { materializeResolvedSequenceConfig } from '../sequences/materialize.ts';
import { getVisualTracks } from '../lib/editor-utils.ts';
import type { ResolvedTimelineConfig, ResolvedTimelineClip, TrackDefinition } from '../types/index.ts';

type EvaluationClip = Parameters<typeof prepareScene>[0][number]['clips'][number];

/** Adapt the host's sanitized source clock without changing the authored clip. */
export const playerEvaluationClip = (clip: ResolvedTimelineClip): EvaluationClip => ({
  ...clip,
  speed: getSanitizedPlaybackRate(clip.speed),
  hold: getClipTimelineDuration(clip) * getSanitizedPlaybackRate(clip.speed),
});

/** Evaluate the native opacity surface, without making claims about media alpha. */
export const preparePlayerClipOpacity = (clip: ResolvedTimelineClip, fps: number) => {
  const surface = 'app-native-opacity';
  const scene = prepareScene([{ track: { id: clip.track, kind: 'visual', label: surface }, transitions: [], clips: [{
    id: clip.id, track: clip.track, at: 0, clipType: surface,
    hold: playerEvaluationClip(clip).hold, speed: getSanitizedPlaybackRate(clip.speed),
    opacity: clip.opacity, effects: clip.effects,
  }] }], { assets: {} }, fps, 1, 1, { capabilities: { components: {
    [clip.id]: { identity: surface, frame: () => ({ presence: 'present', opaqueSupport: 'none',
      bounds: { status: 'known', rect: { x: 0, y: 0, width: 1, height: 1 } } }) },
  } } });
  // The surface follows the caller's content clock even through native pre-roll
  // and host overlap frames. Keep the authored duration on the clip for fades.
  const plan = scene.tracks[0].prepared.plans[0];
  scene.tracks[0].prepared = { plans: [{ ...plan,
    ownDuration: Number.MAX_SAFE_INTEGER, drawDuration: Number.MAX_SAFE_INTEGER,
  }] };
  return (frame: number): number => querySceneFrame(scene, Math.max(0, frame)).layers[0].opacity!;
};

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

/** Called only after the preview owner has selected an actual canonical projection. */
export const compilePlayerTransitions = (config: ResolvedTimelineConfig): CompiledCanonicalTransitions | undefined => {
  const output = materializeResolvedSequenceConfig(projectOutputTimelineConfig(config).config);
  const tracks = getVisualTracks(output).map(track => ({
    track,
    clips: output.clips.filter(clip => clip.track === track.id),
  })).filter(({ clips }) => clips.every(clip => isNativeMedia(clip)
    && clip.enabled !== false && clip.active !== false && clip.disabled !== true
    && clip.hidden !== true && clip.deleted !== true
    && (!clip.transition || (!clip.elementRef
      && ['fade', 'crossfade', 'cross-fade'].includes(clip.transition.type)
      && Object.entries(clip.transition.params ?? {}).every(([key, value]) => key === 'easing' && value === 'linear')))));
  try {
    return compileCanonicalTransitions(tracks.map(({ track, clips }) => ({
      track, clips: clips.map(playerEvaluationClip),
    })), output.output.fps, toRuntimeTheme(resolveTimelineRenderTheme(output)));
  } catch {
    // Invalid or unsupported declarations keep the existing diagnostic/host path.
    return undefined;
  }
};

/** Use the canonical vector when present; native callers retain the reviewed adapter. */
export const preparePlayerTrack = (
  track: TrackDefinition,
  clips: readonly ResolvedTimelineClip[],
  fps: number,
  width: number,
  height: number,
  usesNativeMedia: (clip: ResolvedTimelineClip) => boolean = () => true,
  compiledTransitions?: CompiledCanonicalTransitions,
) => {
  const sorted = [...clips].sort((left, right) => left.at - right.at);
  const evaluatedMedia = (clip: ResolvedTimelineClip) => isNativeMedia(clip) && usesNativeMedia(clip);
  if (compiledTransitions?.tracks.some(input => input.trackId === track.id) && sorted.every(evaluatedMedia)) {
    const assets = { assets: Object.fromEntries(sorted.flatMap(clip => clip.asset && clip.assetEntry
      ? [[clip.asset, { ...clip.assetEntry, file: clip.assetEntry.src }]] : [])) };
    const scene = prepareCompositionScene([{ track, clips: sorted.map(playerEvaluationClip) }], assets,
      fps, toRuntimeTheme(resolveTimelineRenderTheme({})), width, height,
      undefined, undefined, undefined, undefined, undefined, undefined, compiledTransitions);
    return { clips: sorted, scene, plans: new Map(sorted.map((clip, index) =>
      [clip.id, scene.tracks[0].prepared.plans[index]] as const)) };
  }
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
