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
import { captureClipMove, finishClipMove } from './clipMoveCapture.ts';
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
    const sourceIn = 2.123456789;
    const sourceOut = 10.987654321;
    const literalFor = (sourceOut - sourceIn) / 1.3;
    for (const clip of [clips(input)[0], ((input.parent.config as Record<string, JsonValue>).clips as Array<Record<string, JsonValue>>)[0]]) {
      clip.from = sourceIn;
      clip.to = sourceOut;
      clip.speed = 1.3;
      ((clip.app as Record<string, JsonValue>).astrid as Record<string, JsonValue>).for = literalFor;
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
    (row.app as Record<string, JsonValue>).astrid = {
      ...((row.app as Record<string, JsonValue>).astrid as Record<string, JsonValue>), for: 8,
    };
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
    expect(right.from).toBe(4);
    expect(left.to).toBe(4);
    expect(right.to).toBe(10);
  });

  it('splits after a native move with the exact command, recorder, and authored state', async () => {
    const input = await bundle();
    (input.parent.config as Record<string, JsonValue>).output = { fps: 30 };
    const moved = finishClipMove(captureClipMove(input, select), 2).bundle;
    const before = detached(moved);
    const basis = captureClipSplit(moved, select, { ...args, on: 4 });
    const result = finishClipSplit(basis);
    const left = { ...detached(clips(moved)[0]), hold: 4, to: 6 };
    const right = { ...detached(clips(moved)[0]), id: 'right', at: 4, hold: 4, from: 6 };
    for (const half of [left, right]) {
      ((half.app as Record<string, JsonValue>).astrid as Record<string, JsonValue>).for = 2;
    }
    const expected = detached(moved);
    expected.parent.clips = [left, right, detached(clips(moved)[1])];
    (expected.parent.config as Record<string, JsonValue>).clips = detached(expected.parent.clips);

    const record = detached(golden.records[0]);
    record.command.args.on = 4;
    for (const reads of [record.command.reads!, record.reads]) {
      reads.find((read) => read.ref === select && read.path.length === 0)!.state = {
        state: 'present', value: detached(clips(moved)[0]),
      };
      reads.find((read) => read.ref === 'parent' && read.path.join('.') === 'config.output.fps')!.state = {
        state: 'present', value: 30,
      };
    }
    record.writes[0].after = { state: 'present', value: detached(right) };
    record.derived_writes[0].before = { state: 'present', value: detached(clips(moved)) };
    record.derived_writes[0].after = { state: 'present', value: detached(expected.parent.clips) };

    expect(result.command).toEqual(record.command);
    expect(result.record).toEqual(record);
    expect(result.bundle).toEqual(expected);
    expect(moved).toEqual(before);
    expect(finishClipSplit(JSON.parse(JSON.stringify(basis)))).toEqual(result);
  });

  it.each([[[]], [['app']], [['app', 'astrid']]])('preserves exact true fixed_start at %j', async (prefix) => {
    const input = await bundle();
    let container = target(input);
    for (const key of prefix) container = container[key] as Record<string, JsonValue>;
    container.fixed_start = true;
    (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
    const result = finishClipSplit(captureClipSplit(input, select, args));
    for (const half of clips(result.bundle).slice(0, 2)) {
      let authored = half;
      for (const key of prefix) authored = authored[key] as Record<string, JsonValue>;
      expect(authored.fixed_start).toBe(true);
    }
    expect(result.record.writes.some((write) => write.path.includes('fixed_start'))).toBe(false);
  });

  it.each([
    ['fixed_start', false], ['fixed_start', 0], ['fixed_start', 1], ['fixed_start', 'true'],
    ['fixed_start', {}], ['fixed_start', []], ['on', true], ['until', 4], ['words', []],
  ] as const)('refuses unsupported %s=%j at every native intent site', async (key, value) => {
    for (const prefix of [[], ['app'], ['app', 'astrid']]) {
      const input = await bundle();
      let container = target(input);
      for (const part of prefix) container = container[part] as Record<string, JsonValue>;
      container[key] = detached(value) as JsonValue;
      (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
      const before = detached(input);
      expect(() => captureClipSplit(input, select, args)).toThrow(`does not support ${key}`);
      expect(input).toEqual(before);
    }
  });

  it.each(['image', 'audio', ' VIDEO/MP4; codecs=avc1 ', 'Audio/MPEG', ' image/png ',
    'IMAGE', 'image-legacy', 'video-legacy', 'audio-legacy'])('validates %j without rewriting authored media', async (type) => {
    const input = await bundle();
    const assets = (input.parent.registry as Record<string, JsonValue>).assets as Record<string, JsonValue>;
    (assets.picture as Record<string, JsonValue>).type = type;
    const before = detached(input);
    const result = finishClipSplit(captureClipSplit(input, select, args));
    const record = detached(golden.records[0]);
    for (const reads of [record.command.reads!, record.reads]) {
      reads.find((read) => read.ref === 'parent/registry')!.state = {
        state: 'present', value: detached(assets.picture),
      };
    }
    const parent = canonicalParent(golden.output);
    parent.registry = detached(input.parent.registry);
    expect(result.command).toEqual(record.command);
    expect(result.record).toEqual(record);
    expect(result.bundle.parent).toEqual(parent);
    expect(input).toEqual(before);
  });

  it.each(['model', 'images', 'videoish', 'video ; codecs=avc1', ['image'], null, false].map((type) => ({ type })))(
    'refuses an unsupported registry type $type', async ({ type }) => {
      const input = await bundle();
      const assets = (input.parent.registry as Record<string, JsonValue>).assets as Record<string, JsonValue>;
      (assets.picture as Record<string, JsonValue>).type = type;
      const before = detached(input);
      expect(() => captureClipSplit(input, select, args)).toThrow('known media source');
      expect(input).toEqual(before);
    },
  );

  it.each(['image', 'image/png', 'IMAGE', 'image-legacy'])(
    'keeps the native literal-image requirement without a source window: %s', async (type) => {
      const input = await bundle();
      const row = target(input);
      delete row.from;
      delete row.to;
      (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
      const assets = (input.parent.registry as Record<string, JsonValue>).assets as Record<string, JsonValue>;
      (assets.picture as Record<string, JsonValue>).type = type;
      const before = detached(input);
      if (type === 'image') {
        const result = finishClipSplit(captureClipSplit(input, select, args));
        for (const half of clips(result.bundle).slice(0, 2)) {
          expect(half.hold).toBe(4);
          expect(half).not.toHaveProperty('from');
          expect(half).not.toHaveProperty('to');
        }
      } else {
        expect(() => captureClipSplit(input, select, args)).toThrow('explicit source window');
      }
      expect(input).toEqual(before);
    },
  );

  it.each([
    ['absent', undefined, 4], ['null', null, 4], ['one', 1, 4], ['two', 2, 6],
  ] as const)('uses the native speed default and source-cut formula: %s', async (_name, speed, cut) => {
    const input = await bundle();
    const row = target(input);
    row.hold = null;
    if (speed === undefined) delete row.speed;
    else row.speed = speed;
    ((row.app as Record<string, JsonValue>).astrid as Record<string, JsonValue>).for = 8 / (speed ?? 1);
    (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
    const before = detached(input);
    const result = finishClipSplit(captureClipSplit(input, select, args));
    const [left, right] = clips(result.bundle);
    expect(left.from).toBe(2);
    expect(left.to).toBe(cut);
    expect(right.from).toBe(cut);
    expect(right.to).toBe(10);
    for (const half of [left, right]) {
      expect(half.hold).toBeNull();
      if (speed === undefined) expect(half).not.toHaveProperty('speed');
      else expect(half.speed).toBe(speed);
    }
    expect(input).toEqual(before);
  });

  it('accepts native positive integer FPS ratios beyond the safe-integer range', async () => {
    const input = await bundle();
    const fps = { numerator: 300000000000000000, denominator: 10000000000000000 };
    (input.parent.config as Record<string, JsonValue>).output = { fps };
    const result = finishClipSplit(captureClipSplit(input, select, args));
    expect(clips(result.bundle)[0].to).toBe(6);
    expect(clips(result.bundle)[1].from).toBe(6);
    expect(result.command.reads).toContainEqual({
      ref: 'parent', path: ['config', 'output', 'fps'],
      state: { state: 'present', value: fps },
    });
  });

  it('refuses an explicit null collection owner atomically', async () => {
    const input = await bundle();
    input.parent.config = null;
    const before = detached(input);
    expect(() => captureClipSplit(input, select, args)).toThrow('collection owner must be an object');
    expect(input).toEqual(before);
  });

  it('refuses non-finite half-open frame calculations atomically', async () => {
    const input = await bundle();
    const row = target(input);
    row.at = 1e308;
    row.from = 0;
    row.to = 1e308;
    row.hold = 1e308;
    row.speed = 1;
    ((row.app as Record<string, JsonValue>).astrid as Record<string, JsonValue>).for = 1e308;
    (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
    const before = detached(input);
    expect(() => captureClipSplit(input, select, { ...args, on: 1.1e308 })).toThrow('frame value must be finite');
    expect(input).toEqual(before);
  });

  it('preserves native integer frame sums beyond the safe-integer range', async () => {
    const input = await bundle();
    target(input).at = 10000000000000000;
    (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
    (input.parent.config as Record<string, JsonValue>).output = { fps: 30 };
    const before = detached(input);
    // Native left end is 300000000000000060; rounded right start is 300000000000000064.
    expect(() => captureClipSplit(input, select, { ...args, on: 10000000000000002 }))
      .toThrow('half-open frame geometry');
    expect(input).toEqual(before);
  });

  it('checks claimed created IDs before replaying changed timing', async () => {
    const input = await bundle();
    const result = finishClipSplit(captureClipSplit(input, select, args));
    target(result.bundle).speed = 0;
    (result.bundle.parent.config as Record<string, JsonValue>).clips = detached(clips(result.bundle));
    const before = detached(result.bundle);
    expect(() => executeClipSplit(result.bundle, result.command)).toThrow('created identity is occupied');
    expect(result.bundle).toEqual(before);
  });

  it('preserves single colons in stable target and created clip identities', async () => {
    const input = await bundle();
    target(input).id = 'clip:a';
    (input.parent.config as Record<string, JsonValue>).clips = detached(clips(input));
    const before = detached(input);
    const basis = captureClipSplit(input, 'parent/clip:clip:a', { ...args, right_id: 'right:part' });
    const result = finishClipSplit(basis);
    expect(clips(result.bundle).map((row) => row.id)).toEqual(['clip:a', 'right:part', 'clip-b']);
    expect(result.command.resolved).toEqual(['parent/clip:clip:a']);
    expect(result.command.created).toEqual(['parent/clip:right:part']);
    expect(result.command.bindings).toEqual({ 'split.target': 'parent/clip:clip:a' });
    expect(result.command.selections![1].boundaries).toEqual(['parent/clip:clip:a', 'parent/clip:clip-b']);
    expect(finishClipSplit(JSON.parse(JSON.stringify(basis)))).toEqual(result);
    expect(input).toEqual(before);
  });

  it('rejects an incomplete or forged persisted basis without recapturing', async () => {
    const input = await bundle();
    const basis = JSON.parse(JSON.stringify(captureClipSplit(input, select, args))) as {
      bundle: AuthoredBundle; command: EditCommand;
    };
    delete basis.command.reads;
    expect(() => finishClipSplit(freezeJson(basis))).toThrow('incomplete');
    const forged = detached(captureClipSplit(input, select, args).command);
    forged.created = ['parent/clip:other'];
    expect(() => executeClipSplit(input, forged)).toThrow('original capture');
  });
});

