import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { AstridStatusSection } from './AstridStatusSection.tsx';
import { RUNTIME_CONNECTION_COPY as CONNECTION_COPY, installCommand } from '@/shared/components/RuntimeConnection/copy.ts';

const mocks = vi.hoisted(() => ({
  readStatus: vi.fn(),
  clipboard: vi.fn(),
  connect: vi.fn(),
  connection: {
    state: { status: 'connected', realm: { realm_id: 'realm-1', display_name: 'Studio' } },
    awaitingConnect: false, isChecking: false, schemaDigest: null, connect: () => {},
  } as { state: { status: string; realm?: { realm_id: string; display_name: string } }; awaitingConnect: boolean; isChecking: boolean; schemaDigest: string | null; connect: () => void },
}));

vi.mock('@/integrations/runtime/client.ts', () => ({
  AstridRuntimeClient: class {
    readStatus = mocks.readStatus;
  },
}));

vi.mock('@/integrations/runtime/RuntimeConnectionProvider.tsx', () => ({
  useRuntimeConnection: () => mocks.connection,
}));

vi.mock('@/shared/lib/browser/clipboard.ts', () => ({
  writeClipboardTextSafe: mocks.clipboard,
}));

describe('AstridStatusSection', () => {
  beforeEach(() => {
    mocks.connection.state = { status: 'connected', realm: { realm_id: 'realm-1', display_name: 'Studio' } };
    mocks.connection.awaitingConnect = false;
    mocks.connection.isChecking = false;
    mocks.connection.connect = mocks.connect.mockReset();
    mocks.clipboard.mockReset().mockResolvedValue(true);
    mocks.readStatus.mockReset().mockResolvedValue({
      health: {
        status: 'ok',
        protocol: 'workspace.v1',
        schema_digest: `sha256:${'a'.repeat(64)}`,
        runtime_epoch: 2,
        runtime_session_id: 'session-1',
        runtime_instance_id: 'runtime-1',
        services: [
          { name: 'comfyui', state: 'starting', last_exit: null, restart_count: 0 },
          { name: 'pack-host', state: 'running', last_exit: null, restart_count: 1 },
          { name: 'chat', state: 'failed', last_exit: 2, restart_count: 3, reason: 'startup_failed' },
        ],
      },
      realm: { realm_id: 'realm-1', display_name: 'Studio', version: 4, created_at: '2026-01-01T00:00:00Z' },
    });
  });

  it('keeps Runtime and Workspace checks in the single status section', async () => {
    render(<AstridStatusSection isOpen />);
    expect(await screen.findByText('Studio')).toBeInTheDocument();
    expect(screen.getByText('Runtime')).toHaveAttribute('data-state', 'pass');
    expect(document.querySelector('[data-check="workspace"]')).toHaveAttribute('data-state', 'pass');
    expect(screen.queryByRole('heading', { name: 'Connection' })).not.toBeInTheDocument();
  });

  it('offers the browser permission action before checking Runtime details', () => {
    mocks.connection.state = { status: 'connecting' };
    mocks.connection.awaitingConnect = true;
    render(<AstridStatusSection isOpen />);
    fireEvent.click(screen.getByRole('button', { name: CONNECTION_COPY.permission.connect }));
    expect(mocks.connect).toHaveBeenCalledOnce();
    expect(mocks.readStatus).not.toHaveBeenCalled();
    expect(screen.queryByText('Runtime')).not.toBeInTheDocument();
  });

  it('keeps blocked permission recovery instructions inside the status section', () => {
    mocks.connection.state = { status: 'blocked' };
    render(<AstridStatusSection isOpen />);
    expect(screen.getByText(CONNECTION_COPY.blocked.steps.join(' '))).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: CONNECTION_COPY.permission.connect })).not.toBeInTheDocument();
    expect(mocks.readStatus).not.toHaveBeenCalled();
  });

  it('shows the connected workspace and readable service states without inventing versions', async () => {
    render(<AstridStatusSection isOpen />);

    expect(await screen.findByText('Studio')).toBeInTheDocument();
    expect(screen.getByText('workspace.v1')).toBeInTheDocument();
    expect(screen.queryByText('Versions')).not.toBeInTheDocument();
    expect(screen.getByText('Task host')).toBeInTheDocument();
    expect(screen.getByText('ComfyUI')).toBeInTheDocument();
    expect(screen.getByText('Chat')).toBeInTheDocument();
    expect(screen.getByText('Starting…')).toBeInTheDocument();
    expect(screen.getByText('Running')).toBeInTheDocument();
    expect(screen.getByText('Failed')).toBeInTheDocument();
    expect(screen.getByText(/Restarts: 3/)).toBeInTheDocument();
    expect(screen.queryByText('Restarts: 0')).not.toBeInTheDocument();
    expect(screen.queryByText(/Last exit code|Reason:|startup_failed/)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy' })).toBeInTheDocument();
    expect(screen.getByText('curl -fsSL https://astrid.haus/install | sh')).toBeInTheDocument();
  });

  it('keeps unknown service names and hides repair when health is healthy', async () => {
    mocks.readStatus.mockResolvedValue({
      health: {
        status: 'ok',
        protocol: 'workspace.v1',
        schema_digest: `sha256:${'b'.repeat(64)}`,
        services: [
          { name: 'custom-worker', state: 'running', last_exit: null, restart_count: 0 },
          { name: 'retrying-worker', state: 'running', last_exit: 1, restart_count: 0, reason: 'exited' },
        ],
      },
      realm: { realm_id: 'realm-1', display_name: 'Studio', version: 4, created_at: '2026-01-01T00:00:00Z' },
    });
    render(<AstridStatusSection isOpen />);

    const customWorker = await screen.findByText('custom-worker');
    expect(customWorker.closest('li')?.querySelector('span.basis-full')).toBeNull();
    expect(screen.queryByText(/Last exit code|Reason:|exited/)).not.toBeInTheDocument();
    expect(screen.queryByText(/^ · /)).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Copy' })).not.toBeInTheDocument();
    expect(screen.queryByText('curl -fsSL https://astrid.haus/install | sh')).not.toBeInTheDocument();
    expect(screen.queryByText(/Restarts:/)).not.toBeInTheDocument();
  });

  it('shows the shared repair command for degraded health even without a failed service', async () => {
    mocks.readStatus.mockResolvedValue({
      health: {
        status: 'degraded',
        protocol: 'workspace.v1',
        schema_digest: `sha256:${'c'.repeat(64)}`,
        services: [{ name: 'pack-host', state: 'running', last_exit: null, restart_count: 1 }],
      },
      realm: { realm_id: 'realm-1', display_name: 'Studio', version: 4, created_at: '2026-01-01T00:00:00Z' },
    });
    render(<AstridStatusSection isOpen />);

    expect(await screen.findByRole('status')).toHaveTextContent("Connected, but part of Astrid isn't working.");
    expect(screen.getByRole('button', { name: 'Copy' })).toBeInTheDocument();
    expect(screen.getByText('curl -fsSL https://astrid.haus/install | sh')).toBeInTheDocument();
  });

  it('copies the same install command shown in the repair control', async () => {
    render(<AstridStatusSection isOpen />);
    expect(await screen.findByRole('button', { name: 'Copy' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Copy' }));

    await waitFor(() => expect(mocks.clipboard).toHaveBeenCalledWith(installCommand('install')));
    expect(await screen.findByRole('button', { name: 'Copied' })).toBeInTheDocument();
  });

  it('shows the connection state without requesting details while offline', () => {
    mocks.connection.state = { status: 'not_running' };
    render(<AstridStatusSection isOpen />);

    expect(screen.getByRole('status')).toHaveTextContent('Not running');
    expect(mocks.readStatus).not.toHaveBeenCalled();
  });

  it('does not request Runtime details while settings are closed', () => {
    render(<AstridStatusSection isOpen={false} />);

    expect(mocks.readStatus).not.toHaveBeenCalled();
  });

  it('reads current health again when settings are reopened', async () => {
    const first = {
      health: {
        status: 'ok',
        protocol: 'workspace.v1',
        schema_digest: `sha256:${'a'.repeat(64)}`,
        services: [{ name: 'pack-host', state: 'running', last_exit: null, restart_count: 0 }],
      },
      realm: { realm_id: 'realm-1', display_name: 'Studio', version: 4, created_at: '2026-01-01T00:00:00Z' },
    };
    const second = {
      health: { ...first.health, status: 'degraded', services: [{ name: 'pack-host', state: 'failed', last_exit: 1, restart_count: 1 }] },
      realm: first.realm,
    };
    mocks.readStatus.mockReset().mockResolvedValueOnce(first).mockResolvedValueOnce(second);
    const view = render(<AstridStatusSection isOpen />);

    expect(await screen.findByText('Running')).toBeInTheDocument();
    view.rerender(<AstridStatusSection isOpen={false} />);
    view.rerender(<AstridStatusSection isOpen />);

    expect(await screen.findByText("Connected, but part of Astrid isn't working.")).toBeInTheDocument();
    expect(await screen.findByText('Failed')).toBeInTheDocument();
    expect(mocks.readStatus).toHaveBeenCalledTimes(2);
  });
});
