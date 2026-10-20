// @vitest-environment node
import assert from 'node:assert/strict';
import { describe, expect, it } from 'vitest';
import corpus from '../commands/fixtures/corpus/opaque_remap.json';
import fixture from './shotComposition.fixture.json';
import { parseShotComposition } from './shotComposition.ts';
import { updateCanonicalShotSettings, updateCanonicalShotTimeline } from './shotCompositionEditor.ts';
import { timelineContentExtentMs } from './shotCompositionTiming.ts';

type Row = Record<string, any>;
type RemapCase = { name: string; item_ids: Record<string, string>; payload: Row; expected: Row };

// Translate only the corpus's explicit expected output IDs to the popup's IDs.
function expectedWithPopupIds(value: unknown, ids: Map<string, string>): unknown {
  if (typeof value === 'string') return ids.get(value) ?? value;
  if (Array.isArray(value)) return value.map((child) => expectedWithPopupIds(child, ids));
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, child]) => [key, expectedWithPopupIds(child, ids)]));
  }
  return value;
}

const adversarialPayload = JSON.parse(`{
  "items": [
    {"item_id":"item-1","id":"item-1","source_item_id":"item-1","source_item":"item-audio",
      "metadata":{"source_item_id":"item-audio","source_item":"item-1","nested":{"source_item":"item-1"},"__proto__":{"item_id":"item-1"}},
      "__proto__":{"item_id":"item-1"},"constructor":"item-1","prototype":"item-audio"},
    {"id":"item-audio","metadata":null,"source_item_id":"item-1","source_item":"item-audio"},
    {"item_id":"item-third","id":"item-audio","metadata":[],"source_item_id":"item-audio","source_item":"item-1"},
    {"item_id":"item-fourth","metadata":{"source_item_id":null,"source_item":["item-1",null]},"source_item_id":"item-1"}
  ],
  "__proto__":{"selected_item_id":"item-1","constructor":{"prototype":"item-audio"}},
  "constructor":"item-1","prototype":"item-audio",
  "selected_item_id":"item-1","parent_item_id":"item-audio","bound_item_ids":["item-audio",null,"item-1","item-audio"],
  "data":{"items":[{"item_id":"item-1","metadata":{"source_item_id":"item-audio"}}]},
  "nullable":null
}`) as Row;
const adversarialExpected = structuredClone(adversarialPayload);
adversarialExpected.items[0].item_id = 'remap-item-1';
adversarialExpected.items[0].id = 'remap-item-1';
adversarialExpected.items[0].metadata.source_item_id = 'remap-item-audio';
adversarialExpected.items[0].metadata.source_item = 'remap-item-1';
adversarialExpected.items[1].id = 'remap-item-audio';
adversarialExpected.items[1].source_item_id = 'remap-item-1';
adversarialExpected.items[1].source_item = 'remap-item-audio';
adversarialExpected.items[2].item_id = 'remap-item-third';
adversarialExpected.items[2].source_item_id = 'remap-item-audio';
adversarialExpected.items[2].source_item = 'remap-item-1';
adversarialExpected.items[3].item_id = 'remap-item-fourth';

const cases: RemapCase[] = [
  ...corpus.cases,
  {
    name: 'metadata_precedence_null_array_secondary_id_and_prototype_own_keys',
    item_ids: {
      'item-1': 'remap-item-1',
      'item-audio': 'remap-item-audio',
      'item-third': 'remap-item-third',
      'item-fourth': 'remap-item-fourth',
    },
    payload: adversarialPayload,
    expected: adversarialExpected,
  },
];

