import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { ReactElement } from 'react';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { OnboardingModal } from '@/shared/components/modals/OnboardingModal';
import { Dialog, DialogContent } from '@/shared/components/ui/dialog';
import { ASTRID_COMMANDS, RUNTIME_CONNECTION_COPY as COPY, withCommandShell } from '@/shared/components/RuntimeConnection/copy.ts';
import { connectionFor, CONNECTED_REALM } from '@/shared/components/RuntimeConnection/connectionFixture.ts';

const mocks = vi.hoisted(() => ({
  connection: {} as RuntimeConnectionValue,
  projects: vi.fn(),
  clipboard: vi.fn(),
}));
vi.mock('@/integrations/runtime/RuntimeConnectionProvider.tsx', () => ({
  useRuntimeConnection: () => mocks.connection,
}));
vi.mock('@/integrations/runtime/client.ts', () => ({
  AstridRuntimeClient: class { listProjects = mocks.projects; },
}));
vi.mock('@/shared/lib/browser/clipboard.ts', () => ({ writeClipboardTextSafe: mocks.clipboard }));

import { AstridSetupStep } from './AstridSetupStep';

function renderWithQueries(ui: ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } });
  return render(ui, { wrapper: ({ children }) => <QueryClientProvider client={client}>{children}</QueryClientProvider> });
}
const renderInDialog = (ui: ReactElement) => renderWithQueries(<Dialog open><DialogContent>{ui}</DialogContent></Dialog>);

