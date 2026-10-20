import type { AgentState, EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { ClipMoveError, MoveRecording, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type Row = Record<string, JSON>;

const MEDIA_SELECTION_KEYS = ['asset', 'catalog_digest', 'generation_id', 'object_id', 'variant_id'];
const MEDIA_CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const MEDIA_RELATIONS = ['on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence',
  'sequence_index', 'sequence_fit', 'orphan', 'formulas'];

function identity(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && !value.includes('/') && !value.includes('::');
}

function mediaNumber(value: unknown, label: string, positive = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new ClipMoveError(`${label} must be a finite ${positive ? 'positive ' : ''}number`, 'unsupported_timing');
  }
  return value;
}

function mediaRate(value: unknown): void {
  if (value == null) return;
  if (object(value) && equal(Object.keys(value).sort(), ['denominator', 'numerator'])) {
    const numerator = value.numerator, denominator = value.denominator;
    if (typeof numerator !== 'number' || typeof denominator !== 'number' ||
      !Number.isSafeInteger(numerator) || !Number.isSafeInteger(denominator) || numerator <= 0 || denominator <= 0) {
      throw new ClipMoveError('fps rational must be positive', 'unsupported_timing');
    }
    return;
  }
  mediaNumber(value, 'fps', true);
}

function validateMediaSelection(value: unknown): asserts value is MediaSelection {
  if (!object(value) || !equal(Object.keys(value).sort(), [...MEDIA_SELECTION_KEYS].sort()) ||
    !['asset', 'generation_id', 'variant_id'].every((key) => typeof value[key] === 'string' && value[key].length > 0) ||
    !['object_id', 'catalog_digest'].every((key) => typeof value[key] === 'string' &&
      /^sha256:[0-9a-f]{64}$/.test(value[key] as string))) {
    throw new ClipMoveError('media requires a closed immutable five-field selection');
  }
}

function verifiedMedia(pin: MediaSelection, inputs: readonly VerifiedMedia[]): { value: VerifiedMedia; kind: 'image' | 'video' } {
  const matches = inputs.filter((input) => equal(input.selection, pin));
  if (!matches.length || matches.some((input) => !equal(input, matches[0]))) {
    throw new ClipMoveError('media edit requires exact Runtime-verified media input', 'dependency_changed');
  }
  const value = matches[0];
  const kind = typeof value.media_type === 'string' && value.media_type.includes('/')
    ? value.media_type.split('/')[0] : '';
  if (kind !== 'image' && kind !== 'video' || !Number.isInteger(value.size) || value.size <= 0) {
    throw new ClipMoveError('media edit requires verified image/video metadata', 'unsupported_media');
  }
  if (kind === 'video') mediaNumber(value.duration_seconds, 'intrinsic duration', true);
  return { value, kind };
}

function mediaRead(ctx: MoveRecording, ref: string, value: AgentState): void {
  const read = { ref, path: [], state: copy(value) };
  if (!ctx.command.reads!.some((prior) => equal(prior, read))) ctx.command.reads!.push(read);
}

function mediaTagged(container: JSON | undefined, key: string): AgentState {
  if (!object(container) || !has(container, key)) return { state: 'absent' };
  const value = container[key];
  return { state: 'present', value: Array.isArray(value) ? [] : object(value) ? {} : copy(value) };
}

function mediaCollectionShape(bundle: AuthoredBundle, kind: 'track' | 'occurrence' | 'asset' | 'clip'): JSON {
  const parent = bundle.parent;
  const config = object(parent.config) ? parent.config : {};
  if (kind === 'occurrence') return { container: 'array' };
  if (kind === 'asset') {
    const direct = object(parent.registry) ? parent.registry : parent.registry;
    const nested = object(config.registry) ? config.registry : config.registry;
    return {
      '0': { registry: mediaTagged(parent, 'registry'), assets: mediaTagged(direct, 'assets') },
      '1': { registry: mediaTagged(config, 'registry'), assets: mediaTagged(nested, 'assets') },
    };
  }
  const shape: Record<string, JSON> = { members: mediaTagged(config, `${kind}s`) };
  if (kind === 'track' || kind === 'clip') shape.config = mediaTagged(parent, 'config');
  if (kind === 'clip') shape.payload_members = mediaTagged(parent, 'clips');
  return shape;
}

function mediaRows(bundle: AuthoredBundle, kind: 'track' | 'clip'): JSON[] {
  const parent = bundle.parent;
  const config = object(parent.config) ? parent.config : {};
  const direct = parent.clips, mirror = config.clips;
  if (kind === 'clip') {
    if (Array.isArray(direct) && Array.isArray(mirror) && !equal(direct, mirror)) {
      throw new ClipMoveError('divergent parent clip mirrors', 'identity_conflict');
    }
    if (!Array.isArray(direct) && !Array.isArray(mirror)) {
      throw new ClipMoveError('structural edit requires an authored entity collection', 'identity_conflict');
    }
    return (Array.isArray(direct) && (direct.length > 0 || !Array.isArray(mirror) || mirror.length === 0)
      ? direct : mirror) as JSON[];
  }
  if (!Array.isArray(config.tracks)) throw new ClipMoveError('structural edit requires an authored entity collection', 'identity_conflict');
  return config.tracks;
}

function mediaSelection(ctx: MoveRecording, key: 'collection.tracks' | 'collection.occurrences' | 'collection.clips'): string[] {
  const kind = key === 'collection.tracks' ? 'track' : key === 'collection.clips' ? 'clip' : 'occurrence';
  mediaRead(ctx, `parent/collection:${kind}`, { state: 'present', value: mediaCollectionShape(ctx.state.bundle, kind) });
  const rows = kind === 'occurrence' ? ctx.state.bundle.placements : mediaRows(ctx.state.bundle, kind);
  const ids = rows.map((row) => object(row) ? row[kind === 'occurrence' ? 'occurrence_id' : 'id'] : undefined);
  if (ids.some((id) => !identity(id)) || new Set(ids).size !== ids.length) {
    throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
  }
  const members = ids.map((id) => kind === 'occurrence' ? `occurrence:${id}` : `parent/${kind}:${id}`);
  ctx.command.selections!.push({ key, query_version: 1, owner: 'parent', members: [...members],
    order: [...members], boundaries: [...members], policy: 'guard-membership' });
  return members;
}

function mediaRegistry(ctx: MoveRecording, alias: string, pin: MediaSelection, kind: 'image' | 'video'): void {
  if (!identity(alias)) throw new ClipMoveError('media requires a reserved raw asset alias');
  const parent = ctx.state.bundle.parent;
  const config = object(parent.config) ? parent.config : {};
  const direct = has(parent, 'registry') ? parent.registry : undefined;
  const nested = has(config, 'registry') ? config.registry : undefined;
  for (const registry of [direct, nested]) {
    if (registry != null && (!object(registry) || (has(registry, 'assets') && !object(registry.assets)))) {
      throw new ClipMoveError('media edit requires an authored asset registry', 'identity_conflict');
    }
  }
  if (direct != null && nested != null && !equal(direct, nested)) {
    throw new ClipMoveError('parent.registry conflicts with parent.config.registry', 'identity_conflict');
  }
  mediaRead(ctx, 'parent/collection:asset', { state: 'present', value: mediaCollectionShape(ctx.state.bundle, 'asset') });
  const path = has(parent, 'registry') || !has(config, 'registry') ? ['registry'] : ['config', 'registry'];
  ctx.object('parent', path);
  ctx.object('parent', [...path, 'assets']);
  // Equal parent registry mirrors are one effective registry. Record the
  // container creation once, then materialize it in both authored mirrors.
  if (path.length === 1 && object(config.registry) && !has(config.registry, 'assets')) {
    ctx.state.set('parent', ['config', 'registry', 'assets'], { state: 'present', value: {} });
  }
  const registry = (path.length === 1 ? parent.registry : config.registry) as Record<string, JSON>;
  const assetMap = registry.assets as Record<string, JSON>;
  const ref = `parent/asset:${alias}`;
  const before: AgentState = has(assetMap, alias) ? { state: 'present', value: copy(assetMap[alias]) } : { state: 'absent' };
  mediaRead(ctx, ref, before);
  const expected: JSON = { media_id: pin.object_id, type: kind, generationId: pin.generation_id, variantId: pin.variant_id };
  if (before.state === 'present' && !equal(before.value, expected)) {
    throw new ClipMoveError('existing registry binding differs from exact selection', 'dependency_changed');
  }
  if (before.state === 'absent') {
    if (!has(ctx.command.expect!, `${ref}::`)) ctx.command.expect![`${ref}::`] = before;
    ctx.command.authorship![`${ref}::`] = 'direct';
    const after: AgentState = { state: 'present', value: copy(expected) };
    ctx.record.writes.push({ ref, path: [], before, after });
    if (object(parent.registry)) (parent.registry.assets as Record<string, JSON>)[alias] = copy(expected);
    if (object(config.registry)) (config.registry.assets as Record<string, JSON>)[alias] = copy(expected);
    ctx.record.created.push({ ref, kind: 'asset', owner: 'parent' });
    ctx.command.created!.push(ref);
  }
  ctx.dependency('media.new', 'media', pin);
}

function validateParentMediaCommand(command: EditCommand): { row: Row; media: MediaSelection } {
  const fields = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...MEDIA_CLAIMS];
  if (Object.keys(command).some((key) => !fields.includes(key)) ||
    (has(command, 'rationale') && typeof command.rationale !== 'string') ||
    (has(command, 'group_id') && (typeof command.group_id !== 'string' || !command.group_id))) {
    throw new ClipMoveError('clip.add-media requires the closed EditCommand envelope');
  }
  if (command.schema_version !== 1 || command.op !== 'clip.add-media' || command.version !== '1' || command.select !== 'parent' ||
    !object(command.args) || !equal(Object.keys(command.args).sort(), ['media', 'row'].sort()) || !object(command.args.row)) {
    throw new ClipMoveError('clip.add-media requires parent ownership and row/media args');
  }
  if (command.intent !== undefined && !equal(command.intent, {})) throw new ClipMoveError('unsupported operation intention policy');
  validateMediaSelection(command.args.media);
  const row = command.args.row;
  if (!identity(row.id) || !identity(row.track) || typeof row.clipType !== 'string' || !row.clipType ||
    typeof row.asset !== 'string' || !identity(row.asset)) {
    throw new ClipMoveError('clip.add-media requires stable raw clip and asset identities');
  }
  return { row, media: command.args.media };
}

