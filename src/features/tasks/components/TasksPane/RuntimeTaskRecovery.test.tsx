import React from 'react';
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { ManagedOutput, Task, Transport } from '@/integrations/runtime/generated';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata';
import { RuntimeAuthorityContext } from '@/app/runtime/runtimeAuthority';
import { filled } from '@/test/recordedResponses';
import fixture from './__fixtures__/runtimeRecoveryGeneration.json';
import { RuntimeTaskList } from './RuntimeTaskList';
import { RuntimeActivityDock } from './RuntimeActivityDock';
import { useTasksLightbox } from './hooks/useTasksLightbox';

const reads = vi.hoisted(() => ({ transport: vi.fn() }));
vi.mock('@/integrations/runtime/client', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/integrations/runtime/client')>();
  return { ...actual, AstridRuntimeClient: class extends actual.AstridRuntimeClient {
    constructor() { super({ baseUrl: '/recovery-test', transport: reads.transport }); }
  } };
});

const originalTask = fixture.task as Task;
const originalOutput = fixture.outputs.items[0] as ManagedOutput;
let currentTask: Task;
let currentOutput: ManagedOutput;
let outputPage: { items: ManagedOutput[]; next_cursor: string | null };
let selectionAvailable: boolean;
let requests: { method: string; path: string }[];
let delayed: ((path: string) => Promise<void> | undefined) | undefined;
const opened = vi.fn();
const cancelled = vi.fn();
const retried = vi.fn();
const exported = vi.fn();
const inspected = vi.fn();

const transport: Transport = async (method, path) => {
  requests.push({ method, path });
  await delayed?.(path);
  let body: unknown;
  let status = 200;
  if (path === '/v1/health') body = { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: 'recovery-test-instance' };
  else if (path === '/v1/handshake') body = { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, actor_id: 'recovery-test-actor', realm_id: 'recovery-test-realm', session_id: 'recovery-test-session', scopes: RUNTIME_CLIENT_SCOPES, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] };
  else if (path === '/v1/realm') body = { realm_id: 'recovery-test-realm', display_name: 'Recovery test', version: 1, created_at: originalTask.created_at };
  else if (path.includes('/media-selection?')) {
    body = selectionAvailable ? fixture.selection : { code: 'not_found', message: 'output has no authoritative registered variant' };
    status = selectionAvailable ? 200 : 404;
  } else if (path.includes('/managed-outputs?')) body = outputPage;
  else if (path.startsWith('/v1/managed-outputs/')) body = currentOutput;
  else if (path.startsWith('/v1/events?')) body = { items: [], next_cursor: null };
  else if (path === `/v1/tasks/${originalTask.task_id}`) body = currentTask;
  else throw new Error(`Unexpected recovery read: ${method} ${path}`);
  return { status, headers: { 'Content-Type': 'application/json' }, body: new TextEncoder().encode(JSON.stringify(body)) };
};

function list(task = currentTask, projectId = task.project_id!) {
  return <RuntimeTaskList tasks={[task]} projectId={projectId} onOpenOutput={opened}
    isLoading={false} error={null} actionError={null} onCancelTask={cancelled} onRetryTask={retried}
    isTaskActionPending={() => false} timelineId={null} onExportManagedOutput={exported}
    isExportTaskPending={() => false} onInspectTask={inspected} />;
}

function dock(task = currentTask) {
  return <RuntimeActivityDock projectId={task.project_id!} tasks={[task]} links={[]} timelineId={null}
    isLoading={false} error={null} actionError={null} isPinned={false} isHistoryOpen={true}
    onTogglePinned={vi.fn()} onToggleHistory={vi.fn()} onTemporaryHistoryLeave={vi.fn()} onOpenHistory={vi.fn()}
    onCancelTask={cancelled} onRetryTask={retried} isTaskActionPending={() => false}
    onExportManagedOutput={exported} isExportTaskPending={() => false} onOpenOutput={opened}
    requestedTaskInspection={{ taskId: task.task_id, anchor: { top: 50, right: 400 } }} />;
}

