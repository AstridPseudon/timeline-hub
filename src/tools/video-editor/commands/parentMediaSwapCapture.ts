import type { EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { ClipMoveError, MoveRecording, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type Row = Record<string, JSON>;
const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RELATIONS = ['until', 'until_film_end', 'cut', 'sequence', 'sequence_index', 'sequence_fit',
  'orphan', 'formulas', 'beats', 'word', 'words', 'transcript', 'source_id', 'standin', 'standin_intent'];

function number(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new ClipMoveError(`${label} must be a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  }
  return value;
}

function selection(value: unknown): asserts value is MediaSelection {
  const keys = ['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'];
  if (!object(value) || !equal(Object.keys(value).sort(), [...keys].sort()) ||
    !keys.every((key) => typeof value[key] === 'string' && value[key].length > 0) ||
    !['object_id', 'catalog_digest'].every((key) => /^sha256:[0-9a-f]{64}$/.test(String(value[key])))) {
    throw new ClipMoveError('swap requires the exact five-field Runtime media selection');
  }
}

function verified(pin: MediaSelection, values: readonly VerifiedMedia[]) {
  const matches = values.filter((row) => object(row) && equal(row.selection, pin));
  if (!matches.length || matches.some((row) => !equal(row, matches[0]))) {
    throw new ClipMoveError('swap requires exact Runtime-verified media input', 'dependency_changed');
  }
  const value = matches[0];
  const kind = typeof value.media_type === 'string' && value.media_type.includes('/') ? value.media_type.split('/')[0] : undefined;
  if ((kind !== 'image' && kind !== 'video') || !Number.isInteger(value.size) || value.size <= 0) {
    throw new ClipMoveError('swap v1 requires verified image/video metadata', 'unsupported_media');
  }
  if (kind === 'video') number(value.duration_seconds, 'intrinsic duration', true);
  return { value, kind };
}

function registry(ctx: MoveRecording, pin: MediaSelection, value: VerifiedMedia, kind: string): void {
  const entries = [[], ['config']].map((prefix) => ctx.read('parent', [...prefix, 'registry', 'assets', pin.asset]))
    .filter((entry) => entry != null);
  if (!entries.length || entries.some((entry) => !object(entry))) {
    throw new ClipMoveError('swap requires an existing explicit registry binding', 'identity_conflict');
  }
  for (const entry of entries as Row[]) {
    if (entry.media_id !== pin.object_id || (entry.type !== kind && entry.type !== value.media_type)) {
      throw new ClipMoveError('registry binding differs from verified media', 'dependency_changed');
    }
    for (const key of ['object_id', 'digest', 'content_digest', 'content_sha256']) {
      if (has(entry, key) && entry[key] !== (key === 'content_sha256' ? pin.object_id.slice(7) : pin.object_id)) {
        throw new ClipMoveError('contradictory registry media identity', 'dependency_changed');
      }
    }
    for (const [key, field] of [['generationId', 'generation_id'], ['variantId', 'variant_id']] as const) {
      if (has(entry, key) && entry[key] !== pin[field]) throw new ClipMoveError('registry generation/variant differs from selection', 'dependency_changed');
    }
    if (['file', 'path', 'local_path', 'src', 'source', 'format'].some((key) => entry[key] != null)) {
      throw new ClipMoveError('swap v1 does not support registry source locators', 'unsupported_media');
    }
  }
}

/** Local execution of Agent e8f7c2c89; media authority and accepted history stay on Runtime/Agent. */
export function executeParentMediaSwap(bundle: AuthoredBundle, command: EditCommand, verifiedMedia: readonly VerifiedMedia[]) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  assertFiniteJson(verifiedMedia);
  const fields = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS];
  if (!object(command) || Object.keys(command).some((key) => !fields.includes(key)) ||
    (has(command, 'rationale') && typeof command.rationale !== 'string') ||
    (has(command, 'group_id') && (typeof command.group_id !== 'string' || !command.group_id)) ||
    command.schema_version !== 1 || command.op !== 'clip.swap-media' || command.version !== '1' ||
    typeof command.select !== 'string' || !/^parent\/clip:(?!.*::)[^/]+$/.test(command.select) ||
    !object(command.args) || !equal(Object.keys(command.args).sort(), ['media', 'old_media']) ||
    (has(command, 'intent') && !equal(command.intent, {}))) {
    throw new ClipMoveError('unsupported parent clip.swap-media v1 command');
  }
  const old = command.args.old_media, replacement = command.args.media;
  selection(old);
  selection(replacement);
  const ref = command.select;
  const ctx = new MoveRecording(bundle, { ...command, intent: {} });
  if (!equal(ctx.select('media.target', 'parent', [ref]), [ref])) throw new ClipMoveError('swap target disappeared', 'identity_conflict');
  const clip = ctx.read(ref, []) as Row;
  if (!['media', 'image', 'video'].includes(String(clip.clipType)) || clip.asset !== old.asset) {
    throw new ClipMoveError('swap requires the exact old media selection', 'dependency_changed');
  }
  if (['asset_id', 'media_id', 'object_id', 'clip_type'].some((key) => has(clip, key))) {
    throw new ClipMoveError('swap v1 requires one asset selector', 'unsupported_media');
  }
  for (const key of ['time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms', 'source',
    'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'anchor']) {
    if (clip[key] != null) throw new ClipMoveError(`swap v1 does not support ${key}`, 'unsupported_timing');
  }
  const app = clip.app, nested = object(app) ? app.astrid : undefined;
  for (const container of [clip, app, nested]) {
    if (container == null) continue;
    if (!object(container)) throw new ClipMoveError('swap intent containers must be objects or null');
    if (RELATIONS.some((key) => container[key] != null)) {
      throw new ClipMoveError('swap v1 requires literal timing without source anchors', 'unsupported_timing');
    }
    for (const [field, timing] of [['on', 'at'], ['for', 'hold']]) {
      if (container[field] != null && !equal(number(container[field], field), clip[timing])) {
        throw new ClipMoveError('swap literal intent contradicts timing', 'unsupported_timing');
      }
    }
    if (container.fixed_start != null && container.fixed_start !== true) {
      throw new ClipMoveError('swap requires fixed literal timing', 'unsupported_timing');
    }
  }
  number(clip.at, 'clip.at');
  number(clip.hold, 'clip.hold', true);
  if ((clip.at as number) < 0 || ['at_ms', 'duration', 'duration_ms'].some((key) => clip[key] != null)) {
    throw new ClipMoveError('swap v1 requires literal at/hold seconds', 'unsupported_timing');
  }
  const previous = verified(old, verifiedMedia), next = verified(replacement, verifiedMedia);
  if (previous.kind !== next.kind || (clip.clipType !== 'media' && clip.clipType !== next.kind)) {
    throw new ClipMoveError('swap v1 preserves media kind', 'unsupported_media');
  }
  if (ctx.read(`parent/track:${String(clip.track)}`, ['kind']) !== 'visual') {
    throw new ClipMoveError('swap v1 requires a visual track');
  }
  for (const [key, pin, media] of [['media.old', old, previous.value], ['media.new', replacement, next.value]] as const) {
    registry(ctx, pin, media, next.kind);
    ctx.dependency(key, 'media', pin);
  }
  const speed = number(has(clip, 'speed') ? clip.speed : 1, 'clip.speed', true);
  if (next.kind === 'image') {
    if (['from', 'to'].some((key) => clip[key] != null) || speed !== 1) {
      throw new ClipMoveError('still swap requires hold timing without source windows', 'unsupported_timing');
    }
  } else {
    const left = number(clip.from, 'clip.from'), right = number(clip.to, 'clip.to', true);
    if (left < 0 || right <= left || [previous.value, next.value].some((value) => right > value.duration_seconds!)) {
      throw new ClipMoveError('swap source window exceeds verified media', 'unsupported_timing');
    }
    if (!equal((right - left) / speed, clip.hold)) throw new ClipMoveError('swap source window contradicts hold', 'unsupported_timing');
  }
  ctx.bind('media.target', ref, ['media.old', 'media.new']);
  ctx.write(ref, ['asset'], replacement.asset);
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(command, key) && !equal(command[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(ctx.command, copy(command), { intent: {} });
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

// Local capture only; detached Runtime media inputs are never command args or proof of acceptance.
export type ParentMediaSwapBasis = {
  readonly bundle: AuthoredBundle; readonly command: EditCommand; readonly verified_media: readonly VerifiedMedia[];
};

export function captureParentMediaSwap(bundle: AuthoredBundle, select: string, oldMedia: MediaSelection,
  media: MediaSelection, verifiedMedia: readonly VerifiedMedia[]): ParentMediaSwapBasis {
  const { command } = executeParentMediaSwap(bundle, {
    schema_version: 1, op: 'clip.swap-media', version: '1', select, args: { old_media: oldMedia, media },
  }, verifiedMedia);
  return freezeJson({ bundle: copy(bundle), command, verified_media: copy(verifiedMedia) });
}

/** Finish uses only the original capture, including after a finite-JSON outbox roundtrip. */
export function finishParentMediaSwap(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) || !Array.isArray(basis.verified_media) ||
    !CLAIMS.every((key) => has(basis.command as Row, key))) throw new ClipMoveError('incomplete parent media swap basis');
  return executeParentMediaSwap(basis.bundle as AuthoredBundle, basis.command as EditCommand,
    basis.verified_media as VerifiedMedia[]);
}
