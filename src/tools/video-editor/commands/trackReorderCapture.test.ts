import { describe, expect, it } from 'vitest';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  captureTrackReorder,
  executeTrackReorder,
  finishTrackReorder,
} from './trackReorderCapture.ts';
import { copy, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_app_track_label.json';

const makeBundle = (): AuthoredBundle => {
  const bundle = copy(fixture.bundle) as AuthoredBundle;
  const config = bundle.parent.config as Record<string, JSON>;
  config.app = { timelineDataLanePlacement: { 'data-1': 'between' }, opaque: { keep: null } };
  config.tracks = [
    config.tracks![0],
    { id: 'audio', kind: 'audio', label: null, opaque: { null: null, false: false, zero: 0 } },
    { id: 'overlay', kind: 'visual', label: 'Overlay', opaque: { keep: [null, false, 0] } },
  ];
  bundle.parent.opaque_parent = { keep: [null, false, 0] };
  return bundle;
};

const refs = ['parent/track:picture', 'parent/track:audio', 'parent/track:overlay'];

describe('dormant media-only parent track reorder capture', () => {
  it('matches the Agent source shape and preserves raw rows, opaque values, and lane siblings', () => {
    const input = makeBundle();
    const before = copy(input);
    const basis = captureTrackReorder(input, [refs[2], refs[0], refs[1]]);
    const result = finishTrackReorder(basis);
    const config = result.bundle.parent.config as Record<string, JSON>;

    expect(result.command).toMatchObject({
      schema_version: 1, op: 'track.reorder', version: '1', select: 'parent',
      args: { order: [refs[2], refs[0], refs[1]], expected_order: refs }, intent: {},
    });
    expect(result.command.reads?.[0]).toEqual({ ref: 'parent/collection:track', path: [],
      state: { state: 'present', value: refs } });
    expect(result.command.selections).toEqual([{
      key: 'collection.tracks', query_version: 1, owner: 'parent', members: refs,
      order: refs, boundaries: refs, policy: 'guard-membership',
    }]);
    expect(result.command.expect).toEqual({ 'parent::track_order': { state: 'present', value: refs } });
    expect(result.command.authorship).toEqual({ 'parent::track_order': 'direct' });
    expect(config.tracks!.map((row) => (row as Record<string, JSON>).id)).toEqual(['overlay', 'picture', 'audio']);
    expect(config.tracks![0]).toEqual((before.parent.config as Record<string, JSON>).tracks![2]);
    expect(config.app).toEqual((before.parent.config as Record<string, JSON>).app);
    expect(result.bundle.parent.opaque_parent).toEqual(before.parent.opaque_parent);
    expect(input).toEqual(before);
  });

  it('round-trips the captured basis and keeps same-order writes explicit', () => {
    const input = makeBundle();
    const basis = captureTrackReorder(input, refs);
    const result = finishTrackReorder(freezeJson(JSON.parse(JSON.stringify(basis))));
    expect(result.bundle).toEqual(input);
    expect(result.record.writes).toEqual([{
      ref: 'parent', path: ['track_order'], before: { state: 'present', value: refs },
      after: { state: 'present', value: refs },
    }]);
    expect(executeTrackReorder(input, result.command)).toEqual(result);
  });

  it.each([
    ['missing', refs.slice(0, -1)],
    ['duplicate', [refs[0], refs[0], refs[2]]],
    ['foreign', [refs[0], 'occurrence:occ-1/track:picture', refs[2]]],
    ['malformed', ['parent/track:picture::label', refs[1], refs[2]]],
  ])('refuses %s desired identity atomically', (_label, desired) => {
    const input = makeBundle();
    const before = copy(input);
    expect(() => captureTrackReorder(input, desired)).toThrow();
    expect(input).toEqual(before);
  });

  it('refuses lane-bearing input and invalid current collections without mutation', () => {
    const input = makeBundle();
    const before = copy(input);
    expect(() => captureTrackReorder(input, { order: refs, lanes: { 'data-1': 'between' } })).toThrow();
    const duplicate = makeBundle();
    (duplicate.parent.config as Record<string, JSON>).tracks = [
      ...(duplicate.parent.config as Record<string, JSON>).tracks as JSON[],
      { id: 'picture', kind: 'visual' },
    ];
    const duplicateBefore = copy(duplicate);
    expect(() => captureTrackReorder(duplicate, refs)).toThrow();
    expect(input).toEqual(before);
    expect(duplicate).toEqual(duplicateBefore);
  });

  it('refuses stale captured identities and order before any row write', () => {
    for (const change of ['identity', 'order'] as const) {
      const basis = JSON.parse(JSON.stringify(captureTrackReorder(makeBundle(), [refs[2], refs[0], refs[1]])));
      const tracks = (basis.bundle.parent.config as Record<string, JSON>).tracks as JSON[];
      if (change === 'identity') {
        (tracks[0] as Record<string, JSON>).id = 'renamed';
      } else {
        [tracks[0], tracks[1]] = [tracks[1], tracks[0]];
      }
      const before = copy(basis);
      expect(() => finishTrackReorder(freezeJson(basis))).toThrow();
      expect(basis).toEqual(before);
    }
  });
});
