import fixture from '../data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { describe, expect, it } from 'vitest';
import { createRecoveryConfig } from './useTimelineSave.draftConfig.ts';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';

const head = { projectId: 'project', timelineId: 'timeline', headRevisionId: 'revision', headPublicationId: 'publication' };
const opaqueRoots = {
  x_null: null, x_false: false, x_zero: 0, x_empty: [],
  x_nested: { unknown: [null, false, 0, [], { value: 'original' }] },
};

describe('recovery-only config roots', () => {
  it('clones all authored opaque roots while current display fields and clears win', () => {
    const recovery = createRecoveryConfig();
    const raw = { ...createDefaultTimelineConfig(), theme: 'old-theme', ...structuredClone(opaqueRoots) };
    recovery.remember(head, raw);
    raw.x_nested.unknown.push('mutated source');
    const current = createDefaultTimelineConfig();
    current.tracks = [{ id: 'V1', kind: 'visual', label: 'my rename' }];
    delete current.theme;
    const snapshot = recovery.snapshot(head, current) as typeof current & typeof opaqueRoots;
    expect(snapshot).toEqual({ ...current, ...opaqueRoots });
    expect(snapshot).not.toHaveProperty('x_absent');
    expect(snapshot).not.toHaveProperty('theme');
    snapshot.x_nested.unknown.push('mutated draft');
    snapshot.tracks![0].label = 'mutated draft';
    expect(current.tracks[0].label).toBe('my rename');
    expect(recovery.snapshot(head, current)).toEqual({ ...current, ...opaqueRoots });
  });

  it.each([
    { ...head, projectId: 'other' }, { ...head, timelineId: 'other' },
    { ...head, headRevisionId: 'other' }, { ...head, headPublicationId: 'other' },
    { ...head, headPublicationId: undefined }, undefined,
  ])('never lends opaque roots to a different or incomplete base (%j)', (other) => {
    const recovery = createRecoveryConfig();
    recovery.remember(head, opaqueRoots);
    const current = createDefaultTimelineConfig();
    expect(recovery.snapshot(other, current)).toEqual(current);
  });
});


it('snapshots projected drafts from the retained original graph and refuses a different base', () => {
  const composition = createShotCompositionAdapter({ load: async () => fixture }).prepare(fixture);
  const config = projectCanonicalComposition(composition).config;
  const recovery = createRecoveryConfig();
  recovery.remember(head, { x_null: null }, composition);
  const draft = recovery.snapshot(head, config, true);
  expect(draft.clips[0].app?.canonicalTiming).not.toHaveProperty('storedOccurrenceDurationMs');
  expect(draft).toHaveProperty('x_null', null);
  expect(config.clips[0].app?.canonicalTiming).toHaveProperty('storedOccurrenceDurationMs', 2000);
  expect(() => recovery.snapshot({ ...head, headPublicationId: 'other' }, config, true)).toThrow('verified raw');
  expect(() => createRecoveryConfig().snapshot(head, config, true)).toThrow('verified raw');
});
