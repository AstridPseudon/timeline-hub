// @vitest-environment node
import assert from 'node:assert/strict';
import { describe, expect, it } from 'vitest';
import fixture from './shotComposition.fixture.json';
import { parseShotComposition } from './shotComposition.ts';
import { updateCanonicalShotSettings, updateCanonicalShotTimeline } from './shotCompositionEditor.ts';

type Row = Record<string, any>;

const payload = JSON.parse(`{
  "items": [
    {"item_id":"item-1","id":"item-1","source_item_id":"item-1","source_item":"item-audio",
      "metadata":{"source_item_id":"item-audio","source_item":"item-1","nested":{"source_item":"item-1"}},
      "__proto__":{"item_id":"item-1"},"constructor":"item-1","prototype":"item-audio"},
    {"id":"item-audio","source_item_id":"item-1","source_item":"item-audio"}
  ],
  "__proto__":{"selected_item_id":"item-1"},
  "constructor":"item-1","prototype":"item-audio",
  "selected_item_id":"item-1","parent_item_id":"item-audio",
  "bound_item_ids":["item-audio",null,"item-1"],"nullable":null
}`) as Row;

describe.each(['settings', 'timeline'] as const)('popup shared-copy %s opaque remap', (operation) => {
  it('preserves the complete revision while remapping only schema-owned item references', async () => {
    const graph = parseShotComposition(structuredClone(fixture));
    const source = graph.shot_revisions.find((revision) => revision.shot_id === 'shot-alpha' && revision.revision_id === 'rev-a')!;
    const sourceIndex = graph.shot_revisions.indexOf(source);
    graph.shot_revisions[sourceIndex] = { ...source, ...structuredClone(payload) };
    const input = graph.shot_revisions[sourceIndex] as Row;
    const internal = input.internal_timeline_revision as Row;
    internal.timeline.opaque = { retained: [null, false, []] };
    const before = structuredClone(graph);
    const patchTimeline = { ...structuredClone(internal.timeline), popup_opaque: { retained: true } };
    const settings = { ...input.settings, prompt: 'Changed only target', opaque: { retained: true } };

    const updated = operation === 'settings'
      ? await updateCanonicalShotSettings(graph, 'occ-1', settings)
      : await updateCanonicalShotTimeline(graph, 'occ-1', patchTimeline);
    const selected = updated.occurrences.find((occurrence) => occurrence.occurrence_id === 'occ-1')!;
    const revision = updated.shot_revisions.find((candidate) => candidate.revision_id === selected.revision_id)! as Row;
    const items = revision.items as Row[];

    expect(selected.shot_id).not.toBe(input.shot_id);
    expect(items[0].item_id).toBe(`${selected.shot_id}:item-1`);
    expect(items[0].metadata.source_item_id).toBe(`${selected.shot_id}:item-audio`);
    expect(items[0].metadata.source_item).toBe(`${selected.shot_id}:item-1`);
    expect(items[0].constructor).toBe('item-1');
    expect(items[0].prototype).toBe('item-audio');
    expect(Object.hasOwn(revision, '__proto__')).toBe(true);
    expect(revision.nullable).toBe(null);
    expect((revision.internal_timeline_revision as Row).timeline.opaque).toEqual({ retained: [null, false, []] });
    expect(revision.content_digest).toMatch(/^sha256:[0-9a-f]{64}$/);
    assert.deepStrictEqual(updated.shot_revisions.slice(0, -1), before.shot_revisions);
    assert.deepStrictEqual(updated.occurrences.slice(1), before.occurrences.slice(1));
    assert.deepStrictEqual(graph, before);
  });
});
