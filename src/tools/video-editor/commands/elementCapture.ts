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

function assertPin(value: unknown): asserts value is DocumentPin {
  if (!object(value) || typeof value.document_id !== 'string' || !Number.isInteger(value.version) ||
    typeof value.content_digest !== 'string') {
    throw new ClipMoveError('element capture requires an exact schema_source DocumentPin');
  }
}

function retainedPin(bundle: AuthoredBundle, pin: DocumentPin): boolean {
  const mapping = object(bundle.source_mapping) ? bundle.source_mapping : undefined;
  const document = object(mapping?._runtime_document) ? mapping._runtime_document : undefined;
  const manifest = object(document?.dependency_manifest) ? document.dependency_manifest : undefined;
  const retained = Array.isArray(manifest?.documents) ? manifest.documents : [];
  return retained.some((candidate) => equal(candidate, pin)) &&
    (Array.isArray(mapping?.pinned_documents) ? mapping.pinned_documents : [])
      .some((capture) => object(capture) && equal(capture.pin, pin));
}

function schemaSource(bundle: AuthoredBundle, element: ElementRef, supplied?: DocumentPin): DocumentPin | undefined {
  if (!element.packId) {
    if (supplied !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
    return undefined;
  }
  if (supplied !== undefined) {
    assertPin(supplied);
    if (!retainedPin(bundle, supplied)) {
      throw new ClipMoveError('schema_source must be a retained immutable document pin');
    }
    return copy(supplied);
  }
  throw new ClipMoveError('selected project pack requires the retained schema_source DocumentPin');
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
  // The native provider records `element.targets`; this local recorder only
  // supports the ordinary move selections, so do not approximate it with a
  // different membership query.
  for (const key of ['clipType', 'hold', 'asset', 'file', 'src', 'source', 'from', 'to']) ctx.read(ref, [key]);
  const before = ctx.read(ref, ['elementRef']) ?? ctx.read(ref, ['element_ref']);
  assertElement(before);
  const next = supplied.args.elementRef;
  if (before.id !== next.id || before.kind !== next.kind ||
    (before.packId !== undefined && before.packId !== next.packId)) {
    throw new ClipMoveError('clip.set-element must keep the element id, kind and selected pack owner');
  }
  const pin = schemaSource(bundle, next, supplied.args.schema_source as DocumentPin | undefined);
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
  const pin = schemaSource(snapshot, args.elementRef, args.schema_source);
  const command: EditCommand = {
    schema_version: 1,
    op: 'clip.set-element',
    version: '1',
    select,
    args: { elementRef: copy(args.elementRef), ...(pin ? { schema_source: pin } : {}) },
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
  const requestedPin = schemaSource(basis.bundle as AuthoredBundle, args.elementRef,
    args.schema_source ?? expectedPin as DocumentPin | undefined);
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
    const pin = schemaSource(bundle, selected as ElementRef, args.schema_source);
    const command = captureSelectedParams(bundle, select, args, pin);
    return freezeJson({ bundle: copy(bundle), command });
  }
  if (args.schema_source !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
  return captureClipParams(bundle, select, args);
}

function applySelectedParams(bundle: AuthoredBundle, supplied: EditCommand): ElementParamsResult {
  assertTarget(supplied.select);
  if (supplied.schema_version !== 1 || supplied.op !== 'clip.set-params' || supplied.version !== '1' ||
    !object(supplied.args) || !has(supplied.args, 'schema_source') || !has(supplied.args, 'values') ||
    !has(supplied.args, 'clear')) throw new ClipMoveError('unsupported selected clip.set-params v1 command');
  assertPin(supplied.args.schema_source);
  const values = supplied.args.values;
  const clear = supplied.args.clear;
  if (!object(values) || !Array.isArray(clear) || clear.some((key) => typeof key !== 'string') ||
    new Set(clear).size !== clear.length || Object.keys(values).some((key) => clear.includes(key)) ||
    (!Object.keys(values).length && !clear.length)) {
    throw new ClipMoveError('clip parameters require non-empty values or explicit clears');
  }
  assertFiniteJson(values);
  const ctx = targetContext(bundle, supplied);
  const selected = ctx.read(supplied.select, ['elementRef']) ?? ctx.read(supplied.select, ['element_ref']);
  assertElement(selected);
  if (!selected.packId || !retainedPin(bundle, supplied.args.schema_source)) {
    throw new ClipMoveError('selected project pack requires a retained immutable schema_source');
  }
  for (const key of ['clipType', 'clip_type', 'asset', 'asset_id', 'media_id', 'object_id', 'elementRef', 'element_ref']) {
    if (key !== 'elementRef' && key !== 'element_ref') ctx.read(supplied.select, [key]);
  }
  ctx.dependency('params.schema', 'source', supplied.args.schema_source);
  ctx.bind('params.element', supplied.select, ['params.schema']);
  if (Object.keys(values).length) ctx.object(supplied.select, ['params']);
  for (const key of Object.keys(values).sort()) ctx.write(supplied.select, ['params', key], values[key]);
  for (const key of [...clear].sort()) {
    const params = ctx.state.get(supplied.select, ['params']);
    if (params.state === 'present' && params.value !== null) ctx.clear(supplied.select, ['params', key]);
    else {
      ctx.read(supplied.select, ['params']);
      const address = `${supplied.select}::params.${key}`;
      ctx.command.expect![address] = { state: 'absent' };
      ctx.command.authorship![address] = 'direct';
      ctx.record.writes.push({ ref: supplied.select, path: ['params', key], before: { state: 'absent' }, after: { state: 'absent' } });
    }
  }
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

function captureSelectedParams(bundle: AuthoredBundle, select: string, args: ElementParamsArgs, pin: DocumentPin): EditCommand {
  if (!object(args) || !equal(Object.keys(args).sort(), ['clear', 'schema_source', 'values']) ||
    !object(args.values) || !Array.isArray(args.clear) || args.clear.some((key) => typeof key !== 'string') ||
    new Set(args.clear).size !== args.clear.length || Object.keys(args.values).some((key) => args.clear.includes(key)) ||
    (!Object.keys(args.values).length && !args.clear.length)) {
    throw new ClipMoveError('clip parameters require non-empty values or explicit clears');
  }
  const command: EditCommand = {
    schema_version: 1, op: 'clip.set-params', version: '1', select,
    args: { values: copy(args.values), clear: [...args.clear], schema_source: copy(pin) },
  };
  return applySelectedParams(bundle, command).command;
}

export function finishClipElementParams(basis: unknown, args: ElementParamsArgs): ElementParamsResult {
  if (object(basis) && object(basis.command) && basis.command.op === 'clip.set-params' &&
    object(basis.command.args) && has(basis.command.args, 'schema_source')) {
    assertFiniteJson(args);
    const pin = args.schema_source ?? basis.command.args.schema_source as DocumentPin;
    if (!equal(basis.command.args.schema_source, pin)) {
      throw new ClipMoveError('element parameter capture changed its retained schema pin', 'capture_mismatch');
    }
    const command = copy(basis.command as EditCommand);
    command.args = { ...command.args, values: copy(args.values), clear: [...args.clear], schema_source: copy(pin) };
    return applySelectedParams(basis.bundle as AuthoredBundle, command);
  }
  if (args.schema_source !== undefined) throw new ClipMoveError('schema_source requires a selected project pack element');
  return finishClipParams(basis, args);
}
