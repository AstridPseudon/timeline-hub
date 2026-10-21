import type { EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { ClipMoveError, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { OccurrenceMediaRecording, rawIdentity } from './occurrenceMediaPrimitives.ts';

type ObjectValue = { [key: string]: JSON };
export type OccurrenceMediaCommand = Omit<EditCommand, 'op' | 'select'> & {
  op: 'occurrence.add-media'; select: string;
};
const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RELATIONS = ['on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence', 'sequence_index', 'sequence_fit', 'orphan', 'formulas'];
const MAP_FIELDS = [['placement', 'start_ms'], ['at_ms'], ['duration_ms'], ['source_offset'], ['speed'], ['track'], ['placement', 'track'], ['time_map'], ['timeMap'], ['enabled'], ['active'], ['disabled'], ['hidden'], ['deleted']];
const active = (row: ObjectValue) => row.enabled !== false && row.active !== false && !['disabled', 'hidden', 'deleted'].some((key) => row[key] === true);

function number(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) throw new ClipMoveError(`${label} requires a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  return value;
}
function rate(value: JSON | undefined): [bigint, bigint] {
  if (value == null) return [30n, 1n];
  let n: bigint, d: bigint;
  if (object(value) && equal(Object.keys(value).sort(), ['denominator', 'numerator'])) {
    if (!Number.isSafeInteger(value.numerator) || !Number.isSafeInteger(value.denominator)) throw new ClipMoveError('invalid rational fps');
    n = BigInt(number(value.numerator, 'fps numerator', true)); d = BigInt(number(value.denominator, 'fps denominator', true));
  } else {
    const [mantissa, exponent = '0'] = String(number(value, 'fps', true)).split('e');
    const scale = (mantissa.split('.')[1]?.length ?? 0) - Number(exponent);
    n = BigInt(mantissa.replace('.', '')) * (scale < 0 ? 10n ** BigInt(-scale) : 1n); d = scale > 0 ? 10n ** BigInt(scale) : 1n;
  }
  let a = n, b = d; while (b) [a, b] = [b, a % b]; return [n / a, d / a];
}
function selection(pin: unknown): asserts pin is MediaSelection {
  if (!object(pin) || !equal(Object.keys(pin).sort(), ['asset', 'catalog_digest', 'generation_id', 'object_id', 'variant_id'])
    || !['asset', 'generation_id', 'variant_id'].every((key) => typeof pin[key] === 'string' && pin[key].length > 0)
    || !['object_id', 'catalog_digest'].every((key) => typeof pin[key] === 'string' && /^sha256:[0-9a-f]{64}$/.test(pin[key]))) throw new ClipMoveError('media requires a closed immutable five-field selection');
}
function verified(pin: MediaSelection, inputs: readonly VerifiedMedia[]) {
  const matches = inputs.filter((row) => equal(row.selection, pin));
  if (!matches.length || matches.some((row) => !equal(row, matches[0]))) throw new ClipMoveError('media edit requires exact Runtime-verified media input', 'dependency_changed');
  const value = matches[0], kind = typeof value.media_type === 'string' && value.media_type.includes('/') ? value.media_type.split('/')[0] : '';
  if (!['image', 'video'].includes(kind) || !Number.isInteger(value.size) || value.size <= 0) throw new ClipMoveError('media edit requires verified image/video metadata', 'unsupported_media');
  if (kind === 'video') number(value.duration_seconds, 'intrinsic duration', true);
  return { value, kind };
}
function owner(ctx: OccurrenceMediaRecording, ref: string, child: boolean) {
  if (!(child ? /^occurrence:(?!.*::)[^/]+\/clip:(?!.*::)[^/]+$/.test(ref) : /^occurrence:(?!.*::)[^/]+$/.test(ref))) throw new ClipMoveError('media edit requires explicit occurrence/raw child ownership');
  const scope = child ? ref.slice(0, ref.lastIndexOf('/')) : ref;
  ctx.selectCollection('occurrence', 'parent'); ctx.read(scope, ['occurrence_id']); ctx.read(`${scope}/shot`, ['shot_id']);
  for (const path of MAP_FIELDS) ctx.read(scope, path);
  const row = ctx.state.occurrence(scope);
  if (row.placement != null && !object(row.placement)) throw new ClipMoveError('occurrence placement must be an object', 'unsupported_map');
  const start = object(row.placement) ? row.placement.start_ms : null;
  if (start != null && row.at_ms != null && Math.abs(number(start, 'placement.start_ms') - number(row.at_ms, 'at_ms')) > Math.max(1e-9, 1e-9 * Math.max(Math.abs(number(start, 'placement.start_ms')), Math.abs(number(row.at_ms, 'at_ms'))))) throw new ClipMoveError('contradictory occurrence start codecs', 'unsupported_timing');
  number(start ?? row.at_ms ?? 0, 'occurrence start');
  if (!active(row) || (row.source_offset != null && row.source_offset !== 0) || (row.speed != null && row.speed !== 1) || row.time_map != null || row.timeMap != null) throw new ClipMoveError('media edit requires an active translation-only occurrence', 'unsupported_map');
  const limit = number(row.duration_ms, 'occurrence.duration_ms', true) / 1000;
  const fps = rate(ctx.read('parent', ['config', 'output', 'fps']));
  if (!equal(rate(ctx.read(`${scope}/source`, ['output', 'fps'])), fps)) throw new ClipMoveError('parent and child fps differ', 'unsupported_timing');
  if (ctx.read(`${scope}/source`, ['source_window']) != null) throw new ClipMoveError('internal source_window is unsupported', 'unsupported_map');
  ctx.bind('media.owner', scope); return { scope, limit };
}
function clip(ctx: OccurrenceMediaRecording, scope: string, row: ObjectValue, limit: number, kind: string, inputs: VerifiedMedia[]) {
  if (![kind, 'media'].includes(String(row.clipType)) || typeof row.asset !== 'string') throw new ClipMoveError('media edit requires one matching media clip');
  if (['asset_id', 'media_id', 'object_id', 'clip_type'].some((key) => has(row, key))) throw new ClipMoveError('media edit requires one asset selector');
  for (const key of ['time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms', 'at_ms', 'duration', 'duration_ms', 'source', 'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'anchor', 'transition']) if (row[key] != null) throw new ClipMoveError(`media edit does not support ${key}`, 'unsupported_timing');
  const app = row.app, nested = object(app) ? app.astrid : null;
  for (const container of [row, app, nested]) {
    if (container != null && !object(container)) throw new ClipMoveError('intent container must be object or null');
    if (object(container) && [...RELATIONS, 'beats', 'word', 'words', 'transcript', 'source_id', 'standin', 'standin_intent'].some((key) => container[key] != null)) throw new ClipMoveError('media edit requires literal child timing', 'unsupported_timing');
  }
  const at = number(row.at, 'clip.at'), hold = number(row.hold, 'clip.hold', true), speed = number(has(row, 'speed') ? row.speed : 1, 'clip.speed', true);
  if (at < 0 || at + hold / speed > limit) throw new ClipMoveError('child interval exceeds occurrence', 'occurrence_boundary');
  if (kind === 'image') {
    if (speed !== 1 || row.from != null || row.to != null) throw new ClipMoveError('image requires hold without a source window', 'unsupported_timing');
  } else {
    const left = number(row.from, 'clip.from'), right = number(row.to, 'clip.to');
    if (left < 0 || right <= left || right - left !== hold || inputs.some((value) => right > value.duration_seconds!)) throw new ClipMoveError('source window differs from hold or exceeds media', 'unsupported_timing');
  }
  const ref = `${scope}/track:${row.track}`, track = ctx.read(ref, []);
  if (!object(track) || track.kind !== 'visual' || (has(track, 'role') && track.role !== 'output') || !active(track)) throw new ClipMoveError('media edit requires an active raw visual child track');
  ctx.bind('media.track', ref);
}
function registry(ctx: OccurrenceMediaRecording, scope: string, pin: MediaSelection, kind: string, create: boolean, alias = pin.asset) {
  if (!rawIdentity(alias)) throw new ClipMoveError('media requires a reserved raw asset alias');
  const registry = ctx.state.config(scope).registry;
  if (!object(registry) || !object(registry.assets)) throw new ClipMoveError('media edit requires an authored asset registry');
  const ref = `${scope}/asset:${alias}`, expected = { media_id: pin.object_id, type: kind, generationId: pin.generation_id, variantId: pin.variant_id }, entry = ctx.read(ref, []);
  if (create && ctx.state.get(ref, []).state === 'absent') ctx.createAsset(scope, alias, expected);
  else if (create ? !equal(entry, expected) : !object(entry) || entry.media_id !== pin.object_id || entry.type !== kind || Object.entries(expected).some(([key, value]) => has(entry, key) && entry[key] !== value)) throw new ClipMoveError('registry binding differs from exact selection', 'dependency_changed');
  if (!create && object(entry) && ['object_id', 'digest', 'content_digest', 'content_sha256', 'file', 'path', 'local_path', 'src', 'source', 'format'].some((key) => has(entry, key))) throw new ClipMoveError('unsupported old registry identity codec', 'unsupported_media');
  ctx.dependency(create ? 'media.new' : 'media.old', 'media', pin);
}

export function executeOccurrenceMedia(bundle: AuthoredBundle, supplied: OccurrenceMediaCommand, inputs: readonly VerifiedMedia[]) {
  assertFiniteJson(bundle); assertFiniteJson(supplied); assertFiniteJson(inputs);
  if (!object(supplied) || !Array.isArray(inputs) || inputs.some((value) => !object(value))) throw new ClipMoveError('media capture requires command and detached verified inputs');
  if (supplied.schema_version !== 1 || supplied.version !== '1' || supplied.op !== 'occurrence.add-media' || typeof supplied.select !== 'string' || !object(supplied.args) || !equal(Object.keys(supplied.args).sort(), ['media', 'row']) || (has(supplied, 'intent') && !equal(supplied.intent, {}) && !equal(supplied.intent, { ownership: 'occurrence' }))) throw new ClipMoveError('unsupported occurrence media command');
  const pin = supplied.args.media; selection(pin);
  const ctx = new OccurrenceMediaRecording(bundle, { ...supplied, intent: { ownership: 'occurrence' } });
  const { scope, limit } = owner(ctx, supplied.select, false);
  const row = supplied.args.row;
  if (!object(row) || !rawIdentity(row.id) || !rawIdentity(row.track) || typeof row.clipType !== 'string' || !row.clipType.length) throw new ClipMoveError('add requires a reserved raw child and track');
  const { value, kind } = verified(pin, inputs);
  if (row.asset !== pin.asset) throw new ClipMoveError('child asset must equal the reserved selection alias');
  clip(ctx, scope, row, limit, kind, [value]); registry(ctx, scope, pin, kind, true); ctx.createChild(scope, row);
  ctx.compile();
  for (const key of CLAIMS) if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
  const command: OccurrenceMediaCommand = { ...ctx.command, op: supplied.op, select: supplied.select }; ctx.record.command = command;
  return { command, record: ctx.record, bundle: ctx.state.bundle };
}

export function captureOccurrenceAddMedia(bundle: AuthoredBundle, select: string, row: ObjectValue, media: MediaSelection, inputs: readonly VerifiedMedia[]) {
  return freezeJson(executeOccurrenceMedia(bundle, { schema_version: 1, op: 'occurrence.add-media', version: '1', select, args: { row: copy(row), media: copy(media) }, intent: { ownership: 'occurrence' } }, inputs));
}

