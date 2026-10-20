import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import fixture from './fixtures/recipe_m2_app_track_create.json';
import {
  AuthoredState,
  ClipMoveError,
  copy,
  freezeJson,
} from './clipMovePrimitives.ts';
import {
  captureTrackCreate,
  finishTrackCreate,
  type TrackCreateArgs,
} from './trackCreateCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type Golden = {
  agent_source: string;
  schema_sha256: string;
  source_fixture: string;
  input: { select: 'parent'; row: TrackCreateArgs['row'] };
  bundle: AuthoredBundle;
  command: EditCommand;
  record: CommandRecord;
  after_bundle: AuthoredBundle;
};

const golden = fixture as unknown as Golden;
const original = golden.bundle;
const row = golden.input.row;
const ref = `parent/track:${row.id}`;
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const tracks = (bundle: AuthoredBundle) => (bundle.parent.config as { tracks: JSON[] }).tracks;

describe('portable parent-only track.create capture', () => {
  it('matches the complete native command, record, and after-bundle golden', () => {
    const input = freezeJson(copy(original));
    const basis = captureTrackCreate(input, { row: copy(row) });
    const result = finishTrackCreate(basis, { row: copy(row) });

    expect(result.command).toEqual(golden.command);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect(result.record).toEqual(golden.record);
    expect(input).toEqual(original);
    expect(basis.bundle).toEqual(original);
    expect(result.record.command).toEqual(golden.command);
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.bundle)).toBe(true);
    expect(Object.isFrozen(basis.command.args.row)).toBe(true);
  });

  it('replays from a frozen JSON basis without recapturing the source', () => {
    const basis = freezeJson(roundtrip(captureTrackCreate(original, { row })));
    const snapshot = copy(basis);
    const result = finishTrackCreate(basis, { row: copy(row) });
    const replayed = finishTrackCreate(freezeJson(roundtrip(basis)), { row: copy(row) });

    expect(result).toEqual(replayed);
    expect(result.command).toEqual(golden.command);
    expect(basis).toEqual(snapshot);
  });

  it('preserves the complete App A1 row, nulls, unknowns, and opaque siblings', () => {
    const input = copy(original);
    const existing = tracks(input)[0] as Record<string, JSON>;
    existing.opaque = { sibling: [null, false, { keep: true }] };
    (input.parent as Record<string, JSON>).opaque = { source: ['untouched', null] };
    const result = finishTrackCreate(captureTrackCreate(input, { row }), { row });

    expect(result.bundle.parent.config.tracks).toEqual([...tracks(input), row]);
    expect((result.bundle.parent.config.tracks[0] as Record<string, JSON>).opaque).toEqual(existing.opaque);
    expect(result.bundle.parent.opaque).toEqual(input.parent.opaque);
    expect(result.record.writes).toEqual(golden.record.writes);
  });

  it.each(['lane:é 🎬', '0', '__proto__', 'dotted.id[0]'])('keeps raw nonempty identity %s', (id) => {
    const created = { ...copy(row), id };
    const result = finishTrackCreate(captureTrackCreate(original, { row: created }), { row: created });

    expect(result.command.select).toBe('parent');
    expect(result.command.created).toEqual([`parent/track:${id}`]);
    expect(result.command.reads).toEqual([{ ref: `parent/track:${id}`, path: [], state: { state: 'absent' } }]);
    expect(result.command.expect).toEqual({ [`parent/track:${id}::`]: { state: 'absent' } });
    expect((new AuthoredState(result.bundle).entity(`parent/track:${id}`))).toEqual(created);
  });

  it.each([
    { id: '', kind: 'audio' },
    { id: 'bad/id', kind: 'audio' },
    { id: 'bad::id', kind: 'audio' },
    { id: 'new', kind: '' },
  ])('refuses invalid scalar row identities or kinds %j', (invalid) => {
    expect(() => captureTrackCreate(original, { row: { ...copy(row), ...invalid } })).toThrow(ClipMoveError);
  });

  it('refuses duplicate IDs and preserves the caller row on every refusal', () => {
    const duplicate = { ...copy(row), id: 'picture' };
    const snapshot = copy(duplicate);

    expect(() => captureTrackCreate(original, { row: duplicate })).toThrow(/identity|occupied|duplicate/i);
    expect(duplicate).toEqual(snapshot);
  });

  it.each([
    ['absent', undefined],
    ['null', null],
  ] as const)('does not materialize a missing or null parent track container (%s)', (_name, value) => {
    const input = copy(original);
    if (value === undefined) delete input.parent.config.tracks;
    else input.parent.config.tracks = value;
    const snapshot = copy(input);

    expect(() => captureTrackCreate(input, { row })).toThrow();
    expect(input).toEqual(snapshot);
  });

  it('creates into an explicitly empty parent collection', () => {
    const input = copy(original);
    input.parent.config.tracks = [];
    const result = finishTrackCreate(captureTrackCreate(input, { row }), { row });

    expect(result.command.selections).toEqual([{
      key: 'track.create', query_version: 1, owner: 'parent', members: [], order: [], boundaries: [],
      policy: 'guard-membership',
    }]);
    expect(result.bundle.parent.config.tracks).toEqual([row]);
  });

  it('accepts disjoint authored changes but refuses changed membership/order', () => {
    const basis = roundtrip(captureTrackCreate(original, { row }));
    const disjoint = copy(basis);
    (disjoint.bundle.parent as Record<string, JSON>).unrelated = { preserve: true };
    expect(finishTrackCreate(freezeJson(disjoint), { row }).bundle.parent.unrelated).toEqual({ preserve: true });

    const touched = copy(basis);
    const existingTracks = touched.bundle.parent.config.tracks as JSON[];
    existingTracks[0] = { ...(existingTracks[0] as Record<string, JSON>), id: 'renamed' };
    expect(() => finishTrackCreate(freezeJson(touched), { row })).toThrow();
  });

  it('refuses incomplete and forged native claims without mutating the basis', () => {
    for (const key of ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const) {
      const incomplete = roundtrip(captureTrackCreate(original, { row }));
      delete (incomplete.command as Partial<EditCommand>)[key];
      expect(() => finishTrackCreate(incomplete, { row }), key).toThrow('incomplete track create basis');

      const forged = roundtrip(captureTrackCreate(original, { row }));
      if (key === 'expect' || key === 'authorship' || key === 'bindings') forged.command[key] = { forged: 'claim' } as never;
      else forged.command[key] = ['forged'] as never;
      const snapshot = copy(forged);
      expect(() => finishTrackCreate(forged, { row }), key).toThrow(/capture|selection|identity/);
      expect(forged).toEqual(snapshot);
    }
  });

  it.each([
    { select: 'occurrence:one' },
    { op: 'track.set' },
    { version: '2' },
    { intent: { ownership: 'shared' } },
  ])('refuses a changed operation or non-parent scope %j', (change) => {
    const basis = roundtrip(captureTrackCreate(original, { row }));
    Object.assign(basis.command, change);
    expect(() => finishTrackCreate(basis, { row })).toThrow();
  });
});
