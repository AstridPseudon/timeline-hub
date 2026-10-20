import { describe, expect, it } from 'vitest';
import type { CanonicalDocument, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { capturePlacement, finishPlacement } from './placementCapture.ts';
import { AuthoredState, copy, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_placement.json';

type Golden = {
  input: CanonicalDocument;
  output: CanonicalDocument;
  command: EditCommand;
  records: CommandRecord[];
  request: { owner: string; clip_id: string; on: number; ownership: 'parent' | 'occurrence' };
};

const cases = (fixture as unknown as { cases: Golden[] }).cases;
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const clip = (bundle: AuthoredBundle, ref: string) => new AuthoredState(bundle).entity(ref)!;

function expectAuthoredAfter(actual: AuthoredBundle, output: CanonicalDocument, ref: string): Promise<void> {
  return authoringBundleFromDocument(output).then((published) => {
    const actualState = new AuthoredState(actual);
    const publishedState = new AuthoredState(published);
    for (const scope of ['parent', 'occurrence:occ-a', 'occurrence:occ-b']) {
      expect(actualState.config(scope)).toEqual(publishedState.config(scope));
      expect(actualState.entity(`${scope}/clip:clip-a`)).toEqual(publishedState.entity(`${scope}/clip:clip-a`));
      expect(actualState.entity(`${scope}/clip:clip-b`)).toEqual(publishedState.entity(`${scope}/clip:clip-b`));
      expect(actualState.entity(`${scope}/registry`)).toEqual(publishedState.entity(`${scope}/registry`));
    }
    expect(actualState.entity(ref)).toEqual(publishedState.entity(ref));
  });
}

describe('native placement.move capture parity', () => {
  for (const golden of cases) {
    it(`matches the complete frozen command, record, and authored after-state: ${golden.request.owner}`, async () => {
      const input = await authoringBundleFromDocument(golden.input);
      const snapshot = copy(input);
      const { owner, clip_id: clipId, on, ownership } = golden.request;
      const ref = `${owner}/clip:${clipId}`;
      const basis = capturePlacement(freezeJson(input), owner, clipId, on, ownership);
      const result = finishPlacement(basis, on);

      expect(result.command).toEqual(golden.command);
      expect(result.record).toEqual(golden.records[0]);
      expect(result.record.command).toEqual(golden.command);
      await expectAuthoredAfter(result.bundle, golden.output, ref);
      expect(result.bundle.source_mapping).toEqual(snapshot.source_mapping);
      expect(result.bundle.base_parent).toEqual(snapshot.base_parent);
      expect(result.bundle.base_parent_payload).toEqual(snapshot.base_parent_payload);
      expect(result.bundle.placements).toEqual(snapshot.placements);
      expect(input).toEqual(snapshot);
    });
  }

  it('round-trips a frozen original capture without refreshing guards', async () => {
    const golden = cases[1];
    const original = await authoringBundleFromDocument(golden.input);
    const basis = capturePlacement(original, golden.request.owner, golden.request.clip_id,
      golden.request.on, golden.request.ownership);
    const portable = freezeJson(roundtrip(basis));
    const portableSnapshot = copy(portable);
    const preview = finishPlacement(portable, 13);
    clip(preview.bundle, golden.request.owner + '/clip:clip-a').opaque = { preview: true };
    clip(original, golden.request.owner + '/clip:clip-a').at = 999;
    const result = finishPlacement(portable, golden.request.on);
    expect(result.command).toEqual(golden.command);
    expect(result.record).toEqual(golden.records[0]);
    expect(portable).toEqual(portableSnapshot);
    expect(() => finishPlacement({}, golden.request.on)).toThrow('incomplete placement basis');
  });

  it('retains literal source timing, immutable registry pins, and sibling isolation', async () => {
    const golden = cases[1];
    const input = await authoringBundleFromDocument(golden.input);
    const ref = `${golden.request.owner}/clip:${golden.request.clip_id}`;
    const target = clip(input, ref);
    delete target.hold;
    Object.assign(target, { from: 2, to: 6, speed: 2 });
    const sibling = clip(input, 'occurrence:occ-b/clip:clip-a');
    sibling.opaque = { unchanged: [null, false] };
    const result = finishPlacement(capturePlacement(input, golden.request.owner, golden.request.clip_id,
      golden.request.on, golden.request.ownership), golden.request.on);
    expect(clip(result.bundle, ref)).toMatchObject({ from: 2, to: 6, speed: 2, asset: 'picture' });
    expect(clip(result.bundle, 'occurrence:occ-b/clip:clip-a')).toEqual(sibling);
    expect(new AuthoredState(result.bundle).entity(`${golden.request.owner}/registry`))
      .toEqual(new AuthoredState(input).entity(`${golden.request.owner}/registry`));
  });

  it.each([
    ['parent', 'occurrence'], ['occurrence:occ-a', 'parent'], ['parent', 'shared'],
    ['occurrence:occ-a', 'shared'], ['shot:chapter-shot', 'shared'],
  ] as const)('refuses malformed owner/ownership pair %s/%s', async (owner, ownership) => {
    const input = await authoringBundleFromDocument(cases[0].input);
    const snapshot = copy(input);
    expect(() => capturePlacement(input, owner, 'clip-a', 4, ownership)).toThrow('ownership');
    expect(input).toEqual(snapshot);
  });

  it.each(['', ' ', 'parent/clip:clip-a', 'clip-a::at', 'missing'])(
    'refuses non-raw or missing clip identity %s', async (clipId) => {
      const input = await authoringBundleFromDocument(cases[0].input);
      expect(() => capturePlacement(input, 'parent', clipId, 4, 'parent')).toThrow();
    });

  it.each([undefined, true, -1, Number.NaN, Number.POSITIVE_INFINITY, 'auto', { frame: 120 }])(
    'refuses non-literal timing %j without changing the source', async (on) => {
      const input = await authoringBundleFromDocument(cases[0].input);
      const snapshot = copy(input);
      expect(() => capturePlacement(input, 'parent', 'clip-a', on as number, 'parent')).toThrow();
      expect(input).toEqual(snapshot);
    });

  it('refuses shared authored roots even when the sibling has another lane', async () => {
    const input = await authoringBundleFromDocument(cases[1].input);
    const sibling = new AuthoredState(input).occurrence('occurrence:occ-b');
    sibling.shot_id = new AuthoredState(input).occurrence('occurrence:occ-a').shot_id;
    sibling.track = 'unrelated-lane';
    (sibling.placement as Record<string, JSON>).track = 'unrelated-lane';
    const snapshot = copy(input);
    expect(() => capturePlacement(input, 'occurrence:occ-a', 'clip-a', 12.012, 'occurrence'))
      .toThrow('shared authored placement');
    expect(input).toEqual(snapshot);
  });

  it('refuses changed source pins and relevant reads while allowing disjoint edits', async () => {
    const golden = cases[1];
    const input = await authoringBundleFromDocument(golden.input);
    const basis = capturePlacement(input, golden.request.owner, golden.request.clip_id,
      golden.request.on, golden.request.ownership);
    const disjoint = copy(basis);
    disjoint.bundle.parent.name = 'Concurrent rename';
    clip(disjoint.bundle, 'occurrence:occ-b/clip:clip-a').opaque = { disjoint: true };
    expect(finishPlacement(disjoint, golden.request.on).command).toEqual(golden.command);
    const changed = copy(basis);
    const registry = new AuthoredState(changed.bundle).entity('occurrence:occ-a/registry')!;
    (registry.assets as Record<string, JSON>).picture = { media_id: 'changed-pin', type: 'image' };
    expect(() => finishPlacement(changed, golden.request.on)).toThrow();
  });

  it('guards the native record against forged claims and unsupported placement recipes', async () => {
    const golden = cases[0];
    const input = await authoringBundleFromDocument(golden.input);
    const basis = capturePlacement(input, golden.request.owner, golden.request.clip_id,
      golden.request.on, golden.request.ownership);
    for (const [key, value] of [['reads', []], ['selections', []], ['bindings', {}], ['created', ['parent/clip:made-up']]] as const) {
      const forged = copy(basis);
      (forged.command as Record<string, JSON>)[key] = value;
      expect(() => finishPlacement(forged, golden.request.on)).toThrow('original capture');
    }
    const forged = copy(basis);
    forged.command.args = { on: golden.request.on, timeline_frame: 360 };
    expect(() => finishPlacement(forged, golden.request.on)).toThrow();
  });
});
