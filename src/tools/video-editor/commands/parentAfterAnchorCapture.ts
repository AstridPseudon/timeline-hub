import type { AgentBinding, AgentRead, AgentSelection, AgentState, EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  assertFiniteJson, ClipMoveError, copy, equal, freezeJson, has, object,
  type AuthoredBundle,
} from './clipMovePrimitives.ts';
import { executeParentClipAddMedia } from './parentClipAddCapture.ts';

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
  const hold = source.hold;
  const sourceDuration = hold != null ? number(hold, 'clip.hold', true) :
    number(source.to, 'clip.to') - number(source.from, 'clip.from');
  if (sourceDuration <= 0) throw new ClipMoveError('anchor source duration must be positive', 'unsupported_timing');
  const speed = source.speed == null ? 1 : number(source.speed, 'clip.speed', true);
  return sourceDuration / speed;
}

function anchorStart(source: Row): number {
  const start = number(source.at, 'clip.at');
  if (start < 0) throw new ClipMoveError('clip.at must not be negative', 'unsupported_timing');
  if (source.at_ms != null && !Object.is(number(source.at_ms, 'clip.at_ms') / 1000, start)
    && Math.abs(number(source.at_ms, 'clip.at_ms') / 1000 - start) > 1e-9) {
    throw new ClipMoveError('contradictory at/at_ms timing codecs', 'unsupported_timing');
  }
  return start;
}

function cloneAfter(source: Row, requested: Row, media: MediaSelection): Row {
  if (!stableId(requested.id)) throw new ClipMoveError('after-anchor birth requires a reserved destination id');
  if (requested.track != null && requested.track !== source.track) {
    throw new ClipMoveError('after-anchor birth cannot change the source track', 'unsupported_ownership');
  }
  if (requested.asset != null && requested.asset !== media.asset) {
    throw new ClipMoveError('after-anchor birth asset differs from the reserved selection', 'dependency_changed');
  }
  const start = anchorStart(source) + Math.max(0.05, sourceDuration(source));
  const row = copy(source);
  row.id = requested.id;
  row.asset = media.asset;
  if (has(source, 'at')) row.at = start;
  if (has(source, 'at_ms')) row.at_ms = start * 1000;
  for (const key of ['effectId', 'effect_id']) {
    if (has(source, key) || has(requested, key)) row[key] = copy(requested[key] ?? `effect-${requested.id}`);
  }
  return row;
}

function state(bundle: AuthoredBundle, ref: string, path: string[] = []): AgentState {
  const parent = bundle.parent;
  const config = object(parent.config) ? parent.config : {};
  if (ref.startsWith('parent/asset:')) {
    const alias = ref.slice('parent/asset:'.length);
    const containers = [parent.registry, config.registry];
    const values = containers.filter((registry): registry is Row => object(registry))
      .map((registry) => object(registry.assets) ? registry.assets[alias] : undefined)
      .filter((value): value is JSON => value !== undefined);
    const value = values[0];
    return value === undefined ? { state: 'absent' } : { state: 'present', value: copy(value) };
  }
  const rowId = ref.slice('parent/clip:'.length);
  const matches = clipRows(bundle).filter((row) => row.id === rowId);
  if (matches.length !== 1) return { state: 'absent' };
  let value: JSON = matches[0];
  for (const key of path) {
    if (!object(value) || !has(value, key)) return { state: 'absent' };
    value = value[key];
  }
  return { state: 'present', value: copy(value) };
}

function read(command: EditCommand, ref: string, path: string[], value: AgentState): void {
  const item: AgentRead = { ref, path, state: value };
  if (!command.reads!.some((prior) => equal(prior, item))) command.reads!.push(item);
}

function selection(command: EditCommand, value: AgentSelection): void {
  if (!command.selections!.some((prior) => equal(prior, value))) command.selections!.push(value);
}

function addBinding(
  command: EditCommand,
  bindings: AgentBinding[],
  key: string,
  ref: string,
  dependencies: string[] = [],
): void {
  command.bindings![key] = ref;
  if (!bindings.some((item) => item.key === key && item.ref === ref)) {
    bindings.push({ key, ref, policy: 'fixed', dependencies });
  }
}