function gate() {
  let release!: () => void;
  const promise = new Promise<void>((resolve) => { release = resolve; });
  return { promise, release };
}

beforeEach(() => {
  vi.clearAllMocks();
  currentTask = structuredClone(originalTask);
  currentOutput = structuredClone(originalOutput);
  outputPage = { items: [currentOutput], next_cursor: null };
  selectionAvailable = true;
  requests = [];
  delayed = undefined;
  reads.transport.mockImplementation(transport);
});

async function ready() {
  await screen.findByRole('button', { name: 'Open output' });
}

describe('actual Runtime task recovery surfaces with normal read transport', () => {
  it.each(['list', 'inspector'])('keeps the actual image, unknown outcome and available action together in the %s', async (surface) => {
    render(surface === 'list' ? list() : dock());
    await ready();
    const recovery = screen.getByRole('region', { name: 'Manual placement recovery' });
    expect(within(recovery).getByText('Placement unconfirmed: place manually')).toBeInTheDocument();
    expect(screen.queryByText('Not placed: place manually')).not.toBeInTheDocument();
    expect(within(recovery).getByRole('link', { name: 'View recovery.png' })).toHaveAttribute('href', expect.stringContaining(encodeURIComponent(originalOutput.object_id)));
    expect(within(recovery).getByText(/Manual placement unavailable here/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Place manually' })).not.toBeInTheDocument();
    expect(opened).not.toHaveBeenCalled();
    fireEvent.click(within(recovery).getByRole('button', { name: 'Open output' }));
    await waitFor(() => expect(opened).toHaveBeenCalledWith(currentTask, currentOutput, fixture.selection));
    expect(fixture.selection.generation_id).not.toBe(originalOutput.association_id);
    expect(fixture.selection.variant_id).not.toBe(originalOutput.object_id);
    const selectionReads = requests.filter(({ path }) => path.includes('/media-selection?'));
    expect(selectionReads).toHaveLength(2);
    for (const { path } of selectionReads) {
      const query = new URL(path, 'http://fixture').searchParams;
      expect(Object.fromEntries(query)).toEqual({ association_id: originalOutput.association_id, object_id: originalOutput.object_id, version: '1' });
    }
    expect(requests.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake')).toEqual([]);
    expect(cancelled).not.toHaveBeenCalled();
    expect(retried).not.toHaveBeenCalled();
    expect(exported).not.toHaveBeenCalled();
  });

  it('keeps a real managed-only video viewable without inventing generation or variant identities', async () => {
    const recorded = filled('managed_outputs_200').body as typeof outputPage;
    outputPage = recorded;
    const output = recorded.items[0];
    currentTask = { ...currentTask, task_id: output.task_id, run_id: output.run_id, project_id: output.project_id, attempt_id: output.attempt_id };
    selectionAvailable = false;
    render(list());
    await screen.findByText('Placement unconfirmed: place manually');
    expect(screen.getByRole('link', { name: 'View video' })).toHaveAttribute('href', expect.stringContaining(encodeURIComponent(output.object_id)));
    expect(screen.queryByRole('button', { name: 'Open output' })).not.toBeInTheDocument();
    expect(screen.getByText(/Recover this output from the project gallery/)).toBeInTheDocument();
    expect(opened).not.toHaveBeenCalled();
  });

  it.each([
    { state: 'failed' as const },
    { state: 'running' as const },
    { generation_intent: { version: 1 } },
    { spec: { spec: { params: { placement_intent: {}, generation_intent: {} } } } },
    { spec: { spec: { generation_intent: {}, params: { placement_intent: {} } } } },
    { spec: { spec: { params: {} } } },
  ])('excludes running, failed, modern bound and unrelated tasks: %j', async (override) => {
    render(list({ ...currentTask, ...override }));
    await act(async () => {});
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
    expect(requests).toEqual([]);
  });

  it.each([
    { project_id: 'foreign' }, { task_id: 'foreign' }, { run_id: 'foreign' }, { attempt_id: 'foreign' },
    { state: 'reclaimed' }, { media_type: 'application/json' }, { role: 'thumbnail' }, { object_id: 'fake-generation' },
  ])('does not associate foreign, unreadable or noncreative output rows: %j', async (override) => {
    outputPage.items = [{ ...currentOutput, ...override }];
    render(list());
    await waitFor(() => expect(requests.some(({ path }) => path.includes('/managed-outputs?'))).toBe(true));
    await act(async () => {});
    expect(screen.queryByRole('region', { name: 'Manual placement recovery' })).not.toBeInTheDocument();
    expect(requests.some(({ path }) => path.includes('/media-selection?'))).toBe(false);
  });

  it('paginates the normal output read and refuses repeated cursors', async () => {
    let pages = 0;
    reads.transport.mockImplementation(async (...args: Parameters<Transport>) => {
      if (args[1].includes('/managed-outputs?')) {
        pages++;
        return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(pages === 1
          ? { items: [], next_cursor: 'next' } : { items: [currentOutput], next_cursor: null })) };
      }
      return transport(...args);
    });
    const rendered = render(list());
    await ready();
    expect(pages).toBe(2);
    rendered.unmount();
    reads.transport.mockImplementation(transport);
    outputPage.next_cursor = 'repeated';
    render(list());
    await waitFor(() => expect(requests.filter(({ path }) => path.includes('cursor=repeated'))).toHaveLength(1));
    await act(async () => {});
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
  });

  it.each(['modern', 'reclaimed', 'object', 'version', 'selection'])('rechecks %s changes before opening; keeps inspect available on refusal', async (change) => {
    render(list());
    await ready();
    if (change === 'modern') currentTask = { ...currentTask, generation_intent: { version: 1 } };
    if (change === 'reclaimed') currentOutput = { ...currentOutput, state: 'reclaimed' };
    if (change === 'object') currentOutput = { ...currentOutput, object_id: `sha256:${'e'.repeat(64)}` };
    if (change === 'version') currentOutput = { ...currentOutput, version: 2 };
    if (change === 'selection') selectionAvailable = false;
    fireEvent.click(screen.getByRole('button', { name: 'Open output' }));
    await screen.findByRole('status');
    expect(opened).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Inspect Image generation activity' }));
    expect(inspected).toHaveBeenCalled();
  });

  it.each(['project', 'task', 'unmount'])('discards pending action completion after %s changes', async (change) => {
    const rendered = render(list());
    await ready();
    const held = gate();
    delayed = (path) => path.startsWith('/v1/managed-outputs/') ? held.promise : undefined;
    fireEvent.click(screen.getByRole('button', { name: 'Open output' }));
    await waitFor(() => expect(requests.some(({ path }) => path.startsWith('/v1/managed-outputs/'))).toBe(true));
    if (change === 'project') rendered.rerender(list(currentTask, 'foreign'));
    else if (change === 'task') rendered.rerender(list({ ...currentTask, state: 'running', version: 3 }));
    else rendered.unmount();
    await act(async () => { held.release(); });
    expect(opened).not.toHaveBeenCalled();
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
  });

  it('discards a stale initial output read after the project changes', async () => {
    const held = gate();
    delayed = (path) => path.includes('/managed-outputs?') ? held.promise : undefined;
    const rendered = render(list());
    await waitFor(() => expect(requests.some(({ path }) => path.includes('/managed-outputs?'))).toBe(true));
    rendered.rerender(list(currentTask, 'foreign'));
    await act(async () => { held.release(); });
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
    expect(requests.some(({ path }) => path.includes('/media-selection?'))).toBe(false);
  });

  it('removes the old label/media pair during an output lifecycle refresh and cancels the pending opener', async () => {
    const rendered = render(list());
    await ready();
    const held = gate();
    delayed = (path) => path.includes('/media-selection?') ? held.promise : undefined;
    fireEvent.click(screen.getByRole('button', { name: 'Open output' }));
    await waitFor(() => expect(requests.filter(({ path }) => path.includes('/media-selection?'))).toHaveLength(2));
    outputPage = { items: [{ ...currentOutput, state: 'reclaimed', version: 2 }], next_cursor: null };
    rendered.rerender(list({ ...currentTask, updated_at: '2026-10-20T09:00:00Z' }));
    expect(screen.queryByText('Placement unconfirmed: place manually')).not.toBeInTheDocument();
    expect(screen.queryByRole('link', { name: 'View recovery.png' })).not.toBeInTheDocument();
    await act(async () => { held.release(); });
    expect(opened).not.toHaveBeenCalled();
    expect(screen.queryByRole('region', { name: 'Manual placement recovery' })).not.toBeInTheDocument();
  });
});

function LightboxHarness({ projectId }: { projectId: string }) {
  const lightbox = useTasksLightbox({ selectedProjectId: projectId, currentShotId: null, lastAffectedShotId: null,
    setActiveTaskId: vi.fn(), setIsTasksPaneOpen: vi.fn() });
  return <>
    <RuntimeTaskList tasks={[currentTask]} projectId={projectId} onOpenOutput={lightbox.handleOpenRuntimeTaskOutput}
      isLoading={false} error={null} actionError={null} onCancelTask={cancelled} onRetryTask={retried}
      isTaskActionPending={() => false} timelineId={null} onExportManagedOutput={exported}
      isExportTaskPending={() => false} onInspectTask={inspected} />
    {lightbox.lightboxProps && <section aria-label="Existing lightbox adapter">
      <span>{lightbox.lightboxProps.media.id}</span><span>{lightbox.lightboxProps.initialVariantId}</span>
      <span data-testid="recovery-tuple" data-frozen={Object.isFrozen(lightbox.lightboxData?.runtimeRecoverySource?.mediaTuple)}>
        {JSON.stringify(lightbox.lightboxData?.runtimeRecoverySource?.mediaTuple)}
      </span>
      <button onClick={lightbox.handleCloseLightbox}>Close output</button>
    </section>}
  </>;
}

it('uses the real TasksPane lightbox hook and providers with read-authoritative identities; supports reopen and project change', async () => {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const element = (projectId: string) => <QueryClientProvider client={queryClient}>
    <RuntimeAuthorityContext.Provider value={{ runtimeAuthority: true, runtimeProjectId: projectId }}>
      <LightboxHarness projectId={projectId} />
    </RuntimeAuthorityContext.Provider>
  </QueryClientProvider>;
  const rendered = render(element(originalTask.project_id!));
  await ready();
  fireEvent.click(screen.getByRole('button', { name: 'Open output' }));
  let lightbox = await screen.findByRole('region', { name: 'Existing lightbox adapter' });
  expect(within(lightbox).getByText(fixture.selection.generation_id)).toBeInTheDocument();
  expect(within(lightbox).getByText(fixture.selection.variant_id)).toBeInTheDocument();
  expect(JSON.parse(within(lightbox).getByTestId('recovery-tuple').textContent!)).toEqual(fixture.selection);
  expect(within(lightbox).getByTestId('recovery-tuple')).toHaveAttribute('data-frozen', 'true');
  expect(within(lightbox).queryByText(originalOutput.association_id)).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Close output' }));
  expect(screen.queryByRole('region', { name: 'Existing lightbox adapter' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Open output' }));
  lightbox = await screen.findByRole('region', { name: 'Existing lightbox adapter' });
  expect(within(lightbox).getByText(fixture.selection.variant_id)).toBeInTheDocument();
  rendered.rerender(element('foreign'));
  await waitFor(() => expect(screen.queryByRole('region', { name: 'Existing lightbox adapter' })).not.toBeInTheDocument());
  expect(requests.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake')).toEqual([]);
  queryClient.clear();
});
