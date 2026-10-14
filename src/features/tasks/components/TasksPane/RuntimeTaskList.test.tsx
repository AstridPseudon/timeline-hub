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
      />,
    );

    expect(screen.queryByText('runtime.media.import.v1')).not.toBeInTheDocument();
    expect(screen.queryByText('Task import-family-id')).not.toBeInTheDocument();
    expect(screen.queryByText('Task import-capability-id')).not.toBeInTheDocument();
    expect(screen.queryByText('input sha256:import-family-id')).not.toBeInTheDocument();
    expect(screen.queryByText('input sha256:import-capability-id')).not.toBeInTheDocument();
    expect(screen.getByText('generation.generate_image')).toBeInTheDocument();
    expect(screen.getByText('generation.generate_video')).toBeInTheDocument();
    expect(screen.getByText('Task image-task-id')).toBeInTheDocument();
    expect(screen.getByText('Task video-task-id')).toBeInTheDocument();
  });
});
