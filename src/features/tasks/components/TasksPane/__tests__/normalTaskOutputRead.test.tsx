import { afterEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TooltipProvider } from '@/shared/components/ui/tooltip';
import { bridgeTaskSummaryToTask } from '@/integrations/astrid/bridgeTaskReads';
import { runtimeTaskToSummary } from '@/integrations/astrid/runtimeReadModels';
import { runtimeTaskReadResourceSchema } from '@/integrations/astrid/taskReadSchemas';

vi.mock('@/shared/hooks/tasks/useTaskCancellation', () => ({ useCancelTask: () => ({ mutate: vi.fn() }) }));
vi.mock('@/shared/hooks/tasks/useTaskType', () => ({ useTaskType: () => ({ data: { content_type: 'image' } }) }));
vi.mock('@/features/resources/hooks/useResources', () => ({ usePublicLoras: () => ({ data: [] }) }));
vi.mock('../components/TaskItemPreview', () => ({ TaskItemPreview: () => null }));
vi.mock('../components/TaskItemTooltip', () => ({ TaskItemTooltip: ({ children }: { children: React.ReactNode }) => children }));
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: vi.fn(() => vi.fn()),
    useParams: vi.fn(() => ({})),
    useSearchParams: vi.fn(() => [new URLSearchParams(), vi.fn()]),
    useLocation: vi.fn(() => ({ pathname: '/', search: '', hash: '', state: null })),
  };
});
vi.mock('sonner', () => ({ toast: { error: vi.fn(), success: vi.fn(), loading: vi.fn(), dismiss: vi.fn() } }));
vi.mock('@/shared/contexts/ProjectContext', () => ({
  useProject: vi.fn(() => ({ selectedProjectId: 'project-1' })),
  useProjectSelectionContext: vi.fn(() => ({ selectedProjectId: 'project-1', project: null, setSelectedProjectId: vi.fn() })),
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

afterEach(() => vi.unstubAllGlobals());

describe('normal completed task output read', () => {
  it('loads the managed output through task detail when the list Task has no outputLocation', async () => {
    const outputDigest = `sha256:${'c'.repeat(64)}`;
    const resource = runtimeTaskReadResourceSchema.parse({
      task_id: 'task-normal-output',
      run_id: 'run-normal-output',
      project_id: 'project-1',
      state: 'succeeded',
      version: 1,
      capability_id: 'image_generation',
      capability_digest: `sha256:${'a'.repeat(64)}`,
      schema_version: '1',
      input_object_ids: [],
      idempotency_key: 'task-normal-output',
      created_at: '2026-10-20T00:00:00Z',
      updated_at: '2026-10-20T00:01:00Z',
      attempt_id: null,
      runtime_epoch: 1,
      spec: { spec: { family: 'image_generation', params: {} } },
      result: {
        outputs: [{
          name: 'image',
          kind: 'object',
          digest: outputDigest,
          media_type: 'image/png',
          size: 42,
        }],
      },
    });
    const task = bridgeTaskSummaryToTask(runtimeTaskToSummary(resource, 'project-1'));
    expect(task).not.toHaveProperty('outputLocation');

    const fetchMock = vi.fn(async () => Response.json(resource));
    vi.stubGlobal('fetch', fetchMock);
    const onOpenImageLightbox = vi.fn();

    render(
      <QueryClientProvider client={new QueryClient()}>
        <TooltipProvider>
          <TaskItem task={task} onOpenImageLightbox={onOpenImageLightbox} />
        </TooltipProvider>
      </QueryClientProvider>,
    );

    await waitFor(() => expect(screen.getAllByRole('button')).toHaveLength(2));
    fireEvent.click(screen.getAllByRole('button')[1]!);

    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/v1/tasks/task-normal-output'),
      expect.anything(),
    );
    expect(onOpenImageLightbox).toHaveBeenCalledWith(
      task,
      expect.objectContaining({
        location: expect.stringContaining(encodeURIComponent(outputDigest)),
        _variant_id: outputDigest,
      }),
      outputDigest,
    );
  });
});
