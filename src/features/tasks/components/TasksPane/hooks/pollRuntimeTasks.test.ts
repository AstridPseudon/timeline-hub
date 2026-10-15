import { QueryClient } from '@tanstack/react-query';
import { describe, expect, it, vi } from 'vitest';
import type { Task as RuntimeTask } from '@/integrations/runtime/generated.ts';
import { pollRuntimeTasks, runtimeTaskQueryKey } from './useRuntimeTasks';

const t = (id: string, state: RuntimeTask['state']) => ({
  task_id: id, state, version: 1, capability_id: 'c', updated_at: 'u', spec: {},
}) as unknown as RuntimeTask;

describe('pollRuntimeTasks', () => {
  it('after the first full listing, ticks only re-read active tasks', async () => {
    vi.useFakeTimers();
    const done = Array.from({ length: 721 }, (_, i) => t(`done-${i}`, 'succeeded'));
    const running = t('run-1', 'running');
    const client = {
      listProjectTasks: vi.fn(async () => ({ items: [...done, running], next_cursor: null })),
      getTask: vi.fn(async () => t('run-1', 'running')),
    };
    const qc = new QueryClient();
    const key = runtimeTaskQueryKey('p');
    qc.setQueryData(key, await pollRuntimeTasks(client, qc, 'p'));
    expect(client.listProjectTasks).toHaveBeenCalledTimes(1);

    // 3 ticks at 2 s: previously 3 more full listings (721 tasks, 4 pages each).
    for (let i = 0; i < 3; i++) {
      vi.advanceTimersByTime(2_000);
      qc.setQueryData(key, await pollRuntimeTasks(client, qc, 'p'));
    }
    expect(client.listProjectTasks).toHaveBeenCalledTimes(1);
    expect(client.getTask).toHaveBeenCalledTimes(3);

    client.getTask.mockResolvedValue(t('run-1', 'succeeded'));
    vi.advanceTimersByTime(2_000);
    const merged = await pollRuntimeTasks(client, qc, 'p');
    expect(merged.find((x) => x.task_id === 'run-1')?.state).toBe('succeeded');
    expect(merged).toHaveLength(722);

    vi.advanceTimersByTime(10_000); // full listing discovers new tasks
    await pollRuntimeTasks(client, qc, 'p');
    expect(client.listProjectTasks).toHaveBeenCalledTimes(2);
    vi.useRealTimers();
  });
});
