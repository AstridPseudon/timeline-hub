import { describe, expect, it } from 'vitest';
import type { CommitRequest, EditCommand } from './timeline-commit-types.ts';
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

describe('live App EditCommand operation contract', () => {
  it('derives public13 membership from the pinned Runtime bundle and rejects b69 active init', async () => {
    const supported = pinnedRuntimeEditCommandOps();
    expect(supported.has('clip.move')).toBe(true);
    expect(supported.has('timeline.init')).toBe(false);
    expect(() => assertPinnedRuntimeEditCommandOps([initCommand])).toThrow(/timeline\.init/);

    const env = await environment(document(), { validateCommitCommands: assertPinnedRuntimeEditCommandOps });
    const before = structuredClone(env.current().config.clips);
    const request: CommitRequest = {
      api_version: 1,
      project_id: 'project-commit',
      timeline_id: 'timeline-commit',
      base_revision_id: 'r0',
      base_publication_id: 'p0',
      commands: [initCommand],
      source: { via: 'app' },
    };
    await expect(env.provider.commitTimeline(request, 'timeline-init-b69')).rejects.toThrow(/timeline\.init/);
    expect(env.commits()).toHaveLength(1);
    expect(env.current().config.clips).toEqual(before);
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
