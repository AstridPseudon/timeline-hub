// @vitest-environment node
import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { AuthoredState, ClipMoveError, copy, freezeJson, type AuthoredBundle } from './clipMovePrimitives.ts';
import { captureClipDelete } from './clipDeleteCapture.ts';
import { captureClipDeleteBatch, executeClipDeleteBatch, finishClipDeleteBatch, type ClipDeleteBatchMember } from './clipDeleteBatchCapture.ts';
import fixture from './fixtures/recipe_m2_clip_delete_batch.json';

type NativeCase = { name: string; bundle: AuthoredBundle; members: ClipDeleteBatchMember[];
  commands: EditCommand[]; records: CommandRecord[]; after_bundle: AuthoredBundle };
const golden = fixture as unknown as { cases: NativeCase[]; second_member_refusal: AuthoredBundle;
  refusals: { name: string; bundle: AuthoredBundle; commands: EditCommand[]; kind: string }[];
  disjoint: { bundle: AuthoredBundle; after_bundle: AuthoredBundle } };
const original = golden.cases[0];
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));

describe('sequential native parent delete capture', () => {
  it.each(golden.cases)('matches full native sequence, indexed records and bundle: $name', (entry) => {
    const input = freezeJson(copy(entry.bundle));
    const before = copy(input);
    const members = copy(entry.members);
    const basis = captureClipDeleteBatch(input, members);
    members.reverse();
    const result = finishClipDeleteBatch(roundtrip(basis));
    expect(result).toEqual({ commands: entry.commands, records: entry.records, bundle: entry.after_bundle });
    expect(executeClipDeleteBatch(input, roundtrip(basis.commands))).toEqual(result);
    expect(input).toEqual(before);
    expect(Object.isFrozen(basis.commands[0].selections)).toBe(true);
    for (const [index, record] of result.records.entries()) {
      expect(record.ordinal).toBe(index);
      expect(record.derived_writes.every((write) => write.cause === index)).toBe(true);
    }
  });

  it('records each shrinking collection instead of capturing every command against the initial state', () => {
    const basis = captureClipDeleteBatch(original.bundle, original.members);
    const orders = basis.commands.map((command) => command.selections!.find((selection) => selection.key === 'collection.clips')!.order);
    expect(orders).toEqual([
      ['parent/clip:clip-a', 'parent/clip:clip-b', 'parent/clip:clip-c'],
      ['parent/clip:clip-a', 'parent/clip:clip-c'],
    ]);
    const separate = original.members.map(({ clipId }) => captureClipDelete(original.bundle, `parent/clip:${clipId}`).command);
    const before = copy(original.bundle);
    expect(() => executeClipDeleteBatch(original.bundle, separate)).toThrow('original capture');
    expect(original.bundle).toEqual(before);
  });

  it.each(golden.refusals)('atomically refuses the same fixed replay as native: $name', (entry) => {
    const input = freezeJson(copy(entry.bundle));
    const before = copy(input);
    try {
      executeClipDeleteBatch(input, entry.commands);
      expect.fail('unsupported replay accepted');
    } catch (error) {
      expect(error).toBeInstanceOf(ClipMoveError);
      // Existing single-delete capture reports local claim mismatch/unsupported dependency;
      // Agent execute classifies those fixed-command conflicts before running the command.
      expect((error as ClipMoveError).kind).toBe(entry.name === 'dependency' ? 'unsupported_dependency' : 'capture_mismatch');
    }
    expect(input).toEqual(before);
  });

  it('refuses an unsupported second target after an executable first capture without publishing partial state', () => {
    const input = freezeJson(copy(golden.second_member_refusal));
    expect(() => captureClipDelete(input, 'parent/clip:clip-b')).not.toThrow();
    const before = copy(input);
    expect(() => captureClipDeleteBatch(input, original.members)).toThrow('nested clip ownership');
    expect(input).toEqual(before);
  });

  it.each([
    [], [{ clipId: 'clip-b', ownerRef: 'parent' }, { clipId: 'clip-b', ownerRef: 'parent' }],
    [{ clipId: 'clip-b', ownerRef: 'parent' }, { clipId: 'missing', ownerRef: 'parent' }],
    [{ clipId: 'clip-b', ownerRef: 'parent' }, { clipId: 'clip-a', ownerRef: 'occurrence:occ-a' }],
    [{ clipId: 'clip-a', ownerRef: 'parent' }, { clipId: 'bad/id', ownerRef: 'parent' }],
  ])('refuses missing, duplicate or unsupported original members %#', (members) => {
    const before = copy(original.bundle);
    expect(() => captureClipDeleteBatch(original.bundle, members as ClipDeleteBatchMember[])).toThrow();
    expect(original.bundle).toEqual(before);
  });

  it('keeps disjoint accepted work with the exact original sequential commands', () => {
    const basis = captureClipDeleteBatch(original.bundle, original.members);
    const result = executeClipDeleteBatch(golden.disjoint.bundle, roundtrip(basis.commands));
    expect(result.commands).toEqual(original.commands);
    expect(result.bundle).toEqual(golden.disjoint.after_bundle);
    expect(new AuthoredState(result.bundle).entity('parent/clip:clip-c')!.opaque).toEqual({ accepted: [null, false] });
  });

  it('refuses incomplete and altered durable bases', () => {
    const basis = roundtrip(captureClipDeleteBatch(original.bundle, original.members));
    expect(() => finishClipDeleteBatch({ bundle: basis.bundle })).toThrow('incomplete');
    expect(() => finishClipDeleteBatch({ ...basis, commands: [] })).toThrow();
    expect(() => finishClipDeleteBatch({ ...basis, commands: [...basis.commands].reverse() })).toThrow();
  });
});
