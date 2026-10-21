import type { AgentSelection, AgentState, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import {
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

type Row = Record<string, JSON>;

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const RELATIONS = ['on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence',
  'sequence_index', 'sequence_fit', 'orphan', 'formulas'];
const EXTRA_RELATIONS = ['anchor', 'standin', 'standin_intent', 'words', 'beats'];

export type ClipSplitArgs = {
  readonly on: number;
  readonly right_id: string;
};

export type ClipSplitBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
};

function number(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new ClipMoveError(`${label} must be a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  }
  return value;
}
function close(a: number, b: number): boolean {
  return Math.abs(a - b) <= Math.max(1e-9, 1e-9 * Math.max(Math.abs(a), Math.abs(b)));
}

function present(value: JSON): AgentState {
  return { state: 'present', value: copy(value) };
}

function tagged(container: unknown, key: string): AgentState {
  if (!object(container) || !has(container, key)) return { state: 'absent' };
  const value = container[key];
  return present(Array.isArray(value) ? [] : object(value) ? {} : value);
}

function identity(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && !value.includes('/') && !value.includes('::');
}

/** Read-only collection validation shared by native capture and ingress preflight. */
export function parentClipSplitRows(parent: AuthoredBundle['parent']): Row[] {
  const config = has(parent, 'config') ? parent.config : {};
  if (!object(config)) throw new ClipMoveError('collection owner must be an object', 'identity_conflict');
  const payload = parent.clips;
  const mirror = config.clips;
  if (Array.isArray(payload) && Array.isArray(mirror) && !equal(payload, mirror)) {
    throw new ClipMoveError('divergent parent clip mirrors', 'identity_conflict');
  }
  const rows = Array.isArray(payload) &&
    (payload.length > 0 || !Array.isArray(mirror) || mirror.length === 0)
    ? payload : mirror;
  if (!Array.isArray(rows)) {
    throw new ClipMoveError('structural edit requires an authored entity collection', 'identity_conflict');
  }
  if (!rows.every(object)) throw new ClipMoveError('invalid clip collection', 'identity_conflict');
  const ids = rows.map((row) => row.id);
  if (!ids.every(identity) || new Set(ids).size !== ids.length) {
    throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  }
  return rows as Row[];
}

function readCollection(ctx: MoveRecording): void {
  const state: AgentState = present({
    members: tagged(ctx.state.config('parent'), 'clips'),
    config: tagged(ctx.state.bundle.parent, 'config'),
    payload_members: tagged(ctx.state.bundle.parent, 'clips'),
  });
  const read = { ref: 'parent/collection:clip', path: [], state };
  if (!ctx.command.reads!.some((other) => equal(other, read))) ctx.command.reads!.push(read);
}

function selectCollection(ctx: MoveRecording, rows: Row[]): string[] {
  readCollection(ctx);
  const members = rows.map((row) => `parent/clip:${row.id}`);
  const selection: AgentSelection = {
    key: 'collection.clips', query_version: 1, owner: 'parent', members: [...members],
    order: [...members], boundaries: [...members], policy: 'guard-membership',
  };
  ctx.command.selections!.push(selection);
  return members;
}

function selectAfter(ctx: MoveRecording, members: string[], target: string): void {
  const index = members.indexOf(target);
  if (index < 0) throw new ClipMoveError('create-after requires one existing stable member', 'selection_changed');
  ctx.command.selections!.push({
    key: 'collection.clips.after', query_version: 1, owner: 'parent', members: [target],
    order: [...members], boundaries: members.slice(index, index + 2), policy: 'guard-membership',
  });
}

function rate(value: JSON | undefined): number {
  if (value == null) return 30;
  if (object(value) && equal(Object.keys(value).sort(), ['denominator', 'numerator'])) {
    const numerator = value.numerator;
    const denominator = value.denominator;
    if (typeof numerator !== 'number' || typeof denominator !== 'number' ||
      !Number.isInteger(numerator) || !Number.isInteger(denominator) || numerator <= 0 || denominator <= 0) {
      throw new ClipMoveError('fps rational requires positive integers', 'unsupported_timing');
    }
    return numerator / denominator;
  }
  return number(value, 'fps', true);
}

function rounded(value: number): bigint {
  if (!Number.isFinite(value)) throw new ClipMoveError('frame value must be finite');
  return BigInt(Math.floor(value + 0.5));
}

function mediaKind(source: Row): string | undefined {
  if (typeof source.type !== 'string') return undefined;
  return source.type.trim().toLowerCase().split(';', 1)[0].split('/', 1)[0].split('-', 1)[0];
}

function duration(row: Row): number {
  const at = number(row.at, 'at');
  if (at < 0) throw new ClipMoveError('split requires a non-negative authored start', 'unsupported_timing');
  const hold = row.hold;
  let sourceDuration: number;
  if (typeof hold === 'number' && !Number.isNaN(hold)) {
    if (!Number.isFinite(hold) || hold < 0) throw new ClipMoveError('hold must be finite and non-negative', 'unsupported_timing');
    sourceDuration = hold;
  } else {
    const from = row.from == null ? 0 : number(row.from, 'from');
    const to = row.to == null ? 0 : number(row.to, 'to');
    if (from > to) throw new ClipMoveError('from must not be greater than to', 'unsupported_timing');
    sourceDuration = to - from;
  }
  const speed = row.speed == null ? 1 : number(row.speed, 'speed', true);
  const result = sourceDuration / speed;
  if (!Number.isFinite(result)) throw new ClipMoveError('split requires a finite duration', 'unsupported_timing');
  return result;
}

function rootCreate(ctx: MoveRecording, rows: Row[], target: string, right: Row): void {
  const ref = `parent/clip:${right.id}`;
  if (rows.some((row) => row.id === right.id)) {
    throw new ClipMoveError('created identity is occupied', 'identity_collision');
  }
  ctx.read(ref, []);
  ctx.command.expect![`${ref}::`] = { state: 'absent' };
  ctx.command.authorship![`${ref}::`] = 'direct';
  ctx.record.writes.push({ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: copy(right) } });
  ctx.record.created.push({ ref, kind: 'clip', owner: 'parent' });
  ctx.command.created!.push(ref);
  const index = rows.findIndex((row) => row.id === target);
  if (index < 0) throw new ClipMoveError('split target disappeared', 'identity_conflict');
  rows.splice(index + 1, 0, copy(right));
}

function validateCommand(command: EditCommand): void {
  const allowed = new Set(['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS]);
  if (Object.keys(command).some((key) => !allowed.has(key)) ||
    (has(command, 'rationale') && typeof command.rationale !== 'string') ||
    (has(command, 'group_id') && (typeof command.group_id !== 'string' || !command.group_id))) {
    throw new ClipMoveError('clip.split requires the closed EditCommand envelope');
  }
  if (command.schema_version !== 1 || command.op !== 'clip.split' || command.version !== '1' ||
    typeof command.select !== 'string' || !/^parent\/clip:(?!.*::)[^/]+$/.test(command.select)) {
    throw new ClipMoveError('clip.split v1 requires a literal parent clip identity');
  }
  if (!object(command.args) || !equal(Object.keys(command.args).sort(), ['on', 'right_id']) ||
    typeof command.args.right_id !== 'string' || !identity(command.args.right_id)) {
    throw new ClipMoveError('clip.split requires on and a caller-reserved right_id');
  }
  number(command.args.on, 'on');
  if (has(command, 'intent') && !equal(command.intent, {})) {
    throw new ClipMoveError('clip.split has no intention overrides');
  }
}

function apply(bundle: AuthoredBundle, supplied: EditCommand) {
  validateCommand(supplied);
  const ref = supplied.select as string;
  const ctx = new MoveRecording(bundle, { ...supplied, intent: {} });
  for (const created of supplied.created ?? []) {
    if (ctx.state.entity(created, true) !== undefined) {
      throw new ClipMoveError('created identity is occupied', 'identity_collision');
    }
  }
  const rows = parentClipSplitRows(ctx.state.bundle.parent);
  const members = selectCollection(ctx, rows);
  if (!members.includes(ref)) throw new ClipMoveError('split target disappeared', 'identity_conflict');

  const target = ctx.state.entity(ref);
  if (!target) throw new ClipMoveError('split target disappeared', 'identity_conflict');
  ctx.read(ref, []);
  if (target.clipType !== 'media' || typeof target.asset !== 'string') {
    throw new ClipMoveError('clip.split v1 requires registry-backed media');
  }
  const source = ctx.read('parent/registry', ['assets', target.asset]);
  if (!object(source) || !['image', 'video', 'audio'].includes(mediaKind(source) ?? '')) {
    throw new ClipMoveError('clip.split v1 requires a known media source');
  }
  for (const key of ['clip_type', 'asset_id', 'media_id', 'object_id', 'at_ms', 'from_ms', 'to_ms',
    'duration', 'duration_ms', 'time_map', 'timeMap', 'clips', 'children', 'transition', 'effects',
    'animation', 'animations', 'keyframes', 'enter', 'exit', 'continuous']) {
    if (target[key] !== undefined && target[key] !== null) {
      throw new ClipMoveError(`clip.split v1 does not support ${key}`);
    }
  }
  const params = target.params;
  if (object(params) && ['keyframes', 'animation', 'animations', 'effects', 'fade_in', 'fade_out',
    'volume_curve', 'fadeIn', 'fadeOut', 'fadeInCurve', 'fadeOutCurve'].some((key) =>
    params[key] !== undefined && params[key] !== null)) {
    throw new ClipMoveError('clip.split v1 does not support animated media parameters');
  }

  const literalFor: Array<{ path: string[]; value: number }> = [];
  for (const prefix of [[], ['app'], ['app', 'astrid']]) {
    let container: JSON | undefined = target;
    for (const key of prefix) container = object(container) ? container[key] : undefined;
    if (container === undefined || container === null) continue;
    if (!object(container)) throw new ClipMoveError('split intent container must be object or null');
    for (const key of [...RELATIONS, ...EXTRA_RELATIONS]) {
      const value = container[key];
      if (value !== undefined && value !== null) {
        if (key === 'fixed_start' && value === true) continue;
        if (key !== 'for') throw new ClipMoveError(`clip.split v1 does not support ${key}`);
        literalFor.push({ path: [...prefix, key], value: number(value, 'for', true) });
      }
    }
  }
  for (const other of members) {
    if (other === ref) continue;
    for (const prefix of [[], ['app'], ['app', 'astrid']]) {
      for (const key of [...RELATIONS, 'anchor', 'standin', 'standin_intent']) ctx.read(other, [...prefix, key]);
    }
    if (ctx.read(other, ['transition']) !== undefined && ctx.read(other, ['transition']) !== null) {
      throw new ClipMoveError('clip.split v1 does not support parent transitions', 'unsupported_timing');
    }
  }

  const start = number(target.at, 'at');
  const speed = target.speed == null ? 1 : number(target.speed, 'speed', true);
  const hasWindow = target.from !== undefined && target.from !== null || target.to !== undefined && target.to !== null;
  let sourceIn = 0, sourceOut = 0;
  if (hasWindow) {
    sourceIn = number(target.from, 'from');
    sourceOut = number(target.to, 'to');
    if (sourceIn < 0 || sourceOut <= sourceIn) throw new ClipMoveError('split requires a positive source window');
    if (target.hold !== undefined && target.hold !== null &&
      !close(number(target.hold, 'hold', true), sourceOut - sourceIn)) {
      throw new ClipMoveError('split requires matching hold and source window');
    }
  } else if (source.type !== 'image') {
    throw new ClipMoveError('moving media split requires an explicit source window');
  }
  const clipDuration = duration(target);
  for (const relation of literalFor) {
    if (!close(relation.value, clipDuration)) throw new ClipMoveError('split requires matching literal for and duration');
  }
  const on = number(supplied.args.on, 'on');
  if (start < 0 || !(start < on && on < start + clipDuration)) {
    throw new ClipMoveError('split position must be strictly inside the clip');
  }

  const left = copy(target), right = copy(target);
  right.id = supplied.args.right_id;
  right.at = on;
  const consumed = (on - start) * speed;
  if (target.hold !== undefined && target.hold !== null) {
    left.hold = consumed;
    right.hold = (target.hold as number) - consumed;
  }
  if (hasWindow) {
    left.to = sourceIn + consumed;
    right.from = sourceIn + consumed;
  }
  for (const relation of literalFor) {
    let leftContainer: Row = left;
    let rightContainer: Row = right;
    for (const key of relation.path.slice(0, -1)) {
      leftContainer = leftContainer[key] as Row;
      rightContainer = rightContainer[key] as Row;
    }
    const key = relation.path[relation.path.length - 1];
    leftContainer[key] = on - start;
    rightContainer[key] = start + clipDuration - on;
  }
  const fps = rate(ctx.read('parent', ['config', 'output', 'fps']));
  // Native frame sums are integers, including beyond JavaScript's safe-integer range.
  const frameDuration = (row: Row): bigint => {
    const frames = rounded(duration(row) * fps);
    return frames < 1n ? 1n : frames;
  };
  const leftEnd = rounded(start * fps) + frameDuration(left);
  const rightStart = rounded(on * fps);
  const rightEnd = rightStart + frameDuration(right);
  const originalEnd = rounded(start * fps) + frameDuration(target);
  if (leftEnd !== rightStart || rightEnd !== originalEnd) {
    throw new ClipMoveError('split must preserve half-open frame geometry');
  }

  ctx.bind('split.target', ref);
  selectAfter(ctx, members, ref);
  rootCreate(ctx, rows, ref.slice('parent/clip:'.length), right);
  for (const key of ['hold', 'to']) {
    if (has(left, key) && (!has(target, key) || !equal(target[key], left[key]))) ctx.write(ref, [key], left[key]);
  }
  for (const relation of literalFor) ctx.write(ref, relation.path, on - start);
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(ctx.command, copy(supplied), { intent: {} });
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record as CommandRecord };
}

export function executeClipSplit(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  return apply(bundle, command);
}

/** Capture the immutable authored basis before local preview; right_id is never allocated during replay. */
export function captureClipSplit(bundle: AuthoredBundle, select: string, args: ClipSplitArgs): ClipSplitBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(select);
  assertFiniteJson(args);
  const snapshot = copy(bundle);
  const result = apply(snapshot, {
    schema_version: 1, op: 'clip.split', version: '1', select,
    args: copy(args), intent: {},
  });
  return freezeJson({ bundle: snapshot, command: result.command });
}

/** Replay only the caller-reserved command against its original capture. */
export function finishClipSplit(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete clip split basis');
  }
  return apply(basis.bundle as AuthoredBundle, copy(basis.command as EditCommand));
}
