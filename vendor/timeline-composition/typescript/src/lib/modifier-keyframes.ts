import type {ClipModifierReference, ModifierDeclaration, ModifierParameterBinding} from '../modifier-types';
import type {ClipKeyframe} from '../types';
import {ModifierAdmissionError} from './modifier-admission';
import {interpolateKeyframeInterval} from './keyframe-easing';
import {motionCurveName} from './motion-curves.generated';

const fail = (message: string): never => {throw new ModifierAdmissionError('invalid-modifier-keyframes', message);};
const object = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === 'object' && !Array.isArray(value);

export const isModifierParameterAddress = (path: string): boolean => /^modifiers(?:$|[.\[])/.test(path);
export const hasModifierKeyframes = (clip: {keyframes?: unknown}): boolean =>
  object(clip.keyframes) && Object.keys(clip.keyframes).some(isModifierParameterAddress);

/** Same quoted JSON instance ID and property leaf as D's modifier address. */
export const modifierParameterAddress = (id: string, leaf: string): string => {
  const quoted = JSON.stringify(id).replace(/[\u007f-\uffff]/g,
    char => `\\u${char.charCodeAt(0).toString(16).padStart(4, '0')}`);
  return `modifiers[${quoted}].params.${leaf}`;
};

export const parseModifierParameterAddress = (path: string): {id: string; leaf: string} | undefined => {
  if (!isModifierParameterAddress(path)) return undefined;
  const match = /^modifiers\[("(?:[^"\\]|\\.)*")\]\.params\.([A-Za-z_][\p{L}\p{N}_-]*)$/u.exec(path);
  if (!match) return fail(`Malformed modifier parameter address: ${path}`);
  let id: unknown;
  try {id = JSON.parse(match[1]);} catch {return fail(`Malformed modifier instance ID: ${path}`);}
  if (typeof id !== 'string' || !id.trim() || modifierParameterAddress(id, match[2]) !== path) {
    return fail(`Noncanonical modifier parameter address: ${path}`);
  }
  return {id, leaf: match[2]};
};

const numericLeaf = (binding: ModifierParameterBinding, leaf: string): void => {
  const schema = binding.schema;
  const rootKeys = new Set(['type', 'properties', 'required', 'additionalProperties', '$schema', '$id',
    'title', 'description', 'default', 'examples']);
  if (!object(schema) || schema.type !== 'object' || !object(schema.properties)
    || Object.keys(schema).some(key => !rootKeys.has(key))
    || (schema.additionalProperties !== undefined && typeof schema.additionalProperties !== 'boolean')) {
    return fail('Animated modifier requires an independently constrained object descriptor');
  }
  if (!Object.hasOwn(schema.properties, leaf)) return fail(`Undeclared modifier parameter: ${leaf}`);
  const definition = schema.properties[leaf];
  const numberKeys = new Set(['type', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum',
    'title', 'description', 'default', 'examples']);
  if (!object(definition) || definition.type !== 'number' || Object.keys(definition).some(key => !numberKeys.has(key))) {
    return fail(`Unsupported animated modifier parameter: ${leaf}`);
  }
};

const validatedKeys = (value: unknown, path: string, validateValue: (value: number) => void): ClipKeyframe[] => {
  if (!Array.isArray(value)) return fail(`Modifier channel must be an array: ${path}`);
  for (const key of value) {
    if (!object(key) || typeof key.time !== 'number' || !Number.isFinite(key.time)
      || typeof key.value !== 'number' || !Number.isFinite(key.value)
      || (key.interpolation !== 'linear' && key.interpolation !== 'hold')
      || (key.easing !== undefined && typeof key.easing !== 'string')) {
      return fail(`Malformed numeric modifier keyframe: ${path}`);
    }
    if (key.easing !== undefined) motionCurveName(key.easing as string);
    validateValue(key.value);
  }
  // Stable sort, first authored duplicate. Never mutate the authored map/keys.
  return (value as ClipKeyframe[]).slice().sort((a, b) => a.time - b.time)
    .filter((key, index, sorted) => index === 0 || key.time !== sorted[index - 1].time);
};

const sample = (keys: ClipKeyframe[], time: number): number => {
  if (time <= keys[0].time) return keys[0].value as number;
  const last = keys[keys.length - 1];
  if (time >= last.time) return last.value as number;
  const index = keys.findIndex((key, i) => i + 1 < keys.length && time >= key.time && time < keys[i + 1].time);
  const a = keys[index], b = keys[index + 1];
  return interpolateKeyframeInterval(a.value, b.value, time, a.time, b.time, a.interpolation, a.easing) as number;
};

/** One shared owner for both hosts. Time is already in the evaluated origin domain. */
export const resolveModifierKeyframes = (
  instances: readonly ClipModifierReference[], declarations: readonly ModifierDeclaration[],
  keyframes: unknown, keyframeTime: number,
): readonly ClipModifierReference[] => {
  if (keyframes !== undefined && !object(keyframes)) return fail('clip.keyframes must be a parameter map');
  const result = instances.slice();
  declarations.forEach((declaration, i) => declaration.parameters?.validateParams(instances[i].params));
  for (const [path, channel] of Object.entries(keyframes ?? {})) {
    const address = parseModifierParameterAddress(path);
    if (!address) continue;
    const index = instances.findIndex(instance => instance.id === address.id);
    if (index < 0) return fail(`Unknown modifier instance: ${address.id}`);
    const binding = declarations[index].parameters;
    if (!binding || typeof binding.validateParams !== 'function') return fail(`Missing descriptor binding: ${path}`);
    numericLeaf(binding, address.leaf);
    const keys = validatedKeys(channel, path, value => binding.validateParams({...instances[index].params, [address.leaf]: value}));
    if (!keys.length) continue;
    if (!Number.isFinite(keyframeTime)) return fail('Modifier keyframeTime must be finite');
    const params = {...result[index].params, [address.leaf]: sample(keys, keyframeTime)};
    binding.validateParams(params);
    result[index] = {...instances[index], params};
  }
  return result;
};
