// @vitest-environment node
import { beforeAll, describe, expect, it } from 'vitest';
import type { CanonicalDocument, CommandRecord, EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { AuthoredState, ClipMoveError, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { captureClipMove, finishClipMove } from './clipMoveCapture.ts';
import { captureParentMediaSwap, executeParentMediaSwap, finishParentMediaSwap } from './parentMediaSwapCapture.ts';
import fixture from './fixtures/recipe_m2_media_swap.json';

// Byte-exact Agent e8f7c2c890254d700b6235d411ebca1101ded218 native execution golden.
// SHA-256 8b82f593693376e022edb81107611f104374b42d8b4ae3f26b3b90d8a55af05a.
type Row = Record<string, JSON>;
const target = 'parent/clip:clip-a';
const command = fixture.commands[0] as EditCommand;
const old = command.args.old_media as MediaSelection, media = command.args.media as MediaSelection;
const verified = fixture.verified_media as VerifiedMedia[];
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const clips = (bundle: AuthoredBundle) => bundle.parent.clips as Row[];
const mirror = (bundle: AuthoredBundle) => (bundle.parent.config as Row).clips as Row[];
const assets = (bundle: AuthoredBundle) => (bundle.parent.registry as Row).assets as Record<string, Row>;
const tracks = (bundle: AuthoredBundle) => (bundle.parent.config as Row).tracks as Row[];
let original: AuthoredBundle;
beforeAll(async () => { original = await authoringBundleFromDocument(fixture.input as CanonicalDocument); });
const capture = (bundle = original, values = verified) => captureParentMediaSwap(bundle, target, old, media, values);

function video() {
  const bundle = copy(original), values = copy(verified);
  for (const entry of Object.values(assets(bundle))) entry.type = 'video';
  for (const rows of [clips(bundle), mirror(bundle)]) Object.assign(rows[0], { from: 2, to: 6, speed: 2 });
  for (const value of values) Object.assign(value, { media_type: 'video/fixture', duration_seconds: 6 });
  return { bundle, values };
}

describe('native parent-only media swap capture', () => {
  it('matches the unmodified native command and actual record exactly', () => {
    const basis = capture();
    const result = finishParentMediaSwap(basis);
    expect(result.command).toEqual(command);
    expect(result.record).toEqual(fixture.records[0] as CommandRecord);
    expect(result.bundle.parent.clips).toEqual(fixture.output.parent_revision.payload.clips);
    expect(result.bundle.parent.config).toEqual(fixture.output.parent_revision.payload.config);
    expect(executeParentMediaSwap(original, command, verified)).toEqual(result);
    expect(finishParentMediaSwap(roundtrip(basis))).toEqual(result);
    expect(original).toEqual(basis.bundle);
    expect(result.command.created).toEqual([]);
    expect(result.record.created).toEqual([]);
  });

  it('freezes the detached original closure, both pins and verified inputs before preview', () => {
    const bundle = copy(original), oldPin = copy(old), newPin = copy(media), values = copy(verified);
    const basis = captureParentMediaSwap(bundle, target, oldPin, newPin, values);
    const persisted = roundtrip(basis);
    bundle.base_parent = { revision_id: 'new-head', content_digest: 'sha256:new' };
    bundle.source_mapping = {};
    clips(bundle)[0].asset = 'foreign';
    oldPin.variant_id = 'rotated';
    newPin.catalog_digest = 'sha256:rotated';
    values[0].selection.object_id = 'sha256:rotated';
    values[1].media_type = 'audio/foreign';
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.bundle.parent)).toBe(true);
    expect(Object.isFrozen(basis.command.reads)).toBe(true);
    expect(Object.isFrozen(basis.command.args.media)).toBe(true);
    expect(Object.isFrozen(basis.verified_media[0].selection)).toBe(true);
    expect(finishParentMediaSwap(persisted)).toEqual(finishParentMediaSwap(basis));
    expect(persisted.bundle.base_parent).toEqual(original.base_parent);
    expect(persisted.bundle.source_mapping).toEqual(original.source_mapping);
    expect(finishParentMediaSwap(persisted).command).toEqual(command);
  });

  it('changes only the asset and equal clip mirror, preserving IDs, opaque state and source closure', () => {
    const bundle = copy(original);
    for (const rows of [clips(bundle), mirror(bundle)]) rows[0].opaque = { ordered: [null, false, 0, {}, []], absent: null };
    const result = finishParentMediaSwap(capture(bundle));
    const expected = copy(bundle);
    clips(expected)[0].asset = media.asset;
    mirror(expected)[0].asset = media.asset;
    expect(result.bundle).toEqual(expected);
    expect(result.bundle.shots).toEqual(bundle.shots);
    expect(result.bundle.placements).toEqual(bundle.placements);
    expect(result.bundle.parent.registry).toEqual(bundle.parent.registry);
    expect(result.bundle.source_mapping).toEqual(bundle.source_mapping);
  });

  it('preserves the exact video source window, speed and half-open end without quantization', () => {
    const { bundle, values } = video();
    const result = finishParentMediaSwap(capture(bundle, values));
    expect(new AuthoredState(result.bundle).entity(target)).toEqual({ ...clips(bundle)[0], asset: media.asset });
    expect(result.record.writes).toHaveLength(1);
    expect(result.command.reads!.some((read) => read.path.includes('fps'))).toBe(false);
    values[1].duration_seconds = 5.999;
    expect(() => capture(bundle, values)).toThrow('window exceeds');
    expect(clips(bundle)[0].asset).toBe(old.asset);
  });

  it('records a same-value asset write with no derived rewrite or allocated identity', () => {
    const basis = captureParentMediaSwap(original, target, old, old, verified);
    const result = finishParentMediaSwap(basis);
    expect(result.bundle).toEqual(original);
    expect(result.record.writes).toHaveLength(1);
    expect(result.record.writes[0].before).toEqual(result.record.writes[0].after);
    expect(result.record.derived_writes).toEqual([]);
    expect(result.record.dependencies.map((item) => item.pin)).toEqual([old, old]);
    expect(result.command.created).toEqual([]);
  });

  it('composes over a moved original basis without rewriting literal app intent', () => {
    const moved = finishClipMove(captureClipMove(original, target), 3.003);
    const swapped = finishParentMediaSwap(capture(moved.bundle));
    expect(new AuthoredState(swapped.bundle).entity(target)).toEqual({ ...clips(moved.bundle)[0], asset: media.asset });
    expect(finishParentMediaSwap(roundtrip(capture(moved.bundle)))).toEqual(swapped);
    expect(swapped.command.expect).toEqual(command.expect);
  });

  it('retains disjoint values and newer head images with the original command guards', () => {
    const head = copy(original);
    for (const rows of [clips(head), mirror(head)]) rows[1].params = { opaque: [null, false] };
    head.base_parent = { revision_id: 'new', content_digest: 'sha256:new' };
    tracks(head)[0].label = 'disjoint label';
    assets(head).unrelated = { opaque: [] };
    const before = copy(head);
    const result = executeParentMediaSwap(head, command, verified);
    expect(result.command).toEqual(command);
    expect(clips(result.bundle)[1].params).toEqual({ opaque: [null, false] });
    expect(result.bundle.base_parent).toEqual(head.base_parent);
    expect(assets(result.bundle).unrelated).toEqual({ opaque: [] });
    expect(head).toEqual(before);
  });

  it('preserves divergent mirrors instead of overwriting unrelated compiled rows', () => {
    const head = copy(original);
    mirror(head)[1].opaque = ['compiled sentinel'];
    const result = executeParentMediaSwap(head, command, verified);
    expect(result.command).toEqual(command);
    expect(result.record.derived_writes).toEqual([]);
    expect(mirror(result.bundle)).toEqual(mirror(head));
    expect(clips(result.bundle)[0].asset).toBe(media.asset);
  });

  it.each(['nested-registry', 'both-registries', 'absent-mirror', 'null-mirror', 'absent-payload', 'null-payload'])(
    'preserves native authored codec layout: %s', (layout) => {
    const bundle = copy(original), config = bundle.parent.config as Row;
    if (layout.endsWith('registry') || layout === 'both-registries') config.registry = copy(bundle.parent.registry);
    if (layout === 'nested-registry') delete bundle.parent.registry;
    if (layout === 'absent-mirror') delete config.clips;
    if (layout === 'null-mirror') config.clips = null;
    if (layout === 'absent-payload') delete bundle.parent.clips;
    if (layout === 'null-payload') bundle.parent.clips = null;
    const result = finishParentMediaSwap(capture(bundle));
    expect(new AuthoredState(result.bundle).entity(target)!.asset).toBe(media.asset);
    expect(result.bundle.parent.registry).toEqual(bundle.parent.registry);
    expect((result.bundle.parent.config as Row).registry).toEqual(config.registry);
    expect(result.record.derived_writes).toHaveLength(layout.includes('registr') ? 1 : 0);
  });

  it.each(['asset', 'clip-id', 'clip-opaque', 'track', 'old-registry', 'new-registry', 'codec-absence'])(
    'refuses a changed relevant original guard: %s', (change) => {
    const head = copy(original);
    if (change === 'asset') clips(head)[0].asset = media.asset;
    if (change === 'clip-id') clips(head)[0].id = 'different';
    if (change === 'clip-opaque') clips(head)[0].opaque = true;
    if (change === 'track') tracks(head)[0].kind = 'audio';
    if (change === 'old-registry') assets(head)[old.asset].opaque = false;
    if (change === 'new-registry') assets(head)[media.asset].opaque = null;
    if (change === 'codec-absence') (head.parent.config as Row).registry = copy(head.parent.registry);
    const before = copy(head);
    expect(() => executeParentMediaSwap(head, command, verified)).toThrow(ClipMoveError);
    expect(head).toEqual(before);
    expect(finishParentMediaSwap(capture()).command).toEqual(command);
  });

  it.each(['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'] as const)(
    'requires both complete immutable pins without refreshing %s', (field) => {
    for (const index of [0, 1]) {
      const values = copy(verified);
      values[index].selection[field] = 'foreign';
      expect(() => executeParentMediaSwap(original, command, values)).toThrow('exact Runtime-verified');
    }
  });

  it('refuses missing, conflicting duplicate, foreign-kind and malformed verified metadata', () => {
    expect(() => capture(original, verified.slice(0, 1))).toThrow('exact Runtime-verified');
    const conflicting = [...copy(verified), { ...copy(verified[1]), size: 124 }];
    expect(() => capture(original, conflicting)).toThrow('exact Runtime-verified');
    expect(finishParentMediaSwap(capture(original, [...verified, copy(verified[1])])).command).toEqual(command);
    for (const patch of [{ media_type: 'audio/fixture' }, { size: 0 }, { size: 1.5 }, { media_type: 'image' }]) {
      expect(() => capture(original, [verified[0], { ...verified[1], ...patch }])).toThrow(ClipMoveError);
    }
  });

  it.each(['missing-slot', 'null-slot', 'wrong-object', 'digest', 'content_sha256', 'generationId', 'variantId', 'locator'])(
    'never creates or repairs an existing registry binding: %s', (damage) => {
    const bundle = copy(original), entry = assets(bundle)[media.asset];
    if (damage === 'missing-slot') delete assets(bundle)[media.asset];
    else if (damage === 'null-slot') (assets(bundle) as Row)[media.asset] = null;
    else entry[damage === 'wrong-object' ? 'media_id' : damage === 'locator' ? 'file' : damage] = 'foreign';
    const before = copy(bundle);
    expect(() => capture(bundle)).toThrow(ClipMoveError);
    expect(bundle).toEqual(before);
  });

  it.each([
    ['asset_id', null], ['time_map', {}], ['from', 0], ['source_uuid', 'old-transcript'],
    ['app', { astrid: { on: 'word:old:0' } }], ['app', { astrid: { words: [[0, 1, 'old']] } }],
    ['speed', 2], ['speed', null], ['hold', 0], ['at', -1], ['at_ms', 1000], ['duration', 2],
    ['app', false], ['clipType', 'audio'], ['anchor', {}],
  ])('refuses unsupported source/timing semantics: %s', (field, value) => {
    const bundle = copy(original);
    clips(bundle)[0][field as string] = value as JSON;
    const before = copy(bundle);
    expect(() => capture(bundle)).toThrow(ClipMoveError);
    expect(bundle).toEqual(before);
  });

  it.each(['clip-a', 'occurrence:occ-a/clip:clip-a', 'parent/clip:display::id', 'parent/clip:missing', 'parent'])(
    'refuses non-parent, display or missing selectors: %s', (select) => {
    expect(() => captureParentMediaSwap(original, select, old, media, verified)).toThrow(ClipMoveError);
  });

  it('keeps closed native args and selectors; no clear, descriptor, URL or generic replacement', () => {
    for (const args of [{ ...command.args, media_record: {} }, { ...command.args, clear: ['asset'] },
      { ...command.args, media: null }, { ...command.args, media: { ...media, sourceURL: 'display.png' } },
      { ...command.args, media: { ...media, catalog_digest: 'display.png' } }, { media }]) {
      expect(() => executeParentMediaSwap(original, { ...command, args }, verified)).toThrow(ClipMoveError);
    }
    for (const patch of [{ extra: true }, { intent: { ownership: 'shared' } }, { version: '2' }, { group_id: '' }, { rationale: null }]) {
      expect(() => executeParentMediaSwap(original, { ...command, ...patch } as EditCommand, verified)).toThrow(ClipMoveError);
    }
  });

  it.each(['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const)(
    'refuses incomplete and forged %s claims after JSON roundtrip', (key) => {
    const basis = roundtrip(capture());
    delete basis.command[key];
    expect(() => finishParentMediaSwap(basis)).toThrow('incomplete');
    const forged = copy(command);
    Object.assign(forged, { [key]: ['expect', 'authorship', 'bindings'].includes(key) ? {} : [] });
    // Native created is empty; a nonempty claim is the forged case.
    if (key === 'created') forged.created = ['parent/clip:invented'];
    expect(() => executeParentMediaSwap(original, forged, verified)).toThrow('original capture');
  });

  it.each([
    ['undefined', undefined], ['NaN', NaN], ['infinity', Infinity], ['bigint', 1n],
    ['date', new Date(0)], ['map', new Map()], ['undefined element', [undefined]], ['sparse array', Array(1)],
  ])('refuses raw non-finite/non-JSON input before copying: %s', (_name, value) => {
    const bundle = copy(original);
    Object.assign(bundle.parent, { opaque: value });
    expect(() => capture(bundle)).toThrow('finite JSON');
    const basis = roundtrip(capture());
    Object.assign(basis.bundle.parent, { opaque: value });
    expect(() => finishParentMediaSwap(basis)).toThrow('finite JSON');
    Object.assign(basis.verified_media[0], { opaque: value });
    expect(() => executeParentMediaSwap(original, command, basis.verified_media)).toThrow('finite JSON');
    expect(() => captureParentMediaSwap(original, target, old, { ...media, opaque: value } as MediaSelection, verified)).toThrow('finite JSON');
  });

  it('rejects cyclic inputs and an incomplete verified-media basis', () => {
    const bundle = copy(original);
    bundle.parent.cycle = bundle.parent;
    expect(() => capture(bundle)).toThrow('finite JSON');
    const basis = roundtrip(capture());
    expect(() => finishParentMediaSwap({ bundle: basis.bundle, command: basis.command })).toThrow('incomplete');
    expect(() => finishParentMediaSwap({ ...basis, verified_media: [] })).toThrow('exact Runtime-verified');
  });
});
