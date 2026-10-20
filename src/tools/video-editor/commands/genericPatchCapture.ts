import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { captureTrackLabel, finishTrackLabel, type TrackLabelArgs } from './trackLabelCapture.ts';
import {
  captureOrdinaryMoveMember,
  executeOrdinaryMoveMember,
  finishOrdinaryMoveMember,
} from './ordinaryMoveMember.ts';
import {
  captureOrdinaryScalarMember,
  executeOrdinaryScalarMember,
} from './ordinaryScalarMember.ts';
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

export class GenericPatchRefusal extends Error {
  readonly intentions: Array<{ operationIndex: number; op: string; target: string; reason: string }>;

  constructor(patch: TimelinePatch, failures: Map<number, string>) {
    const intentions = patch.operations.map((operation, operationIndex) => ({
      operationIndex,
      op: operation.op,
      target: operation.target,
      reason: failures.get(operationIndex) ?? 'Not submitted because another patch member was refused',
    }));
    super(`Native patch refused: ${intentions.map((item) =>
      `${item.operationIndex} ${item.op} ${item.target}: ${item.reason}`).join('; ')}`);
    this.intentions = intentions;
  }
}

function scalarPatchPayload(operation: TimelinePatchOperation): boolean {
  const payload = operation.payload;
  if (!object(payload) || !equal(Object.keys(payload).sort(), ['clear', 'values'])
    || !object(payload.values) || !Array.isArray(payload.clear)) return false;
  const values = payload.values;
  const clear = payload.clear;
  if (Object.keys(values).some((key) => key !== 'hold')
    || (has(values, 'hold') && (typeof values.hold !== 'number' || !Number.isFinite(values.hold) || values.hold <= 0))
    || clear.some((key) => typeof key !== 'string' || !['hold', 'asset', 'transition'].includes(key))
    || new Set(clear).size !== clear.length
    || Object.keys(values).some((key) => clear.includes(key))
    || (!Object.keys(values).length && !clear.length)) return false;
  return true;
}

function qualified(operation: TimelinePatchOperation): boolean {
  return operation.op === 'clip.move'
    || (operation.op === 'clip.update' && object(operation.payload)
      && (has(operation.payload, 'values') || has(operation.payload, 'clear')));
}

function supported(operation: TimelinePatchOperation): boolean {
  const payload = operation.payload;
  if (Object.keys(operation).some((key) => !['op', 'target', 'payload', 'order'].includes(key))
    || typeof operation.target !== 'string' || !operation.target
    || (operation.order !== undefined && !Number.isFinite(operation.order)) || !object(payload)) return false;
  if (operation.op === 'track.update') {
    return typeof payload.label === 'string' && Object.keys(payload).every((key) => key === 'label' || key === 'mode')
      && (!('mode' in payload) || payload.mode === 'merge');
  }
  if (operation.op === 'clip.move') {
    return equal(Object.keys(payload), ['at'])
      && typeof payload.at === 'number' && Number.isFinite(payload.at) && payload.at >= 0;
  }
  if (operation.op === 'clip.update' && equal(Object.keys(payload), ['hold'])) {
    return typeof payload.hold === 'number' && Number.isFinite(payload.hold) && payload.hold > 0;
  }
  return operation.op === 'clip.update' && scalarPatchPayload(operation);
}

export type GenericPatchSupport = 'supported' | 'unsupported' | 'mixed';

/** Classify the complete patch before native capture or owner resolution. */
export function classifyGenericPatch(patch: TimelinePatch): GenericPatchSupport {
  const supportedCount = patch.operations.filter(supported).length;
  const qualifiedCount = patch.operations.filter(qualified).length;
  if (qualifiedCount === 0) {
    if (supportedCount === patch.operations.length) return 'supported';
    return supportedCount ? 'mixed' : 'unsupported';
  }
  return supportedCount === patch.operations.length ? 'supported' : 'mixed';
}

function commandArgs(command: EditCommand): TrackLabelArgs {
  if (!object(command.args) || !object(command.args.values) || !Array.isArray(command.args.clear)) {
    throw new Error('Unsupported track.set command arguments');
  }
  return command.args as unknown as TrackLabelArgs;
}

