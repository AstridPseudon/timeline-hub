// @vitest-environment node
import { describe, expect, it } from 'vitest';
import type { AgentState } from '@/integrations/runtime/timeline-commit-types.ts';
import { AuthoredState, copy, freezeJson } from './clipMovePrimitives.ts';
import {
  captureClipDelete,
  executeClipDelete,
  finishClipDelete,
} from './clipDeleteCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_app_clip_delete.json';

// Byte-exact Agent bbb60b5cd664f675df0de1679e8fc565ae73fd0c conformance golden.
const original = fixture.bundle as AuthoredBundle;
const ref = fixture.select;
const clip = (bundle: AuthoredBundle, id = 'clip-b') => new AuthoredState(bundle).entity(`parent/clip:${id}`)!;
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));

describe('portable parent clip delete capture', () => {
  it('matches the exact native command, after bundle, and record', () => {
    const input = freezeJson(copy(original));
    const basis = captureClipDelete(input, ref);
    const result = finishClipDelete(basis);

    expect(result.command).toEqual(fixture.command);
    expect(result.bundle).toEqual(fixture.after_bundle);
    expect(result.record).toEqual(fixture.records[0]);
    expect(input).toEqual(original);
    expect(finishClipDelete(freezeJson(roundtrip(basis)))).toEqual(result);
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.bundle)).toBe(true);
    expect(Object.isFrozen(basis.command.expect![`${ref}::`])).toBe(true);
  });

  it('preserves opaque fields and exact source closure while removing only the selected row', () => {
    const input = copy(original);
    const before = copy(input);
    const result = executeClipDelete(input, captureClipDelete(input, ref).command);
    const remaining = result.bundle.parent.clips as Array<Record<string, unknown>>;

    expect(remaining.map((row) => row.id)).toEqual(['clip-a', 'clip-c']);
    expect(remaining[0]?.opaque).toEqual(before.parent.clips[0].opaque);
    expect(result.bundle.parent.config.clips).toEqual(remaining);
    expect(result.bundle.source_mapping).toEqual(before.source_mapping);
    expect(result.bundle.base_parent).toEqual(before.base_parent);
    expect(input).toEqual(before);
  });

  it('captures whole-row presence, including nulls, as the inverse guard', () => {
    const input = copy(original);
    const target = clip(input);
    const expected: AgentState = { state: 'present', value: copy(target) };
    const basis = captureClipDelete(input, ref);
    expect(basis.command.expect).toEqual({ [`${ref}::`]: expected });
    expect(basis.command.authorship).toEqual({ [`${ref}::`]: 'direct' });
    expect(basis.command.created).toEqual([]);
    expect(basis.command.resolved).toEqual([ref]);
  });

  it.each([
    'parent', 'clip-b', 'parent/clip:', 'parent/clip:clip-b/extra', 'parent/clip:clip-a::x',
    'occurrence:occ-a/clip:clip-b', 'shot:s/clip:clip-b',
  ])('refuses unsupported target identity %s', (target) => {
    expect(() => captureClipDelete(original, target)).toThrow();
  });

  it.each([
    ['legacy shot', (bundle: AuthoredBundle) => { clip(bundle).clipType = 'shot'; }],
    ['nested clips', (bundle: AuthoredBundle) => { clip(bundle).children = []; }],
    ['pinned group', (bundle: AuthoredBundle) => { (bundle.parent.config as Record<string, unknown>).pinnedShotGroups = [{ id: 'g' }]; }],
    ['declared relation', (bundle: AuthoredBundle) => { clip(bundle).app = { astrid: { on: 'word:1' } }; }],
    ['transition', (bundle: AuthoredBundle) => { clip(bundle, 'clip-a').transition = { id: 'crossfade' }; }],
  ] as const)('refuses %s without mutating input', (_name, mutate) => {
    const input = copy(original);
    mutate(input);
    const before = copy(input);
    expect(() => captureClipDelete(input, ref)).toThrow();
    expect(input).toEqual(before);
  });

  it('matches native mirror compilation when deleting the final clip with a colon in its raw ID', () => {
    const input = copy(original);
    const target = { ...clip(input), id: 'raw:clip-b' };
    input.parent.clips = [copy(target)];
    input.parent.config.clips = [copy(target)];
    const result = finishClipDelete(captureClipDelete(input, 'parent/clip:raw:clip-b'));
    expect(result.bundle.parent.clips).toEqual([]);
    expect(result.bundle.parent.config.clips).toEqual([]);
    expect(result.record.writes).toEqual([{ ref: 'parent/clip:raw:clip-b', path: [],
      before: { state: 'present', value: target }, after: { state: 'absent' } }]);
    expect(result.record.derived_writes).toEqual([{ ref: 'parent', path: ['config', 'clips'],
      before: { state: 'present', value: [target] }, after: { state: 'present', value: [] }, cause: 0 }]);
    expect(input.parent.clips).toEqual([target]);
  });

  it('refuses a refreshed target instead of recapturing the delete basis', () => {
    const basis = roundtrip(captureClipDelete(original, ref));
    clip(basis.bundle).asset = 'replacement';
    (basis.bundle.parent.config.clips as Array<Record<string, unknown>>)[1]!.asset = 'replacement';
    expect(() => finishClipDelete(freezeJson(basis))).toThrow('original capture');
  });
  it.each(['membership', 'order', 'opaque', 'null-to-absent'])('refuses changed original %s without touching the candidate', (change) => {
    const command = captureClipDelete(original, ref).command;
    const input = copy(original);
    const rows = input.parent.clips as Array<Record<string, unknown>>;
    if (change === 'membership') rows.push({ id: 'new', track: 'picture', at: 10, hold: 1 });
    if (change === 'order') rows.reverse();
    if (change === 'opaque') clip(input).opaque = { changed: [null, 0] };
    if (change === 'null-to-absent') {
      delete clip(input).nullable;
    }
    input.parent.config.clips = copy(input.parent.clips);
    const before = copy(input);
    expect(() => executeClipDelete(input, command)).toThrow('original capture');
    expect(input).toEqual(before);
  });

  it('requires every original capture claim rather than recapturing missing guards', () => {
    for (const key of ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const) {
      const basis = roundtrip(captureClipDelete(original, ref));
      delete basis.command[key];
      expect(() => finishClipDelete(basis), key).toThrow('incomplete clip delete basis');
    }
  });

});
