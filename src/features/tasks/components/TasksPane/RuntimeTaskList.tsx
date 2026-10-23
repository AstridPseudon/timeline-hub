import React from 'react';
import { Button } from '@/shared/components/ui/button';
import type { Task as RuntimeTask } from '@/integrations/runtime/generated.ts';
import {
  runtimeTaskIsCancellable,
  runtimeTaskIsSelectedTimelineRender,
  runtimeTaskIsRetryable,
  type RuntimeTaskAction,
} from './hooks/useRuntimeTasks';
import { runtimeTaskLabel, runtimeTaskStateLabel } from './activityPresentation';

interface RuntimeTaskListProps {
  tasks: RuntimeTask[];
  isLoading: boolean;
  error: Error | null;
  actionError: Error | null;
  onCancelTask: (taskId: string) => void;
  onRetryTask: (taskId: string) => void;
  isTaskActionPending: (taskId: string, action: RuntimeTaskAction) => boolean;
  timelineId: string | null;
  onExportManagedOutput: (taskId: string, timelineId: string) => void;
  isExportTaskPending: (taskId: string) => boolean;
  onInspectTask: (taskId: string, anchor: { top: number; right: number }) => void;
}

function RuntimeTaskItem({
  task,
  onCancelTask,
  onRetryTask,
  isTaskActionPending,
  timelineId,
  onExportManagedOutput,
  isExportTaskPending,
  onInspectTask,
}: Omit<RuntimeTaskListProps, 'tasks' | 'isLoading' | 'error' | 'actionError'> & { task: RuntimeTask }) {
  const cancelPending = isTaskActionPending(task.task_id, 'cancel');
  const retryPending = isTaskActionPending(task.task_id, 'retry');
  const exportPending = isExportTaskPending(task.task_id);
  const canExport = runtimeTaskIsSelectedTimelineRender(task, timelineId);

  return (
    <article
      className="rounded-md border border-border bg-card/60 p-3 text-xs text-card-foreground"
      data-runtime-task-row="true"
      data-runtime-task-id={task.task_id}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 space-y-1">
          <div className="font-medium text-card-foreground">{runtimeTaskLabel(task)}</div>
          <div className="text-muted-foreground/80">{runtimeTaskStateLabel(task.state)}</div>
        </div>
        <div className="flex shrink-0 items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={(event) => {
              const row = event.currentTarget.closest<HTMLElement>('[data-runtime-task-row]');
              const rect = row?.getBoundingClientRect() ?? event.currentTarget.getBoundingClientRect();
              onInspectTask(task.task_id, { top: rect.top, right: rect.right });
            }}
            aria-label={`Inspect ${runtimeTaskLabel(task)} activity`}
            className="px-2 py-0.5"
          >
            Inspect
          </Button>
          {canExport && timelineId && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onExportManagedOutput(task.task_id, timelineId)}
              disabled={cancelPending || retryPending || exportPending}
              aria-label={`Export ${runtimeTaskLabel(task)} result`}
              className="px-2 py-0.5 text-emerald-400 hover:bg-emerald-900/20 hover:text-emerald-300"
            >
              {exportPending ? 'Exporting…' : 'Export managed output'}
            </Button>
          )}
          {runtimeTaskIsCancellable(task) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onCancelTask(task.task_id)}
              disabled={cancelPending || retryPending}
              aria-label={`Cancel ${runtimeTaskLabel(task)}`}
              className="px-2 py-0.5 text-red-400 hover:bg-red-900/20 hover:text-red-300"
            >
              {cancelPending ? 'Cancelling…' : 'Cancel'}
            </Button>
          )}
          {runtimeTaskIsRetryable(task) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onRetryTask(task.task_id)}
              disabled={cancelPending || retryPending}
              aria-label={`Retry ${runtimeTaskLabel(task)}`}
              className="px-2 py-0.5 text-blue-400 hover:bg-blue-900/20 hover:text-blue-300"
            >
              {retryPending ? 'Retrying…' : 'Retry'}
            </Button>
          )}
        </div>
      </div>
    </article>
  );
}

export function RuntimeTaskList({
  tasks,
  isLoading,
  error,
  actionError,
  onCancelTask,
  onRetryTask,
  isTaskActionPending,
  timelineId,
  onExportManagedOutput,
  isExportTaskPending,
  onInspectTask,
}: RuntimeTaskListProps) {
  if (error) {
    return (
      <div className="p-4 text-sm text-red-300" role="alert" data-runtime-task-error="true">
        Runtime task reads failed: {error.message}
      </div>
    );
  }

  if (isLoading && tasks.length === 0) {
    return <div className="p-4 text-sm text-muted-foreground">Loading Runtime tasks…</div>;
  }

  return (
    <div className="space-y-2 p-4 text-sidebar-foreground" data-runtime-task-list="true">
      {actionError && (
        <div className="rounded-md border border-red-800/80 bg-red-950/30 p-3 text-sm text-red-300" role="alert">
          Runtime task action failed: {actionError.message}
        </div>
      )}
      {tasks.length === 0 ? (
        <p className="text-center text-sm text-muted-foreground">No tasks yet</p>
      ) : (
        tasks.map((task) => (
          <RuntimeTaskItem
            key={task.task_id}
            task={task}
            onCancelTask={onCancelTask}
            onRetryTask={onRetryTask}
            isTaskActionPending={isTaskActionPending}
            timelineId={timelineId}
            onExportManagedOutput={onExportManagedOutput}
            isExportTaskPending={isExportTaskPending}
            onInspectTask={onInspectTask}
          />
        ))
      )}
    </div>
  );
}
