import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({ ensureSession: vi.fn(), clipboard: vi.fn() }));
vi.mock('@/integrations/runtime/client.ts', () => ({ AstridRuntimeClient: class { ensureSession = mocks.ensureSession; } }));
vi.mock('@/integrations/runtime/connection.ts', () => ({ runtimeApiBase: () => 'http://127.0.0.1:17340/api/runtime' }));
vi.mock('@/shared/lib/browser/clipboard.ts', () => ({ writeClipboardTextSafe: mocks.clipboard }));

import { EmptyWorkspaceGuidance } from './EmptyWorkspaceGuidance.tsx';

function showGuidance(onRefresh = vi.fn()) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } });
  render(<QueryClientProvider client={client}><EmptyWorkspaceGuidance onRefresh={onRefresh} /></QueryClientProvider>);
  return onRefresh;
}
function openDetails() {
  const details = screen.getByText('Check connected workspace').closest('details')!;
  details.open = true;
  fireEvent(details, new Event('toggle'));
}

beforeEach(() => {
  vi.clearAllMocks();
  mocks.ensureSession.mockResolvedValue({
    realm: { realm_id: 'realm-existing', display_name: 'My workspace' },
    health: { runtime_instance_id: 'instance-existing' },
    handshake: { session_id: 'private-session-value', token: 'private-credential-value' },
  });
  mocks.clipboard.mockResolvedValue(true);
});

describe('connected empty workspace guidance', () => {
  it('explains that a connected workspace can be empty and lets users inspect identity before creating work', async () => {
    const onRefresh = showGuidance();
    expect(screen.getByText('Astrid is connected, but this workspace has no projects.')).toBeInTheDocument();
    expect(screen.getByText('If you expected existing work, check which workspace is connected before creating a project.')).toBeInTheDocument();
    expect(mocks.ensureSession).not.toHaveBeenCalled();
    openDetails();
    expect(await screen.findByText('My workspace')).toBeInTheDocument();
    expect(screen.getByText('realm-existing')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Copy workspace check for your agent' }));
    await screen.findByRole('status');
    const copied = mocks.clipboard.mock.calls[0][0];
    expect(copied).toContain('realm-existing');
    expect(copied).toContain('http://127.0.0.1:17340/api/runtime');
    expect(copied).toContain('configured data root');
    expect(copied).toContain('Do not create a new workspace or project');
    expect(copied).not.toContain('private-session-value');
    expect(copied).not.toContain('private-credential-value');
    fireEvent.click(screen.getByRole('button', { name: 'Check projects again' }));
    expect(onRefresh).toHaveBeenCalledOnce();
  });

  it('keeps a workspace check available when the clipboard cannot be written', async () => {
    mocks.clipboard.mockResolvedValue(false);
    showGuidance();
    openDetails();
    fireEvent.click(await screen.findByRole('button', { name: 'Copy workspace check for your agent' }));
    expect((await screen.findByRole('textbox', { name: 'Workspace check for your agent' }) as HTMLTextAreaElement).value).toContain('realm-existing');
  });

  it('shows an identity read failure honestly and offers a retry', async () => {
    mocks.ensureSession.mockRejectedValueOnce(new Error('connection changed'));
    showGuidance();
    openDetails();
    expect(await screen.findByText('Workspace details are unavailable.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Copy workspace check for your agent' })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Retry workspace details' }));
    await waitFor(() => expect(screen.getByText('My workspace')).toBeInTheDocument());
  });
});
