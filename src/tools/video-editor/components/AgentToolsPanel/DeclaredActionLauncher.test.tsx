// @vitest-environment jsdom
import { createHash } from 'node:crypto';
import { preparedDeclaredActionSchema } from '@/integrations/astrid/declaredActionPreparation';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  catalogGet: vi.fn(),
  createTask: vi.fn(),
  prepare: vi.fn(),
  digest: vi.fn(),
}));

vi.mock('@/integrations/astrid/bridgeTaskReads.ts', () => ({
  getBridgeTaskClient: () => ({ catalog: { getV2: mocks.catalogGet }, declaredActionPreparation: { prepare: mocks.prepare, digest: mocks.digest } }),
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
    storage_estimate: { mode: 'static', scratch_bytes: 1024, output_bytes: 4096 },
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


const digest = async (value: unknown): Promise<string> => {
  const sort = (v: unknown): unknown => Array.isArray(v) ? v.map(sort)
    : v !== null && typeof v === 'object'
      ? Object.fromEntries(Object.entries(v).sort(([a], [b]) => a.localeCompare(b)).map(([k, item]) => [k, sort(item)])) : v;
  return `sha256:${createHash('sha256').update(JSON.stringify(sort(value))).digest('hex')}`;
};
const estimator = { id: 'synthetic.plan', version: 1, implementation_digest: `sha256:${'b'.repeat(64)}` };
async function reply(input: Record<string, unknown>) {
  const binding = {
    request: { ...input, storage_estimate: { scratch_bytes: 37, output_bytes: 103 } },
    estimator, spec_digest: await digest(input.spec), source_digest: `sha256:${'c'.repeat(64)}`,
  };
  return preparedDeclaredActionSchema.parse({ ...binding, preparation_digest: await digest(binding) });
}
async function submitForm() {
  renderLauncher();
  fireEvent.click(screen.getByRole('button', { name: 'Runtime Generator action' }));
  await screen.findByLabelText('Declared action chiptune.compose');
  fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '2' } });
  fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: '[]' } });
  fireEvent.click(screen.getByRole('button', { name: 'Run action' }));
}

describe('DeclaredActionLauncher', () => {
  beforeEach(() => { vi.resetAllMocks(); mocks.digest.mockImplementation(digest); });

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
    }, { capabilityCatalogVersion: 2 });
  });

  it('prepares the actual generic form request and admits the exact canonical request and pair', async () => {
    mocks.catalogGet.mockResolvedValue({ ...readyChiptuneCapability(), storage_estimate: { mode: 'request_estimated', estimator } });
    let prepared: Awaited<ReturnType<typeof reply>>;
    mocks.prepare.mockImplementation(async (input) => { prepared = await reply(input); return prepared; });
    mocks.createTask.mockResolvedValue({ task_id: 'prepared-task', status: 'queued' });
    await submitForm();
    await screen.findByText('Task prepared-task submitted (queued).');
    expect(mocks.prepare).toHaveBeenCalledTimes(1);
    expect(mocks.createTask).toHaveBeenCalledWith(prepared!.request, { capabilityCatalogVersion: 2 });
    expect(mocks.createTask.mock.calls[0][0].storage_estimate).toEqual({ scratch_bytes: 37, output_bytes: 103 });
  });

  it.each(['estimator', 'schema', 'spec-digest', 'pair', 'missing-pair', 'inputs', 'params', 'capability', 'project', 'source', 'missing-estimator', 'missing-schema', 'missing-spec-digest', 'missing-estimator-digest', 'missing-estimator-version', 'missing-estimator-id', 'output-policy', 'overflow', 'unknown-field'])('refuses altered %s before task creation', async (tamper) => {
    mocks.catalogGet.mockResolvedValue({ ...readyChiptuneCapability(), storage_estimate: { mode: 'request_estimated', estimator } });
    mocks.prepare.mockImplementation(async (input) => {
      const prepared = await reply(input);
      if (tamper === 'estimator') prepared.estimator.version++;
      if (tamper === 'schema') Object.assign(prepared.request, { schema_version: 1 });
      if (tamper === 'spec-digest') prepared.spec_digest = `sha256:${'d'.repeat(64)}`;
      if (tamper === 'pair') prepared.request.storage_estimate.output_bytes++;
      if (tamper === 'missing-pair') Reflect.deleteProperty(prepared.request, 'storage_estimate');
      if (tamper === 'inputs') prepared.request.input_object_ids.push(`sha256:${'e'.repeat(64)}`);
      if (tamper === 'params') prepared.request.spec.params.raw_extra = 'changed';
      if (tamper === 'capability') prepared.request.capability_digest = `sha256:${'e'.repeat(64)}`;
      if (tamper === 'project') prepared.request.project = 'foreign';
      if (tamper === 'source') prepared.source_digest = `sha256:${'e'.repeat(64)}`;
      if (tamper === 'missing-estimator') Reflect.deleteProperty(prepared, 'estimator');
      if (tamper === 'missing-schema') Reflect.deleteProperty(prepared.request, 'schema_version');
      if (tamper === 'missing-spec-digest') Reflect.deleteProperty(prepared, 'spec_digest');
      if (tamper === 'missing-estimator-digest') Reflect.deleteProperty(prepared.estimator, 'implementation_digest');
      if (tamper === 'missing-estimator-version') Reflect.deleteProperty(prepared.estimator, 'version');
      if (tamper === 'missing-estimator-id') Reflect.deleteProperty(prepared.estimator, 'id');
      if (tamper === 'output-policy') prepared.request.spec.output_policy.destination = 'caller-path';
      if (tamper === 'overflow') prepared.request.storage_estimate.output_bytes = Number.MAX_SAFE_INTEGER;
      if (tamper === 'unknown-field') Object.assign(prepared, { unknown: true });
      return prepared;
    });
    await submitForm();
    await screen.findByRole('alert');
    expect(mocks.createTask).not.toHaveBeenCalled();
  });

  it.each([undefined, null, false, '0', -1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1])('refuses malformed prepared bytes %s without coercion', async (bytes) => {
    mocks.catalogGet.mockResolvedValue({ ...readyChiptuneCapability(), storage_estimate: { mode: 'request_estimated', estimator } });
    mocks.prepare.mockImplementation(async (input) => {
      const prepared = await reply(input);
      Object.assign(prepared.request.storage_estimate, { scratch_bytes: bytes });
      return prepared;
    });
    await submitForm();
    await screen.findByRole('alert');
    expect(mocks.createTask).not.toHaveBeenCalled();
  });

  it.each([
    { ...readyChiptuneCapability(), storage_estimate: { mode: 'unavailable', reason: 'unknown estimate' } },
    { ...readyChiptuneCapability(), status: 'unsupported', unavailable_reason: 'request_estimated_requires_catalog_v2' },
  ])('refuses unavailable and legacy dynamic modes before preparation/admission', async (row) => {
    mocks.catalogGet.mockResolvedValue(row);
    await submitForm();
    await waitFor(() => expect(document.querySelector('[data-video-editor-declared-action-code="capability-unavailable"]')).not.toBeNull());
    expect(mocks.prepare).not.toHaveBeenCalled();
    expect(mocks.createTask).not.toHaveBeenCalled();
  });

  it('reports a missing host adapter without admission', async () => {
    mocks.catalogGet.mockResolvedValue({ ...readyChiptuneCapability(), storage_estimate: { mode: 'request_estimated', estimator } });
    mocks.prepare.mockRejectedValue(new Error('host preparation unavailable'));
    await submitForm();
    await screen.findByText('host preparation unavailable');
    expect(mocks.createTask).not.toHaveBeenCalled();
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
