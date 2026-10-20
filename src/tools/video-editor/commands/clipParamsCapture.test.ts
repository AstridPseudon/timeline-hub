import { describe, expect, it } from 'vitest';
import type { AgentState, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { AuthoredState, copy, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { captureClipParams, finishClipParams } from './clipParamsCapture.ts';
import type { ClipParamsArgs } from './clipParamsCapture.ts';
import objectFixture from './fixtures/recipe_m2_scalar_params_object.json';
import absentFixture from './fixtures/recipe_m2_scalar_params_absent.json';
import nullFixture from './fixtures/recipe_m2_scalar_params_null.json';
import disjointFixture from './fixtures/recipe_m2_scalar_disjoint.json';

type ScalarGolden = {
  bundle: AuthoredBundle;
  after_bundle: AuthoredBundle;
  command: EditCommand;
  args: ClipParamsArgs;
  select: string;
};

const goldens = [objectFixture, absentFixture, nullFixture, disjointFixture] as unknown as ScalarGolden[];
const objectGolden = objectFixture as unknown as ScalarGolden;
const ref = objectGolden.select;

const state = (bundle: AuthoredBundle, path: string[]): AgentState =>
  new AuthoredState(bundle).get(ref, path);

function expectedRecord(golden: ScalarGolden): CommandRecord {
  const writes: CommandRecord['writes'] = [];
  const beforeParams = state(golden.bundle, ['params']);
  if (beforeParams.state === 'absent' || beforeParams.value === null) {
    writes.push({ ref, path: ['params'], before: beforeParams, after: { state: 'present', value: {} } });
  }
  for (const key of Object.keys(golden.args.values).sort()) {
    writes.push({ ref, path: ['params', key], before: state(golden.bundle, ['params', key]),
      after: { state: 'present', value: golden.args.values[key] } });
  }
  for (const key of [...golden.args.clear].sort()) {
    writes.push({ ref, path: ['params', key], before: state(golden.bundle, ['params', key]), after: { state: 'absent' } });
  }
  const owner = ref.slice(0, ref.lastIndexOf('/'));
  const source = golden.bundle.source_mapping.shots[String(new AuthoredState(golden.bundle).occurrence(owner).shot_id)];
  return {
    ordinal: 0,
    command: golden.command,
    writes,
    reads: golden.command.reads!,
    selections: [],
    bindings: [
      { key: 'scalar.owner', ref: owner, policy: 'fixed', dependencies: [] },
      { key: 'scalar.target', ref, policy: 'fixed', dependencies: ['scalar.images'] },
    ],
    created: [],
    dependencies: [{ key: 'scalar.images', kind: 'entity', pin: {
      parent: golden.bundle.base_parent,
      source,
    }, policy: 'exact' }],
    derived_writes: [],
  };
}

const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));

describe('portable clip.set-params capture', () => {
  it.each(goldens)('matches the exact native command, after bundle and record: %s', (golden) => {
    const input = freezeJson(copy(golden.bundle));
    const basis = captureClipParams(input, golden.select, golden.args);
    const result = finishClipParams(basis, golden.args);
    expect(result.command).toEqual(golden.command);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect(result.record).toEqual(expectedRecord(golden));
    expect(input).toEqual(golden.bundle);
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
    const source = disjointFixture as unknown as ScalarGolden;
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
