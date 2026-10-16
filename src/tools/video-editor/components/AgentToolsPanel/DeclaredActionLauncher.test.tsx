// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  catalogGet: vi.fn(),
  createTask: vi.fn(),
}));

vi.mock('@/integrations/astrid/bridgeTaskReads.ts', () => ({
  getBridgeTaskClient: () => ({ catalog: { get: mocks.catalogGet } }),
}));
vi.mock('@/shared/lib/taskCreation/createTask.ts', () => ({
  createTask: mocks.createTask,
}));

import { DeclaredActionLauncher } from '@/tools/video-editor/components/AgentToolsPanel/DeclaredActionLauncher.tsx';

function readyChiptuneCapability() {
  return {
    capability_id: 'chiptune.compose',
    definition_digest: `sha256:${'a'.repeat(64)}`,
    status: 'ready' as const,
    required_resource_keys: ['cpu'],
    estimated_scratch_bytes: 1024,
    estimated_output_bytes: 4096,
    action_declaration: {
      kind: 'generator' as const,
      name: 'Chiptune Compose',
      short_description: 'Compose a tempo-locked NES-style cue.',
      inputs: [
        { name: 'duration_s', type: 'number', required: true },
        { name: 'bpm', type: 'integer', required: false, default: 132 },
        { name: 'key', type: 'string', required: false, default: 'A minor' },
        { name: 'seed', type: 'integer', required: false, default: 1 },
        { name: 'sections', type: 'json', required: true },
        { name: 'hits', type: 'json', required: false },
        { name: 'duck', type: 'json', required: false },
        { name: 'vo_mask', type: 'json', required: false },
        { name: 'mutes', type: 'json', required: false },
        { name: 'duck_db', type: 'number', required: false, default: -10 },
        { name: 'master_db', type: 'number', required: false, default: -16 },
        { name: 'style', type: 'string', required: false, default: 'nes' },
      ],
      outputs: [
        { name: 'music', type: 'file', artifact_type: 'audio' },
        { name: 'beats', type: 'file', artifact_type: 'application/json' },
      ],
    },
  };
}

function renderLauncher() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <DeclaredActionLauncher projectSlug="j014-test-project" />
    </QueryClientProvider>,
  );
}

describe('DeclaredActionLauncher', () => {
  beforeEach(() => vi.clearAllMocks());

  it('loads the ready Runtime row and admits its selected identity and validated inputs through the host', async () => {
    const capability = readyChiptuneCapability();
    mocks.catalogGet.mockResolvedValue(capability);
    mocks.createTask.mockResolvedValue({ task_id: 'host-task-014', status: 'queued' });

    renderLauncher();
    fireEvent.click(screen.getByRole('button', { name: 'Runtime Generator action' }));
    await screen.findByLabelText('Declared action chiptune.compose');

    const sections = [{ start_s: 0, end_s: 2, energy: 0.4, mood: 'bright' }];
    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '2' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: JSON.stringify(sections) } });
    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));

    await screen.findByText('Task host-task-014 submitted (queued).');
    expect(mocks.catalogGet).toHaveBeenCalledTimes(1);
    expect(mocks.catalogGet).toHaveBeenCalledWith('chiptune.compose');
    expect(mocks.createTask).toHaveBeenCalledTimes(1);
    expect(mocks.createTask).toHaveBeenCalledWith({
      project: 'j014-test-project',
      capability_id: 'chiptune.compose',
      capability_digest: `sha256:${'a'.repeat(64)}`,
      schema_version: '1',
      input_object_ids: [],
      spec: {
        family: 'chiptune.compose',
        params: {
          duration_s: 2,
          bpm: 132,
          key: 'A minor',
          seed: 1,
          sections,
          duck_db: -10,
          master_db: -16,
          style: 'nes',
        },
        output_policy: {},
      },
      storage_estimate: { scratch_bytes: 1024, output_bytes: 4096 },
      settlement_effect: {},
    });
  });

  it('does not load or submit a row when there is no selected project', async () => {
    const queryClient = new QueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <DeclaredActionLauncher projectSlug={null} />
      </QueryClientProvider>,
    );

    await waitFor(() => expect(screen.queryByRole('button', { name: 'Runtime Generator action' })).toBeNull());
    expect(mocks.catalogGet).not.toHaveBeenCalled();
    expect(mocks.createTask).not.toHaveBeenCalled();
  });
});
