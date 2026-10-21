import { describe, expect, it } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { AuthoredState, copy } from './clipMovePrimitives.ts';
import {
  captureProjectDataMember,
  executeProjectDataMember,
  ProjectDataMemberRefusal,
} from './projectDataMember.ts';
import { environment } from './__tests__/commitSessionEnvironment.ts';

const target = 'com.example.compiler-canary';

function write(key: string, value: unknown, extra: Record<string, unknown> = {}, order?: number) {
  return { op: 'project-data.write' as const, target, payload: { key, value, ...extra }, ...(order === undefined ? {} : { order }) };
}

function remove(key: string, order?: number) {
  return { op: 'project-data.delete' as const, target, payload: { key }, ...(order === undefined ? {} : { order }) };
}

async function authoredBundle() {
  const env = await environment();
  return authoringBundleFromDocument(env.initial.canonicalDocument);
}

describe('bounded inert project-data member', () => {
  it('captures source and source-map writes as one ordered native command batch', async () => {
    const bundle = await authoredBundle();
    const patch: TimelinePatch = { version: 1, operations: [
      write('__dsl__:dsl://com.example.compiler-canary/main.json', { version: 1 }),
      write('__dsl_sm__:sm-1', { id: 'sm-1', sourceLine: 3 }),
    ] };

    const result = captureProjectDataMember(bundle, patch);

    expect(result.commands).toHaveLength(2);
    expect(result.commands.map(({ op, select }) => ({ op, select }))).toEqual([
      { op: 'project-data.write', select: 'parent' },
      { op: 'project-data.write', select: 'parent' },
    ]);
    expect(result.commands[0].resolved).toEqual([]);
    expect(result.commands.map((command) => command.args)).toEqual([
      { target, key: '__dsl__:dsl://com.example.compiler-canary/main.json', value: { version: 1 }, mode: 'replace' },
      { target, key: '__dsl_sm__:sm-1', value: { id: 'sm-1', sourceLine: 3 }, mode: 'replace' },
    ]);
    expect(result.records.map(({ ordinal }) => ordinal)).toEqual([0, 1]);
    expect(result.bundle.parent.config.app).toEqual({ [target]: {
      '__dsl__:dsl://com.example.compiler-canary/main.json': { version: 1 },
      '__dsl_sm__:sm-1': { id: 'sm-1', sourceLine: 3 },
    } });
    expect(result.commands[0].expect).toMatchObject({
      'parent::config.app': { state: 'absent' },
      [`parent::config.app[${JSON.stringify(target)}]`]: { state: 'absent' },
      [`parent::config.app[${JSON.stringify(target)}][${JSON.stringify('__dsl__:dsl://com.example.compiler-canary/main.json')}]`]: {
        state: 'absent',
      },
    });
    expect(result.records[0].reads).toEqual(expect.arrayContaining([
      { ref: 'parent', path: ['config', 'app'], state: { state: 'absent' } },
      { ref: 'parent', path: ['config', 'app', target], state: { state: 'absent' } },
    ]));
    expect(result.commands[0]).not.toHaveProperty('reads');

    const replayed = executeProjectDataMember(copy(bundle), result.commands);
    expect(replayed.bundle).toEqual(result.bundle);
    expect(replayed.records).toEqual(result.records);
    expect(bundle.parent.config.app).toBeUndefined();
  });

  it('preserves null, siblings, opaque values, and exact leaf replacement', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = { [target]: {
      keep: { opaque: true },
      slot: null,
      source: null,
    } };
    const before = copy(bundle);
    const opaqueValue = { metadata: { opaque: true }, list: [1, 2] };
    const result = captureProjectDataMember(bundle, { version: 1, operations: [
      write('source', opaqueValue),
    ] });

    expect(result.bundle.parent.config.app).toEqual({ [target]: {
      keep: { opaque: true },
      slot: null,
      source: opaqueValue,
    } });
    expect(result.commands[0].expect?.[`parent::config.app[${JSON.stringify(target)}].source`]).toEqual({
      state: 'present', value: null,
    });
    expect(bundle).toEqual(before);
  });

  it('captures dormant delete as Agent remove and restores a pruned namespace order after JSON reload', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = {
      before: { opaque: true },
      [target]: { gone: null },
      after: { keep: [null, false, 0] },
    };
    const before = copy(bundle);
    const captured = captureProjectDataMember(bundle, { version: 1, operations: [remove('gone')] });

    expect(captured.commands[0].args).toEqual({ target, key: 'gone', mode: 'remove' });
    expect(captured.bundle.parent.config.app).toEqual({
      before: { opaque: true },
      after: { keep: [null, false, 0] },
    });
    expect(captured.records[0].writes).toEqual([
      { ref: 'parent', path: ['config', 'app', target, 'gone'],
        before: { state: 'present', value: null }, after: { state: 'absent' } },
      { ref: 'parent', path: ['config', 'app', target],
        before: { state: 'present', value: {} }, after: { state: 'absent' },
        insertion_order: ['before', target, 'after'] },
    ]);

    const replayed = executeProjectDataMember(copy(bundle), JSON.parse(JSON.stringify(captured.commands)));
    expect(replayed).toEqual({ bundle: captured.bundle, records: captured.records });
    const restored = copy(captured.bundle);
    const state = new AuthoredState(restored);
    for (const write of [...captured.records[0].writes].reverse()) {
      state.set(write.ref, write.path, write.before, write.insertion_order);
    }
    expect(restored).toEqual(before);
    expect(Object.keys(restored.parent.config.app!)).toEqual(['before', target, 'after']);
  });

  it('keeps delete absent/null/opaque compatibility without manufacturing an order carrier', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = { [target]: { keep: { opaque: true }, gone: false }, sibling: null };
    const removed = captureProjectDataMember(bundle, { version: 1, operations: [remove('gone')] });
    expect(removed.bundle.parent.config.app).toEqual({ [target]: { keep: { opaque: true } }, sibling: null });
    expect(removed.records[0].writes).toEqual([
      { ref: 'parent', path: ['config', 'app', target, 'gone'],
        before: { state: 'present', value: false }, after: { state: 'absent' } },
    ]);

    const absent = captureProjectDataMember(bundle, { version: 1, operations: [remove('missing')] });
    expect(absent.bundle).toEqual(bundle);
    expect(absent.records[0].writes).toHaveLength(1);
    expect(absent.records[0].writes[0]).toMatchObject({
      path: ['config', 'app', target, 'missing'],
      before: { state: 'absent' }, after: { state: 'absent' },
    });
    expect('insertion_order' in absent.records[0].writes[0]).toBe(false);

    const nullNamespace = copy(bundle);
    nullNamespace.parent.config.app = { before: 1, [target]: null, after: { opaque: true } };
    const nulled = captureProjectDataMember(nullNamespace, { version: 1, operations: [remove('gone')] });
    expect(nulled.bundle.parent.config.app).toEqual({ before: 1, after: { opaque: true } });
    expect(nulled.records[0].writes[0]).toMatchObject({
      insertion_order: ['before', target, 'after'],
    });
  });

  it('lowers Main merge, default replace, and declared order to native replace cells', async () => {
    const env = await environment();
    const bundle = await authoringBundleFromDocument(env.initial.canonicalDocument);
    const initial = {
      settings: {
        volume: 1,
        theme: 'light',
        nested: { keep: true, override: 'old' },
      },
      replacement: { old: true },
      opaque: { keep: ['in', 'order'] },
    };
    bundle.parent.config = { app: { [target]: copy(initial) } };
    expect(bundle.parent.config.app).toEqual({ [target]: initial });
    env.current().config.app = { [target]: copy(initial) };
    const patch: TimelinePatch = { version: 1, operations: [
      write('settings', { volume: 3, nested: { late: true } }, { mode: 'merge' }, 5),
      write('settings', { theme: 'dark', nested: { first: true } }, { mode: 'merge' }, 1),
      write('replacement', { fresh: true }),
    ] };

    const main = compileTimelinePatch(patch, env.current());
    expect(main.valid).toBe(true);
    const native = captureProjectDataMember(bundle, patch);

    expect(native.commands.map((command) => command.args)).toEqual([
      { target, key: 'settings', value: {
        volume: 1, theme: 'dark', nested: { keep: true, override: 'old', first: true },
      }, mode: 'replace' },
      { target, key: 'settings', value: {
        volume: 3, theme: 'dark', nested: { keep: true, override: 'old', first: true, late: true },
      }, mode: 'replace' },
      { target, key: 'replacement', value: { fresh: true }, mode: 'replace' },
    ]);
    expect(native.bundle.parent.config.app).toEqual(main.nextData!.config.app);
    expect(Object.keys(native.bundle.parent.config.app![target] as object)).toEqual([
      'settings', 'replacement', 'opaque',
    ]);
  });

  it('births a dictionary through a null extension namespace without losing the command basis', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = { [target]: null };
    const before = copy(bundle);
    const result = captureProjectDataMember(bundle, { version: 1, operations: [write('source', 1)] });

    expect(result.bundle.parent.config.app).toEqual({ [target]: { source: 1 } });
    expect(result.commands[0].expect?.[`parent::config.app[${JSON.stringify(target)}]`]).toEqual({
      state: 'present', value: null,
    });
    expect(bundle).toEqual(before);
  });

  it.each([
    ['unsafe nested object key', write('source', JSON.parse('{"nested":{"__proto__":true}}'))],
    ['non-canonical key', write(' source', 1)],
  ])('refuses %s as a retained draft', async (_label, operation) => {
    const bundle = await authoredBundle();
    const before = copy(bundle);
    expect(() => captureProjectDataMember(bundle, { version: 1, operations: [operation] })).toThrow(ProjectDataMemberRefusal);
    expect(bundle).toEqual(before);
  });

  it('refuses malformed namespaces before materializing the supported member', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = { [target]: ['legacy'] };
    const before = copy(bundle);

    expect(() => captureProjectDataMember(bundle, { version: 1, operations: [write('source', 1)] }))
      .toThrow(ProjectDataMemberRefusal);
    expect(bundle).toEqual(before);
  });

  it('retains original same-leaf guards while allowing a disjoint replay', async () => {
    const bundle = await authoredBundle();
    bundle.parent.config.app = { [target]: { source: 'A', sibling: { opaque: true } } };
    const captured = captureProjectDataMember(bundle, { version: 1, operations: [write('source', 'B')] });

    const stale = copy(bundle);
    (stale.parent.config.app![target] as Record<string, unknown>).source = 'C';
    expect(() => executeProjectDataMember(stale, captured.commands)).toThrow(/submitted expect/);

    const disjoint = copy(bundle);
    (disjoint.parent.config.app![target] as Record<string, unknown>).other = null;
    const replayed = executeProjectDataMember(disjoint, captured.commands);
    expect(replayed.bundle.parent.config.app).toEqual({ [target]: {
      source: 'B', sibling: { opaque: true }, other: null,
    } });
  });

  it('refuses a mixed batch atomically and reports every intention', async () => {
    const bundle = await authoredBundle();
    const before = copy(bundle);
    const patch: TimelinePatch = { version: 1, operations: [
      write('source', 1),
      { op: 'clip.update', target: 'x', payload: { hold: 2 } },
    ] };

    try {
      captureProjectDataMember(bundle, patch);
      throw new Error('expected refusal');
    } catch (error) {
      expect(error).toBeInstanceOf(ProjectDataMemberRefusal);
      expect((error as ProjectDataMemberRefusal).intentions).toEqual([
        expect.objectContaining({ operationIndex: 0, reason: expect.stringContaining('another patch member') }),
        expect.objectContaining({ operationIndex: 1, op: 'clip.update' }),
      ]);
    }
    expect(bundle).toEqual(before);
  });
});