function executeTrackSet(bundle: AuthoredBundle, command: EditCommand, ordinal = 0) {
  if (command.op !== 'track.set' || typeof command.select !== 'string') {
    throw new Error('Unsupported native patch member');
  }
  const result = finishTrackLabel(captureTrackLabel(bundle, command.select), commandArgs(command));
  if (!equal(result.command, command)) throw new Error('Submitted track.set does not match its captured claims');
  result.record.ordinal = ordinal;
  result.record.derived_writes.forEach((write) => { write.cause = ordinal; });
  return result;
}

type ScalarValue = Record<string, JSON>;

function number(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new ClipMoveError(`${label} must be a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  }
  return value;
}

function close(a: number, b: number): boolean {
  return Math.abs(a - b) <= Math.max(1e-9, 1e-9 * Math.max(Math.abs(a), Math.abs(b)));
}

function decimal(value: number): [bigint, bigint] {
  const [mantissa, exponent = '0'] = String(value).split('e');
  const digits = mantissa.replace('.', '');
  const scale = (mantissa.split('.')[1]?.length ?? 0) - Number(exponent);
  return scale >= 0
    ? [BigInt(digits), 10n ** BigInt(scale)]
    : [BigInt(digits) * 10n ** BigInt(-scale), 1n];
}

function rate(value: JSON | undefined): [bigint, bigint] {
  let numerator: bigint;
  let denominator: bigint;
  if (value == null) return [30n, 1n];
  if (object(value) && equal(Object.keys(value).sort(), ['denominator', 'numerator'])) {
    if (!Number.isSafeInteger(value.numerator) || !Number.isSafeInteger(value.denominator)) {
      throw new ClipMoveError('fps rational requires safe integer numerator/denominator');
    }
    numerator = BigInt(number(value.numerator, 'fps numerator', true));
    denominator = BigInt(number(value.denominator, 'fps denominator', true));
  } else {
    [numerator, denominator] = decimal(number(value, 'fps', true));
  }
  let a = numerator;
  let b = denominator;
  while (b) [a, b] = [b, a % b];
  if (!Number.isSafeInteger(Number(numerator / a)) || !Number.isSafeInteger(Number(denominator / a))) {
    throw new ClipMoveError('fps fraction exceeds browser JSON integer precision', 'unsupported_timing');
  }
  return [numerator / a, denominator / a];
}

function fractionNumber(numerator: bigint, denominator: bigint): number {
  if (numerator === 0n) return 0;
  let exponent = numerator.toString(2).length - denominator.toString(2).length;
  if (exponent >= 0
    ? numerator < (denominator << BigInt(exponent))
    : (numerator << BigInt(-exponent)) < denominator) exponent--;
  const shift = exponent < -1022 ? 1074 : 52 - exponent;
  const scaledNumerator = shift >= 0 ? numerator << BigInt(shift) : numerator;
  const scaledDenominator = shift >= 0 ? denominator : denominator << BigInt(-shift);
  let quotient = scaledNumerator / scaledDenominator;
  const remainder = scaledNumerator % scaledDenominator;
  if (remainder * 2n > scaledDenominator ||
    (remainder * 2n === scaledDenominator && quotient % 2n !== 0n)) quotient++;
  return Number(quotient) * 2 ** -shift;
}

function timelineDuration(clip: ScalarValue): number {
  const speed = clip.speed == null ? 1 : number(clip.speed, 'clip.speed', true);
  const at = has(clip, 'at')
    ? number(clip.at, 'clip.at')
    : number(clip.at_ms, 'clip.at_ms') / 1000;
  if (!has(clip, 'at') && !has(clip, 'at_ms')) {
    throw new ClipMoveError('move requires an explicit authored start', 'unsupported_timing');
  }
  if (at < 0) throw new ClipMoveError('clip.set does not support a clipped negative start', 'unsupported_timing');
  if (has(clip, 'at') && has(clip, 'at_ms') &&
    !close(at, number(clip.at_ms, 'clip.at_ms') / 1000)) {
    throw new ClipMoveError('contradictory at/at_ms timing codecs', 'unsupported_timing');
  }
  const lengths: number[] = [];
  if (typeof clip.hold === 'number' && typeof clip.hold !== 'boolean') {
    lengths.push(number(clip.hold, 'hold') / speed);
  } else if (clip.from != null && clip.to != null) {
    lengths.push((number(clip.to, 'to') - number(clip.from, 'from')) / speed);
  }
  for (const [key, scale] of [['duration', 1], ['duration_ms', 1000] ] as const) {
    if (clip[key] != null) lengths.push(number(clip[key], key) / scale / speed);
  }
  if (!lengths.length || lengths[0] <= 0 ||
    lengths.some((length) => !Number.isFinite(length) || !close(length, lengths[0]))) {
    throw new ClipMoveError('move needs an unambiguous positive authored duration/window', 'unsupported_timing');
  }
  return lengths[0];
}

function clipStartFrame(clip: ScalarValue, fps: number): number {
  return Math.floor(number(clip.at, 'clip.at') * number(fps, 'fps', true) + 0.5);
}

function clipEndFrame(clip: ScalarValue, fps: number): number {
  const start = clipStartFrame(clip, fps);
  const frames = Math.max(1, Math.floor(timelineDuration(clip) * fps + 0.5));
  return start + frames;
}

function occurrenceStart(row: ScalarValue): number {
  if (row.placement != null && !object(row.placement)) {
    throw new ClipMoveError('occurrence placement must be an object', 'unsupported_map');
  }
  const placement = row.placement as ScalarValue | undefined;
  const start = placement?.start_ms;
  const fallback = row.at_ms;
  if (start != null && fallback != null &&
    !close(number(start, 'placement.start_ms'), number(fallback, 'at_ms'))) {
    throw new ClipMoveError('contradictory occurrence start codecs', 'unsupported_timing');
  }
  return number(start ?? fallback ?? 0, 'occurrence start') / 1000;
}

function clipTarget(ctx: MoveRecording, command: EditCommand): string {
  const ref = command.select;
  if (typeof ref !== 'string' || !/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(ref) || ref.includes('::')) {
    throw new ClipMoveError('clip.set requires a parent or occurrence clip identity');
  }
  const owner = ref.slice(0, ref.lastIndexOf('/'));
  if (ctx.read(ref, ['id']) === undefined) {
    throw new ClipMoveError('scalar target disappeared', 'identity_conflict');
  }
  const pin: ScalarValue = { parent: copy(ctx.state.bundle.base_parent ?? {}) };
  if (owner !== 'parent') {
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    const shot = ctx.state.occurrence(owner).shot_id;
    const mapping = object(ctx.state.bundle.source_mapping) ? ctx.state.bundle.source_mapping : {};
    const shots = object(mapping.shots) ? mapping.shots : {};
    pin.source = copy(shots[String(shot)] ?? {});
    ctx.bind('scalar.owner', owner);
  }
  ctx.dependency('scalar.images', 'entity', pin);
  ctx.bind('scalar.target', ref, ['scalar.images']);
  return ref;
}

function clipBasis(ctx: MoveRecording, ref: string): void {
  for (const key of ['clipType', 'clip_type', 'asset', 'asset_id', 'media_id', 'object_id', 'elementRef', 'element_ref']) {
    ctx.read(ref, [key]);
  }
  const row = ctx.state.entity(ref)!;
  const selector = ['asset', 'asset_id', 'media_id', 'object_id']
    .find((key) => has(row, key));
  const selected = selector ? row[selector] : undefined;
  if ((selector === 'asset' || selector === 'asset_id') && typeof selected === 'string') {
    const registry = `${ref.slice(0, ref.lastIndexOf('/'))}/registry`;
    for (const key of ['media_id', 'object_id', 'digest', 'content_digest']) {
      ctx.read(registry, ['assets', selected, key]);
    }
  }
}

function clipHold(ctx: MoveRecording, ref: string, hold: number): [string[][], number] {
  const owner = ref.slice(0, ref.lastIndexOf('/'));
  const clipFields = [
    'id', 'at', 'at_ms', 'track', 'asset', 'asset_id', 'media_id', 'object_id',
    'clipType', 'clip_type', 'enabled', 'active', 'disabled', 'hidden', 'deleted',
    'from', 'to', 'from_ms', 'to_ms', 'hold', 'duration', 'duration_ms', 'speed',
    'time_map', 'timeMap', 'clips', 'children',
  ];
  for (const key of clipFields) ctx.read(ref, [key]);
  const row = copy(ctx.state.entity(ref)!);
  for (const key of ['time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms']) {
    if (row[key] != null) throw new ClipMoveError(`clip.set does not support ${key}`, 'unsupported_timing');
  }
  const durationPaths: string[][] = [];
  for (const prefix of [[], ['app'], ['app', 'astrid']]) {
    for (const key of ['on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence',
      'sequence_index', 'sequence_fit', 'orphan', 'formulas']) {
      const value = ctx.read(ref, [...prefix, key]);
      if (value == null || (key === 'fixed_start' && typeof value === 'boolean')) continue;
      if (key === 'for') {
        if (!close(number(value, 'for', true), timelineDuration(row))) {
          throw new ClipMoveError('clip.set hold conflicts with static for', 'unsupported_timing');
        }
        durationPaths.push([...prefix, key]);
        continue;
      }
      throw new ClipMoveError(`clip.set hold does not support ${key}`, 'unsupported_timing');
    }
  }
  row.hold = hold;
  const duration = timelineDuration(row);
  row.at = has(row, 'at') ? row.at : number(row.at_ms ?? 0, 'at_ms') / 1000;
  const fps = rate(ctx.read('parent', ['config', 'output', 'fps']));
  const fpsNumber = fractionNumber(fps[0], fps[1]);
  const end = clipEndFrame(row, fpsNumber);
  ctx.dependency('clip.set.quantization', 'time-map', {
    numerator: Number(fps[0]),
    denominator: Number(fps[1]),
    rounding: 'half-toward-positive-infinity',
  });
  if (owner === 'parent') return [durationPaths, duration];
  const childFps = ctx.read(`${owner}/source`, ['output', 'fps']);
  if (childFps != null && !equal(rate(childFps), fps)) {
    throw new ClipMoveError('parent and child fps differ', 'unsupported_timing');
  }
  for (const path of [['placement', 'start_ms'], ['at_ms'], ['duration_ms'], ['track'], ['placement', 'track'],
    ['time_map'], ['timeMap'], ['speed'], ['source_offset'], ['enabled'], ['active'], ['disabled'], ['hidden'], ['deleted']]) {
    ctx.read(owner, path);
  }
  const occurrence = ctx.state.occurrence(owner);
  if (occurrence.time_map != null || occurrence.timeMap != null ||
    (typeof occurrence.speed === 'boolean') || (occurrence.speed != null && occurrence.speed !== 1) ||
    (typeof occurrence.source_offset === 'boolean') ||
    (occurrence.source_offset != null && occurrence.source_offset !== 0)) {
    throw new ClipMoveError('clip.set requires a translation-only occurrence', 'unsupported_map');
  }
  const origin = occurrenceStart(occurrence);
  const extent = occurrence.duration_ms;
  if (extent == null) throw new ClipMoveError('clip.set requires an explicit occurrence extent', 'unsupported_timing');
  let limit = origin + number(extent, 'occurrence.duration_ms', true) / 1000;
  const blockers = ctx.select('move.blockers', owner);
  for (const other of blockers) {
    for (const path of [['placement', 'start_ms'], ['at_ms'], ['track'], ['placement', 'track'],
      ['enabled'], ['active'], ['disabled'], ['hidden'], ['deleted']]) ctx.read(other, path);
    const start = occurrenceStart(ctx.state.occurrence(other));
    if (other !== owner && start > origin) limit = Math.min(limit, start);
  }
  const boundary = clipStartFrame({ at: limit - origin, hold: 1 }, fpsNumber);
  if (number(row.at, 'clip.at') < 0 || number(row.at, 'clip.at') + duration > limit - origin + 1e-9 || end > boundary) {
    throw new ClipMoveError('clip.set interval crosses occurrence boundary', 'occurrence_boundary');
  }
  return [durationPaths, duration];
}

function setClip(bundle: AuthoredBundle, command: EditCommand) {
  if (command.schema_version !== 1 || command.op !== 'clip.set' || command.version !== '1') {
    throw new ClipMoveError('unsupported clip.set v1 command');
  }
  if (command.intent !== undefined && !equal(command.intent, {})) {
    throw new ClipMoveError('unsupported clip.set v1 intention');
  }
  if (!object(command.args) || !object(command.args.values) || !Array.isArray(command.args.clear)
    || !equal(Object.keys(command.args).sort(), ['clear', 'values'])
    || !equal(Object.keys(command.args.values), ['hold']) || !equal(command.args.clear, [])) {
    throw new ClipMoveError('native clip.set supports only a hold value with an explicit empty clear');
  }
  const hold = command.args.values.hold;
  number(hold, 'hold', true);
  const ctx = new MoveRecording(bundle, { ...command, intent: {} });
  const ref = clipTarget(ctx, command);
  clipBasis(ctx, ref);
  const row = ctx.state.entity(ref)!;
  const asset = has(row, 'asset') ? row.asset : row.asset_id;
  if (typeof asset === 'string') {
    ctx.read(`${ref.slice(0, ref.lastIndexOf('/'))}/registry`, ['assets', asset, 'content_sha256']);
  }
  const [durationPaths, duration] = clipHold(ctx, ref, hold);
  for (const path of durationPaths) ctx.write(ref, path, duration);
  ctx.write(ref, ['hold'], hold);
  ctx.compile();
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

function verifyCapturedFields(bundle: AuthoredBundle, command: EditCommand, actual: EditCommand): void {
  for (const key of ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const) {
    let matches = equal(command[key], actual[key]);
    if (key === 'reads' && Array.isArray(command.reads)) {
      const state = new AuthoredState(bundle);
      matches = command.reads.length === (actual.reads?.length ?? 0) && command.reads.every((claimed, index) => {
        const read = actual.reads![index];
        return claimed.ref === read.ref && equal(claimed.path, read.path) &&
          (equal(claimed.state, read.state) ||
            (read.ref.endsWith('/shot') && state.matches(read.ref, read.path, claimed.state)));
      });
    }
    if (has(command, key) && !matches) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
}

function executeClipSet(bundle: AuthoredBundle, command: EditCommand, ordinal = 0) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  const result = setClip(bundle, command);
  verifyCapturedFields(bundle, command, result.command);
  result.record.ordinal = ordinal;
  result.record.derived_writes.forEach((write) => { write.cause = ordinal; });
  Object.assign(result.command, copy(command), { intent: result.command.intent });
  return result;
}

function captureClipSet(bundle: AuthoredBundle, select: string, hold: number): EditCommand {
  assertFiniteJson(bundle);
  const snapshot = copy(bundle);
  return freezeJson(executeClipSet(snapshot, {
    schema_version: 1,
    op: 'clip.set',
    version: '1',
    select,
    args: { values: { hold }, clear: [] },
    intent: {},
  }).command);
}

export function executeGenericPatch(bundle: AuthoredBundle, commands: readonly EditCommand[]) {
  let after = copy(bundle);
  const records: CommandRecord[] = [];
  for (const [ordinal, command] of commands.entries()) {
    const result = command.op === 'track.set'
      ? executeTrackSet(after, command, ordinal)
      : command.op === 'clip.move'
        ? executeOrdinaryMoveMember(after, command, ordinal)
      : command.op === 'clip.set'
        ? object(command.args) && Array.isArray(command.args.clear) && command.args.clear.length
          ? executeOrdinaryScalarMember(after, command, ordinal)
          : executeClipSet(after, command, ordinal)
        : (() => { throw new Error('Unsupported native patch member'); })();
    after = result.bundle;
    records.push(result.record);
  }
  return { bundle: after, records };
}

/** Native ordinary members; ownership comes from the host resolver. */
export function captureGenericPatch(
  bundle: AuthoredBundle,
  patch: TimelinePatch,
  resolve: (operation: TimelinePatchOperation) => string,
) {
  assertFiniteJson(patch);
  const original = freezeJson(copy(patch));
  const failures = new Map<number, string>();
  original.operations.forEach((operation, index) => {
    if (!supported(operation)) failures.set(index, qualified(operation)
      ? operation.op === 'clip.move'
        ? 'Requires an absolute clip.move with one finite non-negative at value'
        : 'Requires clip.set-compatible values and explicit clears'
      : 'Requires a parent label-only merge or exact positive hold SET');
  });
  if (!original.operations.length || !Number.isSafeInteger(original.version) || original.version < 0) {
    throw new Error('Native patch requires operations and a non-negative integer version');
  }
  if (failures.size) throw new GenericPatchRefusal(original, failures);
  const owners = original.operations.map((operation, index) => {
    try { return resolve(operation); }
    catch (error) {
      failures.set(index, error instanceof Error ? error.message : String(error));
      return '';
    }
  });
  if (failures.size) throw new GenericPatchRefusal(original, failures);

  const ordered = original.operations.map((operation, index) => ({ operation, index })).sort((a, b) => {
    if (a.operation.order === undefined) return b.operation.order === undefined ? a.index - b.index : 1;
    if (b.operation.order === undefined) return -1;
    return a.operation.order - b.operation.order || a.index - b.index;
  });
  let after = copy(bundle);
  const commands: EditCommand[] = [];
  const records: CommandRecord[] = [];
  const previewOperations: TimelinePatchOperation[] = [];
  for (const { operation, index } of ordered) {
    try {
      let result;
      if (operation.op === 'track.update') {
        result = finishTrackLabel(captureTrackLabel(after, owners[index]), {
          values: { label: operation.payload!.label as string }, clear: [],
        });
        previewOperations.push({ op: operation.op, target: operation.target, payload: { label: operation.payload!.label } });
      } else if (operation.op === 'clip.move') {
        const basis = captureOrdinaryMoveMember(after, operation, owners[index]);
        const move = finishOrdinaryMoveMember(basis, commands.length);
        result = move;
        previewOperations.push({ op: operation.op, target: operation.target, payload: { at: move.previewAt } });
      } else if (object(operation.payload) && (has(operation.payload, 'values') || has(operation.payload, 'clear'))) {
        const values = operation.payload.values as Record<string, JSON>;
        const clear = operation.payload.clear as string[];
        if (clear.length) {
          const command = captureOrdinaryScalarMember(after, { select: owners[index], values, clear });
          result = executeOrdinaryScalarMember(after, command, commands.length);
        } else {
          result = executeClipSet(after, captureClipSet(after, owners[index], values.hold as number), commands.length);
        }
        previewOperations.push({ op: operation.op, target: operation.target, payload: {
          values: copy(values), clear: [...clear],
        } });
      } else {
        result = executeClipSet(after, captureClipSet(after, owners[index], operation.payload!.hold as number), commands.length);
        previewOperations.push({ op: operation.op, target: operation.target, payload: { hold: operation.payload!.hold } });
      }
      result.record.ordinal = commands.length;
      result.record.derived_writes.forEach((write) => { write.cause = commands.length; });
      after = result.bundle;
      commands.push(result.command);
      records.push(result.record);
    } catch (error) {
      failures.set(index, error instanceof Error ? error.message : String(error));
    }
  }
  if (failures.size) throw new GenericPatchRefusal(original, failures);
  const preview: TimelinePatch = {
    version: 1,
    source: 'timeline.native-ordinary',
    operations: previewOperations,
  };
  return freezeJson({ patch: original, owners, commands, records, bundle: after, preview });
}

export type GenericPatchBasis = {
  readonly current: TimelineData;
  readonly capture: ReturnType<typeof captureGenericPatch>;
  readonly localGeneration: number;
  readonly localBasis: import('./commitOutbox.ts').OutboxBasis;
};

export interface GenericPatchCapturePort {
  capture(input: { patch: TimelinePatch; current: TimelineData }): GenericPatchBasis;
  finish(basis: GenericPatchBasis): { commands: EditCommand[]; preview: TimelinePatch };
  submit(input: { commands: EditCommand[]; preview: TimelinePatch }): void;
}

/** One local projection, preserving exact authored values and unrelated display state. */
export function projectGenericPatchPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'timeline.native-label-hold' && patch.source !== 'timeline.native-ordinary') return undefined;
  assertFiniteJson(patch);
  if (patch.version !== 1 || !patch.operations.length || patch.operations.some((operation) => !supported(operation))) {
    throw new Error('Invalid native patch preview');
  }
  const config = copy(current.config);
  const resolvedConfig = copy(current.resolvedConfig);
  for (const operation of patch.operations) {
    for (const target of [config, resolvedConfig]) {
      const rows = operation.op === 'track.update' ? target.tracks ?? [] : target.clips;
      const matches = rows.filter((row) => row.id === operation.target);
      if (matches.length !== 1) throw new Error('Native patch preview requires one displayed target');
      if (operation.op === 'clip.update' && object(operation.payload)
        && (has(operation.payload, 'values') || has(operation.payload, 'clear'))) {
        const values = object(operation.payload.values) ? operation.payload.values : {};
        const clear = Array.isArray(operation.payload.clear) ? operation.payload.clear : [];
        Object.assign(matches[0], copy(values));
        for (const key of clear) delete matches[0][key];
      } else {
        Object.assign(matches[0], copy(operation.payload));
      }
    }
  }
  return { ...current, ...assembleTimelineData({ ...current, config, resolvedConfig }), dataLanes: current.dataLanes };
}
