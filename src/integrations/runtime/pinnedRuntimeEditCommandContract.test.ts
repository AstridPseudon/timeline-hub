import { describe, expect, it } from 'vitest';
import type { EditCommand } from './timeline-commit-types.ts';
import {
  assertPinnedRuntimeEditCommandOps,
  pinnedRuntimeEditCommandOps,
  pinnedRuntimeEditCommandOpsFromBundle,
} from './__tests__/pinnedRuntimeEditCommandContract.ts';
import { document, environment } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';

const initCommand: EditCommand = {
  schema_version: 1,
  op: 'timeline.init',
  version: '1',
  select: 'parent',
  args: { name: 'Main', slug: 'main', output: {} },
};

const nativeMove = (on: number): EditCommand => ({
  schema_version: 1,
  op: 'clip.move',
  version: '1',
  select: 'parent/clip:x',
  args: { on },
});

const projectDataWrite: EditCommand = {
  schema_version: 1,
  op: 'project-data.write',
  version: '1',
  select: 'parent',
  args: {
    target: 'com.example.compiler-canary',
    key: '__dsl__:dsl://com.example.compiler-canary/main.json',
    value: { version: 1 },
    mode: 'replace',
  },
};

const unknownCommand = (): EditCommand => ({
  ...initCommand,
  op: 'timeline.unknown' as EditCommand['op'],
});

describe('live App EditCommand operation contract', () => {
  it.each([
    ['not an object', null],
    ['missing resources', {}],
    ['unknown schema resource', { resources: { unknown: { $id: 'https://astrid.local/schemas/other.json' } } }],
    ['missing EditCommand definition', { resources: { edit: { $id: 'https://astrid.local/schemas/timeline/edit-command.schema.json', $defs: {} } } }],
  ])('refuses a pinned bundle with %s', (_description, bundle) => {
    expect(() => pinnedRuntimeEditCommandOpsFromBundle(bundle)).toThrow(/Pinned Runtime/);
  });

  it('derives operation membership from the pinned Runtime bundle', () => {
    const supported = pinnedRuntimeEditCommandOps();
    expect(supported.has('clip.move')).toBe(true);
    expect(supported.has('timeline.init')).toBe(true);
    const assertInit = () => assertPinnedRuntimeEditCommandOps([initCommand]);
    expect(assertInit).not.toThrow();
    expect(() => assertPinnedRuntimeEditCommandOps([unknownCommand()])).toThrow(/timeline\.unknown/);
  });

  it('gates project-data.write on the pinned schema operation capability', () => {
    const supported = pinnedRuntimeEditCommandOps();
    const assertProjectDataWrite = () => assertPinnedRuntimeEditCommandOps([projectDataWrite]);

    if (supported.has(projectDataWrite.op)) {
      expect(assertProjectDataWrite).not.toThrow();
    } else {
      expect(assertProjectDataWrite).toThrow(/project-data\.write/);
    }
  });

  it('accepts a known native command through the existing session and fake ACK seam', async () => {
    const env = await environment(document(), { validateCommitCommands: assertPinnedRuntimeEditCommandOps });
    const session = await env.mount();
    env.move(session, 5);
    await session.flush();

    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body?.commands).toEqual([expect.objectContaining({ op: nativeMove(5).op })]);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });
});
