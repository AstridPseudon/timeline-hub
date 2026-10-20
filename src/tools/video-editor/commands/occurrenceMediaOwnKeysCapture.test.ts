import { describe, expect, it } from 'vitest';
import type { CommandRecord, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { copy, freezeJson, has } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { captureOccurrenceAddMedia, captureOccurrenceSwapMedia, executeOccurrenceMedia } from './occurrenceMediaCapture.ts';
import type { OccurrenceMediaCommand } from './occurrenceMediaCapture.ts';
import { OccurrenceMediaState } from './occurrenceMediaPrimitives.ts';
import fixtureJson from './fixtures/recipe_m2_occurrence_media_own_keys.json?raw';

type Input = {
  name: string;
  bundle: AuthoredBundle;
  plain: OccurrenceMediaCommand;
  verified_media: VerifiedMedia[];
};
type Golden = Input & {
  key: string;
  mode: 'birth' | 'existing' | 'old';
  operation: 'add' | 'swap';
  command: OccurrenceMediaCommand;
  after_bundle: AuthoredBundle;
  records: CommandRecord[];
};
type Refusal = Input & { error: { kind: string; message: string } };
type ReplayRefusal = Omit<Refusal, 'plain'> & { command: OccurrenceMediaCommand };

// Parse raw JSON: a bundled object literal can consume __proto__ as prototype syntax.
// Full expected output comes only from unmodified frozen Agent cf7448ed execute().
const fixture = JSON.parse(fixtureJson) as { cases: Golden[]; refusals: Refusal[]; replay_refusals: ReplayRefusal[] };
const owner = 'occurrence:occ-a';
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const capture = ({ bundle, plain, verified_media }: Input) => plain.op === 'occurrence.add-media'
  ? captureOccurrenceAddMedia(bundle, plain.select, plain.args.row as Record<string, JSON>, plain.args.media as MediaSelection, verified_media)
  : captureOccurrenceSwapMedia(bundle, plain.select, plain.args.old_media as MediaSelection, plain.args.media as MediaSelection, verified_media);

describe('native occurrence asset own-key parity', () => {
  it.each(fixture.cases)('matches the complete native capture, record and after bundle: $name', (golden) => {
    const input = freezeJson(copy(golden)), before = copy(input);
    const result = capture(input);
    expect(result.command).toEqual(golden.command);
    expect([result.record]).toEqual(golden.records);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect(roundtrip(result)).toEqual(result);
    expect(executeOccurrenceMedia(input.bundle, input.plain, input.verified_media)).toEqual(result);
    expect(executeOccurrenceMedia(input.bundle, roundtrip(result.command), input.verified_media)).toEqual(result);
    expect(capture(input)).toEqual(result);
    expect(input).toEqual(before);

    const state = new OccurrenceMediaState(result.bundle);
    const registry = state.config(owner).registry as { assets: Record<string, unknown> };
    const expected = new OccurrenceMediaState(golden.after_bundle).get(`${owner}/asset:${golden.key}`, []);
    expect(has(registry.assets, golden.key)).toBe(true);
    expect(state.get(`${owner}/asset:${golden.key}`, [])).toEqual(expected);
    expect(Object.getPrototypeOf(registry.assets)).toBe(Object.getPrototypeOf(copy({})));
    expect(Object.getOwnPropertyDescriptor(registry.assets, golden.key)).toEqual({
      value: expected.state === 'present' ? expected.value : undefined,
      enumerable: true, configurable: false, writable: false,
    });
    const created = [`${owner}/asset:${(golden.plain.args.media as MediaSelection).asset}`,
      ...(golden.operation === 'add' ? [`${owner}/clip:reserved-child`] : [])];
    expect(result.command.created).toEqual(golden.mode === 'existing' ? created.slice(1) : created);
    expect(result.record.dependencies.map((dependency) => dependency.pin)).toEqual(golden.operation === 'add'
      ? [golden.plain.args.media] : [golden.plain.args.old_media, golden.plain.args.media]);
    expect(Object.isFrozen(result.command)).toBe(true);
    expect(Object.isFrozen(result.record.writes)).toBe(true);
  });

  it.each(fixture.refusals)('refuses the native occupied alias atomically: $name', (golden) => {
    const input = freezeJson(copy(golden)), before = copy(input);
    expect(() => capture(input)).toThrow();
    expect(input).toEqual(before);
  });

  it.each(fixture.replay_refusals)('refuses native changed membership or reservation atomically: $name', (golden) => {
    const input = freezeJson(copy(golden)), before = copy(input);
    expect(() => executeOccurrenceMedia(input.bundle, input.command, input.verified_media)).toThrow();
    expect(input).toEqual(before);
  });
});
