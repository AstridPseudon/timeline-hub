// Pure clip-look and animation-shape helpers. No React imports; Remotion is
// used only for its pure animation math so render and scene share the result.

import type {TimelineClip} from '../types';
import {getClipDurationInFrames, secondsToFrames} from './duration';
import {normalizeRenderCropValues} from './render-bounds';
import {interpolate, spring} from 'remotion';
import {animationProgress} from './animation-easing';

// Structurally identical to effects-types AnimationReferenceList (kept local so
// this module does not pull in React component trees).
export type AnimationReferenceItem = string | {
  id: string;
  durationFrames?: number;
  easing?: string;
  params?: Record<string, unknown>;
};
export type AnimationReferenceList = AnimationReferenceItem | AnimationReferenceItem[];

const getEffectValue = (
  effects: TimelineClip['effects'],
  name: 'fade_in' | 'fade_out',
): number | null => {
  if (!effects) {
    return null;
  }

  if (!Array.isArray(effects)) {
    const effectsObj = effects as Record<string, unknown>;
    return typeof effectsObj[name] === 'number' ? (effectsObj[name] as number) : null;
  }

  for (const effect of effects as Array<Record<string, unknown>>) {
    if (typeof effect[name] === 'number') {
      return (effect[name] as number) ?? null;
    }
  }

  return null;
};

// Same arithmetic as Remotion interpolate() with linear easing and both ends
// clamped, for a single ramp from x0 (output y0) to x1 (output y1).
const clampedRamp = (x: number, x0: number, x1: number, y0: number, y1: number): number => {
  if (x <= x0) {
    return y0;
  }
  if (x >= x1) {
    return y1;
  }
  const t = (x - x0) / (x1 - x0);
  return y0 + t * (y1 - y0);
};

// Fade multiplier from effects.fade_in / effects.fade_out (seconds). Math is the
// same as the former useFadeOpacity hook body. A fade whose frame count rounds
// to 0 is skipped (the old interpolate call would have had a degenerate range).
export const fadeMultiplier = (clip: TimelineClip, frame: number, fps: number): number => {
  const durationInFrames = getClipDurationInFrames(clip, fps);
  let opacity = 1;

  const fadeInSeconds = getEffectValue(clip.effects, 'fade_in');
  if (typeof fadeInSeconds === 'number' && Number.isFinite(fadeInSeconds) && fadeInSeconds > 0) {
    const fadeInFrames = secondsToFrames(fadeInSeconds, fps);
    if (fadeInFrames > 0) {
      opacity *= clampedRamp(frame, 0, fadeInFrames, 0, 1);
    }
  }

  const fadeOutSeconds = getEffectValue(clip.effects, 'fade_out');
  if (typeof fadeOutSeconds === 'number' && Number.isFinite(fadeOutSeconds) && fadeOutSeconds > 0) {
    const fadeOutFrames = secondsToFrames(fadeOutSeconds, fps);
    if (fadeOutFrames > 0) {
      opacity *= clampedRamp(frame, durationInFrames - fadeOutFrames, durationInFrames, 1, 0);
    }
  }

  return opacity;
};

/** Authored clip opacity times effects.fade_in/fade_out (seconds), clamped to [0, 1].
 * Takes the native TimelineClip duration: hold, or to - from, divided by speed,
 * rounded to frames at fps (minimum one frame). Pass the clip-local content
 * frame before media/component speed remapping, including transition handles.
 * Does not filter by the draw interval or include track/transition opacity,
 * intrinsic media alpha, animations, modifiers or occlusion. No scene is needed.
 */
export const clipOpacity = (clip: TimelineClip, frame: number, fps: number): number => {
  const value = fadeMultiplier(clip, frame, fps) * (clip.opacity ?? 1);
  return Math.min(1, Math.max(0, value));
};

const CROP_FIELDS = ['cropTop', 'cropBottom', 'cropLeft', 'cropRight'] as const;

const toPercent = (value: number): number => Number((value * 100).toFixed(4));

export const cropClipPath = (clip: TimelineClip): string | undefined => {
  if (CROP_FIELDS.every((field) => clip[field] === undefined)) {
    return undefined;
  }
  const crop = normalizeRenderCropValues({
    cropTop: clip.cropTop,
    cropBottom: clip.cropBottom,
    cropLeft: clip.cropLeft,
    cropRight: clip.cropRight,
  });
  return `inset(${toPercent(crop.cropTop)}% ${toPercent(crop.cropRight)}% ${toPercent(crop.cropBottom)}% ${toPercent(crop.cropLeft)}%)`;
};

