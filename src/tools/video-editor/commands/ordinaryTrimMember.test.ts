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

  it('keeps source-second payloads and replay guards without mutating the captured input', async () => {
    const input = await bundle();
    const original = detached(input);
    const basis = captureOrdinaryTrimMember(input, operation('clip-a', { in_s: 9.8999, out_s: 10 }));
    const prepared = finishOrdinaryTrimMember(basis);
    const replay = executeOrdinaryTrimMember(input, prepared.command, 4);

    expect(input).toEqual(original);
    expect((prepared.bundle.parent.clips as Array<Record<string, unknown>>)[0])
      .toMatchObject({ at: 1, from: 9.8999, to: 10, hold: 0.1001, speed: 2 });
    expect(replay.command).toEqual(prepared.command);
    expect(replay.bundle).toEqual(prepared.bundle);
    expect(replay.record).toEqual({ ...prepared.record, ordinal: 4,
      derived_writes: prepared.record.derived_writes.map((write) => ({ ...write, cause: 4 })) });
  });

  it.each([
    ['wrong op', { op: 'clip.set', target: 'clip-a', payload: { in_s: 1, out_s: 5 } }],
    ['missing target', { op: 'clip.trim', target: '', payload: { in_s: 1, out_s: 5 } }],
    ['extra payload', { op: 'clip.trim', target: 'clip-a', payload: { in_s: 1, out_s: 5, hold: 4 } }],
    ['non-finite input', { op: 'clip.trim', target: 'clip-a', payload: { in_s: 1, out_s: Infinity } }],
  ])('refuses malformed member atomically: %s', async (_name, invalid) => {
    const input = await bundle();
    const before = detached(input);
    expect(() => captureOrdinaryTrimMember(input, invalid as never)).toThrow();
    expect(input).toEqual(before);
  });

  it.each([
    ['occurrence/clip:clip-a', 'clip-a'],
    ['parent/clip:other', 'clip-a'],
    ['parent/clip:clip-a::at', 'clip-a'],
  ])('refuses non-reserved identity without a fallback: %s', async (select, target) => {
    const input = await bundle();
    const basis = captureOrdinaryTrimMember(input, operation(target));
    const forged = { ...basis, select };
    expect(() => finishOrdinaryTrimMember(forged)).toThrow('reserved parent clip identity');
  });

  it('refuses a basis whose native command no longer matches the raw operation', async () => {
    const input = await bundle();
    const basis = captureOrdinaryTrimMember(input, operation());
    const forged = {
      ...basis,
      trim: { ...basis.trim, command: { ...basis.trim.command, args: { in_s: 2, out_s: 5 } } },
    };
    expect(() => finishOrdinaryTrimMember(forged)).toThrow('basis command does not match');
  });

  it('refuses unsupported native families through the existing capture contract', async () => {
    const input = await bundle();
    const clip = (input.parent.clips as Array<Record<string, unknown>>)[0];
    for (const changes of [{ source_window: { start: 0, end: 10 } }, { speed: 0 }, { clipType: 'text' }]) {
      Object.assign(clip, changes);
      const changed = detached(input);
      expect(() => captureOrdinaryTrimMember(input, operation())).toThrow();
      expect(input).toEqual(changed);
      delete clip.source_window;
      clip.speed = 2;
      clip.clipType = 'media';
    }
  });
});
