import { describe, expect, it } from 'vitest';
import type { CanonicalDocument, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureOccurrenceAddMedia, captureOccurrenceSwapMedia, executeOccurrenceMedia } from './occurrenceMediaCapture.ts';
import type { OccurrenceMediaCommand } from './occurrenceMediaCapture.ts';
import { copy, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { OccurrenceMediaState } from './occurrenceMediaPrimitives.ts';
import fixture from './fixtures/recipe_m2_occurrence_media.json';

// Expanded with the official fixture loader from Agent cf7448ed6c1298b172d004914cfe2bb8c99048e7; not Runtime acceptance.
const owner = 'occurrence:occ-a', target = `${owner}/clip:clip-a`;
const originalRow = fixture.add.commands[0].args.row;
const newPin = fixture.add.commands[0].args.media, oldPin = fixture.swap.commands[0].args.old_media;
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const state = (bundle: AuthoredBundle) => new OccurrenceMediaState(bundle);
const config = (bundle: AuthoredBundle) => state(bundle).config(owner);
const child = (bundle: AuthoredBundle) => state(bundle).entity(target)!;
const assets = (bundle: AuthoredBundle) => {
  const registry = config(bundle).registry as { assets: Record<string, JSON> };
  return registry.assets;
};
const plain = (operation: 'add' | 'swap'): OccurrenceMediaCommand => ({ schema_version: 1,
  op: operation === 'add' ? 'occurrence.add-media' : 'occurrence.swap-media', version: '1',
  select: operation === 'add' ? owner : target,
  args: operation === 'add' ? { row: copy(originalRow), media: copy(newPin) } : { old_media: copy(oldPin), media: copy(newPin) },
  intent: { ownership: 'occurrence' } });
const open = async (operation: 'add' | 'swap') => {
  const document: CanonicalDocument = { ...fixture[operation].input, schema_version: 1 };
  return authoringBundleFromDocument(document);
};

for (const operation of ['add', 'swap'] as const) {
  describe(`detached occurrence ${operation} media`, () => {
    const golden = fixture[operation];
    const capture = (bundle: AuthoredBundle, inputs: VerifiedMedia[] = copy(golden.verified_media)) => operation === 'add'
      ? captureOccurrenceAddMedia(bundle, owner, copy(originalRow), newPin, inputs)
      : captureOccurrenceSwapMedia(bundle, target, oldPin, newPin, inputs);

    it('matches both exact native commands/records and the complete authored golden output', async () => {
      const bundle = freezeJson(await open(operation)), before = copy(bundle);
      const result = capture(bundle);
      expect([result.command]).toEqual(golden.commands);
      expect([result.record]).toEqual(golden.records);
      // Canonical revision/manifest generation stays in Agent. Compare every authored
      // output field with the retained golden, preserving the entire original bundle.
      const expected = copy(bundle);
      for (const placement of expected.placements) {
        const outputOccurrence = golden.output.parent_revision.payload.occurrences.find((row) => row.occurrence_id === placement.occurrence_id)!;
        const shot = golden.output.shot_revisions.find((row) => row.revision_id === outputOccurrence.shot_revision_id)!;
        const internal = golden.output.internal_timeline_revisions.find((row) => row.revision_id === shot.internal_timeline_revision_id)!;
        expected.shots[String(placement.shot_id)].internal_timeline = copy(internal.payload);
      }
      expect(result.bundle).toEqual(expected);
      const outputParent = copy(golden.output.parent_revision.payload);
      const { occurrences, ...parent } = outputParent;
      expect(occurrences.map((row) => row.occurrence_id)).toEqual(bundle.placements.map((row) => row.occurrence_id));
      expect(result.bundle.parent).toEqual(parent);
      expect(result.bundle).toEqual(executeOccurrenceMedia(bundle, plain(operation), golden.verified_media).bundle);
      expect(executeOccurrenceMedia(bundle, roundtrip(result.command), golden.verified_media)).toEqual(result);
      expect(bundle).toEqual(before);
      expect(result.bundle.shots[String(bundle.placements[1].shot_id)]).toEqual(bundle.shots[String(bundle.placements[1].shot_id)]);
      expect(Object.isFrozen(result.command)).toBe(true);
      expect(Object.isFrozen(result.command.args.media)).toBe(true);
      expect(Object.isFrozen(result.record.writes)).toBe(true);
      expect(result.command.created).toEqual([`${owner}/asset:reserved-new`, ...(operation === 'add' ? [`${owner}/clip:reserved-child`] : [])]);
      expect(capture(bundle)).toEqual(result); // Caller-owned reserved IDs never regenerated.
    });

    it('requires an exact existing registry binding without creating or rewriting it', async () => {
      const bundle = await open(operation);
      assets(bundle)['reserved-new'] = { media_id: newPin.object_id, type: 'video', generationId: newPin.generation_id, variantId: newPin.variant_id };
      const result = capture(bundle);
      expect(result.command.created).toEqual(operation === 'add' ? [`${owner}/clip:reserved-child`] : []);
      expect(result.record.writes.some((write) => write.ref.includes('/asset:'))).toBe(false);
      expect(result.record.reads).toContainEqual({ ref: `${owner}/asset:reserved-new`, path: [], state: { state: 'present', value: assets(bundle)['reserved-new'] } });
      expect(result.record.dependencies.at(-1)).toEqual({ key: 'media.new', kind: 'media', pin: newPin, policy: 'exact' });
      expect(assets(result.bundle)['reserved-new']).toEqual(assets(bundle)['reserved-new']);
    });

    it.each([null, false, [], {}, { media_id: newPin.object_id, type: 'video' },
      { media_id: newPin.object_id, type: 'video', generationId: newPin.generation_id, variantId: newPin.variant_id, opaque: null },
      { media_id: oldPin.object_id, type: 'video', generationId: newPin.generation_id, variantId: newPin.variant_id },
    ])('refuses an occupied mismatched alias %j atomically', async (entry) => {
      const bundle = await open(operation);
      assets(bundle)['reserved-new'] = copy(entry);
      const before = copy(bundle);
      expect(() => capture(bundle)).toThrow();
      expect(bundle).toEqual(before);
    });

    it('keeps the immutable alias fixed on an identical second selection', async () => {
      const bundle = await open(operation), first = capture(bundle);
      if (operation === 'add') {
        expect(() => capture(first.bundle)).toThrow('occupied');
      } else {
        const second = captureOccurrenceSwapMedia(first.bundle, target, newPin, newPin, golden.verified_media);
        expect(second.command.created).toEqual([]);
        expect(second.record.writes).toHaveLength(1);
        expect(second.record.writes[0].before).toEqual(second.record.writes[0].after);
        expect(second.command.authorship).toEqual({ [`${target}::asset`]: 'direct' });
      }
    });

    it('preserves source seconds, noninteger speed and exact half-open bounds', async () => {
      const bundle = await open(operation), command = plain(operation);
      const row = operation === 'add' ? command.args.row as Record<string, JSON> : child(bundle);
      Object.assign(row, { at: 7, hold: 4.5, speed: 1.5, from: 1.5, to: 6 });
      const result = executeOccurrenceMedia(bundle, command, golden.verified_media);
      const ref = operation === 'add' ? `${owner}/clip:reserved-child` : target;
      expect(state(result.bundle).entity(ref)).toEqual({ ...row, asset: newPin.asset });
      row.at = 7.001;
      expect(() => executeOccurrenceMedia(bundle, command, golden.verified_media)).toThrow('exceeds occurrence');
    });

    it('supports verified images with source-free holds and preserves all opaque data', async () => {
      const bundle = await open(operation), command = plain(operation), inputs = copy(golden.verified_media);
      for (const input of inputs) { input.media_type = 'image/fixture'; delete input.duration_seconds; }
      const row = operation === 'add' ? command.args.row as Record<string, JSON> : child(bundle);
      delete row.from; delete row.to; delete row.speed;
      row.clipType = 'image'; row.hold = 1.25;
      assets(bundle).picture = { media_id: oldPin.object_id, type: 'image', opaque: [null, false] };
      const result = executeOccurrenceMedia(bundle, command, inputs);
      expect(state(result.bundle).entity(operation === 'add' ? `${owner}/clip:reserved-child` : target)).toEqual({ ...row, asset: newPin.asset });
      expect(assets(result.bundle).picture).toEqual(assets(bundle).picture);
    });

    it.each(['missing-input', 'wrong-object', 'wrong-catalog', 'duplicate-input', 'audio', 'size', 'intrinsic', 'kind',
      'parent', 'display-child', 'shared', 'track', 'map', 'window', 'zero-speed', 'negative-speed', 'boolean-speed', 'outside',
      'fps', 'source-window', 'registry', 'duplicate-child', 'duplicate-track', 'malformed-collection',
    ])('refuses %s without mutating caller state', async (damage) => {
      const bundle = await open(operation), command = plain(operation), inputs = copy(golden.verified_media);
      const row = operation === 'add' ? command.args.row as Record<string, JSON> : child(bundle);
      const pin = command.args.media as MediaSelection;
      if (damage === 'missing-input') inputs.pop();
      if (damage === 'wrong-object') pin.object_id = oldPin.object_id;
      if (damage === 'wrong-catalog') pin.catalog_digest = oldPin.catalog_digest;
      if (damage === 'duplicate-input') inputs.push({ ...copy(inputs[1]), size: 999 });
      if (damage === 'audio') inputs[1].media_type = 'audio/wav';
      if (damage === 'size') inputs[1].size = 0.5;
      if (damage === 'intrinsic') inputs[1].duration_seconds = 5.999;
      if (damage === 'kind') inputs[1].media_type = 'image/fixture';
      if (damage === 'parent') command.select = 'parent';
      if (damage === 'display-child') command.select = `${owner}/clip:occ-a:clip-a`;
      if (damage === 'shared') command.intent = { ownership: 'shared' };
      if (damage === 'track') (config(bundle).tracks as Record<string, JSON>[])[0].hidden = true;
      if (damage === 'map') state(bundle).occurrence(owner).source_offset = 1;
      if (damage === 'window') row.to = 7;
      if (damage === 'zero-speed') row.speed = 0;
      if (damage === 'negative-speed') row.speed = -1;
      if (damage === 'boolean-speed') row.speed = true;
      if (damage === 'outside') row.at = 9;
      if (damage === 'fps') config(bundle).output = { fps: 30 };
      if (damage === 'source-window') config(bundle).source_window = { from: 0, to: 10 };
      if (damage === 'registry') config(bundle).registry = null;
      if (damage === 'duplicate-child') (config(bundle).clips as JSON[]).push(copy(child(bundle)));
      if (damage === 'duplicate-track') (config(bundle).tracks as JSON[]).push({ id: 'picture', kind: 'visual' });
      if (damage === 'malformed-collection') config(bundle).tracks = {};
      const before = copy(bundle), originalCommand = copy(command), originalInputs = copy(inputs);
      expect(() => executeOccurrenceMedia(bundle, command, inputs)).toThrow();
      expect(bundle).toEqual(before);
      expect(command).toEqual(originalCommand);
      expect(inputs).toEqual(originalInputs);
    });

    it.each(['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const)('rejects forged %s and stale capture', async (key) => {
      const bundle = await open(operation), captured = capture(bundle);
      const command = copy(captured.command);
      if (key === 'authorship' || key === 'expect' || key === 'bindings') command[key] = {};
      else command[key] = [];
      expect(() => executeOccurrenceMedia(bundle, command, golden.verified_media)).toThrow('original capture');
      state(bundle).occurrence(owner).duration_ms = 11000;
      expect(() => executeOccurrenceMedia(bundle, captured.command, golden.verified_media)).toThrow('original capture');
    });
  });
}

describe('native occurrence media input boundaries', () => {
  it.each(['owners', 'pool', 'groups', 'children'])('retains the current native ADD %s guard on replay', async (change) => {
    const bundle = await open('add');
    const captured = captureOccurrenceAddMedia(bundle, owner, originalRow, newPin, fixture.add.verified_media);
    if (change === 'owners') bundle.placements[1].shot_id = bundle.placements[0].shot_id;
    if (change === 'pool') config(bundle).app = { astrid: { pool: ['changed'] } };
    if (change === 'groups') (bundle.parent.config as Record<string, JSON>).pinnedShotGroups = [];
    if (change === 'children') (config(bundle).clips as JSON[]).push({ id: 'intervening-child' });
    const before = copy(bundle);
    expect(() => executeOccurrenceMedia(bundle, captured.command, fixture.add.verified_media)).toThrow();
    expect(bundle).toEqual(before);
  });

  it.each(['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'])('requires the immutable %s field', async (key) => {
    const command = plain('add'), pin = command.args.media as Record<string, JSON>;
    delete pin[key];
    const bundle = await open('add');
    expect(() => executeOccurrenceMedia(bundle, command, fixture.add.verified_media)).toThrow('five-field');
  });
});

for (const operation of ['add', 'swap'] as const) {
  describe(`occurrence ${operation} unsupported authored codecs`, () => {
    it.each(['asset_id', 'media_id', 'object_id', 'clip_type', 'time_map', 'children', 'from_ms', 'at_ms', 'duration',
      'source', 'sourceURL', 'anchor', 'transition', 'on', 'word', 'standin', 'app', 'nested-relation',
    ])('refuses %s without losing authored fields', async (key) => {
      const bundle = await open(operation), command = plain(operation);
      const row = operation === 'add' ? command.args.row as Record<string, JSON> : child(bundle);
      if (key === 'nested-relation') row.app = { astrid: { on: null, until: 2 } };
      else row[key] = key === 'asset_id' ? null : key === 'app' ? false : 1;
      const before = copy(bundle);
      expect(() => executeOccurrenceMedia(bundle, command, fixture[operation].verified_media)).toThrow();
      expect(bundle).toEqual(before);
    });

    it.each(['source_offset', 'speed', 'time_map', 'timeMap', 'active', 'placement', 'duration_ms'])('refuses invalid occurrence %s', async (key) => {
      const bundle = await open(operation);
      state(bundle).occurrence(owner)[key] = key === 'active' ? false : key === 'placement' ? [] : key === 'duration_ms' ? 0 : true;
      expect(() => executeOccurrenceMedia(bundle, plain(operation), fixture[operation].verified_media)).toThrow();
    });

    it.each(['path', 'object_id', 'digest', 'source', 'generationId', 'variantId'])('refuses incompatible old registry %s', async (key) => {
      const bundle = await open('swap'), binding = assets(bundle).picture as Record<string, JSON>;
      binding[key] = null;
      expect(() => captureOccurrenceSwapMedia(bundle, target, oldPin, newPin, fixture.swap.verified_media)).toThrow();
    });
  });
}

describe('closed capture inputs', () => {
  it.each([
    { schema_version: 2 }, { version: '2' }, { op: 'clip.add' }, { select: null }, { intent: null },
    { intent: { ownership: 'occurrence', ripple: 'none' } }, { args: {} },
    { args: { row: originalRow, media: newPin, intrinsic: {} } },
    { args: { row: originalRow, media: { ...newPin, duration_seconds: 6 } } },
    { args: { row: { ...originalRow, id: 'parent/clip:reserved-child' }, media: newPin } },
    { args: { row: { ...originalRow, asset: 'different' }, media: newPin } },
    { args: { row: { ...originalRow, track: '' }, media: newPin } },
    { args: { row: { ...originalRow, hold: null }, media: newPin } },
    { args: { row: { ...originalRow, speed: null }, media: newPin } },
    { args: { row: { ...originalRow, from: 0, to: 6 }, media: newPin } },
    { args: { row: { ...originalRow, at: -1 }, media: newPin } },
  ])('refuses malformed command %j', async (change) => {
    const command = Object.assign(plain('add'), copy(change));
    const bundle = await open('add'), before = copy(bundle);
    expect(() => executeOccurrenceMedia(bundle, command, fixture.add.verified_media)).toThrow();
    expect(bundle).toEqual(before);
  });

  it.each([NaN, Infinity, undefined, new Date(), new Map(), () => 'bad'])('refuses non-JSON authored data %s', async (value) => {
    const bundle = await open('add');
    Object.assign(bundle.parent, { malformed: value });
    expect(() => captureOccurrenceAddMedia(bundle, owner, originalRow, newPin, fixture.add.verified_media)).toThrow('finite JSON');
  });

  it('detaches caller IDs, selections, row data and original bundle at capture', async () => {
    const bundle = await open('add'), row = copy(originalRow), pin = copy(newPin), inputs = copy(fixture.add.verified_media);
    const captured = captureOccurrenceAddMedia(bundle, owner, row, pin, inputs), snapshot = copy(captured);
    row.id = 'changed'; pin.asset = 'changed'; inputs[1].size = 1; child(bundle).at = 999;
    expect(captured).toEqual(snapshot);
    expect(captured.command.args.row).toEqual(originalRow);
    expect(captured.command.args.media).toEqual(newPin);
    expect(captured.command.created).toEqual([`${owner}/asset:reserved-new`, `${owner}/clip:reserved-child`]);
  });
});
