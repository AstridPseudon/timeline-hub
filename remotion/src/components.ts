import * as host from '@banodoco/timeline-composition/theme-api';
import Ajv from 'ajv';
import type {ModifierDeclaration, ModifierDefinition, ModifierRegistry, ModifierParameterBinding} from '@banodoco/timeline-composition/theme-api';

// Normalize contributed React-style registrations before Composition captures
// its canonical component; an explicit canonical value keeps precedence.
const componentHost = (parameters: ModifierParameterBinding) => ({
  ...host,
  declareModifier<TParams>(definition: ModifierDefinition<TParams> | (
    Omit<ModifierDefinition<TParams>, 'component'> & {Component: ModifierDefinition<TParams>['component']}
  )): ModifierDeclaration {
    const canonical = 'component' in definition
      ? definition
      : {...definition, component: definition.Component};
    return host.declareModifier({...canonical, parameters});
  },
});

const freeze = <T,>(value: T): T => {
  if (value && typeof value === 'object') {
    Object.values(value).forEach(freeze);
    Object.freeze(value);
  }
  return value;
};

export type ComponentBinding = {
  identity: string;
  implementation_digest: string;
  key: string;
  descriptor: {point: string; id: string; kind: string; hosts: readonly string[]; params: object;
    bounds?: 'preserve'; alpha: 'preserve'; support: 'preserve';
    implementation: {export: string}};
  module: Record<string, unknown>;
};

export const bindComponentRegistry = (bindings: readonly ComponentBinding[]): ModifierRegistry => {
  const registry: Record<string, ModifierDeclaration> = {};
  for (const binding of bindings) {
    const {identity, implementation_digest: digest, module} = binding;
    const descriptor = freeze(structuredClone(binding.descriptor));
    if (descriptor.point !== 'timeline.component' || descriptor.kind !== 'modifier' || identity !== `${descriptor.point}/${descriptor.id}`
      || !/^[a-f0-9]{64}$/.test(digest) || binding.key !== `${identity}@${digest}`
      || !descriptor.hosts.includes('composition') || Object.prototype.hasOwnProperty.call(registry, identity)) {
      throw new Error(`Invalid native component binding: ${identity}`);
    }
    const factory = module[descriptor.implementation.export];
    if (typeof factory !== 'function') throw new Error(`Missing declared component export: ${identity}`);
    const validate = new Ajv({allErrors: true, strict: false}).compile(descriptor.params);
    const parameters = {schema: descriptor.params, validateParams(params: Record<string, unknown>) {
      if (!validate(params)) throw new Error(`invalid component params: ${JSON.stringify(validate.errors)}`);
    }};
    const declaration = factory(componentHost(parameters), descriptor) as ModifierDeclaration;
    if (!declaration || declaration.element !== identity || declaration.kind !== 'modifier'
      || !declaration.hosts.includes('composition') || typeof declaration.wrap !== 'function'
      || declaration.bounds !== (descriptor.bounds ?? 'unknown') || declaration.alpha !== 'preserve'
      || declaration.support !== 'preserve' || descriptor.alpha !== 'preserve' || descriptor.support !== 'preserve'
      || JSON.stringify(declaration.hosts) !== JSON.stringify(descriptor.hosts)) {
      throw new Error(`Component declaration identity mismatch: ${identity}`);
    }
    registry[identity] = Object.freeze(declaration);
  }
  return Object.freeze(registry);
};
