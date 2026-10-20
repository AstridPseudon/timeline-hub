import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';

import { readBridgeTaskOutputs } from './bridgeTaskOutputs';
import type { Task } from '@/types/tasks';

const listManagedOutputs = vi.hoisted(() => vi.fn());
vi.mock('@/integrations/runtime/client', () => ({
  AstridRuntimeClient: class { listManagedOutputs = listManagedOutputs; },
}));
beforeEach(() => {
  listManagedOutputs.mockReset().mockResolvedValue({ items: [], next_cursor: null });
});

afterEach(() => vi.unstubAllGlobals());

describe('readBridgeTaskOutputs', () => {
  it('projects committed output rows to stable R9 media records', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json({
      task_id: 'task-1',
      run_id: 'run-1',
      project_id: 'demo',
      state: 'succeeded',
      version: 1,
      capability_id: 'render_export',
      capability_digest: `sha256:${'a'.repeat(64)}`,
      schema_version: '1',
      input_object_ids: [],
      spec: {
        input_object_ids: [],
        schema_version: '1',
        capability_digest: `sha256:${'a'.repeat(64)}`,
        spec: { family: 'render_export', params: {}, output_policy: {} },
      },
      idempotency_key: 'task-1',
      created_at: '2026-08-24T00:00:00Z',
      updated_at: '2026-08-24T00:01:00Z',
      attempt_id: null,
      runtime_epoch: 1,
      result: {
        outputs: [{
          name: 'video',
          kind: 'object',
          digest: `sha256:${'a'.repeat(64)}`,
          media_type: 'video/mp4',
          size: 42,
        }],
      },
    })));

    const task = {
      id: 'task-1',
      projectId: 'demo',
      taskType: 'render_export',
      status: 'Complete',
      params: {},
      createdAt: '2026-08-24T00:00:00Z',
    } satisfies Task;

    await expect(readBridgeTaskOutputs(task)).resolves.toEqual([
      expect.objectContaining({
        location: `/api/astrid/v1/objects/${encodeURIComponent(`sha256:${'a'.repeat(64)}`)}`,
        type: 'video',
        params: { media_type: 'video/mp4', size: 42 },
        _variant_is_primary: true,
      }),
    ]);
  });
});

describe('managed-output recovery boundary', () => {
  const task = {
    id: 'task-1', projectId: 'demo', taskType: 'image_generation', status: 'Complete',
    createdAt: '2026-10-20T00:00:00Z',
    params: { outputLocation: 'https://untrusted.example/image.png', source_generation_id: 'not-authority' },
  } satisfies Task;
  const managed = {
    association_id: 'association-1', project_id: 'demo', task_id: 'task-1',
    state: 'available', object_id: `sha256:${'b'.repeat(64)}`,
    media_type: 'image/png', ordinal: 0,
  };

  it('reads all managed-output pages without consulting params or the legacy result', async () => {
    listManagedOutputs
      .mockResolvedValueOnce({ items: [], next_cursor: 'page-2' })
      .mockResolvedValueOnce({ items: [managed], next_cursor: null });
    const fetch = vi.fn();
    vi.stubGlobal('fetch', fetch);
    expect(await readBridgeTaskOutputs(task)).toEqual([expect.objectContaining({
      id: 'association-1', type: 'image', params: {}, _variant_id: managed.object_id,
      location: expect.stringContaining(encodeURIComponent(managed.object_id)),
    })]);
    expect(listManagedOutputs).toHaveBeenNthCalledWith(2, task.id, 'page-2', 50);
    expect(fetch).not.toHaveBeenCalled();
  });

  it.each([
    { ...managed, task_id: 'other-task' },
    { ...managed, project_id: 'other-project' },
    { ...managed, state: 'reclaimed' },
    { ...managed, object_id: 'not-a-managed-object' },
  ])('does not resurrect an unavailable or unrelated managed row: %j', async (output) => {
    listManagedOutputs.mockResolvedValue({ items: [output], next_cursor: null });
    const fetch = vi.fn();
    vi.stubGlobal('fetch', fetch);
    await expect(readBridgeTaskOutputs(task)).resolves.toEqual([]);
    expect(fetch).not.toHaveBeenCalled();
  });

  it('refuses repeated managed-output cursors', async () => {
    listManagedOutputs.mockResolvedValue({ items: [], next_cursor: 'same-page' });
    await expect(readBridgeTaskOutputs(task)).rejects.toThrow('repeated a cursor');
    expect(listManagedOutputs).toHaveBeenCalledTimes(2);
  });

  it('keeps a failed managed-output read visible to the caller', async () => {
    listManagedOutputs.mockRejectedValue(new Error('managed output unavailable'));
    await expect(readBridgeTaskOutputs(task)).rejects.toThrow('managed output unavailable');
  });
});
