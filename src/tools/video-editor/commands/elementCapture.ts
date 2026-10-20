import type { CommandRecord, DocumentPin, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipParams, finishClipParams } from './clipParamsCapture.ts';
import {
  AuthoredState,
  ClipMoveError,
  MoveRecording,
  assertFiniteJson,
  copy,
  equal,
  freezeJson,
  has,
  object,
} from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import type { ClipParamsArgs, ClipParamsBasis, ClipParamsResult } from './clipParamsCapture.ts';

export type ElementRef = {
  id: string;
  kind: string;
  revision: string;
  packId?: string;
};

export type ElementCaptureArgs = {
  elementRef: ElementRef;
  schema_source?: DocumentPin;
};

export type ElementCaptureBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
};

export type ElementCaptureResult = {
  command: EditCommand;
  bundle: AuthoredBundle;
  record: CommandRecord;
};

export type ElementParamsArgs = ClipParamsArgs & { schema_source?: DocumentPin };
export type ElementParamsBasis = ClipParamsBasis;
export type ElementParamsResult = ClipParamsResult;

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const elementKeys = ['id', 'kind', 'revision', 'packId'] as const;

function assertTarget(select: unknown): asserts select is string {
  if (typeof select !== 'string' || select.includes('::') ||
    !/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(select)) {
    throw new ClipMoveError('element capture requires a stable scoped clip identity');
  }
}

function assertElement(value: unknown): asserts value is ElementRef {
  if (!object(value) || !Object.keys(value).every((key) => elementKeys.includes(key as typeof elementKeys[number])) ||
    !['id', 'kind', 'revision'].every((key) => typeof value[key] === 'string' && value[key].length > 0) ||
    (has(value, 'packId') && (typeof value.packId !== 'string' || value.packId.length === 0))) {
    throw new ClipMoveError('element capture requires an exact element reference');
  }
}

