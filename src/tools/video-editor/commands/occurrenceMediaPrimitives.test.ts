import { describe, expect, it } from 'vitest';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { copy, has } from './clipMovePrimitives.ts';
import { OccurrenceMediaRecording, OccurrenceMediaState, rawIdentity } from './occurrenceMediaPrimitives.ts';
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
  it.each(['__proto__', 'constructor', 'toString'])('births valid raw alias %s as own dictionary data', async (identity) => {
    const ctx = await recording(), ref = `${owner}/asset:${identity}`;
    const registry = ctx.state.config(owner).registry as { assets: Record<string, unknown> };
    const prototype = Object.getPrototypeOf(registry.assets);
    expect(rawIdentity(identity)).toBe(true);
    expect(has(registry.assets, identity)).toBe(false);
    expect(ctx.state.entity(ref, true)).toBeUndefined();
    expect(() => ctx.state.entity(ref)).toThrow('missing asset identity');
    expect(ctx.state.get(ref, [])).toEqual({ state: 'absent' });
    ctx.createAsset(owner, identity, binding);
    expect(Object.getPrototypeOf(registry.assets)).toBe(prototype);
    expect(Object.getOwnPropertyDescriptor(registry.assets, identity)).toEqual({
      value: binding, enumerable: true, configurable: true, writable: true,
    });
    expect(ctx.state.get(ref, [])).toEqual({ state: 'present', value: binding });
    expect(JSON.parse(JSON.stringify(registry.assets))[identity]).toEqual(binding);
    expect(ctx.command.created).toEqual([ref]);
    expect(ctx.record.created).toEqual([{ ref, kind: 'asset', owner }]);
    expect(ctx.command.expect).toEqual({ [`${ref}::`]: { state: 'absent' } });
    expect(ctx.command.authorship).toEqual({ [`${ref}::`]: 'direct' });
    expect(ctx.record.writes).toEqual([{ ref, path: [], before: { state: 'absent' }, after: { state: 'present', value: binding } }]);
    const captured = copy(ctx.record);
    expect(() => ctx.createAsset(owner, identity, binding)).toThrow('occupied');
    expect(ctx.record).toEqual(captured);
  });

  it.each(['__proto__', 'constructor', 'toString'])('overwrites, clones and deletes own alias %s without changing its dictionary prototype', async (identity) => {
    const ctx = await recording(), ref = `${owner}/asset:${identity}`;
    const registry = ctx.state.config(owner).registry as { assets: Record<string, unknown> };
    const before = copy(registry.assets), prototype = Object.getPrototypeOf(registry.assets);
    const value = JSON.parse(`{"${identity}":{"opaque":[null,false,{}],"nullable":null}}`)[identity];
    registry.assets = JSON.parse(JSON.stringify({ ...registry.assets, [identity]: binding }));
    expect(() => ctx.createAsset(owner, identity, binding)).toThrow('occupied');
    ctx.state.set(ref, [], { state: 'present', value });
    value.opaque.push('caller mutation');
    expect(ctx.state.get(ref, [])).toEqual({ state: 'present', value: { opaque: [null, false, {}], nullable: null } });
    expect(ctx.state.get(ref, ['nullable'])).toEqual({ state: 'present', value: null });
    expect(ctx.state.get(ref, ['missing'])).toEqual({ state: 'absent' });
    expect(Object.getPrototypeOf(registry.assets)).toBe(prototype);
    expect(Object.getOwnPropertyDescriptor(registry.assets, identity)).toEqual({
      value: { opaque: [null, false, {}], nullable: null }, enumerable: true, configurable: true, writable: true,
    });
    ctx.state.set(ref, [], { state: 'absent' });
    expect(has(registry.assets, identity)).toBe(false);
    expect(ctx.state.get(ref, [])).toEqual({ state: 'absent' });
    expect(registry.assets).toEqual(before);
    expect(Object.getPrototypeOf(registry.assets)).toBe(prototype);
  });

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
