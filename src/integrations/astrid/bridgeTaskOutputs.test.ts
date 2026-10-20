import { afterEach, describe, expect, it, vi } from 'vitest';

import { readBridgeTaskOutputs } from './bridgeTaskOutputs';
import type { Task } from '@/types/tasks';

afterEach(() => vi.unstubAllGlobals());

describe('readBridgeTaskOutputs', () => {
  const outputDigest = `sha256:${'a'.repeat(64)}`;

  function taskResource(overrides: Record<string, unknown> = {}) {
    return {
      task_id: 'task-1',
      run_id: 'run-1',
      project_id: 'demo',
      state: 'succeeded',
      version: 1,
      capability_id: 'render_export',
      capability_digest: `sha256:${'b'.repeat(64)}`,
      schema_version: '1',
      input_object_ids: [],
      spec: {},
      idempotency_key: 'task-1',
      created_at: '2026-08-24T00:00:00Z',
      updated_at: '2026-08-24T00:01:00Z',
      attempt_id: null,
      runtime_epoch: 1,
      ...overrides,
    };
  }

  const task = {
    id: 'task-1',
    projectId: 'demo',
    taskType: 'render_export',
    status: 'Complete' as const,
    params: {},
    createdAt: '2026-08-24T00:00:00Z',
  } satisfies Task;

  it('projects committed output rows to stable R9 media records', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json({
      ...taskResource({
        spec: {
          input_object_ids: [],
          schema_version: '1',
          capability_digest: `sha256:${'b'.repeat(64)}`,
          spec: { family: 'render_export', params: {}, output_policy: {} },
        },
      }),
      result: {
        outputs: [{
          name: 'video',
          kind: 'object',
          digest: outputDigest,
          media_type: 'video/mp4',
          size: 42,
        }],
      },
    })));

    await expect(readBridgeTaskOutputs(task)).resolves.toEqual([
      expect.objectContaining({
        location: `/api/astrid/v1/objects/${encodeURIComponent(outputDigest)}`,
        type: 'video',
        params: { media_type: 'video/mp4', size: 42 },
        _variant_is_primary: true,
      }),
    ]);
  });

  it('returns no media for a terminal read with no recorded outputs', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json(taskResource())));

    await expect(readBridgeTaskOutputs(task)).resolves.toEqual([]);
  });

  it('does not expose outputs from a task that is not succeeded', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json(taskResource({
      state: 'running',
      result: { outputs: [{ name: 'video', digest: outputDigest, media_type: 'video/mp4', size: 42 }] },
    }))));

    await expect(readBridgeTaskOutputs(task)).resolves.toEqual([]);
  });

  it.each([
    ['task', { task_id: 'other-task' }],
    ['project', { project_id: 'other-project' }],
  ])('rejects a mismatched %s detail before mapping its media', async (_scope, overrides) => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json(taskResource({
      ...overrides,
      result: { outputs: [{ name: 'video', digest: outputDigest, media_type: 'video/mp4', size: 42 }] },
    }))));

    await expect(readBridgeTaskOutputs(task)).rejects.toThrow(/mismatch/);
  });
});
