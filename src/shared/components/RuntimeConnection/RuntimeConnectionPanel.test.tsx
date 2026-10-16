// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { RuntimeConnectionPanel } from './RuntimeConnectionPanel.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, segmentsText } from './copy.ts';
import { CONNECTED_REALM, connectionFor } from './connectionFixture.ts';

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function panel(connection: RuntimeConnectionValue) {
  return render(<RuntimeConnectionPanel connection={connection} />);
}

/** The install line links readable text to the guide's full address, not a bare repo path. */
function expectInstallLink() {
  const link = screen.getByRole('link', { name: COPY.install.linkText });
  expect(link).toHaveAttribute('href', COPY.commands.installUrl);
  expect(link.textContent).not.toMatch(/\.md/);
  expect(document.body.textContent).not.toContain('docs/setup/local-source-install.md');
}

function stubClipboard(writeText: (text: string) => Promise<void>) {
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
}

describe('RuntimeConnectionPanel', () => {
  it('connecting: says it is looking for Reigh, with no buttons', () => {
    panel(connectionFor({ status: 'connecting' }, { isBooting: true }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
    expect(screen.getByRole('heading', { name: COPY.connecting.title })).toBeInTheDocument();
    expect(screen.getByText(COPY.connecting.sentence)).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('permission prompt: explains first, sends nothing, and Connect is what asks', () => {
    const connect = vi.fn();
    panel(connectionFor({ status: 'cant_reach', firstTime: true }, { awaitingConnect: true, connect }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'permission');
    expect(screen.getByRole('heading', { name: COPY.permission.title })).toBeInTheDocument();
    expect(screen.getByText(COPY.permission.explainer[0])).toBeInTheDocument();
    expect(screen.getByText(COPY.permission.explainer[1])).toBeInTheDocument();
    expectInstallLink();
    expect(screen.getByRole('button', { name: 'Copy instructions for your agent' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: COPY.permission.connect }));
    expect(connect).toHaveBeenCalledOnce();
  });

  it('permission prompt while Chrome is asked: the Connect button says so and is disabled', () => {
    panel(connectionFor({ status: 'connecting' }, { awaitingConnect: true, isChecking: true }));

    expect(screen.getByRole('button', { name: COPY.permission.connectPending })).toBeDisabled();
    expect(screen.queryByRole('button', { name: COPY.permission.connect })).not.toBeInTheDocument();
  });

  it('first visit with nothing running: the set-up heading and the already-installed line', () => {
    panel(connectionFor({ status: 'cant_reach', firstTime: true }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'cant_reach');
    expect(screen.getByRole('heading', { name: 'Set up Reigh on this computer' })).toBeInTheDocument();
    expect(screen.getByText(COPY.cantReach.firstTime.sentence)).toBeInTheDocument();
    expect(screen.getByText('Already installed? Start it, and this page connects by itself.')).toBeInTheDocument();
    expectInstallLink();
    expect(screen.queryByText("Reigh isn't running")).not.toBeInTheDocument();
  });

  it('returning visit with nothing running: "Reigh isn\'t running", and no first-time wording', () => {
    panel(connectionFor({ status: 'cant_reach', firstTime: false }));

    expect(screen.getByRole('heading', { name: "Reigh isn't running" })).toBeInTheDocument();
    expect(screen.getByText(COPY.cantReach.returning.sentence)).toBeInTheDocument();
    expect(screen.queryByText('Set up Reigh on this computer')).not.toBeInTheDocument();
    expect(screen.queryByText('Already installed? Start it')).not.toBeInTheDocument();
  });

  it('browser blocked: says so once, names local network access, and shows the fix', () => {
    panel(connectionFor({ status: 'blocked' }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'blocked');
    expect(screen.getByRole('heading', { name: COPY.blocked.title })).toBeInTheDocument();
    expect(screen.getByText(/browser blocked/i)).toBeInTheDocument();
    expect(screen.getByText(/local network access/i)).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: COPY.blocked.fixTitle })).toBeInTheDocument();
    for (const step of COPY.blocked.fixSteps) expect(screen.getByText(step)).toBeInTheDocument();
    const address = screen.getByText(COPY.blocked.settingsAddress(window.location.origin));
    expect(address.tagName).toBe('CODE');
    expect(address).toHaveClass('break-all', 'select-all');
    expect(screen.queryByRole('button', { name: COPY.permission.connect })).not.toBeInTheDocument();
    // The fix is a Chrome setting an agent cannot change, so the only action is the fix steps.
    expect(screen.queryByRole('button', { name: 'Copy instructions for your agent' })).not.toBeInTheDocument();
    expect(screen.queryByText('Set up Reigh on this computer')).not.toBeInTheDocument();
  });

  it.each(Object.keys(COPY.notReady.reasons) as Array<keyof typeof COPY.notReady.reasons>)(
    'not ready (%s): its own heading, and the reason as the one sentence under it',
    (reason) => {
      panel(connectionFor({ status: 'not_ready', reason }));
      const { title, sentence } = COPY.notReady.reasons[reason];

      expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'not_ready');
      expect(screen.getByRole('heading', { level: 1, name: title })).toBeInTheDocument();
      expect(screen.getByText((_, element) => element?.tagName === 'P' && element.textContent === segmentsText(sentence))).toBeInTheDocument();
      expect(screen.queryByText(/running but not ready/i)).not.toBeInTheDocument();
    },
  );

  it('a stopped Runtime says how to start it, with the command in code', () => {
    panel(connectionFor({ status: 'not_ready', reason: 'runtime_stopped' }));

    expect(screen.getByRole('heading', { name: 'Reigh needs to be started again' })).toBeInTheDocument();
    expect(screen.getByText(/Runtime has stopped/)).toBeInTheDocument();
    expect(screen.getByText('banodoco-local up --profile astrid').tagName).toBe('CODE');
  });

  it('a changed workspace reuses the restart message heading', () => {
    panel(connectionFor({ status: 'not_ready', reason: 'realm_changed' }));
    expect(screen.getByRole('heading', { name: COPY.restarted.realmChanged.title })).toBeInTheDocument();
  });

  it('an unknown reason does not promise it connects by itself', () => {
    expect(segmentsText(COPY.notReady.reasons.unknown.sentence)).not.toMatch(/connects (as soon as|by itself)/);
    expect(segmentsText(COPY.notReady.reasons.identity_mismatch.sentence)).not.toMatch(/connects (as soon as|by itself)/);
  });

  it('only waiting offers nothing to copy; a stopped Runtime still offers the agent instructions', () => {
    panel(connectionFor({ status: 'not_ready', reason: 'starting' }));
    expect(screen.queryByRole('button', { name: 'Copy instructions for your agent' })).not.toBeInTheDocument();
    cleanup();
    panel(connectionFor({ status: 'not_ready', reason: 'runtime_stopped' }));
    expect(screen.getByRole('button', { name: 'Copy instructions for your agent' })).toBeInTheDocument();
  });

  it('Copy is the primary action when it is the only button', () => {
    panel(connectionFor({ status: 'cant_reach', firstTime: false }));
    expect(screen.getByRole('button', { name: 'Copy instructions for your agent' }).className).toContain('bg-primary');
  });

  it('the pending Connect label does not blame Chrome', () => {
    expect(COPY.permission.connectPending).toBe('Connecting…');
    expect(COPY.permission.explainer[1]).toContain('look for and connect to devices on your local network');
  });

  it('the agent instructions wait for the gateway line, point to the full guide URL and name the realm', () => {
    const text = COPY.agent.instructions('https://hosted.example');
    expect(text).toContain(COPY.commands.installUrl);
    expect(text).toContain('loopback gateway starting on 127.0.0.1:<port> for https://hosted.example');
    expect(text).not.toContain('workspace.v1 runtime healthy');
    expect(text).toContain('report the realm it names');
  });

  it('shows the instructions on request, without copying', () => {
    panel(connectionFor({ status: 'cant_reach', firstTime: false }));
    expect(screen.queryByLabelText(COPY.agent.fieldLabel)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: COPY.agent.showInstructions }));
    expect((screen.getByLabelText(COPY.agent.fieldLabel) as HTMLTextAreaElement).value).toContain('npm run dev:local');
    expect(screen.getByRole('button', { name: COPY.agent.hideInstructions })).toBeInTheDocument();
  });

  it('renders nothing once connected: the gate shows the app and the pill', () => {
    const { container } = panel(connectionFor({ status: 'connected', realm: CONNECTED_REALM }));
    expect(container).toBeEmptyDOMElement();
  });

  it('copies the instructions for the page origin, with the commands the journey looks for', async () => {
    const writeText = vi.fn(async (_text: string) => undefined);
    stubClipboard(writeText);
    panel(connectionFor({ status: 'cant_reach', firstTime: false }));

    fireEvent.click(screen.getByRole('button', { name: 'Copy instructions for your agent' }));
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent(COPY.agent.copied));
    const copied = String(writeText.mock.calls[0][0]);
    expect(copied).toContain('banodoco-local up --profile astrid');
    expect(copied).toContain('npm run dev:local');
    expect(copied).toContain(window.location.origin);
    expect(screen.queryByLabelText(COPY.agent.fieldLabel)).not.toBeInTheDocument();
  });

  it('when the clipboard refuses, shows the instructions in a field to copy by hand', async () => {
    stubClipboard(vi.fn(async () => { throw new Error('Clipboard denied'); }));
    panel(connectionFor({ status: 'cant_reach', firstTime: false }));

    fireEvent.click(screen.getByRole('button', { name: 'Copy instructions for your agent' }));
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent(COPY.agent.copyFailed));
    const field = screen.getByLabelText(COPY.agent.fieldLabel) as HTMLTextAreaElement;
    expect(field.value).toContain('npm run dev:local');
    expect(field).toHaveAttribute('readonly');
  });
});
