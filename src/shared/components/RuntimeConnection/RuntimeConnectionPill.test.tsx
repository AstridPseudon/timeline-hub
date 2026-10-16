// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
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

/** Answers the health route in order; the last answer repeats. Counts every call. */
function healthRoute(...answers: Array<() => Response>) {
  let index = 0;
  return vi.fn(async (_input: string, _init?: RequestInit) => {
    const answer = answers[Math.min(index, answers.length - 1)];
    index += 1;
    return answer();
  });
}

const connected = () => connectionFor({ status: 'connected', realm: CONNECTED_REALM });

describe('RuntimeConnectionPill', () => {
  it('connected: names the realm, and no restart message while the instance stays the same', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    const pill = screen.getByTestId('runtime-connection-status');
    expect(pill).toHaveAttribute('data-state', 'connected');
    expect(pill).toHaveTextContent('Connected · Direct Journey');
    await waitFor(() => expect(fetchImpl.mock.calls.length).toBeGreaterThanOrEqual(3));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(String(fetchImpl.mock.calls[0][0])).toMatch(/\/api\/runtime\/v1\/health$/);
  });

  it('restarted on a new instance: the restart message with Reload, and the draft stays on the page', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), healthy('instance-2'));
    const onReload = vi.fn();
    render(<RuntimeConnectionPill connection={connected()} onReload={onReload} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    expect(screen.getByRole('heading', { name: COPY.restarted.title })).toBeInTheDocument();
    expect(screen.getByText(COPY.restarted.sentence)).toBeInTheDocument();
    expect(screen.getByTestId('runtime-connection-status')).toHaveAttribute('data-state', 'restarted');
    expect(screen.getByText('Reload needed')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: COPY.restarted.reload }));
    expect(onReload).toHaveBeenCalledOnce();
  });

  it('a different realm: the realm-changed message, not the restart one', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), json({ error: 'realm_changed' }, 503));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(screen.getByRole('heading', { name: COPY.restarted.realmChanged.title })).toBeInTheDocument());
    expect(screen.getByText(COPY.restarted.realmChanged.sentence)).toBeInTheDocument();
    expect(screen.queryByText(COPY.restarted.sentence)).not.toBeInTheDocument();
  });

  it('the Runtime briefly down (a 503 that is not a realm change) is not a restart', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'), json({ error: 'runtime_unavailable' }, 503));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />);

    await waitFor(() => expect(fetchImpl.mock.calls.length).toBeGreaterThanOrEqual(4));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(screen.getByTestId('runtime-connection-status')).toHaveAttribute('data-state', 'connected');
  });

  it('re-checks on focus as well as on the interval', async () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    render(<RuntimeConnectionPill connection={connected()} fetchImpl={fetchImpl} restartCheckIntervalMs={60_000} />);

    await waitFor(() => expect(fetchImpl).toHaveBeenCalledTimes(1));
    // Let the first check settle, so the focus check is not skipped as still in flight.
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(fetchImpl).toHaveBeenCalledTimes(2));
  });

  it('renders nothing while not connected, and asks the Runtime nothing', () => {
    const fetchImpl = healthRoute(healthy('instance-1'));
    const { container } = render(
      <RuntimeConnectionPill connection={connectionFor({ status: 'cant_reach', firstTime: false })} fetchImpl={fetchImpl} restartCheckIntervalMs={5} />,
    );
    expect(container).toBeEmptyDOMElement();
    expect(fetchImpl).not.toHaveBeenCalled();
  });
});
