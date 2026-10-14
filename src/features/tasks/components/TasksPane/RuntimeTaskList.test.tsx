import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { Task as RuntimeTask } from '@/integrations/runtime/generated.ts';
import { projectRuntimeTasksForTaskPane } from './hooks/useRuntimeTasks';
import { RuntimeTaskList } from './RuntimeTaskList';

function task(
  taskId: string,
  family: string,
  capabilityId = family,
): RuntimeTask {
  return {
    task_id: taskId,
    run_id: `run-${taskId}`,
    project_id: 'runtime-project',
    state: 'succeeded',
    version: 2,
    capability_id: capabilityId,
    capability_digest: 'sha256:capability',
    idempotency_key: `admit:${taskId}`,
    created_at: '2026-10-14T00:00:00Z',
    updated_at: '2026-10-14T00:01:00Z',
    runtime_epoch: 4,
    input_object_ids: [`sha256:${taskId}`],
    spec: { spec: { family, params: { prompt: taskId } } },
  };
}

describe('RuntimeTaskList', () => {
  it('provides an explicit history inspection action with the completed row anchor', () => {
    const inspectTask = vi.fn();
    render(
      <RuntimeTaskList
        tasks={[task('completed-task', 'media.clip_extract')]}
        isLoading={false}
        error={null}
        actionError={null}
        onCancelTask={vi.fn()}
        onRetryTask={vi.fn()}
        isTaskActionPending={() => false}
        timelineId={null}
        onExportManagedOutput={vi.fn()}
        isExportTaskPending={() => false}
        onInspectTask={inspectTask}
      />,
    );

    const row = document.querySelector<HTMLElement>('[data-runtime-task-row="true"]')!;
    vi.spyOn(row, 'getBoundingClientRect').mockReturnValue({
      top: 150, right: 680, bottom: 200, left: 500, width: 180, height: 50,
      x: 500, y: 150, toJSON: () => ({}),
    });
    screen.getByRole('button', { name: 'Inspect Clip extraction activity' }).click();
    expect(inspectTask).toHaveBeenCalledWith('completed-task', { top: 150, right: 680 });
  });

  it('renders generation tasks and omits media imports by family or capability', () => {
    const mediaImportFamily = task(
      'import-family-id',
      'runtime.media.import.v1',
      'astrid.media-import-worker',
    );
    const mediaImportCapability = task(
      'import-capability-id',
      'generation.generate_image',
      'runtime.media.import.v1',
    );
    const generationImage = task('image-task-id', 'generation.generate_image');
    const generationVideo = task('video-task-id', 'generation.generate_video');

    render(
      <RuntimeTaskList
        tasks={projectRuntimeTasksForTaskPane([
          mediaImportFamily,
          mediaImportCapability,
          generationImage,
          generationVideo,
        ])}
        isLoading={false}
        error={null}
        actionError={null}
        onCancelTask={vi.fn()}
        onRetryTask={vi.fn()}
        isTaskActionPending={() => false}
        timelineId={null}
        onExportManagedOutput={vi.fn()}
        isExportTaskPending={() => false}
        onInspectTask={vi.fn()}
      />,
    );

    expect(screen.queryByText('runtime.media.import.v1')).not.toBeInTheDocument();
    expect(screen.queryByText('import-family-id')).not.toBeInTheDocument();
    expect(screen.queryByText('import-capability-id')).not.toBeInTheDocument();
    expect(screen.queryByText('sha256:import-family-id')).not.toBeInTheDocument();
    expect(screen.queryByText('sha256:import-capability-id')).not.toBeInTheDocument();
    expect(screen.getAllByText('Image generation')).toHaveLength(1);
    expect(screen.getByText('Video generation')).toBeInTheDocument();
    expect(screen.queryByText('image-task-id')).not.toBeInTheDocument();
    expect(screen.queryByText('video-task-id')).not.toBeInTheDocument();
  });
});