beforeEach(() => {
  vi.clearAllMocks();
  mocks.connection = connectionFor({ status: 'set_up' });
  mocks.clipboard.mockResolvedValue(true);
  mocks.projects.mockResolvedValue([]);
});
afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe('AstridSetupStep', () => {
  it('opens the modal on its content and lets Tab reach the shared Copy action', async () => {
    const user = userEvent.setup();
    renderWithQueries(<OnboardingModal isOpen onClose={vi.fn()} />);
    const copy = screen.getByRole('button', { name: COPY.agent.copy });
    await waitFor(() => {
      expect(document.activeElement).toContainElement(screen.getByRole('heading', { name: COPY.setUp.title }));
      expect(copy).not.toHaveFocus();
    });
    await user.tab();
    expect(copy).toHaveFocus();
  });

  it.each([
    ['MacIntel', ASTRID_COMMANDS.macLinux],
    ['Win32', ASTRID_COMMANDS.windows],
  ])('uses the shared install flow on %s', async (platform, command) => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue(platform);
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);

    expect(screen.getByRole('heading', { name: COPY.setUp.title })).toBeInTheDocument();
    expect(screen.getByText(withCommandShell(COPY.setUp.sentence))).toBeInTheDocument();
    expect(screen.getByText(command, { selector: 'code' })).toBeInTheDocument();
    expect(screen.getByText(COPY.agent.note)).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: COPY.agent.copy })).toHaveLength(1);
    expect(screen.queryByRole('radio')).toBeNull();
    expect(screen.queryByRole('link')).toBeNull();
    expect(document.querySelector('[data-check]')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Continue' })).toBeNull();
    expect(mocks.projects).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: COPY.agent.copy }));
    expect(await screen.findByRole('button', { name: COPY.agent.copied })).toBeInTheDocument();
    expect(mocks.clipboard).toHaveBeenCalledWith(command);
  });

  it('keeps the command selectable when the shared copy action fails', async () => {
    mocks.clipboard.mockResolvedValue(false);
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    const command = screen.getByText(/https:\/\/astrid.haus\/install/, { selector: 'code' }).textContent;
    fireEvent.click(screen.getByRole('button', { name: COPY.agent.copy }));

    expect(await screen.findByRole('status')).toHaveTextContent(COPY.agent.copyFailed);
    const fallback = screen.getByRole('textbox', { name: COPY.agent.copyFailed }) as HTMLTextAreaElement;
    expect(fallback).toHaveValue(command);
    expect(fallback.selectionStart).toBe(0);
    expect(fallback.selectionEnd).toBe(command?.length);
    expect(screen.queryByRole('button', { name: COPY.agent.copied })).toBeNull();
  });

  it('uses the shared start copy and install line for reconnecting', () => {
    mocks.connection = connectionFor({ status: 'not_running' });
    renderInDialog(<AstridSetupStep reconnect onNext={vi.fn()} onClose={vi.fn()} />);

    expect(screen.getByRole('heading', { name: COPY.notRunning.title })).toBeInTheDocument();
    expect(screen.getByText(withCommandShell(COPY.notRunning.sentence))).toBeInTheDocument();
    expect(screen.getByText(ASTRID_COMMANDS.macLinux, { selector: 'code' })).toBeInTheDocument();
    expect(screen.queryByText(/Runtime|Workspace|Tools/)).toBeNull();
  });

  it.each([
    { label: 'empty', projects: [] },
    { label: 'existing', projects: [{ project_id: 'existing-project' }] },
  ])('continues once the connected workspace is readable: $label', async ({ projects }) => {
    mocks.connection = connectionFor({ status: 'connected', realm: CONNECTED_REALM });
    mocks.projects.mockResolvedValue(projects);
    const onNext = vi.fn();
    renderInDialog(<AstridSetupStep onNext={onNext} onClose={vi.fn()} />);

    expect(await screen.findByRole('heading', { name: COPY.connected.sentence })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: COPY.agent.copy })).toBeNull();
    expect(screen.queryByRole('link')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(onNext).toHaveBeenCalledOnce();
    expect(mocks.projects).toHaveBeenCalledOnce();
  });

  it('waits for a same-origin workspace to become readable and accepts an empty project list', async () => {
    vi.useFakeTimers();
    mocks.connection = connectionFor({ status: 'connected', realm: CONNECTED_REALM }, { gated: false });
    mocks.projects.mockRejectedValueOnce(new Error('project list unavailable')).mockResolvedValue([]);
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => { await vi.advanceTimersByTimeAsync(1); });

    expect(mocks.projects).toHaveBeenCalledOnce();
    expect(screen.getByRole('heading', { name: COPY.setUp.title })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue' })).toBeNull();
    await act(async () => { await vi.advanceTimersByTimeAsync(4000); });
    await act(async () => { await vi.advanceTimersByTimeAsync(1); });

    expect(mocks.projects).toHaveBeenCalledTimes(2);
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
    await act(async () => { await vi.advanceTimersByTimeAsync(8000); });
    expect(mocks.projects).toHaveBeenCalledTimes(2);
  });

  it.each([false, true])('keeps waiting when a connected workspace cannot be read, reconnect=%s', async reconnect => {
    mocks.connection = connectionFor({ status: 'connected', realm: CONNECTED_REALM });
    mocks.projects.mockRejectedValue(new Error('project list unavailable'));
    const onNext = vi.fn();
    renderInDialog(<AstridSetupStep reconnect={reconnect} onNext={onNext} onClose={vi.fn()} />);

    await waitFor(() => expect(mocks.projects).toHaveBeenCalledOnce());
    expect(screen.getByRole('heading', { name: reconnect ? COPY.notRunning.title : COPY.setUp.title })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Back to Astrid' })).toBeNull();
    expect(onNext).not.toHaveBeenCalled();
  });

  it('returns directly to Astrid when a reconnecting install becomes ready', async () => {
    const onNext = vi.fn();
    const view = renderInDialog(<AstridSetupStep reconnect onNext={onNext} onClose={vi.fn()} />);
    expect(onNext).not.toHaveBeenCalled();
    mocks.connection = connectionFor({ status: 'connected', realm: CONNECTED_REALM });
    view.rerender(<Dialog open><DialogContent><AstridSetupStep reconnect onNext={onNext} onClose={vi.fn()} /></DialogContent></Dialog>);

    await waitFor(() => expect(onNext).toHaveBeenCalledOnce());
  });
});
