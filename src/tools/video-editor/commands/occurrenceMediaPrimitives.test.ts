import { describe, expect, it } from 'vitest';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { copy } from './clipMovePrimitives.ts';
import { OccurrenceMediaRecording, OccurrenceMediaState } from './occurrenceMediaPrimitives.ts';
import fixture from './fixtures/recipe_m2_occurrence_media.json';

const owner = 'occurrence:occ-a', ref = `${owner}/asset:reserved-new`;
const binding = { media_id: fixture.add.commands[0].args.media.object_id, type: 'video',
  generationId: 'generation-new', variantId: 'variant-new' };
const recording = async () => {
  const document: CanonicalDocument = { ...fixture.add.input, schema_version: 1 };
  return new OccurrenceMediaRecording(await authoringBundleFromDocument(document), {
    schema_version: 1, op: 'occurrence.add-media', version: '1', select: owner, args: {},
  });
};

describe('scoped authored media primitives', () => {
  it('records whole-entity absent/present writes and one ordinary asset birth', async () => {
    const ctx = await recording(), before = copy(ctx.state.bundle);
    ctx.createAsset(owner, 'reserved-new', binding);
    expect(ctx.state.get(ref, [])).toEqual({ state: 'present', value: binding });
    expect(ctx.command.expect).toEqual({ [`${ref}::`]: { state: 'absent' } });
    expect(ctx.command.authorship).toEqual({ [`${ref}::`]: 'direct' });
    expect(ctx.record.writes).toEqual([{ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: binding } }]);
    expect(ctx.record.created).toEqual([{ ref, kind: 'asset', owner }]);
    expect(ctx.command.created).toEqual([ref]);
    expect(ctx.record.dependencies).toEqual([]); // Recipe owns media dependencies.
    const captured = copy(ctx.record);
    expect(() => ctx.createAsset(owner, 'reserved-new', binding)).toThrow('occupied');
    expect(ctx.record).toEqual(captured);
    ctx.state.set(ref, [], { state: 'absent' });
    expect(ctx.state.bundle).toEqual(before);
  });

  it('records child order, raw owner binding and whole-child creation', async () => {
    const ctx = await recording(), row = copy(fixture.add.commands[0].args.row);
    ctx.createChild(owner, row);
    const ref = `${owner}/clip:${row.id}`;
    expect(ctx.command.created).toEqual([ref]);
    expect(ctx.record.created).toEqual([{ ref, kind: 'clip', owner }]);
    expect(ctx.command.selections![0]).toEqual({ key: 'collection.clips', query_version: 1, owner,
      members: [`${owner}/clip:clip-a`, `${owner}/clip:clip-b`], order: [`${owner}/clip:clip-a`, `${owner}/clip:clip-b`],
      boundaries: [`${owner}/clip:clip-a`, `${owner}/clip:clip-b`], policy: 'guard-membership' });
    expect(ctx.command.bindings).toEqual({ 'create.owner': owner, 'collection.owner:collection.clips': owner });
    expect(ctx.state.entity(ref)).toEqual(row);
    expect(ctx.record.writes).toEqual([{ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: row } }]);
    ctx.selectCollection('clip', owner);
    expect(ctx.command.selections).toHaveLength(2); // New membership is a different observation.
  });

  it('keeps collection shape distinct from membership and refuses duplicate identities', async () => {
    const ctx = await recording();
    expect(ctx.state.get(`${owner}/collection:clip`, [])).toEqual({ state: 'present', value: { members: { state: 'present', value: [] } } });
    ctx.selectCollection('clip', owner);
    ctx.selectCollection('clip', owner);
    expect(ctx.command.selections).toHaveLength(1);
    const clips = ctx.state.config(owner).clips;
    if (!Array.isArray(clips)) throw new Error('fixture clips');
    clips.push(copy(clips[0]));
    expect(() => ctx.selectCollection('clip', owner)).toThrow('ambiguous');
  });

  it('preserves tagged absence/null and refuses nonobject asset bindings', async () => {
    const ctx = await recording(), state = new OccurrenceMediaState(ctx.state.bundle);
    expect(state.get(ref, [])).toEqual({ state: 'absent' });
    expect(() => state.set(ref, [], { state: 'present', value: null })).toThrow('object');
    state.set(ref, [], { state: 'present', value: { ...binding, opaque: null } });
    expect(state.get(ref, ['opaque'])).toEqual({ state: 'present', value: null });
    expect(state.get(ref, ['missing'])).toEqual({ state: 'absent' });
    expect(() => state.set(`${owner}/clip:new`, [], { state: 'present', value: { id: 'other' } })).toThrow('identity');
  });
});
