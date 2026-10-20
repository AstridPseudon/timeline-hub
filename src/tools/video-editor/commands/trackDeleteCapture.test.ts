import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  captureTrackDelete,
  executeTrackDelete,
} from './trackDeleteCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_track_delete.json';

type Golden = {
  bundle: AuthoredBundle;
  select: string;
  command: EditCommand;
  after_bundle: AuthoredBundle;
  record: unknown;
};

const golden = fixture as unknown as Golden;
const clone = <T>(value: T): T => structuredClone(value);

describe('Agent built-in track.delete capture parity', () => {
  it('matches the native command, authored after-state, and recorder record exactly', () => {
    const input = clone(golden.bundle);
    const result = captureTrackDelete(input, golden.select);

    expect(result.command).toEqual(golden.command);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect(result.record).toEqual(golden.record);
    expect(input).toEqual(golden.bundle);
    expect(result.record).toMatchObject({
      writes: [{ ref: golden.select, path: [], after: { state: 'absent' } }],
      created: [],
      dependencies: [],
      derived_writes: [],
    });
  });

  it('keeps the original capture across JSON cloning and rejects refreshed claims', () => {
    const captured = captureTrackDelete(golden.bundle, golden.select);
    const portable = clone(captured.command);
    const cloned = executeTrackDelete(clone(golden.bundle), portable);
    expect(cloned).toEqual(captured);

    const refreshed = clone(golden.bundle);
    (refreshed.parent.config!.tracks as Array<Record<string, unknown>>)[1].nullable = 'changed';
    expect(() => executeTrackDelete(refreshed, portable)).toThrow('original capture');
  });

  it.each([
    ['parent clip reference', (bundle: AuthoredBundle) => {
      (bundle.parent.clips as Array<Record<string, unknown>>)[0].track = 'empty';
    }],
    ['occurrence placement reference', (bundle: AuthoredBundle) => {
      (bundle.placements[0].placement as Record<string, unknown>).track = 'empty';
    }],
    ['occurrence track reference', (bundle: AuthoredBundle) => {
      bundle.placements[0].track = 'empty';
    }],
    ['child source reference', (bundle: AuthoredBundle) => {
      (bundle.shots['shot-a'].internal_timeline as Record<string, unknown>).audio = [{ track_ref: 'parent/track:empty' }];
    }],
  ])('refuses an in-use track atomically: %s', (_name, change) => {
    const input = clone(golden.bundle);
    change(input);
    const before = clone(input);
    expect(() => captureTrackDelete(input, golden.select)).toThrow('surviving dependents');
    expect(input).toEqual(before);
  });

  it('rejects non-native scope, cascade arguments, and projected ownership', () => {
    expect(() => captureTrackDelete(golden.bundle, 'occurrence:occ-a/track:empty')).toThrow();
    expect(() => executeTrackDelete(golden.bundle, {
      ...clone(golden.command),
      args: { cascade: true },
    })).toThrow('unsupported track.delete');
    expect(() => captureTrackDelete(golden.bundle, 'parent/track:empty::display')).toThrow();
  });

  it('retains opaque track data and exact parent/occurrence closure after deletion', () => {
    const result = captureTrackDelete(golden.bundle, golden.select);
    const removed = result.bundle.parent.config!.tracks as Array<Record<string, unknown>>;
    expect(removed).toEqual([
      { id: 'before', kind: 'visual' },
      { id: 'picture', kind: 'visual' },
    ]);
    expect(result.bundle.parent.clips).toEqual(golden.bundle.parent.clips);
    expect(result.bundle.placements).toEqual(golden.bundle.placements);
    expect(result.bundle.shots).toEqual(golden.bundle.shots);
  });
});