describe.each(['settings', 'timeline'] as const)('popup shared-copy %s opaque remap', (operation) => {
  it.each(cases)('preserves the complete revision for $name', async ({ name, payload, expected, item_ids }) => {
    const graph = parseShotComposition(structuredClone(fixture));
    const source = graph.shot_revisions.find((revision) => revision.shot_id === 'shot-alpha' && revision.revision_id === 'rev-a')!;
    const originalItems = (payload as Row).items as Row[];
    // The corpus's supplied map may include dependency targets outside its
    // example items. Declare them here so the real consumer builds that map.
    const missingItems = Object.keys(item_ids)
      .filter((id) => !originalItems.some((item) => ('item_id' in item ? item.item_id : item.id) === id))
      .map((item_id) => ({ item_id }));
    const opaque = structuredClone(corpus.opaque);
    const sourcePayload = {
      ...structuredClone(payload),
      items: [...structuredClone(originalItems), ...missingItems],
      opaque,
    };
    // Object spread keeps __proto__ as an own data property.
    const sourceIndex = graph.shot_revisions.indexOf(source);
    graph.shot_revisions[sourceIndex] = { ...source, ...sourcePayload };
    const input = graph.shot_revisions[sourceIndex] as Row;
    const internal = input.internal_timeline_revision as Row;
    internal.timeline.opaque = structuredClone(opaque);
    internal.timeline.clips[0].selected_item_id = 'item-1';
    internal.timeline.clips[0].metadata = { source_item_id: 'item-1' };
    const before = structuredClone(graph);
    const patchTimeline = { ...structuredClone(internal.timeline), popup_opaque: structuredClone(opaque) };
    const settings = { ...input.settings, prompt: 'Changed only target', opaque: structuredClone(opaque) };
    const beforePatch = structuredClone({ patchTimeline, settings });

    const updated = operation === 'settings'
      ? await updateCanonicalShotSettings(graph, 'occ-1', settings)
      : await updateCanonicalShotTimeline(graph, 'occ-1', patchTimeline);
    const selected = updated.occurrences.find((occurrence) => occurrence.occurrence_id === 'occ-1')!;
    const revision = updated.shot_revisions.find((candidate) => candidate.revision_id === selected.revision_id)!;
    const expectedIds = new Map(Object.entries(item_ids).map(([id, mapped]) => [mapped, `${selected.shot_id}:${id}`]));
    const expectedPayload = expectedWithPopupIds({
      ...expected,
      items: [...(expected as Row).items, ...missingItems.map(({ item_id }) => ({ item_id: item_ids[item_id] }))],
      opaque,
    }, expectedIds) as Row;
    // The popup maps every owned item, whereas this helper case supplies a
    // partial map. Its undeclared source_item_id (item-9) still stays literal.
    if (name === 'unmapped_identities_are_left_alone') {
      expectedPayload.items[0].item_id = `${selected.shot_id}:item-2`;
    }
    const timeline = operation === 'settings' ? internal.timeline : patchTimeline;

    expect(selected.shot_id).not.toBe(input.shot_id);
    expect(selected.revision_id).not.toBe(input.revision_id);
    const updatedInternal = revision.internal_timeline_revision as Row;
    expect(updatedInternal.revision_id).not.toBe(internal.revision_id);
    expect(updatedInternal.revision_id).toEqual(expect.any(String));
    expect(updatedInternal.content_digest).toMatch(/^sha256:[0-9a-f]{64}$/);
    expect(revision.content_digest).toMatch(/^sha256:[0-9a-f]{64}$/);
    assert.deepStrictEqual(revision, {
      ...input,
      ...expectedPayload,
      shot_id: selected.shot_id,
      revision_id: selected.revision_id,
      content_digest: revision.content_digest,
      publish: true,
      ...(operation === 'settings' ? { settings } : {}),
      timing: { ...input.timing, duration_ms: timelineContentExtentMs(timeline) },
      internal_timeline_revision: {
        ...internal,
        revision_id: updatedInternal.revision_id,
        content_digest: updatedInternal.content_digest,
        publish: true,
        timeline: {
          ...timeline,
          clips: timeline.clips.map((clip: Row) => ({ ...clip, id: `${selected.shot_id}:${clip.id}` })),
        },
      },
    });
    expect(Object.getPrototypeOf(revision)).toBe(Object.prototype);
    if (Object.hasOwn(payload, '__proto__')) {
      for (const key of ['__proto__', 'constructor', 'prototype']) {
        expect(Object.hasOwn(revision, key)).toBe(true);
        assert.deepStrictEqual(revision[key], payload[key]);
      }
    }
    assert.deepStrictEqual(updated.shot_revisions.slice(0, -1), before.shot_revisions);
    assert.deepStrictEqual(updated.occurrences.slice(1), before.occurrences.slice(1));
    assert.deepStrictEqual(graph, before);
    assert.deepStrictEqual({ patchTimeline, settings }, beforePatch);
  });
});
