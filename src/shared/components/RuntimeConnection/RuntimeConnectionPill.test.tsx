// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { isRecoveryCardShowing } from '@/integrations/runtime/recoveryCard.ts';
import { RuntimeConnectionPill } from './RuntimeConnectionPill.tsx';
import { RUNTIME_CONNECTION_COPY as COPY } from './copy.ts';
import { CONNECTED_REALM, connectionFor } from './connectionFixture.ts';

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

const json = (body: unknown, status = 200) => () => new Response(JSON.stringify(body), {
  status,
  headers: { 'Content-Type': 'application/json' },
});
const healthy = (instanceId: string) => json({ status: 'ok', runtime_instance_id: instanceId });
/** Nothing answers: the gateway is gone. */
const unreachable = () => { throw new TypeError('Failed to fetch'); };

/** Answers the health route in order; the last answer repeats. Counts every call. */
function healthRoute(...answers: Array<() => Response>) {
  let index = 0;
  return vi.fn(async (_input: string, _init?: RequestInit) => {
    const answer = answers[Math.min(index, answers.length - 1)];
    index += 1;
    return answer();
  });
}

/** A health route whose answer the test changes while the page is watching. */
function switchableRoute(first: () => Response) {
  const route = { answer: first };
  const fetchImpl = vi.fn(async (_input: string, _init?: RequestInit) => route.answer());
  return { route, fetchImpl };
}

const connected = () => connectionFor({ status: 'connected', realm: CONNECTED_REALM });
const status = () => screen.getByTestId('runtime-connection-status');

function onWindows() {
  vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36');
}

