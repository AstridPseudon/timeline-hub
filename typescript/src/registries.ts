import {EFFECT_REGISTRY, CLIP_TYPE_ALIASES} from './effects.generated';
import {ANIMATION_REGISTRY, ANIMATION_DEFAULTS, ANIMATION_META} from './animations.generated';
import {TRANSITION_REGISTRY, TRANSITION_DEFAULTS, TRANSITION_META} from './transitions.generated';
import {THEME_PACKAGE_REGISTRY} from './registry.generated';
import type {AnimationComponent, AnimationMeta, EffectComponent, TransitionComponent} from './effects-types';
import type {SceneCapableComponent} from './scene-capabilities';
import type {RuntimeTheme} from './ThemeContext';

export type AnimationRegistries = {
  animations?: Readonly<Record<string, AnimationComponent>>;
  animationDefaults?: Readonly<Record<string, Record<string, unknown>>>;
  animationMeta?: Readonly<Record<string, AnimationMeta>>;
};

export type TransitionRegistries = {
  transitions?: Readonly<Record<string, TransitionComponent>>;
  transitionDefaults?: Readonly<Record<string, Record<string, unknown>>>;
  transitionMeta?: Readonly<Record<string, Record<string, unknown>>>;
};

// Each supplied member is the host's complete resolved map for that category.
// Omitted members use the bundled defaults; no installed file is regenerated.
export type CompositionRegistries = AnimationRegistries & TransitionRegistries & {
  effects?: Readonly<Record<string, EffectComponent<never> & SceneCapableComponent>>;
  clipTypeAliases?: Readonly<Record<string, string>>;
};
export type ResolvedCompositionRegistries = Required<CompositionRegistries>;

export const resolveElementRegistries = (
  theme: Pick<RuntimeTheme, 'id'>,
  registries: CompositionRegistries = {},
): ResolvedCompositionRegistries => ({
  effects: registries.effects ?? {
    ...EFFECT_REGISTRY,
    ...Object.fromEntries(Object.entries(THEME_PACKAGE_REGISTRY)
      .filter(([, entry]) => entry.themeId === theme.id)
      .map(([id, entry]) => [id, entry.component])),
  },
  clipTypeAliases: registries.clipTypeAliases ?? CLIP_TYPE_ALIASES,
  animations: registries.animations ?? ANIMATION_REGISTRY,
  animationDefaults: registries.animationDefaults ?? ANIMATION_DEFAULTS,
  animationMeta: registries.animationMeta ?? ANIMATION_META,
  transitions: registries.transitions ?? TRANSITION_REGISTRY,
  transitionDefaults: registries.transitionDefaults ?? TRANSITION_DEFAULTS,
  transitionMeta: registries.transitionMeta ?? TRANSITION_META,
});

export {ElementRegistryProvider, useElementRegistries} from './RegistryContext';