function schemaSource(element: ElementRef, supplied?: DocumentPin): DocumentPin | undefined {
  if (!element.packId) {
    if (supplied !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
    return undefined;
  }
  throw new ClipMoveError('selected project pack capture requires authoritative Agent schema capture');
}

function targetContext(bundle: AuthoredBundle, command: EditCommand): MoveRecording {
  assertTarget(command.select);
  if (!object(bundle.parent) || !object(bundle.base_parent)) {
    throw new ClipMoveError('element capture requires an authored parent source pin');
  }
  const ctx = new MoveRecording(bundle, { ...command, intent: {} });
  const ref = command.select;
  if (ctx.read(ref, ['id']) == null) throw new ClipMoveError('element target disappeared', 'identity_conflict');
  const owner = ref.slice(0, ref.lastIndexOf('/'));
  if (owner !== 'parent') {
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    const mapping = object(bundle.source_mapping) && object(bundle.source_mapping.shots)
      ? bundle.source_mapping.shots : undefined;
    const source = ctx.state.occurrence(owner).shot_id;
    const pin = mapping?.[String(source)];
    if (!object(pin)) throw new ClipMoveError('missing occurrence source pin', 'identity_conflict');
    ctx.bind('scalar.owner', owner);
    ctx.dependency('scalar.images', 'entity', { parent: copy(bundle.base_parent), source: copy(pin) });
  } else {
    ctx.dependency('scalar.images', 'entity', { parent: copy(bundle.base_parent) });
  }
  ctx.bind('scalar.target', ref, ['scalar.images']);
  return ctx;
}

function applyElement(bundle: AuthoredBundle, supplied: EditCommand): ElementCaptureResult {
  assertTarget(supplied.select);
  if (supplied.schema_version !== 1 || supplied.op !== 'clip.set-element' || supplied.version !== '1' ||
    (supplied.intent !== undefined && !equal(supplied.intent, {})) || !object(supplied.args) ||
    !equal(Object.keys(supplied.args).sort(), ['elementRef', ...(has(supplied.args, 'schema_source') ? ['schema_source'] : [])].sort())) {
    throw new ClipMoveError('unsupported clip.set-element v1 command');
  }
  assertElement(supplied.args.elementRef);
  assertFiniteJson(supplied.args);
  const ctx = targetContext(bundle, supplied);
  const ref = supplied.select;
  const selected = ctx.read(ref, ['elementRef']);
  const alias = ctx.read(ref, ['element_ref']);
  const before = selected ?? alias;
  assertElement(before);
  const next = supplied.args.elementRef;
  if (before.id !== next.id || before.kind !== next.kind ||
    (before.packId !== undefined && before.packId !== next.packId)) {
    throw new ClipMoveError('clip.set-element must keep the element id, kind and selected pack owner');
  }
  const pin = schemaSource(next, supplied.args.schema_source as DocumentPin | undefined);
  if (pin) {
    ctx.dependency('element.schema', 'source', pin);
    ctx.bind('element.target', ref, ['element.schema']);
  }
  ctx.write(ref, ['elementRef'], next);
  if (has(ctx.state.entity(ref)!, 'element_ref')) ctx.clear(ref, ['element_ref']);
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export function executeClipElement(bundle: AuthoredBundle, command: EditCommand): ElementCaptureResult {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  return applyElement(bundle, command);
}

export function captureClipElement(bundle: AuthoredBundle, select: string, args: ElementCaptureArgs): ElementCaptureBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(select);
  assertFiniteJson(args);
  assertElement(args.elementRef);
  const snapshot = copy(bundle);
  const command: EditCommand = {
    schema_version: 1,
    op: 'clip.set-element',
    version: '1',
    select,
    args: {
      elementRef: copy(args.elementRef),
      ...(args.schema_source !== undefined ? { schema_source: copy(args.schema_source) } : {}),
    },
  };
  const result = applyElement(snapshot, command);
  return freezeJson({ bundle: snapshot, command: result.command });
}

export function finishClipElement(basis: unknown, args: ElementCaptureArgs): ElementCaptureResult {
  assertFiniteJson(basis);
  assertFiniteJson(args);
  assertElement(args.elementRef);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete element capture basis');
  }
  const command = copy(basis.command as EditCommand);
  const expectedPin = object(command.args) ? command.args.schema_source : undefined;
  const requestedPin = schemaSource(args.elementRef, args.schema_source ?? expectedPin as DocumentPin | undefined);
  if (!equal(expectedPin, requestedPin) || !equal(command.args.elementRef, args.elementRef)) {
    throw new ClipMoveError('element capture changed after original capture', 'capture_mismatch');
  }
  return applyElement(basis.bundle as AuthoredBundle, command);
}

/** PARAM capture shares the existing native parity implementation for draft refs. */
export function captureClipElementParams(bundle: AuthoredBundle, select: string, args: ElementParamsArgs): ElementParamsBasis {
  assertFiniteJson(args);
  const ref = new AuthoredState(bundle).entity(select);
  const selected = ref && (ref.elementRef ?? ref.element_ref);
  if (object(selected) && selected.packId) {
    throw new ClipMoveError('selected project pack capture requires authoritative Agent schema capture');
  }
  if (args.schema_source !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
  return captureClipParams(bundle, select, args);
}

export function finishClipElementParams(basis: unknown, args: ElementParamsArgs): ElementParamsResult {
  if (object(basis) && object(basis.command) && object(basis.bundle) &&
    typeof basis.command.select === 'string') {
    const selected = new AuthoredState(basis.bundle as AuthoredBundle).entity(basis.command.select);
    const element = selected?.elementRef ?? selected?.element_ref;
    if (object(element) && element.packId) {
      throw new ClipMoveError('selected project pack capture requires authoritative Agent schema capture');
    }
    if (object(basis.command.args) && has(basis.command.args, 'schema_source')) {
      throw new ClipMoveError('selected project pack capture requires authoritative Agent schema capture');
    }
  }
  if (args.schema_source !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
  return finishClipParams(basis, args);
}
