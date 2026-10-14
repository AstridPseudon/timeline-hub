// @vitest-environment jsdom
import React from 'react';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { Event, ManagedOutput, Task as RuntimeTask } from '@/integrations/runtime/generated.ts';
import type { AgentTaskLink } from '@/tools/video-editor/runtime/agentTaskLinks';
import { RuntimeActivityDock } from './RuntimeActivityDock';

const runtimeClientMock = vi.hoisted(() => ({ listTaskEvents: vi.fn(), listManagedOutputs: vi.fn() }));
vi.mock('@/integrations/runtime/client.ts', () => ({
  ReighRuntimeClient: class {
    listTaskEvents = runtimeClientMock.listTaskEvents;
    listManagedOutputs = runtimeClientMock.listManagedOutputs;
  },
}));

function task(taskId: string, family = 'generation.generate_image', overrides: Partial<RuntimeTask> & { progress?: unknown } = {}): RuntimeTask {
  return {
    task_id: taskId,
    run_id: `run-${taskId}`,
    project_id: 'project-1',
    state: 'running',
    version: 1,
    capability_id: family,
    capability_digest: 'sha256:capability',
    idempotency_key: `admit:${taskId}`,
    created_at: '2026-10-14T00:00:00Z',
    updated_at: '2026-10-14T00:01:00Z',
    runtime_epoch: 1,
    input_object_ids: [],
    spec: { spec: { family } },
    ...overrides,
  };
}

function event(overrides: Partial<Event> = {}): Event {
  return {
    event_id: 'event-1', sequence: 1, cursor: 'cursor-1', event_type: 'runtime.task.started',
    aggregate_type: 'task', aggregate_id: 'task-1', payload: {}, occurred_at: '2026-10-14T00:01:00Z',
    ...overrides,
  };
}

function output(overrides: Partial<ManagedOutput> = {}): ManagedOutput {
  return {
    association_id: 'association-1', project_id: 'project-1', run_id: 'run-task-1', task_id: 'task-1',
    attempt_id: 'attempt-1', output_port: 'video', group_key: 'group', variant_key: 'variant',
    selector: { group_key: 'group', variant_key: 'variant' }, object_id: 'sha256:secret-digest',
    digest: 'sha256:secret-digest', manifest_ref: null, size: 10, filename: '/private/user/output.mp4',
    media_type: 'video/mp4', ordinal: 0, role: 'render', producer: {}, provenance: {}, durability: 'durable',
    state: 'available', version: 1, lifecycle: {}, ...overrides,
  };
}

function renderDock(tasks: RuntimeTask[], links: AgentTaskLink[] = []) {
  return render(<RuntimeActivityDock
    projectId="project-1" timelineId={null} tasks={tasks} links={links} isLoading={false} error={null} actionError={null}
    isPinned={false} onTogglePinned={vi.fn()} onOpenHistory={vi.fn()} onCancelTask={cancelTask} onRetryTask={vi.fn()}
    isTaskActionPending={() => false} onExportManagedOutput={vi.fn()} isExportTaskPending={() => false}
  />);
}

const cancelTask = vi.fn();

