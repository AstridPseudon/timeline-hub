// Pure animation math shared by rendered clip wrappers and scene evaluation.
// This keeps the evaluator independent of React and Remotion runtime peers.

import {animationProgress} from './animation-easing';

type SpringState = {
  toValue: number;
  lastTimestamp: number;
  current: number;
  velocity: number;
  prevPosition: number;
};

const DEFAULT_SPRING = {damping: 14, mass: 1, stiffness: 110};
const springDurationCache = new Map<number, number>();

const advanceSpring = (animation: SpringState, now: number): SpringState => {
  const deltaTime = Math.min(now - animation.lastTimestamp, 64);
  const c2 = DEFAULT_SPRING.damping;
  const m = DEFAULT_SPRING.mass;
  const k = DEFAULT_SPRING.stiffness;
  const v0 = -animation.velocity;
  const x0 = animation.toValue - animation.current;
  const zeta = c2 / (2 * Math.sqrt(k * m));
  const omega0 = Math.sqrt(k / m);
  const omega1 = omega0 * Math.sqrt(1 - zeta ** 2);
  const t = deltaTime / 1000;
  const sin1 = Math.sin(omega1 * t);
  const cos1 = Math.cos(omega1 * t);
  const underDampedEnvelope = Math.exp(-zeta * omega0 * t);
  const underDampedFrag1 = underDampedEnvelope
    * (sin1 * ((v0 + zeta * omega0 * x0) / omega1) + x0 * cos1);
  const underDampedPosition = animation.toValue - underDampedFrag1;
  const underDampedVelocity = zeta * omega0 * underDampedFrag1
    - underDampedEnvelope * (cos1 * (v0 + zeta * omega0 * x0) - omega1 * x0 * sin1);
  const criticallyDampedEnvelope = Math.exp(-omega0 * t);
  const criticallyDampedPosition = animation.toValue
    - criticallyDampedEnvelope * (x0 + (v0 + omega0 * x0) * t);
  const criticallyDampedVelocity = criticallyDampedEnvelope
    * (v0 * (t * omega0 - 1) + t * x0 * omega0 * omega0);
  return {
    toValue: animation.toValue,
    prevPosition: animation.current,
    lastTimestamp: now,
    current: zeta < 1 ? underDampedPosition : criticallyDampedPosition,
    velocity: zeta < 1 ? underDampedVelocity : criticallyDampedVelocity,
  };
};

const springCalculation = (frame: number, fps: number): SpringState => {
  let animation: SpringState = {lastTimestamp: 0, current: 0, toValue: 1, velocity: 0, prevPosition: 0};
  const frameClamped = Math.max(0, frame);
  const unevenRest = frameClamped % 1;
  for (let f = 0; f <= Math.floor(frameClamped); f++) {
    if (f === Math.floor(frameClamped)) f += unevenRest;
    animation = advanceSpring(animation, f / fps * 1000);
  }
  return animation;
};

const measureSpring = (fps: number): number => {
  const cached = springDurationCache.get(fps);
  if (cached !== undefined) return cached;
  const threshold = .005;
  let frame = 0;
  let animation = springCalculation(frame, fps);
  while (Math.abs(animation.current - animation.toValue) >= threshold) {
    frame++;
    animation = springCalculation(frame, fps);
  }
  let finishedFrame = frame;
  for (let i = 0; i < 20; i++) {
    frame++;
    animation = springCalculation(frame, fps);
    if (Math.abs(animation.current - animation.toValue) >= threshold) {
      i = 0;
      finishedFrame = frame + 1;
    }
  }
  springDurationCache.set(fps, finishedFrame);
  return finishedFrame;
};

const springProgress = (frame: number, fps: number, durationFrames: number): number => {
  if (!Number.isFinite(frame) || !Number.isFinite(durationFrames) || durationFrames <= 0) {
    throw new TypeError('Animation frame and positive duration must be finite');
  }
  if (!Number.isFinite(fps) || fps <= 0) throw new TypeError('Animation fps must be positive and finite');
  if (frame > durationFrames) return 1;
  const naturalDuration = measureSpring(fps);
  return springCalculation(frame / (durationFrames / naturalDuration), fps).current;
};

const linearInterpolate = (value: number, outputStart: number, outputEnd: number): number =>
  outputStart + value * (outputEnd - outputStart);

export type BuiltinClipLookStyle = {opacity: number; transform: string; translateY?: number; scale?: number};

/** Existing fade-up/scale-in calculation, shared by renderer and evaluator. */
export const builtinClipLookStyle = (id: 'fade-up' | 'scale-in', elapsedFrames: number,
  durationFrames: number, fps: number, easing?: unknown, suppliedProgress?: number): BuiltinClipLookStyle => {
  const explicitProgress = suppliedProgress ?? animationProgress(elapsedFrames, durationFrames, easing);
  const progress = explicitProgress ?? springProgress(elapsedFrames, fps, durationFrames);
  if (id === 'fade-up') {
    const translateY = explicitProgress === undefined ? linearInterpolate(progress, 40, 0) : 40 * (1 - progress);
    return {opacity: progress, translateY, transform: `translateY(${translateY}px)`};
  }
  const scale = explicitProgress === undefined ? linearInterpolate(progress, 0.85, 1) : 0.85 + 0.15 * progress;
  return {opacity: progress, scale, transform: `scale(${scale})`};
};
