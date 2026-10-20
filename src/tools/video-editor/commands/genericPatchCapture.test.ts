import { describe, expect, it } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import {
  captureGenericPatch,
  classifyGenericPatch,
  executeGenericPatch,
  GenericPatchRefusal,
  projectGenericPatchPreview,
} from './genericPatchCapture.ts';
import { AuthoredState, copy, freezeJson } from './clipMovePrimitives.ts';
import { environment } from './__tests__/commitSessionEnvironment.ts';

const nativePatch = (hold = 1.25): TimelinePatch => ({ version: 1, operations: [
  { op: 'track.update', target: 'V1', payload: { label: '', mode: 'merge' }, order: 2 },
  { op: 'clip.update', target: 'x', payload: { hold }, order: 1 },
] });

async function authoredBundle() {
  const env = await environment();
  return { env, bundle: await authoringBundleFromDocument(env.initial.canonicalDocument) };
}

describe('bounded native generic patch capture', () => {
  it('classifies the complete patch before native capture', () => {
    expect(classifyGenericPatch({ version: 1, operations: [
      { op: 'track.update', target: 'V1', payload: { label: 'Native' } },
      { op: 'clip.update', target: 'x', payload: { hold: 1.25 } },
    ] })).toBe('supported');
    expect(classifyGenericPatch({ version: 1, operations: [
      { op: 'track.update', target: 'V1', payload: { label: 'Native' } },
      { op: 'project-data.write', target: 'extension', payload: { value: 1 } },
    ] })).toBe('mixed');
    expect(classifyGenericPatch({ version: 1, operations: [
      { op: 'project-data.write', target: 'extension', payload: { value: 1 } },
    ] })).toBe('unsupported');
  });

  it('captures one ordered command list against one sequential authored bundle', async () => {
    const { bundle } = await authoredBundle();
    const input = nativePatch(1.23456789);
    const originalBundle = freezeJson(copy(bundle));
    const originalPatch = copy(input);
    const result = captureGenericPatch(bundle, input, (operation) =>
      operation.op === 'track.update' ? 'parent/track:V1' : 'parent/clip:x');

    expect(result.commands.map((command) => command.op)).toEqual(['clip.set', 'track.set']);
    expect(result.commands[0].args).toEqual({ values: { hold: 1.23456789 }, clear: [] });
    expect(result.commands[1].args).toEqual({ values: { label: '' }, clear: [] });
    expect(result.commands[0].expect?.['parent/clip:x::hold']).toEqual({ state: 'present', value: 1 });
    expect(result.commands[1].expect?.['parent/track:V1::label']).toEqual({ state: 'absent' });
    expect(result.records.map((record) => record.ordinal)).toEqual([0, 1]);
    expect(executeGenericPatch(originalBundle, result.commands)).toEqual({
      bundle: result.bundle,
      records: result.records,
    });
    expect(bundle).toEqual(originalBundle);
    expect(input).toEqual(originalPatch);
    expect(Object.isFrozen(result.patch.operations[0].payload)).toBe(true);
    expect(Object.isFrozen(result.commands[0].expect)).toBe(true);
  });

  it('composes hold/clear, label, and absolute move into one replayable batch', async () => {
    const { bundle: source } = await authoredBundle();
    const bundle = copy(source);
    (bundle.parent.clips[0] as Record<string, unknown>).transition = { type: 'wipe' };
    const patch: TimelinePatch = { version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { values: { hold: 4 }, clear: ['transition'] }, order: 0 },
      { op: 'track.update', target: 'V1', payload: { label: 'Picture' }, order: 1 },
      { op: 'clip.move', target: 'x', payload: { at: 4 }, order: 2 },
    ] };
    const result = captureGenericPatch(bundle, patch, (operation) => operation.op === 'track.update'
      ? 'parent/track:V1' : 'parent/clip:x');

    expect(result.commands.map((command) => command.op)).toEqual(['clip.set', 'track.set', 'clip.move']);
    expect(result.records.map((record) => record.ordinal)).toEqual([0, 1, 2]);
    expect(result.preview.operations).toEqual([
      { op: 'clip.update', target: 'x', payload: { values: { hold: 4 }, clear: ['transition'] } },
      { op: 'track.update', target: 'V1', payload: { label: 'Picture' } },
      { op: 'clip.move', target: 'x', payload: { at: 4 } },
    ]);
    const replay = executeGenericPatch(copy(bundle), result.commands);
    expect(replay).toEqual({ bundle: result.bundle, records: result.records });
    expect(result.bundle.parent.clips[0]).toMatchObject({ hold: 4, at: 4 });
    expect(result.bundle.parent.clips[0]).not.toHaveProperty('transition');
  });

  it('carries a matching move-derived static duration through the producer hold member', async () => {
    const { bundle: source } = await authoredBundle();
    const bundle = copy(source);
    const clip = new AuthoredState(bundle).entity('parent/clip:x')!;
    clip.app = { opaque: { keep: [null, false] }, astrid: { for: 1 } };
    const patch: TimelinePatch = { version: 1, source: 'timeline.native-ordinary', operations: [
      { op: 'clip.move', target: 'x', payload: { at: 4 }, order: 0 },
      { op: 'clip.update', target: 'x', payload: { values: { hold: 5 }, clear: [] }, order: 1 },
    ] };

    const result = captureGenericPatch(bundle, patch, () => 'parent/clip:x');

    expect(result.commands.map((command) => command.op)).toEqual(['clip.move', 'clip.set']);
    expect(result.records[1]!.writes).toEqual([
      { ref: 'parent/clip:x', path: ['app', 'astrid', 'for'], before: { state: 'present', value: 1 }, after: { state: 'present', value: 5 } },
      { ref: 'parent/clip:x', path: ['hold'], before: { state: 'present', value: 1 }, after: { state: 'present', value: 5 } },
    ]);
    expect(new AuthoredState(result.bundle).entity('parent/clip:x')).toMatchObject({
      at: 4, hold: 5, app: { opaque: { keep: [null, false] }, astrid: { for: 5, fixed_start: true } },
    });

    const replay = executeGenericPatch(copy(bundle), result.commands);
    expect(replay).toEqual({ bundle: result.bundle, records: result.records });
  });

  it('refuses an independent static duration atomically after a move', async () => {
    const { bundle: source } = await authoredBundle();
    const bundle = copy(source);
    const moved = executeGenericPatch(bundle, [{
      schema_version: 1, op: 'clip.move', version: '1', select: 'parent/clip:x',
      args: { on: 4 }, intent: { ripple: 'none', anchor: 'fixed', position: 'absolute' },
    }]).bundle;
    const clip = new AuthoredState(moved).entity('parent/clip:x')!;
    clip.app = { opaque: null, astrid: { for: 2 } };
    const patch: TimelinePatch = { version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { values: { hold: 5 }, clear: [] } },
    ] };
    const before = copy(moved);

    expect(() => captureGenericPatch(moved, patch, () => 'parent/clip:x')).toThrow(GenericPatchRefusal);
    expect(moved).toEqual(before);
  });

  it('refuses the complete batch before resolving any owner or executing a member', async () => {
    const { bundle } = await authoredBundle();
    const patch: TimelinePatch = {
      version: 1,
      operations: [
        { op: 'track.update', target: 'V1', payload: { label: 'kept' } },
        { op: 'project-data.write', target: 'extension', payload: { value: 1 } },
        { op: 'clip.update', target: 'x', payload: { hold: 2 } },
      ],
    };
    let resolved = false;
    expect(() => captureGenericPatch(bundle, patch, () => {
      resolved = true;
      return 'parent/track:V1';
    })).toThrow(GenericPatchRefusal);
    try {
      captureGenericPatch(bundle, patch, () => 'parent/track:V1');
    } catch (error) {
      expect((error as GenericPatchRefusal).intentions).toEqual([
        expect.objectContaining({ operationIndex: 0, reason: expect.stringContaining('another patch member') }),
        expect.objectContaining({ operationIndex: 1, op: 'project-data.write', target: 'extension' }),
        expect.objectContaining({ operationIndex: 2, reason: expect.stringContaining('another patch member') }),
      ]);
    }
    expect(resolved).toBe(false);
  });

  it('routes malformed qualified move and scalar shapes to visible native refusal', async () => {
    const { bundle } = await authoredBundle();
    expect(classifyGenericPatch({ version: 1, operations: [
      { op: 'clip.move', target: 'x', payload: { at: -1 } },
    ] })).toBe('mixed');
    expect(classifyGenericPatch({ version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { values: { asset: 'bad' }, clear: [] } },
    ] })).toBe('mixed');
    let resolved = false;
    expect(() => captureGenericPatch(bundle, {
      version: 1,
      operations: [{ op: 'clip.move', target: 'x', payload: { at: -1 } }],
    }, () => {
      resolved = true;
      return 'parent/clip:x';
    })).toThrow(GenericPatchRefusal);
    expect(resolved).toBe(false);
  });

  it.each([
    { op: 'clip.update', target: 'x', payload: { hold: 0 } },
    { op: 'clip.update', target: 'x', payload: { hold: 2 }, clear: ['asset'] },
    { op: 'track.update', target: 'V1', payload: { label: 'x', mode: 'replace' } },
    { op: 'project-data.write', target: 'extension', payload: { value: 1 } },
    { op: 'extension.noop', target: 'extension', payload: {} },
  ])('does not map unsupported operation %j', async (operation) => {
    const { bundle } = await authoredBundle();
    const patch = { version: 1, operations: [operation] } as TimelinePatch;
    expect(() => captureGenericPatch(bundle, patch, () => 'unreachable')).toThrow(GenericPatchRefusal);
  });

  it('projects the native local diff without mutating the displayed state', async () => {
    const { env } = await authoredBundle();
    const current = env.current();
    const before = copy(current);
    const patch: TimelinePatch = {
      version: 1,
      source: 'timeline.native-label-hold',
      operations: [
        { op: 'track.update', target: 'V1', payload: { label: '' } },
        { op: 'clip.update', target: 'x', payload: { hold: 1.123456789 } },
      ],
    };
    const next = projectGenericPatchPreview(patch, current)!;
    expect(next.config.tracks![0].label).toBe('');
    expect(next.resolvedConfig.tracks[0].label).toBe('');
    expect(next.config.clips[0].hold).toBe(1.123456789);
    expect(next.resolvedConfig.clips[0].hold).toBe(1.123456789);
    expect(next.config.clips[0].text).toEqual(before.config.clips[0].text);
    expect(next.config.clips[0].app).toEqual(before.config.clips[0].app);
    expect(next.dataLanes).toBe(current.dataLanes);
    expect(current).toEqual(before);
    expect(() => projectGenericPatchPreview({ ...patch, operations: [
      ...patch.operations, { op: 'clip.update', target: 'missing', payload: { hold: 1 } },
    ] }, current)).toThrow('one displayed target');
  });
});
