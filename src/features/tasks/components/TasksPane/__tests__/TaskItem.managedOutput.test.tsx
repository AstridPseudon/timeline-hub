import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ManagedOutput, Task as RuntimeTask } from '@/integrations/runtime/generated';
import { bridgeTaskSummaryToTask } from '@/integrations/astrid/bridgeTaskReads';
import { runtimeTaskToSummary } from '@/integrations/astrid/runtimeReadModels';
import { runtimeTaskReadResourceSchema } from '@/integrations/astrid/taskReadSchemas';
import { filled } from '@/test/recordedResponses';
import { TaskItem } from '../TaskItem';

const reads = vi.hoisted(() => ({ getTask: vi.fn(), listManagedOutputs: vi.fn(), contentType: 'image' }));
vi.mock('@/integrations/runtime/client', () => ({
  AstridRuntimeClient: class {
    getTask = reads.getTask;
    listManagedOutputs = reads.listManagedOutputs;
  },
}));
vi.mock('@/shared/hooks/tasks/useTaskCancellation', () => ({ useCancelTask: () => ({ mutate: vi.fn() }) }));
vi.mock('@/shared/hooks/tasks/useTaskType', () => ({ useTaskType: () => ({ data: { content_type: reads.contentType } }) }));
vi.mock('@/features/resources/hooks/useResources', () => ({ usePublicLoras: () => ({ data: [] }) }));
vi.mock('../components/TaskItemPreview', () => ({ TaskItemPreview: () => null }));
vi.mock('../components/TaskItemTooltip', () => ({ TaskItemTooltip: ({ children }: { children: React.ReactNode }) => children }));
vi.mock('react-router-dom', () => ({ useNavigate: () => vi.fn() }));
vi.mock('@/shared/contexts/ProjectContext', () => ({
  useProjectSelectionContext: () => ({ selectedProjectId: 'demo', setSelectedProjectId: vi.fn() }),
}));

// Normal Runtime Task + managed-output association. Completion metadata is not
// fabricated: the only result is the ordinary successful worker result.
const task: RuntimeTask = {
  task_id: 'task-1', run_id: 'run-1', project_id: 'demo', state: 'succeeded', version: 1,
  capability_id: 'image_generation', capability_digest: `sha256:${'a'.repeat(64)}`,
  input_object_ids: [], idempotency_key: 'task-1', runtime_epoch: 1,
  created_at: '2026-10-20T00:00:00Z', updated_at: '2026-10-20T00:01:00Z', attempt_id: 'attempt-1',
  spec: { spec: { family: 'image_generation', params: {
    placement_intent: {
      timeline_id: 'timeline-1', anchor_clip_id: 'clip-source-1',
      anchor_generation_id: 'gen-source-1', anchor_variant_id: 'variant-source-1',
      relation: 'after', preferred_track_id: 'V1', fallback_at: 22.25, fallback_track_id: 'V1',
    },
  } } },
  result: { status: 'succeeded' },
};
const output: ManagedOutput = {
  association_id: 'association-1', task_id: task.task_id, run_id: task.run_id,
  project_id: task.project_id, attempt_id: 'attempt-1', output_port: 'image',
  group_key: 'main', variant_key: 'original', selector: { group_key: 'main', variant_key: 'original' },
  object_id: `sha256:${'b'.repeat(64)}`, digest: `sha256:${'b'.repeat(64)}`,
  manifest_ref: null, size: 42, filename: 'output.png', media_type: 'image/png', ordinal: 0,
  role: 'result', producer: {}, provenance: {}, durability: 'durable', state: 'available', version: 1, lifecycle: {},
};

function renderTask(resource = task) {
  // The existing migration projection's schema_version is admission metadata;
  // the actual Runtime read above and managed-output shapes need no new fields.
  const appTask = bridgeTaskSummaryToTask(runtimeTaskToSummary(
    runtimeTaskReadResourceSchema.parse({ ...resource, schema_version: '1' }), 'demo',
  ));
  expect(appTask.outputLocation).toBeUndefined();
  const onOpenImageLightbox = vi.fn();
  const onOpenVideoLightbox = vi.fn();
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const rendered = render(<QueryClientProvider client={client}>
    <TaskItem task={appTask} onOpenImageLightbox={onOpenImageLightbox} onOpenVideoLightbox={onOpenVideoLightbox} />
  </QueryClientProvider>);
  return { ...rendered, appTask, onOpenImageLightbox, onOpenVideoLightbox, client };
}

