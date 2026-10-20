// @vitest-environment node
import { describe, expect, it } from 'vitest';
import type { CanonicalDocument, CommandRecord, EditCommand, JSON as JsonValue } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import {
  captureClipSplit,
  executeClipSplit,
  finishClipSplit,
} from './clipSplitCapture.ts';
import { AuthoredState, ClipMoveError, freezeJson } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_clip_split.json';

type SplitFixture = {
  input: CanonicalDocument;
  commands: EditCommand[];
  records: CommandRecord[];
  output: CanonicalDocument;
};

const golden = fixture as SplitFixture;
const select = 'parent/clip:clip-a';
const args = { on: 3, right_id: 'right' } as const;
const detached = <T>(value: T): T => structuredClone(value);

async function bundle(): Promise<AuthoredBundle> {
  return authoringBundleFromDocument(detached(golden.input));
}

function clips(value: AuthoredBundle): Array<Record<string, JsonValue>> {
  return value.parent.clips as Array<Record<string, JsonValue>>;
}

function target(value: AuthoredBundle, ref = select): Record<string, JsonValue> {
  return new AuthoredState(value).entity(ref)!;
}

function canonicalParent(value: CanonicalDocument): Record<string, JsonValue> {
  const parent = detached(value.parent_revision.payload) as Record<string, JsonValue>;
  delete parent.occurrences;
  return parent;
}