function validateMediaRow(ctx: MoveRecording, row: Row, kind: 'image' | 'video', input: VerifiedMedia): void {
  if (row.clipType !== 'media' && row.clipType !== kind ||
    ['asset_id', 'media_id', 'object_id', 'clip_type'].some((key) => has(row, key))) {
    throw new ClipMoveError('media edit requires one matching media clip');
  }
  for (const key of ['time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms', 'at_ms', 'duration', 'duration_ms',
    'source', 'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'anchor']) {
    if (row[key] != null) throw new ClipMoveError(`media edit does not support ${key}`, 'unsupported_timing');
  }
  const app = row.app, nested = object(app) ? app.astrid : undefined;
  for (const container of [row, app, nested]) {
    if (container != null && !object(container)) throw new ClipMoveError('intent container must be object or null');
    if (object(container) && [...MEDIA_RELATIONS, 'beats', 'word', 'words', 'transcript', 'source_id']
      .some((key) => container[key] != null)) throw new ClipMoveError('media edit requires literal child timing', 'unsupported_timing');
  }
  if (row.transition != null) throw new ClipMoveError('media edit does not support transition', 'unsupported_timing');
  const at = mediaNumber(row.at, 'clip.at'), hold = mediaNumber(row.hold, 'clip.hold', true);
  const speed = row.speed == null ? 1 : mediaNumber(row.speed, 'clip.speed', true);
  if (at < 0) throw new ClipMoveError('clip.at must be non-negative', 'unsupported_timing');
  if (kind === 'image') {
    if (speed !== 1 || row.from != null || row.to != null) throw new ClipMoveError('image requires hold without a source window', 'unsupported_timing');
  } else {
    const from = mediaNumber(row.from, 'clip.from'), to = mediaNumber(row.to, 'clip.to');
    if (from < 0 || to <= from || to - from !== hold || to > mediaNumber(input.duration_seconds, 'intrinsic duration', true)) {
      throw new ClipMoveError('source window differs from hold or exceeds media', 'unsupported_timing');
    }
  }
  const trackRef = `parent/track:${row.track}`;
  mediaSelection(ctx, 'collection.tracks');
  const track = ctx.read(trackRef, []);
  if (!object(track) || track.kind !== 'visual' || (has(track, 'role') && track.role !== 'output') ||
    track.enabled === false || track.active === false || ['disabled', 'hidden', 'deleted'].some((key) => track[key] === true)) {
    throw new ClipMoveError('media edit requires an active raw visual track', 'unsupported_ownership');
  }
  ctx.bind('media.track', trackRef);
}

/** Local authored execution of Agent clip.add-media; Runtime remains the authority for media selection. */
export function executeParentClipAddMedia(
  bundle: AuthoredBundle, command: EditCommand, inputs: readonly VerifiedMedia[],
) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  assertFiniteJson(inputs);
  if (!Array.isArray(inputs) || inputs.some((input) => !object(input))) {
    throw new ClipMoveError('media capture requires detached verified inputs');
  }
  const { row, media } = validateParentMediaCommand(command);
  const { value, kind } = verifiedMedia(media, inputs);
  const ctx = new MoveRecording(bundle, { ...copy(command), intent: {} });
  ctx.command.intent = {};
  ctx.command.resolved = [];
  mediaRate(ctx.read('parent', ['config', 'output', 'fps']));
  if (ctx.read('parent/source', ['source_window']) != null) {
    throw new ClipMoveError('parent source_window is unsupported', 'unsupported_map');
  }
  ctx.bind('media.owner', 'parent');
  validateMediaRow(ctx, row, kind, value);
  for (const occurrence of mediaSelection(ctx, 'collection.occurrences')) {
    for (const path of [['placement', 'track'], ['track']]) {
      if (ctx.read(occurrence, path) === row.track) {
        throw new ClipMoveError('track is the lane of an occurrence-owned shot', 'unsupported_ownership');
      }
    }
  }
  mediaRegistry(ctx, row.asset as string, media, kind);
  const members = mediaSelection(ctx, 'collection.clips');
  const ref = `parent/clip:${row.id}`;
  if (members.includes(ref)) throw new ClipMoveError('created identity is occupied', 'identity_collision');
  ctx.read(ref, []);
  ctx.command.expect![`${ref}::`] = { state: 'absent' };
  ctx.command.authorship![`${ref}::`] = 'direct';
  ctx.record.writes.push({ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: copy(row) } });
  ctx.record.created.push({ ref, kind: 'clip', owner: 'parent' });
  ctx.command.created!.push(ref);
  const parent = ctx.state.bundle.parent;
  const config = ctx.state.config('parent');
  const direct = parent.clips, mirror = config.clips;
  const rows = Array.isArray(direct) && (direct.length > 0 || !Array.isArray(mirror) || mirror.length === 0)
    ? direct : mirror;
  if (!Array.isArray(rows)) throw new ClipMoveError('structural edit requires an authored entity collection', 'identity_conflict');
  rows.push(copy(row));
  if (Array.isArray(direct) && Array.isArray(mirror)) {
    const before = ctx.state.get('parent', ['config', 'clips']);
    const after: AgentState = { state: 'present', value: copy(direct) };
    if (!equal(before, after)) {
      ctx.record.derived_writes.push({ ref: 'parent', path: ['config', 'clips'], before, after, cause: 0 });
      ctx.state.set('parent', ['config', 'clips'], after);
    }
  }
  ctx.compile();
  for (const key of MEDIA_CLAIMS) {
    if (has(command, key) && !equal(command[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  Object.assign(ctx.command, copy(command), { intent: {} });
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

/** Caller reserves the clip/asset IDs and keeps the original verified selection for retry. */
export type ParentClipAddMediaBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
  readonly verifiedMedia: readonly VerifiedMedia[];
};

export function captureParentClipAddMedia(
  bundle: AuthoredBundle, row: Row, media: MediaSelection, inputs: readonly VerifiedMedia[],
): ParentClipAddMediaBasis {
  const command: EditCommand = { schema_version: 1, op: 'clip.add-media', version: '1', select: 'parent',
    args: { row: copy(row), media: copy(media) }, intent: {} };
  const result = executeParentClipAddMedia(bundle, command, inputs);
  return freezeJson({ bundle: copy(bundle), command: result.command, verifiedMedia: copy(inputs) });
}

export function finishParentClipAddMedia(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) || !Array.isArray(basis.verifiedMedia) ||
    !MEDIA_CLAIMS.every((key) => has(basis.command as Row, key))) {
    throw new ClipMoveError('incomplete parent clip.add-media basis');
  }
  return executeParentClipAddMedia(
    basis.bundle as AuthoredBundle, basis.command as EditCommand, basis.verifiedMedia as VerifiedMedia[],
  );
}
