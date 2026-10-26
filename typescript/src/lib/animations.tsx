// Sprint 5: physically moved here from tools/remotion/src/lib/animations.tsx.
// The theme-api re-export now points at this in-package module.

import type {ReactNode} from 'react';
import type {AnimationRegistries} from '../registries';
import {
  ANIMATION_DEFAULTS,
  ANIMATION_META,
  ANIMATION_REGISTRY,
} from '../animations.generated';
import type {
  AnimationComponent,
  AnimationPhase,
  AnimationReference,
  AnimationReferenceList,
  HookAnimationComponent,
  HookAnimationResult,
  WrapperAnimationComponent,
} from '../effects-types';
import type {RuntimeTheme} from '../ThemeContext';
import type {TimelineClip} from '../types';
import {animationEasingParams, animationProgress, normalizeAnimationEasing} from './animation-easing';

export type NormalizedAnimationReference = {
  id: string;
  durationFrames?: number;
  easing?: string;
  params: Record<string, unknown>;
};

export type ResolvedAnimation = NormalizedAnimationReference & {
  component: AnimationComponent;
  kind: 'wrapper' | 'hook';
  phase: AnimationPhase;
  durationFrames: number;
};

export type ComposeAnimationsInput = {
  clip: TimelineClip;
  refs: AnimationReferenceList | undefined;
  phase: AnimationPhase;
  content: ReactNode;
  text?: string;
  theme: RuntimeTheme;
  fps: number;
  elapsedFrames: number;
  registries?: AnimationRegistries;
};

const isObjectReference = (value: unknown): value is Exclude<AnimationReference, string> => {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
};

export const normalizeAnimationReferences = (
  refs: AnimationReferenceList | undefined,
  registries: AnimationRegistries = {},
): NormalizedAnimationReference[] => {
  const animationRegistry = registries.animations ?? ANIMATION_REGISTRY;
  const hasAnimationId = (id: string) => Object.prototype.hasOwnProperty.call(animationRegistry, id);
  if (refs === undefined) {
    return [];
  }
  const refList = Array.isArray(refs) ? refs : [refs];
  return refList.map((ref) => {
    if (typeof ref === 'string') {
      if (!hasAnimationId(ref)) {
        throw new Error(`Unknown animation id '${ref}'`);
      }
      return {id: ref, params: {}};
    }
    if (!isObjectReference(ref) || typeof ref.id !== 'string' || ref.id.length === 0) {
      throw new Error('Animation reference objects must include a non-empty string id');
    }
    if (!hasAnimationId(ref.id)) {
      throw new Error(`Unknown animation id '${ref.id}'`);
    }
    if (ref.easing !== undefined && typeof ref.easing !== 'string') throw new Error('Animation easing must be a declared curve name');
    const params = animationEasingParams({}, ref.params && typeof ref.params === 'object' ? {...ref.params} : {}, ref.easing);
    return {
      id: ref.id,
      durationFrames: ref.durationFrames,
      easing: typeof ref.easing === 'string' ? normalizeAnimationEasing(ref.easing) : undefined,
      params,
    };
  });
};

export const resolveAnimationReferences = (
  refs: AnimationReferenceList | undefined,
  phase: AnimationPhase,
  registries: AnimationRegistries = {},
): ResolvedAnimation[] => {
  const animationRegistry = registries.animations ?? ANIMATION_REGISTRY;
  const animationDefaults = registries.animationDefaults ?? ANIMATION_DEFAULTS;
  const animationMeta = registries.animationMeta ?? ANIMATION_META;
  return normalizeAnimationReferences(refs, registries).map((ref) => {
    const meta = animationMeta[ref.id];
    if (!meta) {
      throw new Error(`Unknown animation id '${ref.id}'`);
    }
    const metaPhase = meta.phase ?? 'any';
    const phaseMatches = metaPhase === 'any'
      || metaPhase === phase
      || (Array.isArray(metaPhase) && metaPhase.includes(phase));
    if (!phaseMatches) {
      throw new Error(`Animation '${ref.id}' is phase '${meta.phase}', not '${phase}'`);
    }

    const defaults = animationDefaults[ref.id] ?? {};
    const defaultDuration = typeof defaults.durationFrames === 'number'
      ? defaults.durationFrames
      : meta.defaultDurationFrames;
    const durationFrames = ref.durationFrames ?? defaultDuration;
    if (typeof durationFrames !== 'number' || !Number.isFinite(durationFrames) || durationFrames < 0) {
      throw new Error(`Animation '${ref.id}' must resolve to a non-negative durationFrames value`);
    }

    const params = animationEasingParams(defaults, ref.params, ref.easing);
    const easing = ref.easing ?? (typeof ref.params.easing === 'string' ? normalizeAnimationEasing(ref.params.easing) : undefined);
    if (easing !== undefined && meta.supportsEasing !== true) {
      throw new Error(`Animation '${ref.id}' cannot consume explicit easing progress`);
    }
    return {
      ...ref,
      easing,
      params,
      component: animationRegistry[ref.id] as AnimationComponent,
      kind: meta.kind,
      phase,
      durationFrames,
    };
  });
};

const isHookResultObject = (value: unknown): value is HookAnimationResult => {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
};

export const composeAnimations = ({
  clip,
  refs,
  phase,
  content,
  text,
  theme,
  fps,
  elapsedFrames,
  registries,
}: ComposeAnimationsInput): ReactNode => {
  const resolved = resolveAnimationReferences(refs, phase, registries);
  const hookAnimations = resolved.filter((animation) => animation.kind === 'hook');
  const wrapperAnimations = resolved.filter((animation) => animation.kind === 'wrapper');

  let nextContent = content;
  let nextText = text;
  let nextParams: Record<string, unknown> = {};

  for (const animation of hookAnimations) {
    const progress = animationProgress(elapsedFrames, animation.durationFrames, animation.easing);
    const HookComponent = animation.component as HookAnimationComponent<Record<string, unknown>>;
    const result = HookComponent({
      clip,
      params: animation.params,
      theme,
      fps,
      phase,
      durationFrames: animation.durationFrames,
      elapsedFrames,
      progress,
      easing: animation.easing,
      animationId: animation.id,
      content: nextContent,
      text: nextText,
    });
    if (isHookResultObject(result)) {
      nextContent = result.content ?? nextContent;
      nextText = result.text ?? nextText;
      nextParams = {...nextParams, ...(result.params ?? {})};
    } else {
      nextContent = result;
    }
  }

  return wrapperAnimations.reduceRight((children, animation) => {
    const progress = animationProgress(elapsedFrames, animation.durationFrames, animation.easing);
    const WrapperComponent = animation.component as WrapperAnimationComponent<Record<string, unknown>>;
    return (
      <WrapperComponent
        clip={clip}
        params={{...animation.params, ...nextParams}}
        theme={theme}
        fps={fps}
        phase={phase}
        durationFrames={animation.durationFrames}
        elapsedFrames={elapsedFrames}
        progress={progress}
        easing={animation.easing}
        animationId={animation.id}
      >
        {children}
      </WrapperComponent>
    );
  }, nextContent);
};