describe('RuntimeActivityDock', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    runtimeClientMock.listTaskEvents.mockResolvedValue({ items: [event()], next_cursor: null });
    runtimeClientMock.listManagedOutputs.mockResolvedValue({ items: [output()], next_cursor: null });
  });

  it('keeps the idle dock compact without permanent status tabs', () => {
    renderDock([]);
    const dock = document.querySelector<HTMLElement>('[data-runtime-activity-dock="true"]')!;
    expect(screen.getByText('No active tasks')).toBeInTheDocument();
    expect(dock.querySelector('header')?.className).toContain('h-[38px]');
    expect(screen.queryByRole('button', { name: /show (processing|succeeded|failed) tasks/i })).not.toBeInTheDocument();
  });

  it('shows at most three horizontal active rows and a history affordance for the rest', () => {
    renderDock(Array.from({ length: 5 }, (_, index) => task(`task-${index + 1}`, index % 2 ? 'generation.generate_video' : 'generation.generate_image')));
    expect(screen.getAllByTestId('activity-task-row')).toHaveLength(3);
    expect(screen.getByText('+2 more active tasks · open history')).toBeInTheDocument();
    expect(screen.getAllByText('Image generation')).toHaveLength(2);
    expect(screen.queryByText('task-1')).not.toBeInTheDocument();
  });

  it('opens a floating inspector with safe events, delegated children, results, and controls', async () => {
    const parent = task('task-1', 'media.clip_extract', { attempt_id: 'attempt-parent' });
    const child = task('child-1', 'media.clip_extract', {
      run_id: 'different-run',
      spec: { spec: { family: 'media.clip_extract', delegated_parent: { parent_task_id: 'task-1', parent_attempt_id: 'attempt-parent' } } },
    });
    const unrelated = task('unrelated-child', 'media.clip_extract', {
      project_id: 'other-project',
      spec: { spec: { family: 'media.clip_extract', delegated_parent: { parent_task_id: 'task-1' } } },
    });
    runtimeClientMock.listTaskEvents.mockResolvedValue({
      items: [
        event({ sequence: 2, event_id: 'private', payload: { message: '/private/user/secret.log sha256:private' } }),
        event({ sequence: 1, aggregate_id: 'other-task', event_id: 'wrong-aggregate', event_type: 'ignored.event' }),
      ], next_cursor: null,
    });
    const view = renderDock([parent, child, unrelated]);
    const row = document.querySelector<HTMLButtonElement>('[data-activity-task-id="task-1"]')!;
    fireEvent.mouseEnter(row);
    const inspector = await screen.findByLabelText('Clip extraction activity details');
    expect(inspector).toHaveClass('fixed');
    expect(inspector.closest('[data-runtime-activity-dock="true"]')).toBeNull();
    expect(within(inspector).getByText('Subtasks (1)')).toBeInTheDocument();
    expect(within(inspector).getAllByText('Clip extraction').length).toBeGreaterThan(0);
    expect(within(inspector).getByText('output.mp4')).toBeInTheDocument();
    expect(within(inspector).queryByText('/private/user/output.mp4')).not.toBeInTheDocument();
    expect(within(inspector).queryByText('sha256:secret-digest')).not.toBeInTheDocument();
    await waitFor(() => expect(within(inspector).queryByText('Ignored Event')).not.toBeInTheDocument());
    expect(within(inspector).queryByText('/private/user/secret.log sha256:private')).not.toBeInTheDocument();
    expect(runtimeClientMock.listTaskEvents).toHaveBeenCalledWith('task-1', undefined, 40);
    fireEvent.click(within(inspector).getByRole('button', { name: 'Cancel Clip extraction' }));
    expect(cancelTask).toHaveBeenCalledWith('task-1');
    expect(view.container.querySelector('[data-runtime-activity-dock="true"]')).toBeTruthy();
  });

  it('pins on row click, keeps the pinned inspector open on pointer exit, and closes on Escape', async () => {
    renderDock([task('task-1')]);
    fireEvent.click(screen.getByRole('button', { name: 'Image generation, Running' }));
    const inspector = await screen.findByLabelText('Image generation activity details');
    expect(inspector).toHaveAttribute('data-pinned', 'true');
    fireEvent.mouseLeave(inspector, { relatedTarget: document.body });
    expect(screen.getByLabelText('Image generation activity details')).toBeInTheDocument();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByLabelText('Image generation activity details')).not.toBeInTheDocument();
  });

  it('animates only a live linked task once and honors rehydrated links without the arrival effect', async () => {
    const current = task('task-1');
    const liveLink: AgentTaskLink = { project_id: 'project-1', run_id: 'run-task-1', task_id: 'task-1', capability_id: 'generation.generate_image', sessionId: 'session-1', toolCallId: 'call-1', liveObserved: true };
    const { unmount } = renderDock([current], [liveLink]);
    await waitFor(() => expect(screen.getByTestId('activity-task-row')).toHaveClass('motion-safe:animate-[pulse_700ms_ease-out_1]'));
    unmount();
    renderDock([current], [{ ...liveLink, liveObserved: false }]);
    expect(screen.getByTestId('activity-task-row')).not.toHaveClass('motion-safe:animate-[pulse_700ms_ease-out_1]');
  });
});
