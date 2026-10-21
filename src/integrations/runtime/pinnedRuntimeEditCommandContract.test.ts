import { describe, expect, it } from 'vitest';
import type { EditCommand } from './timeline-commit-types.ts';
import { assertPinnedRuntimeEditCommandOps, pinnedRuntimeEditCommandOps } from './__tests__/pinnedRuntimeEditCommandContract.ts';
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

const unknownCommand = (): EditCommand => ({
  ...initCommand,
  op: 'timeline.unknown' as EditCommand['op'],
});

describe('live App EditCommand operation contract', () => {
  it('derives operation membership from the pinned Runtime bundle', () => {
    const supported = pinnedRuntimeEditCommandOps();
    expect(supported.has('clip.move')).toBe(true);
    const assertInit = () => assertPinnedRuntimeEditCommandOps([initCommand]);
    if (supported.has('timeline.init')) expect(assertInit).not.toThrow();
    else expect(assertInit).toThrow(/timeline\.init/);
    expect(() => assertPinnedRuntimeEditCommandOps([unknownCommand()])).toThrow(/timeline\.unknown/);
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