describe('native parent clip.split capture parity', () => {
  it('matches the frozen source command, complete recorder, and authored output exactly', async () => {
    const input = await bundle();
    const result = executeClipSplit(input, detached(golden.commands[0]));

    expect(result.command).toEqual(golden.records[0].command);
    expect(result.record).toEqual(golden.records[0]);
    expect(result.bundle.parent).toEqual(canonicalParent(golden.output));
    expect(result.bundle.parent.config).toEqual(canonicalParent(golden.output).config);
    expect(result.bundle.placements).toEqual(input.placements);
    expect(input).toEqual(await bundle());
  });

  it('captures the original basis, preserves opaque/null/absent values, and retries with one reserved ID', async () => {
    const input = await bundle();
    const original = detached(input);
    const basis = captureClipSplit(input, select, args);
    const persisted = JSON.parse(JSON.stringify(basis)) as typeof basis;

    expect(basis.command).toEqual(golden.records[0].command);
    expect(finishClipSplit(persisted)).toEqual(finishClipSplit(basis));
    expect(input).toEqual(original);
    expect(Object.isFrozen(basis)).toBe(true);
    expect(Object.isFrozen(basis.bundle)).toBe(true);
    expect(Object.isFrozen(basis.command.reads)).toBe(true);

    const result = finishClipSplit(persisted);
    const [left, right, neighbor] = clips(result.bundle);
    expect(left).toMatchObject({ id: 'clip-a', at: 1, from: 2, to: 6, hold: 4, speed: 2 });
    expect(right).toMatchObject({ id: 'right', at: 3, from: 6, to: 10, hold: 4, speed: 2 });
    expect(right.opaque).toEqual(left.opaque);
    expect(right.params).toEqual(left.params);
    expect(neighbor).toEqual(clips(original)[1]);
    expect(result.command.created).toEqual(['parent/clip:right']);
    expect(() => executeClipSplit(result.bundle, result.command)).toThrow('occupied');
  });

  it('keeps literal source windows, speed, native units, and half-open frame ownership', async () => {
    const input = await bundle();
    for (const clip of [clips(input)[0], ((input.parent.config as Record<string, JsonValue>).clips as Array<Record<string, JsonValue>>)[0]]) {
      clip.from = 2.123456789;
      clip.to = 10.987654321;
      clip.speed = 1.3;
      delete clip.hold;
    }
    const captured = captureClipSplit(input, select, args);
    const result = finishClipSplit(captured);
    const [left, right] = clips(result.bundle);
    expect(left.from).toBe(2.123456789);
    expect(left.to).toBe(2.123456789 + (3 - 1) * 1.3);
    expect(right.from).toBe(left.to);
    expect(right.to).toBe(10.987654321);
    expect(left.speed).toBe(1.3);
    expect(right.speed).toBe(1.3);
    expect(right.at).toBe(3);
    expect(result.command.created).toEqual(['parent/clip:right']);
  });

  it('allows disjoint neighbor edits while refusing touched source and selection claims', async () => {
    const original = await bundle();
    const command = captureClipSplit(original, select, args).command;

    const disjoint = detached(original);
    const disjointRows = clips(disjoint);
    disjointRows[1].params = { unrelated: [null, false] };
    (disjoint.parent.config as Record<string, JsonValue>).clips = detached(disjointRows);
    expect(executeClipSplit(disjoint, command).command).toEqual(command);

    const touched = detached(original);
    touched.parent.clips = clips(touched).map((row, index) => index === 1
      ? { ...row, app: { astrid: { on: 'word:changed' } } } : row);
    (touched.parent.config as Record<string, JsonValue>).clips = detached(touched.parent.clips);
    expect(() => executeClipSplit(touched, command)).toThrow(ClipMoveError);

    const reordered = detached(original);
    reordered.parent.clips = clips(reordered).reverse();
    (reordered.parent.config as Record<string, JsonValue>).clips = detached(reordered.parent.clips);
    expect(() => executeClipSplit(reordered, command)).toThrow(ClipMoveError);
  });

  it.each([
    ['mapped clip', (value: AuthoredBundle) => { target(value).time_map = {}; }],
    ['unsupported transition', (value: AuthoredBundle) => { target(value).transition = 'fade'; }],
    ['animated params', (value: AuthoredBundle) => { target(value).params = { keyframes: [] }; }],
    ['unsupported clip type', (value: AuthoredBundle) => { target(value).clipType = 'text'; }],
    ['registry source', (value: AuthoredBundle) => {
      ((value.parent.registry as Record<string, JsonValue>).assets as Record<string, JsonValue>).picture = { type: 'model' };
    }],
    ['moving media without source window', (value: AuthoredBundle) => {
      delete target(value).from;
      delete target(value).to;
      delete target(value).hold;
    }],
  ])('refuses %s without mutating the authored input', async (_name, mutate) => {
    const input = await bundle();
    mutate(input);
    const before = detached(input);
    expect(() => captureClipSplit(input, select, args)).toThrow();
    expect(input).toEqual(before);
  });

  it.each([
    ['boundary before start', { on: 1, right_id: 'new-right' }],
    ['boundary at end', { on: 5, right_id: 'new-right' }],
    ['invalid ID', { on: 3, right_id: 'bad/id' }],
    ['missing target', { on: 3, right_id: 'new-right', select: 'parent/clip:missing' }],
    ['occurrence target', { on: 3, right_id: 'new-right', select: 'occurrence:occ-a/clip:clip-a' }],
  ] as const)('refuses malformed split input atomically: %s', async (_name, change) => {
    const input = await bundle();
    const before = detached(input);
    const command = {
      schema_version: 1, op: 'clip.split', version: '1',
      select: 'select' in change ? change.select : select,
      args: { on: change.on, right_id: change.right_id }, intent: {},
    } as unknown as EditCommand;
    expect(() => executeClipSplit(input, command)).toThrow();
    expect(input).toEqual(before);
  });

  it('preserves exact explicit nulls and absent timing fields through both halves', async () => {
    const input = await bundle();
    const row = target(input);
    row.hold = null;
    row.speed = null;
    row.params = null;
    row.from = 2;
    row.to = 10;
    const mirror = (input.parent.config as Record<string, JsonValue>).clips as JsonValue[];
    mirror[0] = detached(row);
    const result = finishClipSplit(captureClipSplit(input, select, args));
    const [left, right] = clips(result.bundle);
    expect(left.hold).toBeNull();
    expect(right.hold).toBeNull();
    expect(left.speed).toBeNull();
    expect(right.speed).toBeNull();
    expect(left.params).toBeNull();
    expect(right.params).toBeNull();
    expect(left.from).toBe(2);
    expect(right.from).toBe(6);
    expect(left.to).toBe(6);
    expect(right.to).toBe(10);
  });

  it('rejects an incomplete or forged persisted basis without recapturing', async () => {
    const input = await bundle();
    const basis = JSON.parse(JSON.stringify(captureClipSplit(input, select, args))) as {
      bundle: AuthoredBundle; command: EditCommand;
    };
    delete basis.command.reads;
    expect(() => finishClipSplit(freezeJson(basis))).toThrow('incomplete');
    const forged = captureClipSplit(input, select, args).command;
    forged.created = ['parent/clip:other'];
    expect(() => executeClipSplit(input, forged)).toThrow('original capture');
  });
});

