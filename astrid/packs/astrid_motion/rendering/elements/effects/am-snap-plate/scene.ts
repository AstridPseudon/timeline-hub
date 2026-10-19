import type {CSSProperties} from 'react';
import type {ComponentCapabilityContext, ComponentFrameSupport, PreparedComponentCapability, SceneCapableComponent} from '@banodoco/timeline-composition/evaluation';
import type {ElementComponent, ElementComponentProps} from '../../../../../rendering/shared/element_contracts';

// 0.0.9 exposes the renderer's optional selected entry. Its existing public
// effect-prop type keeps the still-pinned 0.0.8 hook source-compatible, without
// casting extra data. An omitted property is not an explicitly missing entry.
type SceneContext = ComponentCapabilityContext & Pick<ElementComponentProps, 'assetEntry'>;

export const withSceneCapability = <T extends ElementComponent>(component: T,
  prepareSceneCapability: (context: SceneContext) => PreparedComponentCapability,
): T & SceneCapableComponent => Object.assign(component, {prepareSceneCapability});

export const absentSupport = (): ComponentFrameSupport => ({
  presence: 'absent', opaqueSupport: 'none', bounds: {status: 'known', rect: {x: 0, y: 0, width: 0, height: 0}},
});

export const unknownSupport = (reason: string): ComponentFrameSupport => ({
  presence: 'unknown', opaqueSupport: 'unknown', bounds: {status: 'unknown', reason},
});

// Only solid hex colours are proven here. Other CSS (names, alpha, variables,
// gradients, invalid declarations) needs a real CSS context, never a guess.
export const fieldSupport = (background: CSSProperties['background'], width: number,
  height: number,
): ComponentFrameSupport => ({
  presence: 'present',
  opaqueSupport: typeof background === 'string' && /^#(?:[\da-f]{3}|[\da-f]{6}|[\da-f]{3}f|[\da-f]{6}ff)$/i.test(background)
    ? 'rect' : 'unknown',
  bounds: {status: 'known', rect: {x: 0, y: 0, width, height}},
});