describe('RuntimeConnectionPill', () => {
  it('connected: shows nothing, and says "Connected to Astrid" to a screen reader only', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    expect(status()).toHaveAttribute('data-state', 'connected');
    expect(status()).toHaveClass('sr-only');
    expect(status()).toHaveTextContent('Connected to Astrid');
    expect(screen.queryByText(/Direct Journey/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Connected ·/)).not.toBeInTheDocument();
    await waitFor(() => expect(fetchImpl.mock.calls.length).toBeGreaterThanOrEqual(3));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'connected');
    expect(String(fetchImpl.mock.calls[0][0])).toMatch(/\/api\/runtime\/v1\/health$/);
    expect(isRecoveryCardShowing()).toBe(false);
  });

  it('restarted on a new instance: one card with Reload, bottom-right with a gutter, and nothing else', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), healthy('instance-2'));
    const onReload = vi.fn();
    render(<RuntimeConnectionPill connection={connected()} onReload={onReload} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    expect(screen.getByRole('heading', { name: 'Astrid restarted' })).toBeInTheDocument();
    expect(screen.getByText('Reload to carry on. Your changes are kept.')).toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'restarted');
    expect(screen.queryByText('Reload needed')).not.toBeInTheDocument();
    expect(screen.queryByRole('img')).not.toBeInTheDocument();
    const card = screen.getByRole('alert');
    expect(card).toHaveClass('fixed', 'right-4', 'bottom-20', 'sm:bottom-4', 'w-[calc(100%-2rem)]', 'max-w-sm', 'rounded-2xl', 'p-5');
    expect(card).not.toHaveClass('left-0');
    expect(screen.getByRole('heading')).toHaveClass('font-serif', 'text-base');
    expect(screen.getByText(COPY.restarted.sentence)).toHaveClass('text-sm', 'text-muted-foreground');
    expect(isRecoveryCardShowing()).toBe(true);

    fireEvent.click(screen.getByRole('button', { name: 'Reload' }));
    expect(onReload).toHaveBeenCalledOnce();
  });

  it('another identity behind the door after connecting is the same restart card, not a second message', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), json({ error: 'runtime_identity_mismatch' }, 503));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid restarted' })).toBeInTheDocument());
    expect(screen.getAllByRole('heading')).toHaveLength(1);
    expect(screen.getByText(COPY.restarted.sentence)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Reload' })).toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'restarted');
  });

  it('Astrid down for two readings in a row: the "Astrid stopped" card with the install line, and no Connected', async () => {
    const writeText = vi.fn(async (_text: string) => undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = unreachable;

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
    expect(screen.getByText('Give these instructions to your coding agent to start Astrid again. Your changes are kept.')).toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'stopped');
    expect(status()).not.toHaveTextContent('Connected');
    expect(screen.getByRole('alert')).toHaveClass('fixed', 'right-4', 'bottom-20', 'sm:bottom-4');
    expect(isRecoveryCardShowing()).toBe(true);

      fireEvent.click(screen.getByRole('button', { name: COPY.agent.commandCopy }));
    await waitFor(() => expect(writeText).toHaveBeenCalledOnce());
    expect(String(writeText.mock.calls[0][0])).toMatch(/^curl -fsSL https:\/\/astrid\.haus\/install \| sh$/);
  });

  it('names PowerShell on the stopped card on Windows', async () => {
    onWindows();
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = unreachable;

    await waitFor(() => expect(screen.getByText('Or run this command yourself in PowerShell:')).toBeInTheDocument());
  });

  it('one dropped reading is not a stop', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), unreachable, healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(fetchImpl.mock.calls.length).toBeGreaterThanOrEqual(6));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'connected');
  });

  it('the stopped card clears by itself when the same Astrid answers again', async () => {
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = unreachable;

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
    route.answer = healthy('instance-1');
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
    expect(status()).toHaveAttribute('data-state', 'connected');
    expect(isRecoveryCardShowing()).toBe(false);
  });

  it('a new Astrid answering after the stop turns the stopped card into the restart card', async () => {
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = unreachable;
    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
    route.answer = healthy('instance-2');

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid restarted' })).toBeInTheDocument());
    expect(screen.queryByRole('heading', { name: 'Astrid stopped' })).not.toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'restarted');
  });

  it('the gateway answers 503 but the engine is down: two readings in a row show the "Astrid stopped" card', async () => {
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = json({ error: 'runtime_unavailable' }, 503);

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
    expect(status()).toHaveAttribute('data-state', 'stopped');
    expect(isRecoveryCardShowing()).toBe(true);
    expect(document.body.textContent).not.toMatch(/Runtime|workspace|realm|gateway|127\.0\.0\.1|npm run/);

    route.answer = healthy('instance-1');
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
    expect(isRecoveryCardShowing()).toBe(false);
  });

  it('any other answer that is not ok (a 500, a 404) counts as a failed reading too', async () => {
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = json({ error: 'boom' }, 500);

    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
  });

  it('one 503 between good readings is not a stop', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), json({ error: 'runtime_unavailable' }, 503), healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(fetchImpl.mock.calls.length).toBeGreaterThanOrEqual(6));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(status()).toHaveAttribute('data-state', 'connected');
  });

  it('re-checks on focus as well as on the interval', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={60_000} />);

    await waitFor(() => expect(fetchImpl).toHaveBeenCalledTimes(1));
    // Let the first check settle, so the focus check is not skipped as still in flight.
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(fetchImpl).toHaveBeenCalledTimes(2));
  });

  it('the cards say Astrid and never name a Runtime, workspace, realm or command', async () => {
    const { route, fetchImpl } = switchableRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(fetchImpl).toHaveBeenCalled());
    route.answer = unreachable;
    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid stopped' })).toBeInTheDocument());
    expect(document.body.textContent).not.toMatch(/Runtime|workspace|realm|gateway|127\.0\.0\.1|npm run/);
    route.answer = healthy('instance-2');
    await waitFor(() => expect(screen.getByRole('heading', { name: 'Astrid restarted' })).toBeInTheDocument());
    expect(document.body.textContent).not.toMatch(/Runtime|workspace|realm|gateway|127\.0\.0\.1|npm run/);
  });

  it('renders nothing while not connected, and asks Astrid nothing', () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    const { container } = render(
      <RuntimeConnectionPill connection={connectionFor({ status: 'not_running' })} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />,
    );
    expect(container).toBeEmptyDOMElement();
    expect(fetchImpl).not.toHaveBeenCalled();
  });

  it('lets the editor go back to its own messages once the card is gone', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), healthy('instance-2'));
    const view = render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);
    await waitFor(() => expect(isRecoveryCardShowing()).toBe(true));
    view.unmount();
    expect(isRecoveryCardShowing()).toBe(false);
  });
});