function decorate(
  bundle: AuthoredBundle,
  command: EditCommand,
  result: ReturnType<typeof executeParentClipAddMedia>,
  anchor: string,
  source: Row,
  members: string[],
): ReturnType<typeof executeParentClipAddMedia> {
  command.select = anchor;
  // clip.add-media is a non-singleton operation; the raw select carries the
  // insertion anchor and no resolved target projection is manufactured.
  command.resolved = [];
  const recordBindings = result.record.bindings;
  read(command, anchor, [], { state: 'present', value: copy(source) });
  read(command, `parent/asset:${source.asset}`, [], state(bundle, `parent/asset:${source.asset}`));
  selection(command, {
    key: 'collection.clips.after', query_version: 1, owner: 'parent', members: [anchor],
    order: [...members], boundaries: members.slice(members.indexOf(anchor), members.indexOf(anchor) + 2),
    policy: 'guard-membership',
  });
  addBinding(command, recordBindings, 'parent.after-clip', anchor);
  addBinding(command, recordBindings, 'parent.after-track', `parent/track:${source.track}`);

  const duration = Math.max(0.05, sourceDuration(source));
  const anchorIndex = members.indexOf(anchor);
  const later = members.slice(anchorIndex + 1);
  const originalConfigRows = object(bundle.parent.config) && Array.isArray(bundle.parent.config.clips)
    ? copy(bundle.parent.config.clips) as Row[] : undefined;
  const shiftedConfigRows = originalConfigRows ? copy(originalConfigRows) : undefined;
  if (shiftedConfigRows) {
    for (const peer of shiftedConfigRows.slice(anchorIndex + 1)) {
      if (peer.track !== source.track) continue;
      peer.at = number(peer.at, 'clip.at') + duration;
      if (has(peer, 'at_ms')) peer.at_ms = number(peer.at_ms, 'clip.at_ms') + duration * 1000;
    }
  }
  const peerWrites = [];
  for (const ref of later) {
    const peer = clipRows(bundle).find((row) => `parent/clip:${row.id}` === ref);
    if (!peer) throw new ClipMoveError('parent clip membership changed', 'dependency_changed');
    read(command, ref, ['track'], { state: 'present', value: peer.track });
    if (peer.track !== source.track) continue;
    read(command, ref, [], { state: 'present', value: copy(peer) });
    const shifted = anchorStart(peer) + duration;
    const paths = [['at'], ...(has(peer, 'at_ms') ? [['at_ms']] : [])];
    for (const path of paths) {
      const before = state(bundle, ref, path);
      const value = path[0] === 'at' ? shifted : shifted * 1000;
      const after: AgentState = { state: 'present', value };
      const address = `${ref}::${path.join('.')}`;
      command.expect![address] = before;
      command.authorship![address] = 'direct';
      peerWrites.push({ ref, path, before, after });
    }
  }
  const commandRow = command.args.row as Row;
  const clipWriteIndex = result.record.writes.findIndex((write) => write.ref === `parent/clip:${commandRow.id}`);
  const insertAt = clipWriteIndex < 0 ? result.record.writes.length : clipWriteIndex;
  result.record.writes.splice(insertAt, 0, ...peerWrites);
  result.record.reads = command.reads!;
  result.record.selections = command.selections!;
  result.record.bindings = recordBindings;

  const outputRows = (value: JSON): Row[] | undefined => Array.isArray(value) ? value as Row[] : undefined;
  const parentRows = outputRows(result.bundle.parent.clips);
  const configRows = outputRows(object(result.bundle.parent.config) ? result.bundle.parent.config.clips : null);
  for (const rows of [parentRows, configRows]) {
    if (!rows) continue;
    const index = rows.findIndex((row) => object(row) && row.id === source.id);
    if (index < 0) throw new ClipMoveError('anchor disappeared during after-anchor capture', 'dependency_changed');
    for (const peer of rows.slice(index + 1)) {
      if (peer.track !== source.track) continue;
      peer.at = number(peer.at, 'clip.at') + duration;
      if (has(peer, 'at_ms')) peer.at_ms = number(peer.at_ms, 'clip.at_ms') + duration * 1000;
    }
    const created = rows.findIndex((row) => object(row) && row.id === commandRow.id);
    if (created >= 0) rows.splice(created, 1);
    rows.splice(index + 1, 0, copy(command.args.row as Row));
  }
  if (originalConfigRows && shiftedConfigRows && configRows) {
    result.record.derived_writes = [
      { ref: 'parent', path: ['config', 'clips'], before: { state: 'present', value: originalConfigRows },
        after: { state: 'present', value: shiftedConfigRows }, cause: 0 },
      { ref: 'parent', path: ['config', 'clips'], before: { state: 'present', value: shiftedConfigRows },
        after: { state: 'present', value: copy(configRows) }, cause: 0 },
    ];
  }
  return result;
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
  const anchor = command.select as string;
  const requested = command.args.row as Row;
  const media = command.args.media as MediaSelection;
  const members = clipRows(bundle).map((row) => `parent/clip:${row.id}`);
  const anchorIndex = members.indexOf(anchor);
  if (anchorIndex < 0) throw new ClipMoveError('parent after-anchor is missing', 'selection_changed');
  const source = clipRows(bundle)[anchorIndex];
  const row = cloneAfter(source, requested, media);
  if (!equal(row, requested)) throw new ClipMoveError('after-anchor row is not the captured source clone', 'capture_mismatch');
  const baseCommand = copy(command);
  baseCommand.select = 'parent';
  for (const key of CLAIMS) delete baseCommand[key];
  // The existing append capture intentionally rejects the legacy at_ms field.
  // Agent's after-anchor source preserves and records it, so use the existing
  // validator for the common row shape and restore this authored codec below.
  const executableRow = copy(requested);
  delete executableRow.at_ms;
  baseCommand.args.row = executableRow;
  const result = executeParentClipAddMedia(bundle, baseCommand, inputs);
  result.command.args.row = copy(requested);
  const createdWrite = result.record.writes.find((write) => write.ref === `parent/clip:${requested.id}`);
  if (createdWrite) createdWrite.after = { state: 'present', value: copy(requested) };
  const decorated = decorate(bundle, result.command, result, anchor, source, members);
  for (const key of CLAIMS) {
    if (has(command, key) && !equal(command[key], decorated.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(decorated.command, copy(command));
  return decorated;
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
