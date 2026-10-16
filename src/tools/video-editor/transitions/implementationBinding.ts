import type {
  TransitionContribution,
  TransitionImplementationResource,
} from '@reigh/editor-sdk';

function isPlainRecord(value: unknown): value is Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function deepFreeze<T>(value: T): T {
  if (!value || typeof value !== 'object' || Object.isFrozen(value)) return value;
  Object.values(value as Record<string, unknown>).forEach(deepFreeze);
  return Object.freeze(value);
}

/**
 * Build the canonical data-only resource from one public manifest declaration.
 * The declared revision remains separate and is verified by Composition's
 * Player admission before a plan is exposed.
 */
export function createTransitionImplementationResource(
  ownerExtensionId: string,
  contribution: Pick<
    TransitionContribution,
    'id' | 'transitionId' | 'implementation' | 'supportedParams' | 'defaults'
  >,
): TransitionImplementationResource | undefined {
  if (contribution.implementation === undefined) return undefined;
  const candidate: unknown = {
    owner: ownerExtensionId,
    id: contribution.id,
    kind: 'transition',
    transitionId: contribution.transitionId,
    implementation: contribution.implementation,
    supportedParams: contribution.supportedParams ?? [],
    defaults: contribution.defaults ?? {},
  };
  if (validateTransitionImplementationResource(candidate).length > 0) return undefined;

  const source = candidate as TransitionImplementationResource;
  return deepFreeze({
    owner: source.owner,
    id: source.id,
    kind: 'transition' as const,
    transitionId: source.transitionId,
    implementation: { host: source.implementation.host, id: source.implementation.id },
    supportedParams: [...source.supportedParams],
    defaults: { ...source.defaults },
  });
}

export function validateTransitionImplementationRevision(value: unknown): string[] {
  return typeof value === 'string' && /^sha256:[a-f0-9]{64}$/.test(value)
    ? []
    : ['implementation resource revision must be a lowercase SHA-256 digest'];
}

export function validateTransitionImplementationResource(value: unknown): string[] {
  if (!isPlainRecord(value)) return ['implementation resource must be an object'];
  const errors: string[] = [];
  const exactKeys = ['owner', 'id', 'kind', 'transitionId', 'implementation', 'supportedParams', 'defaults'];
  if (Object.keys(value).some((key) => !exactKeys.includes(key))) {
    errors.push('implementation resource has unexpected fields');
  }
  if (typeof value.owner !== 'string' || value.owner.trim() === '') {
    errors.push('implementation resource owner is missing');
  }
  if (typeof value.id !== 'string' || value.id.trim() === '') {
    errors.push('implementation resource contribution id is missing');
  }
  if (value.kind !== 'transition') errors.push('implementation resource kind must be transition');
  if (typeof value.transitionId !== 'string' || value.transitionId.trim() === '') {
    errors.push('implementation resource transition id is missing');
  }
  if (['crossfade', 'cross-fade', 'fade'].includes(String(value.transitionId))) {
    errors.push('implementation resource cannot shadow a built-in transition');
  }

  const implementation = value.implementation;
  if (!isPlainRecord(implementation)
    || Object.keys(implementation).some((key) => !['host', 'id'].includes(key))) {
    errors.push('implementation declaration is malformed');
  } else {
    if (implementation.host !== 'timeline-composition') {
      errors.push('implementation host must be timeline-composition');
    }
    if (implementation.id !== 'cross-fade' && implementation.id !== 'fade') {
      errors.push('implementation id must be cross-fade or fade');
    }
  }

  const supportedParams = value.supportedParams;
  const defaults = value.defaults;
  if (!Array.isArray(supportedParams)
    || supportedParams.some((name) => name !== 'easing')
    || new Set(supportedParams).size !== supportedParams.length) {
    errors.push('implementation supportedParams must be a unique subset of [easing]');
  }
  if (!isPlainRecord(defaults)
    || Object.keys(defaults).some((key) => key !== 'easing')) {
    errors.push('implementation defaults must be an object containing only supported values');
  }

  if (Array.isArray(supportedParams) && isPlainRecord(defaults)) {
    const params = [...supportedParams].sort();
    const defaultNames = Object.keys(defaults).sort();
    if (JSON.stringify(params) !== JSON.stringify(defaultNames)) {
      errors.push('implementation defaults must match its supported parameter names');
    }
    if (defaultNames.length > 0
      && (params.length !== 1 || params[0] !== 'easing'
        || !isPlainRecord(implementation)
        || implementation.id !== 'cross-fade'
        || defaults.easing !== 'linear')) {
      errors.push('only cross-fade with easing=linear is currently supported');
    }
  }
  return errors;
}
