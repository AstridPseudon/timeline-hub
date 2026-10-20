import { beforeEach, describe, it, expect, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TooltipProvider } from '@/shared/components/ui/tooltip';
import { bridgeTaskSummaryToTask } from '@/integrations/astrid/bridgeTaskReads';
import { runtimeTaskToDetail, runtimeTaskToSummary } from '@/integrations/astrid/runtimeReadModels';
import { runtimeTaskReadResourceSchema } from '@/integrations/astrid/taskReadSchemas';

const getTask = vi.hoisted(() => vi.fn());
vi.mock('@/integrations/runtime/client', () => ({
  AstridRuntimeClient: class { getTask = getTask; },
}));
beforeEach(() => {
  getTask.mockReset().mockResolvedValue({
    task_id: 'task-1', project_id: 'project-1', state: 'succeeded',
  });
});

const output = vi.hoisted(() => ({
  id: 'gen-1', location: 'https://cdn.example.com/tasks/task-1/out.png',
  type: 'image', _variant_id: 'variant-1',
}));
vi.mock('@/shared/hooks/tasks/useTaskCancellation', () => ({ useCancelTask: () => ({ mutate: vi.fn() }) }));
vi.mock('@/shared/hooks/tasks/useTaskType', () => ({ useTaskType: () => ({ data: { content_type: 'image' } }) }));
vi.mock('@/features/resources/hooks/useResources', () => ({ usePublicLoras: () => ({ data: [] }) }));
vi.mock('../hooks/useImageGeneration', () => ({ useImageGeneration: () => ({ generationData: output, variantId: 'variant-1' }) }));
vi.mock('../hooks/useVideoGenerations', () => ({ useVideoGenerations: () => ({ videoOutputs: null }) }));
vi.mock('../components/TaskItemPreview', () => ({ TaskItemPreview: () => null }));
vi.mock('../components/TaskItemTooltip', () => ({ TaskItemTooltip: ({ children }: { children: React.ReactNode }) => children }));
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: vi.fn(() => vi.fn()), useParams: vi.fn(() => ({})), useSearchParams: vi.fn(() => [new URLSearchParams(), vi.fn()]), useLocation: vi.fn(() => ({ pathname: '/', search: '', hash: '', state: null })) };
});
vi.mock('sonner', () => ({ toast: { error: vi.fn(), success: vi.fn(), loading: vi.fn(), dismiss: vi.fn() } }));
vi.mock('@/shared/contexts/ProjectContext', () => ({
  useProject: vi.fn(() => ({ selectedProjectId: 'test' })),
  useProjectSelectionContext: vi.fn(() => ({ selectedProjectId: 'test', project: null, setSelectedProjectId: vi.fn() })),
  useProjectCrudContext: vi.fn(() => ({
    projects: [],
    isLoadingProjects: false,
    fetchProjects: vi.fn(),
    addNewProject: vi.fn(),
    isCreatingProject: false,
    updateProject: vi.fn(),
    isUpdatingProject: false,
    deleteProject: vi.fn(),
    isDeletingProject: false,
  })),
  useProjectIdentityContext: vi.fn(() => ({ userId: null })),
}));
import { TaskItem } from '../TaskItem';

describe('TaskItem', () => {
  it('exports a component', () => {
    expect(TaskItem).toBeDefined();
    expect(typeof TaskItem === 'function' || typeof TaskItem === 'object').toBe(true);
    expect(TaskItem).not.toBeNull();
    expect(String(TaskItem)).toBeDefined();
  });

  // Keep the exact request params from origin/main's successful completion
  // fixtures. Those handlers saved clips without removing the old intent.
  it.each([
    { timeline_placement: {
      timeline_id: 'timeline-1', source_clip_id: 'clip-source-1', target_track: 'V1',
      insertion_time: 12.5, intent: 'after_source',
    } },
    { placement_intent: {
      timeline_id: 'timeline-1', anchor_clip_id: 'clip-source-1',
      anchor_generation_id: 'gen-source-1', anchor_variant_id: 'variant-source-1',
      relation: 'after', preferred_track_id: 'V1', fallback_at: 22.25, fallback_track_id: 'V1',
    } },
  ])('keeps the lightbox available without calling placed history unplaced: %j', async (params) => {
    const task = {
      id: 'task-1', taskType: 'image_generation', projectId: 'project-1',
      status: 'Complete' as const, params, outputLocation: output.location,
      createdAt: '2026-10-20T00:00:00Z',
    };
    const onOpenImageLightbox = vi.fn();
    render(
      <QueryClientProvider client={new QueryClient()}>
        <TooltipProvider>
          <TaskItem task={task} onOpenImageLightbox={onOpenImageLightbox} />
        </TooltipProvider>
      </QueryClientProvider>,
    );
    expect(screen.queryByText('Not placed: place manually')).not.toBeInTheDocument();
    expect(await screen.findByText('Placement unconfirmed: place manually')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '' }));
    expect(onOpenImageLightbox).toHaveBeenCalledWith(task, output, 'variant-1');
    fireEvent.click(screen.getByRole('button', { name: /place .* manually/i }));
    expect(onOpenImageLightbox).toHaveBeenCalledTimes(2);
  });

  it('does not infer old placement from a modern task after the actual read projections', () => {
    // Runtime detail shape follows bridgeTaskOutputs.test.ts's committed-output
    // fixture; no Supabase completion_follow_up field is added to this read.
    const resource = runtimeTaskReadResourceSchema.parse({
      task_id: 'task-1', run_id: 'run-1', project_id: 'test', state: 'succeeded', version: 1,
      capability_id: 'image_generation', capability_digest: `sha256:${'a'.repeat(64)}`,
      schema_version: '1', input_object_ids: [], idempotency_key: 'task-1',
      created_at: '2026-10-20T00:00:00Z', updated_at: '2026-10-20T00:01:00Z',
      attempt_id: null, runtime_epoch: 1,
      spec: { spec: { family: 'image_generation', params: {
        placement_intent: { timeline_id: 'timeline-1', anchor_clip_id: 'clip-1' },
      } } },
      generation_intent: {
        version: 1, modality: 'image', partial_success_policy: 'allow',
        groups: [{ group_key: 'main', selectors: [{ selector: 'image', ordinal: 0, variant_key: 'original' }] }],
      },
      result: { outputs: [{
        name: 'image', kind: 'object', digest: `sha256:${'b'.repeat(64)}`,
        media_type: 'image/png', size: 42,
      }] },
    });
    getTask.mockResolvedValue(resource);
    const summary = runtimeTaskToSummary(resource, 'test');
    const task = bridgeTaskSummaryToTask(summary);
    expect(runtimeTaskToDetail(resource, 'test').result).toEqual(resource.result);
    expect(summary).not.toHaveProperty('result');
    expect(task.params).toEqual({
      placement_intent: { timeline_id: 'timeline-1', anchor_clip_id: 'clip-1' },
    });
    expect(task).not.toHaveProperty('generation_intent');
    expect(task).not.toHaveProperty('resultData');
    render(
      <QueryClientProvider client={new QueryClient()}>
        <TooltipProvider><TaskItem task={task} /></TooltipProvider>
      </QueryClientProvider>,
    );
    expect(screen.getByText('Complete')).toBeInTheDocument();
    expect(screen.queryByText('Not placed: place manually')).not.toBeInTheDocument();
  });
});