const normalizeOneAnimationRef = (ref: unknown, fps: number): AnimationReferenceItem | undefined => {
  if (typeof ref === 'string') {
    return ref;
  }
  if (typeof ref !== 'object' || ref === null) {
    return undefined;
  }
  const record = ref as {id?: unknown; type?: unknown; duration?: unknown; params?: unknown; easing?: unknown};
  if (typeof record.id === 'string') {
    return ref as AnimationReferenceItem;
  }
  if (typeof record.type !== 'string') {
    return undefined;
  }
  if (record.easing !== undefined && typeof record.easing !== 'string') {
    throw new Error('Animation easing must be a declared curve name');
  }
  if (record.duration !== undefined && (typeof record.duration !== 'number' || !Number.isFinite(record.duration) || record.duration < 0)) {
    throw new Error('Animation duration must be a finite non-negative number of seconds');
  }
  const duration = typeof record.duration === 'number' && Number.isFinite(record.duration)
    ? record.duration
    : undefined;
  return {
    id: record.type,
    durationFrames: duration === undefined ? undefined : Math.round(duration * fps),
    ...(record.easing === undefined ? {} : {easing: record.easing}),
    params: record.params as Record<string, unknown> | undefined,
  };
};

// Accepts the timeline schema's {type, duration (seconds), params?} shape and maps
// it to the {id, durationFrames} shape composeAnimations expects. Strings and
// {id} references pass through unchanged.
export const normalizeAnimationRefs = (
  refs: unknown,
  fps: number,
): AnimationReferenceList | undefined => {
  if (refs === undefined) {
    return undefined;
  }
  if (Array.isArray(refs)) {
    return refs
      .map((ref) => normalizeOneAnimationRef(ref, fps))
      .filter((ref): ref is AnimationReferenceItem => ref !== undefined);
  }
  return normalizeOneAnimationRef(refs, fps);
};

// Frame inside an entrance/exit animation window, or null when outside it.
export const animationElapsed = (
  phase: 'entrance' | 'exit',
  frame: number,
  clipFrames: number,
  durationFrames: number,
): number | null => {
  if (phase === 'entrance') {
    return frame < durationFrames ? frame : null;
  }
  const exitStart = clipFrames - durationFrames;
  return frame >= exitStart ? frame - exitStart : null;
};

// Sanitises clip.speed the same way getSanitizedPlaybackRate does: a finite
// number greater than 0, otherwise 1.
export const clipSpeed = (speed: unknown): number =>
  typeof speed === 'number' && Number.isFinite(speed) && speed > 0 ? speed : 1;

// Element clips remap time by speed: the element sees floor(local * speed) as its
// frame, so speed 2 runs its animation twice as fast. Identity when speed is 1.
export const remappedFrame = (frame: number, speed: unknown): number => {
  const s = clipSpeed(speed);
  return s === 1 ? frame : Math.floor(frame * s);
};

export type BuiltinClipLookStyle = {opacity: number; transform: string; translateY?: number; scale?: number};

/** Shared by the rendered wrapper and the scene geometry query. */
export const builtinClipLookStyle = (id: 'fade-up' | 'scale-in', elapsedFrames: number,
  durationFrames: number, fps: number, easing?: unknown, suppliedProgress?: number): BuiltinClipLookStyle => {
  const explicitProgress = suppliedProgress ?? animationProgress(elapsedFrames, durationFrames, easing);
  const progress = explicitProgress ?? spring({frame: elapsedFrames, fps, from: 0, to: 1,
    durationInFrames: durationFrames, config: {damping: 14, stiffness: 110}});
  if (id === 'fade-up') {
    const translateY = explicitProgress === undefined ? interpolate(progress, [0, 1], [40, 0]) : 40 * (1 - progress);
    return {opacity: progress, translateY, transform: `translateY(${translateY}px)`};
  }
  const scale = explicitProgress === undefined ? interpolate(progress, [0, 1], [0.85, 1]) : 0.85 + 0.15 * progress;
  return {opacity: progress, scale, transform: `scale(${scale})`};
};
