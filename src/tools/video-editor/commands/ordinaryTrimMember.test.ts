// @vitest-environment node
import { describe, expect, it } from 'vitest';
import type { CanonicalDocument, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import fixture from './fixtures/recipe_m2_clip_trim.json';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import {
  captureOrdinaryTrimMember,
  executeOrdinaryTrimMember,
  finishOrdinaryTrimMember,
} from './ordinaryTrimMember.ts';
import type { OrdinaryTrimOperation, OrdinaryTrimPayload } from './ordinaryTrimMember.ts';

type TrimFixture = {
  input: CanonicalDocument;
  commands: EditCommand[];
  records: Array<{ ordinal: number; command: EditCommand; [key: string]: unknown }>;
  output: CanonicalDocument;
};

const golden = fixture as TrimFixture;
const operation = (target = 'clip-a', payload: OrdinaryTrimPayload = { in_s: 1, out_s: 5 }): OrdinaryTrimOperation => ({
  op: 'clip.trim' as const,
  target,
  payload,
});
const detached = <T>(value: T): T => structuredClone(value);

async function bundle(): Promise<AuthoredBundle> {
  return authoringBundleFromDocument(detached(golden.input));
}

describe('ordinary clip.trim patch member', () => {
  it('uses the approved native source capture for exact command, record, and bundle output', async () => {
    const input = await bundle();
    const basis = captureOrdinaryTrimMember(input, operation());
    const prepared = finishOrdinaryTrimMember(basis, 0);

    expect(prepared.operation).toEqual(operation());
    expect(prepared.command).toEqual(golden.records[0].command);
    expect(prepared.record).toEqual(golden.records[0]);
    const outputPayload = golden.output.parent_revision.payload as Record<string, unknown>;
    expect((prepared.bundle.parent.clips as Array<Record<string, unknown>>)[0])
      .toEqual((outputPayload.clips as Array<Record<string, unknown>>)[0]);
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.trim.bundle)).toBe(true);
    expect((basis.trim.command.args as Record<string, unknown>)).toEqual({ in_s: 1, out_s: 5 });
  });

  it('replays the captured command with its original source and identity guards', async () => {
    const input = await bundle();
    const prepared = finishOrdinaryTrimMember(captureOrdinaryTrimMember(input, operation()), 0);
    const replay = executeOrdinaryTrimMember(input, prepared.command, 4);

    expect(replay.command).toEqual(prepared.command);
    expect(replay.bundle).toEqual(prepared.bundle);
    expect(replay.record).toEqual({
      ...prepared.record,
      ordinal: 4,
      derived_writes: prepared.record.derived_writes.map((write) => ({ ...write, cause: 4 })),
    });
  });

  it('refuses malformed qualified endpoints before capture', async () => {
    const input = await bundle();
    expect(() => captureOrdinaryTrimMember(input, operation('clip-a', { in_s: 'bad' } as unknown as OrdinaryTrimPayload)))
      .toThrow('finite source-second value');
    expect(() => captureOrdinaryTrimMember(input, operation('clip-a', { in_s: 5, out_s: 1 })))
      .toThrow('source range');
    expect(() => captureOrdinaryTrimMember(input, operation('occurrence:clip-a')))
      .toThrow('target disappeared');
  });
});
