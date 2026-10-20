import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { JsonObject } from './types.ts';
import { captureClipSplit } from './clipSplitCapture.ts';
import { captureClipSplitBatch, executeClipSplitBatch, finishClipSplitBatch } from './clipSplitBatchCapture.ts';
import { copy, freezeJson, type AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_clip_split_batch.json';

const golden = fixture as unknown as { bundle: AuthoredBundle; after_bundle: AuthoredBundle;
  commands: EditCommand[]; records: CommandRecord[]; members: Array<{ clipId: string; rightId: string }>; on: number };
const rows = (bundle: AuthoredBundle) => bundle.parent.clips as JsonObject[];
const mirror = (bundle: AuthoredBundle) => { (bundle.parent.config as Record<string, unknown>).clips = copy(bundle.parent.clips); };

describe('sequential native split batch capture', () => {
  it('matches frozen Agent 027 commands, complete records and full authored bundle', () => {
    const input = freezeJson(copy(golden.bundle));
    const basis = captureClipSplitBatch(input, golden.members, golden.on);
    const result = finishClipSplitBatch(JSON.parse(JSON.stringify(basis)));
    expect(basis.commands).toEqual(golden.commands);
    expect(result).toEqual({ bundle: golden.after_bundle, commands: golden.commands, records: golden.records });
    expect(executeClipSplitBatch(input, basis.commands)).toEqual(result);
    expect(input).toEqual(golden.bundle);
    expect(Object.isFrozen(basis.commands[1].reads)).toBe(true);
    expect(result.commands[1].selections![0].order).toEqual(['parent/clip:clip-a', 'parent/clip:clip-b', 'parent/clip:right:b']);
    expect(result.commands[1].reads).toContainEqual({ ref: 'parent/clip:right:b', path: ['app', 'astrid', 'for'],
      state: { state: 'present', value: 2 } });
  });

  it('refuses independently captured members instead of rewriting their original claims', () => {
    const independently = golden.members.map(({ clipId, rightId }) =>
      captureClipSplit(golden.bundle, `parent/clip:${clipId}`, { on: golden.on, right_id: rightId }).command);
    expect(() => executeClipSplitBatch(golden.bundle, independently)).toThrow('original capture');
  });

  it.each(['reorder', 'insert', 'second-source', 'occupied'] as const)('refuses %s atomically on replay', (change) => {
    const input = copy(golden.bundle);
    if (change === 'reorder') rows(input).reverse();
    if (change === 'insert') rows(input).push({ ...copy(rows(input)[0]), id: 'inserted' });
    if (change === 'second-source') rows(input)[0].from = 3;
    if (change === 'occupied') rows(input).push({ ...copy(rows(input)[0]), id: 'right:a' });
    mirror(input);
    const before = copy(input);
    expect(() => executeClipSplitBatch(input, golden.commands)).toThrow();
    expect(input).toEqual(before);
  });

  it('refuses an unsupported second member after isolated first execution', () => {
    const input = copy(golden.bundle);
    rows(input)[0].time_map = {};
    mirror(input);
    const before = copy(input);
    expect(() => captureClipSplitBatch(input, golden.members, golden.on)).toThrow('time_map');
    expect(input).toEqual(before);
  });

  it('keeps fixed original targets, identities, playhead and complete persisted claims', () => {
    const basis = copy(captureClipSplitBatch(golden.bundle, golden.members, golden.on));
    delete basis.commands[1].reads;
    expect(() => finishClipSplitBatch(basis)).toThrow('incomplete');
    for (const members of [[], [golden.members[0], golden.members[0]],
      [{ clipId: 'clip-b', rightId: 'new' }, { clipId: 'new', rightId: 'newer' }]]) {
      expect(() => captureClipSplitBatch(golden.bundle, members, golden.on)).toThrow();
    }
  });
});
