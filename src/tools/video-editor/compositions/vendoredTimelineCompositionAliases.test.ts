import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { EFFECT_REGISTRY, CLIP_TYPE_ALIASES } from '@banodoco/timeline-composition/effects.generated';
import { ANIMATION_REGISTRY, ANIMATION_DEFAULTS, ANIMATION_META } from '@banodoco/timeline-composition/animations.generated';
import { TRANSITION_REGISTRY, TRANSITION_DEFAULTS } from '@banodoco/timeline-composition/transitions.generated';
import { THEME_PACKAGE_REGISTRY } from '@banodoco/timeline-composition/registry.generated';
import { resolveElementRegistries, type CompositionRegistries } from '@banodoco/timeline-composition/registries';
import { resolveAnimationReferences } from '@banodoco/timeline-composition/theme-api';

const packageRoot = path.join(process.cwd(), 'node_modules/@banodoco/timeline-composition');
const defaults = resolveElementRegistries({ id: '2rp' });
const REGISTRY_FAMILIES = [
  { family: 'effects', registry: EFFECT_REGISTRY, ids: ['text-card'] },
  { family: 'animations', registry: ANIMATION_REGISTRY, ids: ['fade', 'fade-up', 'scale-in', 'slide-left', 'slide-up', 'type-on'] },
  { family: 'transitions', registry: TRANSITION_REGISTRY, ids: ['cross-fade', 'fade'] },
] as const;

describe('public timeline-composition defaults', () => {
  it('loads the declaration contract from the stable public package surface', () => {
    const manifest = JSON.parse(readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));
    for (const entry of Object.values(manifest.exports) as ({ types: string; import: string } | string)[]) {
      if (typeof entry === 'string') continue;
      expect(existsSync(path.join(packageRoot, entry.types))).toBe(true);
      expect(existsSync(path.join(packageRoot, entry.import))).toBe(true);
    }
    const themeApi = readFileSync(path.join(packageRoot, manifest.exports['./theme-api'].types), 'utf8');
    expect(themeApi).toContain('EffectProps');
    expect(themeApi).toContain('CompositionRegistries');
  });

  it.each(REGISTRY_FAMILIES)(
    'resolves every default $family component through the public registry',
    ({ family, registry, ids }) => {
      expect(Object.keys(registry).sort()).toEqual([...ids].sort());
      for (const [id, component] of Object.entries(registry)) {
        expect(typeof component).toBe('function');
        expect(defaults[family][id]).toBe(component);
      }
    },
  );

  it('resolves all thirteen defaults, their metadata and the bundled theme identity', () => {
    expect(Object.keys(defaults.effects).sort()).toEqual(['art-card', 'cta-card', 'resource-card', 'section-hook', 'text-card']);
    expect(Object.keys(defaults.effects).length + Object.keys(defaults.animations).length + Object.keys(defaults.transitions).length).toBe(13);
    expect(defaults.clipTypeAliases).toEqual(CLIP_TYPE_ALIASES);
    expect(defaults.clipTypeAliases.text).toBe('text-card');
    expect(defaults.animationDefaults).toEqual(ANIMATION_DEFAULTS);
    expect(defaults.animationMeta).toEqual(ANIMATION_META);
    expect(defaults.transitionDefaults).toEqual(TRANSITION_DEFAULTS);
    for (const id of ['art-card', 'cta-card', 'resource-card', 'section-hook']) {
      expect(defaults.effects[id]).toBe(THEME_PACKAGE_REGISTRY[id].component);
      expect(THEME_PACKAGE_REGISTRY[id].source).toBe('bundled:2rp@0.1.0');
    }
    expect(resolveAnimationReferences('fade', 'exit')[0].durationFrames).toBe(12);
  });

  it('keeps host elements and animation defaults scoped to their supplied registries', () => {
    const custom = () => null;
    const registries: CompositionRegistries = {
      effects: { custom },
      clipTypeAliases: { title: 'custom' },
      animations: { custom },
      animationDefaults: { custom: { durationFrames: 3 } },
      animationMeta: { custom: { kind: 'wrapper', phase: 'entrance' } },
    };
    const selected = resolveElementRegistries({ id: '2rp' }, registries);
    expect(selected.effects.custom).toBe(custom);
    expect(selected.clipTypeAliases.title).toBe('custom');
    expect(resolveAnimationReferences('custom', 'entrance', registries)[0].durationFrames).toBe(3);
    expect(resolveElementRegistries({ id: '2rp' }).effects['text-card']).toBe(EFFECT_REGISTRY['text-card']);
    expect(resolveAnimationReferences('fade', 'exit')[0].durationFrames).toBe(12);
  });
});
