import { describe, expect, it } from 'vitest';
import { ASTRID_RENDERING_ELEMENTS } from '../../../../vendor/astrid-browser/astrid/packs/rendering/elements/catalog.ts';
import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { AuthoredState, copy, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { captureClipParams, finishClipParams } from './clipParamsCapture.ts';
import type { ClipParamsArgs } from './clipParamsCapture.ts';
import disjointFixture from './fixtures/recipe_m2_scalar_disjoint.json';
import nativeFixture from './fixtures/recipe_m2_clip_params_bundle2.json';

type ScalarGolden = {
  name: string;
  records: CommandRecord[];
  bundle: AuthoredBundle;
  after_bundle: AuthoredBundle;
  command: EditCommand;
  args: ClipParamsArgs;
  select: string;
  rebased_records?: CommandRecord[];
};

// Full records exported by unmodified Agent execute(), not reconstructed here.
const goldens = nativeFixture.cases as unknown as ScalarGolden[];
const objectGolden = goldens[0];
const ref = objectGolden.select;

const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));

describe('portable clip.set-params capture', () => {
  it('uses the exact frozen native built-in property schemas without a second schema definition', () => {
    expect(Object.fromEntries(ASTRID_RENDERING_ELEMENTS.map((element) =>
      [element.id, element.schema.properties ?? {}]))).toEqual(nativeFixture.builtin_properties);
  });

  it.each(nativeFixture.refusals)('refuses the native invalid input atomically: $name', (golden) => {
    const bundle = freezeJson(copy(golden.bundle)) as unknown as AuthoredBundle;
    const snapshot = copy(bundle);
    expect(() => captureClipParams(bundle, golden.select, golden.args as ClipParamsArgs))
      .toThrow(expect.objectContaining({ kind: golden.error.kind }));
    expect(bundle).toEqual(snapshot);
  });

  it.each(nativeFixture.replay_refusals)('refuses changed native reads: $name', (golden) => {
    const basis = freezeJson(copy(golden.basis));
    const snapshot = copy(basis);
    expect(() => finishClipParams(basis, golden.args)).toThrow();
    expect(basis).toEqual(snapshot);
  });

  it.each(goldens)('matches the exported native command, after bundle and full record: $name', (golden) => {
    const input = freezeJson(copy(golden.bundle));
    const basis = captureClipParams(input, golden.select, golden.args);
    const result = finishClipParams(freezeJson(roundtrip(basis)), golden.args);
    expect(result.command).toEqual(golden.command);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect([result.record]).toEqual(golden.records);
    expect(basis.bundle).toEqual(golden.bundle);
    expect(input).toEqual(golden.bundle);
    const before = new AuthoredState(golden.bundle).entity(golden.select)!;
    const after = new AuthoredState(result.bundle).entity(golden.select)!;
    for (const key of ['at', 'from', 'to', 'speed', 'app', 'opaque', 'elementRef', 'element_ref']) {
      expect(after[key], key).toEqual(before[key]);
      expect(Object.hasOwn(after, key), key).toBe(Object.hasOwn(before, key));
    }
  });

  it.each(goldens.filter((golden) => /^(parent|occurrence)_clear_(absent|null|object|empty)$/.test(golden.name)))(
    'preserves clear-only container presence without materialization: $name', (golden) => {
      const result = finishClipParams(captureClipParams(golden.bundle, golden.select, golden.args), golden.args);
      const before = new AuthoredState(golden.bundle).get(golden.select, ['params']);
      const after = new AuthoredState(result.bundle).get(golden.select, ['params']);
      if (before.state === 'absent' || before.value === null) expect(after).toEqual(before);
      expect(result.record.writes.every((write) => write.path.length === 2)).toBe(true);
      expect(result.command.reads!.some((read) => read.path.join('.') === 'params'))
        .toBe(before.state === 'absent' || before.value === null);
    },
  );

  it('keeps unrelated registry edits and opaque source-window fields out of the read guards', () => {
    const golden = goldens.find((item) => item.name === 'registry_asset')!;
    const basis = roundtrip(captureClipParams(golden.bundle, golden.select, golden.args));
    const state = new AuthoredState(basis.bundle);
    const clip = state.entity(golden.select)!;
    clip.from = 9;
    clip.to = 12;
    clip.speed = 0.5;
    clip.app = { untouched: [false, null, {}] };
    const registry = state.entity('occurrence:o/registry')!;
    const assets = registry.assets as Record<string, Record<string, JSON>>;
    assets.other.media_id = 'unrelated-new-media';
    assets.chosen.opaque = { changed: true };
    const result = finishClipParams(basis, golden.args);
    expect(result.command).toEqual(golden.command);
    const after = new AuthoredState(result.bundle).entity(golden.select)!;
    for (const key of ['from', 'to', 'speed', 'app']) expect(after[key]).toEqual(clip[key]);
    expect(new AuthoredState(result.bundle).entity('occurrence:o/registry')).toEqual(registry);
  });

  it('visibly refuses changed selected-pack values without accepting a descriptor or a fabricated schema pin', () => {
    const golden = nativeFixture.refusals.find((item) => item.name === 'selected_elementRef_changed')!;
    expect(() => captureClipParams(golden.bundle as unknown as AuthoredBundle, golden.select, golden.args))
      .toThrow(/exact schema_source and verified immutable inputs/);
    expect(() => captureClipParams(golden.bundle as unknown as AuthoredBundle, golden.select, {
      ...golden.args, schema_source: { document_id: 'fabricated', version: 1, content_digest: 'sha256:fake' },
    } as ClipParamsArgs)).toThrow();
  });

  it.each(goldens.slice(0, 11).filter((golden) => golden.select.startsWith('parent/')))(
    'compiles equal parent mirrors once and preserves opaque siblings: $name', (golden) => {
      expect(golden.bundle.parent.clips).toEqual(golden.bundle.parent.config.clips);
      const result = finishClipParams(captureClipParams(golden.bundle, golden.select, golden.args), golden.args);
      expect(result.bundle.parent.clips).toEqual(result.bundle.parent.config.clips);
      expect(result.record.derived_writes).toEqual(golden.records[0].derived_writes);
      expect(result.record.derived_writes).toHaveLength(1);
      expect(result.bundle.parent.clips[1]).toEqual(golden.bundle.parent.clips[1]);
      expect(result.bundle.parent.opaque).toEqual(golden.bundle.parent.opaque);
      expect(result.bundle.parent.config.opaque).toEqual(golden.bundle.parent.config.opaque);
      expect(result.bundle.shots).toEqual(golden.bundle.shots);
    },
  );

  it('records only retained native compiler inputs alongside the scalar dependency', () => {
    const golden = goldens.find((item) => item.name === 'parent_retained_inputs')!;
    const result = finishClipParams(captureClipParams(golden.bundle, golden.select, golden.args), golden.args);
    expect(result.record.dependencies).toEqual(golden.records[0].dependencies);
    expect(result.record.dependencies.map((dependency) => dependency.kind)).toEqual(['entity', 'transcript', 'source']);
  });

  it('replays the original disjoint leaf claims with the full native record', () => {
    const source = goldens[3];
    const basis = roundtrip(captureClipParams(source.bundle, source.select, source.args));
    basis.bundle = copy(disjointFixture.head_bundle) as unknown as AuthoredBundle;
    const result = finishClipParams(freezeJson(basis), source.args);
    expect(result.command).toEqual(source.command);
    expect(result.bundle).toEqual(disjointFixture.rebased_bundle);
    expect([result.record]).toEqual(source.rebased_records);
  });

  it('keeps the original scope and claims through cloning, freezing and JSON round trips', () => {
    const basis = captureClipParams(objectGolden.bundle, ref, objectGolden.args);
    const snapshot = copy(basis);
    const jsonBasis = roundtrip(basis);
    const result = finishClipParams(freezeJson(jsonBasis), objectGolden.args);
    expect(result.command).toEqual(objectGolden.command);
    expect(result.bundle).toEqual(objectGolden.after_bundle);
    expect(basis).toEqual(snapshot);
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.bundle)).toBe(true);
    expect(Object.isFrozen(basis.command.expect![`${ref}::params.old`])).toBe(true);
  });

  it('preserves explicit clear, empty-key and null values while leaving opaque siblings untouched', () => {
    const result = finishClipParams(
      captureClipParams(objectGolden.bundle, ref, objectGolden.args), objectGolden.args,
    );
    const clip = new AuthoredState(result.bundle).entity(ref)!;
    expect(clip.params).toEqual(objectGolden.after_bundle.shots[
      'shot-placement-365d0383838d687737f499dfcdc96e880baaf8d4747ecf5f657993be89d8522b'
    ].internal_timeline.clips[0].params);
    expect(clip.app).toEqual(objectGolden.bundle.shots[
      'shot-placement-365d0383838d687737f499dfcdc96e880baaf8d4747ecf5f657993be89d8522b'
    ].internal_timeline.clips[0].app);
    expect(result.record.writes.every((write) => write.path[0] === 'params')).toBe(true);
  });

  it('protects relevant leaf changes while accepting a disjoint leaf change', () => {
    const source = goldens[3];
    const xArgs: ClipParamsArgs = { values: { x: 2 }, clear: [] };
    const basis = captureClipParams(source.bundle, source.select, xArgs);
    const relevant = roundtrip(basis);
    const relevantClip = new AuthoredState(relevant.bundle).entity(source.select)!;
    (relevantClip.params as Record<string, JSON>).x = 3;
    expect(() => finishClipParams(freezeJson(relevant), xArgs)).toThrow(/original capture|capture_mismatch/);

    const disjoint = roundtrip(basis);
    const disjointClip = new AuthoredState(disjoint.bundle).entity(source.select)!;
    (disjointClip.params as Record<string, JSON>).y = false;
    const result = finishClipParams(freezeJson(disjoint), xArgs);
    const params = result.bundle.shots[
      'shot-placement-365d0383838d687737f499dfcdc96e880baaf8d4747ecf5f657993be89d8522b'
    ].internal_timeline.clips[0].params as Record<string, JSON>;
    expect(params.x).toBe(2);
    expect(params.y).toBe(false);
    expect(params.old).toBe(null);
    expect(params.opaque).toEqual({ keep: [false, {}, ''] });
    expect(result.command.expect).toEqual({ [`${source.select}::params.x`]: { state: 'present', value: 1 } });
  });

  it.each(['delete', 'owner', 'source', 'value', 'type', 'asset'])(
    'refuses changed original identity/value guards atomically: %s', (change) => {
      const source = goldens[3];
      const basis = roundtrip(captureClipParams(source.bundle, source.select, source.args));
      const state = new AuthoredState(basis.bundle);
      const clip = state.entity(source.select)!;
      const owner = source.select.slice(0, source.select.lastIndexOf('/'));
      if (change === 'delete') state.config(owner).clips = [];
      else if (change === 'owner') state.occurrence(owner).shot_id = basis.bundle.placements[1].shot_id;
      else if (change === 'source') {
        basis.bundle.source_mapping.shots[String(state.occurrence(owner).shot_id)].shot_id = 'other-source';
      } else if (change === 'value') (clip.params as Record<string, JSON>).x = 3;
      else if (change === 'type') clip.clipType = 'audio';
      else clip.asset = 'new-asset';
      const snapshot = copy(basis);
      expect(() => finishClipParams(freezeJson(basis), source.args)).toThrow();
      expect(basis).toEqual(snapshot);
    },
  );

  it.each([
    'parent/clip:c', 'clip:c', 'shot:s/clip:c', 'occurrence:o/clip:c::params.x',
    'occurrence:o/track:c', 'occurrence:o/clip:',
  ])('refuses foreign or malformed scope %s', (select) => {
    expect(() => captureClipParams(objectGolden.bundle, select, objectGolden.args)).toThrow();
  });

  it('refuses missing or forged immutable capture claims without mutating the basis', () => {
    const claims = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
    for (const key of claims) {
      const incomplete = roundtrip(captureClipParams(objectGolden.bundle, ref, objectGolden.args));
      delete (incomplete.command as Partial<EditCommand>)[key];
      expect(() => finishClipParams(incomplete, objectGolden.args), key).toThrow(/incomplete clip parameters basis/);

      const forged = roundtrip(captureClipParams(objectGolden.bundle, ref, objectGolden.args));
      if (key === 'expect' || key === 'authorship' || key === 'bindings') {
        (forged.command as Record<string, unknown>)[key] = { forged: 'value' };
      } else {
        (forged.command as Record<string, unknown>)[key] = ['forged'];
      }
      const snapshot = copy(forged);
      expect(() => finishClipParams(forged, objectGolden.args), key).toThrow(/original capture|capture_mismatch/);
      expect(forged).toEqual(snapshot);
    }
  });

  it('refuses changed operation, version, args and foreign claims', () => {
    const changes: Array<Partial<EditCommand>> = [
      { op: 'track.set' }, { version: '2' }, { schema_version: 2 },
      { select: 'occurrence:o/track:picture' }, { intent: { ownership: 'shared' } },
    ];
    for (const change of changes) {
      const basis = roundtrip(captureClipParams(objectGolden.bundle, ref, objectGolden.args));
      Object.assign(basis.command, change);
      expect(() => finishClipParams(freezeJson(basis), objectGolden.args)).toThrow();
    }
    const missingGuard = roundtrip(captureClipParams(objectGolden.bundle, ref, objectGolden.args));
    missingGuard.command.expect = {};
    expect(() => finishClipParams(freezeJson(missingGuard), objectGolden.args)).toThrow(/original capture|capture_mismatch/);
  });

  it('refuses malformed args without coercion', () => {
    const basis = captureClipParams(objectGolden.bundle, ref, objectGolden.args);
    for (const args of [
      undefined, null, {}, { values: {}, clear: [] },
      { values: { x: null }, clear: ['x'] }, { values: { x: undefined }, clear: [] },
      { values: { x: 1 }, clear: ['x', 'x'] }, { values: { x: 1 }, clear: ['missing'] },
    ]) {
      expect(() => finishClipParams(basis, args as ClipParamsArgs)).toThrow();
    }
  });
});
