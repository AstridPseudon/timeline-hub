import type { EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  assertFiniteJson, ClipMoveError, copy, equal, freezeJson, has, object, type MoveRecording,
  type AuthoredBundle,
} from './clipMovePrimitives.ts';
import { executeParentClipAddMedia, mediaSelection, readParentMediaAsset } from './parentClipAddCapture.ts';

type Row = Record<string, JSON>;

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RAW_PARENT_CLIP = /^parent\/clip:(?!.*::)[^/]+$/;

export type ParentAfterAnchorMediaBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
  readonly verifiedMedia: readonly VerifiedMedia[];
};

function stableId(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && !value.includes('/') && !value.includes('::');
}

function number(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new ClipMoveError(`${label} must be a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  }
  return value;
}

function clipRows(bundle: AuthoredBundle): Row[] {
  const parent = bundle.parent;
  const config = object(parent.config) ? parent.config : {};
  const direct = parent.clips;
  const mirror = config.clips;
  if (Array.isArray(direct) && Array.isArray(mirror) && !equal(direct, mirror)) {
    throw new ClipMoveError('divergent parent clip mirrors', 'identity_conflict');
  }
  const rows = Array.isArray(direct) && (direct.length > 0 || !Array.isArray(mirror) || mirror.length === 0)
    ? direct : mirror;
  if (!Array.isArray(rows)) throw new ClipMoveError('parent clips require an authored collection', 'identity_conflict');
  if (rows.some((row) => !object(row) || !stableId(row.id))) {
    throw new ClipMoveError('missing or ambiguous parent clip identity', 'identity_conflict');
  }
  const authoredRows = rows as Row[];
  if (new Set(authoredRows.map((row) => row.id as string)).size !== authoredRows.length) {
    throw new ClipMoveError('missing or ambiguous parent clip identity', 'identity_conflict');
  }
  return authoredRows;
}

function rawId(ref: string): string {
  if (!RAW_PARENT_CLIP.test(ref)) {
    throw new ClipMoveError('parent after-anchor capture requires a raw parent clip', 'unsupported_ownership');
  }
  return ref.slice('parent/clip:'.length);
}

function sourceDuration(source: Row): number {
  const duration = typeof source.hold === 'number' ? number(source.hold, 'clip.hold') :
    number(source.to ?? 0, 'clip.to') - number(source.from ?? 0, 'clip.from');
  if (duration < 0) throw new ClipMoveError('anchor source duration must not be negative', 'unsupported_timing');
  const speed = source.speed == null ? 1 : number(source.speed, 'clip.speed', true);
  return duration / speed;
}

function anchorStart(source: Row): number {
  const start = number(source.at, 'clip.at');
  if (start < 0) throw new ClipMoveError('clip.at must not be negative', 'unsupported_timing');
  if (source.at_ms != null) {
    const milliseconds = number(source.at_ms, 'clip.at_ms') / 1000;
    if (Math.abs(milliseconds - start) > Math.max(1e-9, 1e-9 * Math.max(Math.abs(milliseconds), Math.abs(start)))) {
      throw new ClipMoveError('contradictory at/at_ms timing codecs', 'unsupported_timing');
    }
  }
  return start;
}

function cloneAfter(source: Row, requested: Row, media: MediaSelection): Row {
  if (!stableId(requested.id)) throw new ClipMoveError('after-anchor birth requires a reserved destination id');
  if (has(requested, 'track') && requested.track !== source.track) {
    throw new ClipMoveError('after-anchor birth cannot change the source track', 'unsupported_ownership');
  }
  if (has(requested, 'asset') && requested.asset !== media.asset) {
    throw new ClipMoveError('after-anchor birth asset differs from the reserved selection', 'dependency_changed');
  }
  const start = anchorStart(source) + Math.max(0.05, sourceDuration(source));
  const row = copy(source);
  row.id = requested.id;
  row.asset = media.asset;
  if (has(source, 'at')) row.at = start;
  if (has(source, 'at_ms')) row.at_ms = start * 1000;
  for (const key of ['effectId', 'effect_id']) {
    if (has(source, key) || has(requested, key)) row[key] = copy(has(requested, key) ? requested[key] : `effect-${requested.id}`);
  }
  return row;
}

function rippleAfterAnchor(ctx: MoveRecording, row: Row, media: MediaSelection): string[] {
  const anchor = ctx.command.select!;
  const members = mediaSelection(ctx, 'collection.clips.after', anchor);
  const index = members.indexOf(anchor);
  if (index < 0) throw new ClipMoveError('parent after-anchor is missing', 'selection_changed');
  const source = ctx.read(anchor, []);
  if (!object(source) || source.track !== row.track) {
    throw new ClipMoveError('after-anchor track changed', 'dependency_changed');
  }
  if (typeof source.asset !== 'string') throw new ClipMoveError('anchor has no raw media identity', 'unsupported_media');
  readParentMediaAsset(ctx, source.asset);
  ctx.bind('parent.after-clip', anchor);
  ctx.bind('parent.after-track', `parent/track:${source.track}`);
  if (!equal(cloneAfter(source, row, media), row)) {
    throw new ClipMoveError('after-anchor row is not the captured source clone', 'capture_mismatch');
  }
  const duration = Math.max(0.05, sourceDuration(source));
  for (const ref of members.slice(index + 1)) {
    if (ctx.read(ref, ['track']) !== source.track) continue;
    const peer = ctx.read(ref, []);
    if (!object(peer)) throw new ClipMoveError('parent clip membership changed', 'dependency_changed');
    const shifted = anchorStart(peer) + duration;
    ctx.write(ref, ['at'], shifted);
    if (has(peer, 'at_ms')) ctx.write(ref, ['at_ms'], shifted * 1000);
  }
  return members;
}

function validateCommand(command: EditCommand): void {
  const allowed = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS];
  if (Object.keys(command).some((key) => !allowed.includes(key)) || command.schema_version !== 1 ||
    command.op !== 'clip.add-media' || command.version !== '1' || typeof command.select !== 'string' ||
    !RAW_PARENT_CLIP.test(command.select) || !object(command.args) ||
    !equal(Object.keys(command.args).sort(), ['media', 'row'].sort()) || !object(command.args.row) ||
    !object(command.args.media) || !equal(command.intent, {})) {
    throw new ClipMoveError('parent after-anchor capture requires the closed clip.add-media envelope');
  }
}

export function executeParentClipAddMediaAfterAnchor(
  bundle: AuthoredBundle, command: EditCommand, inputs: readonly VerifiedMedia[],
) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  assertFiniteJson(inputs);
  validateCommand(command);
  return executeParentClipAddMedia(bundle, command, inputs, (ctx) =>
    rippleAfterAnchor(ctx, command.args.row as Row, command.args.media as MediaSelection));
}

export function captureParentClipAddMediaAfterAnchor(
  bundle: AuthoredBundle, anchor: string, row: Row, media: MediaSelection, inputs: readonly VerifiedMedia[],
): ParentAfterAnchorMediaBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(row);
  assertFiniteJson(media);
  rawId(anchor);
  const members = clipRows(bundle).map((item) => `parent/clip:${item.id}`);
  const index = members.indexOf(anchor);
  if (index < 0) throw new ClipMoveError('parent after-anchor is missing', 'selection_changed');
  const source = clipRows(bundle)[index];
  const clone = cloneAfter(source, row, media);
  const command: EditCommand = {
    schema_version: 1, op: 'clip.add-media', version: '1', select: anchor,
    args: { row: clone, media: copy(media) }, intent: {},
  };
  const result = executeParentClipAddMediaAfterAnchor(bundle, command, inputs);
  return freezeJson({ bundle: copy(bundle), command: result.command, verifiedMedia: copy(inputs) });
}

export function finishParentClipAddMediaAfterAnchor(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) || !Array.isArray(basis.verifiedMedia) ||
    !CLAIMS.every((key) => has(basis.command as Row, key))) {
    throw new ClipMoveError('incomplete parent after-anchor clip.add-media basis');
  }
  return executeParentClipAddMediaAfterAnchor(
    basis.bundle as AuthoredBundle, basis.command as EditCommand, basis.verifiedMedia as VerifiedMedia[],
  );
}

export const captureParentAfterAnchorMedia = captureParentClipAddMediaAfterAnchor;
export const finishParentAfterAnchorMedia = finishParentClipAddMediaAfterAnchor;
export const executeParentAfterAnchorMedia = executeParentClipAddMediaAfterAnchor;
