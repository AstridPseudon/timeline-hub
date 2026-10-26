import {createElement, type ReactNode} from 'react';
import type {
  ClipModifierReference, ModifierContext, ModifierDeclaration, ModifierDefinition,
  ModifierFinding, ModifierRegistry,
} from '../modifier-types';

import {admitModifiers, ModifierAdmissionError} from './modifier-admission';
import {resolveModifierKeyframes} from './modifier-keyframes';
export {ModifierAdmissionError} from './modifier-admission';

// The component is a child-content subtype, never an EffectComponent/overlay.
export const declareModifier = <TParams,>(definition: ModifierDefinition<TParams>): ModifierDeclaration => ({
  kind: definition.kind,
  element: definition.element,
  hosts: definition.hosts,
  bounds: definition.bounds,
  alpha: definition.alpha,
  support: definition.support,
  parameters: definition.parameters,
  wrap: (instance, context, children) => createElement(definition.component, {
    key: instance.id,
    instanceId: instance.id,
    params: definition.resolveParams(instance.params, context),
    context,
    children,
  }),
});

export const composeModifiers = ({instances, registry, context, content, host = 'composition', onFinding}: {
  instances: readonly ClipModifierReference[];
  registry: ModifierRegistry;
  context: ModifierContext;
  content: ReactNode;
  host?: string;
  onFinding?: (finding: ModifierFinding) => void;
}): ReactNode => {
  const declarations = admitModifiers(instances, registry, host);
  const evaluated = resolveModifierKeyframes(instances, declarations, context.clip.keyframes, context.keyframeTime);
  if (instances.length === 0) return content;
  if (context.bounds.status === 'unknown') {
    onFinding?.({code: 'unknown-target-bounds', clipId: context.clip.id, reason: context.bounds.reason});
    throw new ModifierAdmissionError('unknown-target-bounds', `Cannot apply modifiers to ${context.clip.id}: ${context.bounds.reason}`);
  }
  const rect = context.bounds.rect;
  if (![rect.x, rect.y, rect.width, rect.height, context.frame, context.fps,
    context.keyframeFrame, context.keyframeTime, context.globalFrame].every(Number.isFinite)
    || context.fps <= 0 || rect.width < 0 || rect.height < 0) {
    throw new ModifierAdmissionError('invalid-context', 'Modifier requires finite evaluated clock and nonnegative target bounds');
  }
  declarations.forEach((declaration, index) => {
    if (declaration.bounds === 'unknown') onFinding?.({
      code: 'unknown-modifier-bounds', clipId: context.clip.id,
      instanceId: instances[index].id, element: declaration.element,
      reason: 'Modifier declares unknown output bounds',
    });
  });
  // Authored [A, B] is B(A(content)); no animation-hook grouping or reversal.
  return evaluated.reduce<ReactNode>((children, instance, index) => declarations[index].wrap(instance, context, children), content);
};
