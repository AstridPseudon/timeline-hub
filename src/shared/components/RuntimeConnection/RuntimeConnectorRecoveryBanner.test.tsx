import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { RuntimeConnectorRecoveryBanner, buildWorkspaceRestartBrief } from './RuntimeConnectorRecoveryBanner';

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe('RuntimeConnectorRecoveryBanner', () => {
  it('offers retry and both restart paths, with a truthful idle and retrying state', () => {
    const onRetry = vi.fn();
    const view = render(<RuntimeConnectorRecoveryBanner retrying={false} error={new Error("Connection refused.")} onRetry={onRetry} />);

    expect(screen.getByRole('heading', { name: 'Workspace Runtime is unavailable' })).toBeInTheDocument();
    expect(screen.getByTestId('workspace-connection-summary')).toHaveTextContent('The editor could not complete workspace discovery.');
    expect(screen.getByTestId('workspace-connection-diagnostic')).toHaveTextContent('Connection refused.');
    expect(screen.getByTestId('workspace-connection-diagnostic').closest('details')).not.toHaveAttribute('open');
    fireEvent.click(screen.getByText('Show full connection error'));
    expect(screen.getByTestId('workspace-connection-diagnostic').closest('details')).toHaveAttribute('open');
    expect(screen.getByRole('button', { name: 'Copy restart instructions' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Show restart steps' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Retry Runtime connection' }));
    expect(onRetry).toHaveBeenCalledOnce();

    view.rerender(<RuntimeConnectorRecoveryBanner retrying error={new Error("Connection refused.")} onRetry={onRetry} />);
    expect(screen.getByRole('button', { name: 'Retrying Runtime connection…' })).toBeDisabled();
  });

  it('copies instructions for the same existing Runtime, sanitizing the optional configured URL', async () => {
    const writeText = vi.fn(async (_text: string) => undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    render(<RuntimeConnectorRecoveryBanner
      retrying={false}
      error={new Error("Runtime health check failed.")}
      connectionUrl="http://user:secret@localhost:22894/runtime?token=secret#private"
      onRetry={vi.fn()}
    />);

    fireEvent.click(screen.getByRole('button', { name: 'Copy restart instructions' }));
    await waitFor(() => expect(writeText).toHaveBeenCalledOnce());
    const brief = String(writeText.mock.calls[0][0]);
    expect(brief).toContain('npm run dev:local');
    expect(brief).toContain('Runtime health check failed.');
    expect(brief).toContain('http://localhost:22894/runtime');
    expect(brief).toContain('Do not reset, reinstall, create a new data root');
    expect(brief).toContain('Verify that the same configured Runtime is healthy');
    expect(brief).not.toContain('secret');
    expect(screen.getByLabelText('Restart brief')).toHaveValue(brief);
    expect(screen.getByRole('status')).toHaveTextContent('Restart instructions copied');
  });

  it('shows a selectable brief when browser clipboard permission is unavailable', async () => {
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText: vi.fn(async () => { throw new Error('Clipboard denied'); }) },
    });
    render(<RuntimeConnectorRecoveryBanner retrying={false} error={new Error("Bridge timeout.")} onRetry={vi.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: 'Copy restart instructions' }));
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Clipboard access is unavailable'));
    expect((screen.getByLabelText('Restart brief') as HTMLTextAreaElement).value).toContain('Bridge timeout.');
  });

  it('reveals manual restart steps that preserve the existing installation and Runtime data', () => {
    render(<RuntimeConnectorRecoveryBanner retrying={false} error={new Error("Runtime is offline.")} onRetry={vi.fn()} />);
    expect(screen.queryByText(/Return to the same Astrid App checkout/)).toBeNull();
    const toggle = screen.getByRole('button', { name: 'Show restart steps' });
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute('aria-expanded', 'true');

    expect(screen.getByText(/Return to the same Astrid App checkout/)).toBeInTheDocument();
    expect(screen.getByText('npm run dev:local')).toBeInTheDocument();
    expect(screen.getByText(/restart that same Runtime with its current command, profile, and data-root configuration/)).toBeInTheDocument();
    expect(screen.getByText(/Do not reset or reinstall the workspace/)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Copy restart instructions' }));
    expect(screen.getByText(/Return to the same Astrid App checkout/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Hide restart steps' }));
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect(screen.queryByText(/Return to the same Astrid App checkout/)).toBeNull();
    expect(screen.getByLabelText('Restart brief')).toBeInTheDocument();
  });

  it('builds the agent brief with only a sanitized HTTP(S) target', () => {
    expect(buildWorkspaceRestartBrief({ error: '', connectionUrl: 'file:///private/runtime.db' }))
      .not.toContain('file:///private/runtime.db');
    expect(buildWorkspaceRestartBrief({ error: '', connectionUrl: 'not a URL' }))
      .toContain('The editor cannot reach its configured Astrid Runtime.');
  });

  it('includes the current project and timeline route identity in the agent brief', () => {
    const brief = buildWorkspaceRestartBrief({
      error: 'Timeline lookup timed out.',
      projectId: 'newblanktimeline3',
      timelineId: 'timeline-a',
    });

    expect(brief).toContain('project newblanktimeline3, timeline timeline-a');
    expect(brief).toContain('Timeline lookup timed out.');
  });
});
