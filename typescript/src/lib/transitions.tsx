import type {TransitionRegistries} from '../registries';
import type {TransitionComponent, TransitionReference, TransitionReferenceObject} from '../effects-types';
import type {RuntimeTheme} from '../ThemeContext';
import {
  TRANSITION_DEFAULTS,
  TRANSITION_REGISTRY,
} from '../transitions.generated';
import type {Align, IncomingTransitionPolicy} from './transition-spans';

export type ResolvedTransition = {
  id: string;
  durationFrames: number;
  align: Align;
  params: Record<string, unknown>;
  incomingPolicy?: IncomingTransitionPolicy;
};

const isObjectReference = (value: unknown): value is TransitionReferenceObject => {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
};

const readAlign = (ref: TransitionReference | undefined): Align => {
  const align = isObjectReference(ref) ? (ref as {align?: unknown}).align : undefined;
  return align === 'start' || align === 'center' || align === 'end' ? align : 'end';
};

export const resolveTransitionReference = (
  ref: TransitionReference | undefined,
  theme: RuntimeTheme,
  fps: number,
  registries: TransitionRegistries = {},
): ResolvedTransition | null => {
  const transitionRegistry = registries.transitions ?? TRANSITION_REGISTRY;
  const transitionDefaults = registries.transitionDefaults ?? TRANSITION_DEFAULTS;
  if (ref === undefined) {
    return null;
  }
  const id = typeof ref === 'string' ? ref : isObjectReference(ref) ? (ref.id ?? ref.type ?? '') : '';
  if (!id || !Object.prototype.hasOwnProperty.call(transitionRegistry, id)) {
    throw new Error(`Unknown transition id '${id}'`);
  }
  const incomingPolicy = isObjectReference(ref) ? ref.incomingPolicy : undefined;
  if (incomingPolicy !== undefined && (incomingPolicy !== 'preroll-crossfade' || !['fade', 'cross-fade'].includes(id))) {
    throw new Error('Unsupported incoming transition policy or implementation');
  }
  const defaults = transitionDefaults[id] ?? {};
  const params = typeof ref === 'string'
    ? {...defaults}
    : {...defaults, ...(ref.params ?? {})};
  const rawDurationFrames = typeof ref === 'string' ? undefined : ref.durationFrames;
  const durationSeconds = typeof ref === 'string' ? undefined : (ref as {duration?: number}).duration;
  const durationFrames = rawDurationFrames
    ?? (typeof durationSeconds === 'number' ? Math.round(durationSeconds * fps) : undefined)
    ?? (typeof defaults.durationFrames === 'number' ? defaults.durationFrames : 12);
  const component = transitionRegistry[id] as TransitionComponent<Record<string, unknown>>;
  // The registry component is called to validate the reference; the visual
  // result is produced by transition-spans (dissolve or dip), not by this call.
  component({transitionId: id, params, theme, fps, durationFrames});
  return {id, durationFrames, align: readAlign(ref), params, ...(incomingPolicy ? {incomingPolicy} : {})};
};