beforeEach(() => {
  reads.getTask.mockReset().mockResolvedValue(task);
  reads.listManagedOutputs.mockReset().mockResolvedValue({ items: [output], next_cursor: null });
  reads.contentType = 'image';
});

describe('TaskItem managed-output recovery read', () => {
  it('reads the retained image without outputLocation and reopens the existing manual action', async () => {
    const row = renderTask();
    await screen.findByText('Placement unconfirmed: place manually');
    expect(screen.queryByText('Not placed: place manually')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /place .* manually/i }));
    expect(row.onOpenImageLightbox).toHaveBeenCalledWith(row.appTask, expect.objectContaining({
      id: output.association_id, type: 'image',
      location: expect.stringContaining(encodeURIComponent(output.object_id)),
      parent_generation_id: undefined, based_on: null,
    }), output.object_id);
    expect(reads.listManagedOutputs).toHaveBeenCalledWith(task.task_id, undefined, 50);
    row.unmount();
    row.client.clear();
    const reopened = renderTask();
    await screen.findByText('Placement unconfirmed: place manually');
    fireEvent.click(screen.getByRole('button', { name: /place .* manually/i }));
    expect(reopened.onOpenImageLightbox).toHaveBeenCalledTimes(1);
  });

  it('leaves a modern bound task with the same historical params out of recovery', async () => {
    const bound = { ...task, generation_intent: {
      version: 1, modality: 'image', partial_success_policy: 'allow',
      groups: [{ group_key: 'main', selectors: [{ selector: 'image', ordinal: 0, variant_key: 'original' }] }],
    } };
    reads.getTask.mockResolvedValue(bound);
    const row = renderTask(bound);
    await waitFor(() => expect(screen.getByRole('button', { name: '' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: '' }));
    expect(row.onOpenImageLightbox).toHaveBeenCalledTimes(1);
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
    expect(screen.queryByText('Not placed: place manually')).not.toBeInTheDocument();
  });

  it('loads a managed video on hover without outputLocation and retains the video action', async () => {
    reads.contentType = 'video';
    reads.listManagedOutputs.mockResolvedValue({ items: [{ ...output, media_type: 'video/mp4' }], next_cursor: null });
    const row = renderTask();
    fireEvent.mouseEnter(row.container.firstElementChild!);
    await screen.findByText('Placement unconfirmed: place manually');
    fireEvent.click(screen.getByRole('button', { name: /place .* manually/i }));
    expect(row.onOpenVideoLightbox).toHaveBeenCalledWith(row.appTask, [expect.objectContaining({
      id: output.association_id, type: 'video', _variant_id: output.object_id,
    })], 0, output.object_id);
  });

  it('uses the recorded daemon managed-output page unchanged for a completed old-intent task', async () => {
    const recordedTask = filled('task_read_200').body as RuntimeTask;
    const recordedPage = filled('managed_outputs_200').body as { items: ManagedOutput[]; next_cursor: null };
    const completed = {
      ...recordedTask, state: 'succeeded' as const,
      spec: { ...recordedTask.spec, spec: { family: 'video_generation', params: {
        timeline_placement: {
          timeline_id: 'timeline-1', source_clip_id: 'clip-source-1', target_track: 'V1',
          insertion_time: 12.5, intent: 'after_source',
        },
        parent_generation_id: 'untrusted-request-parent',
      } } },
    };
    reads.contentType = 'video';
    reads.getTask.mockResolvedValue(completed);
    reads.listManagedOutputs.mockResolvedValue(recordedPage);
    const row = renderTask(completed);
    fireEvent.mouseEnter(row.container.firstElementChild!);
    await screen.findByText('Placement unconfirmed: place manually');
    fireEvent.click(screen.getByRole('button', { name: /place .* manually/i }));
    expect(row.onOpenVideoLightbox).toHaveBeenCalledWith(row.appTask, [expect.objectContaining({
      id: recordedPage.items[0].association_id,
      _variant_id: recordedPage.items[0].object_id,
      parent_generation_id: undefined,
    })], 0, recordedPage.items[0].object_id);
  });
});
