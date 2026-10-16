// @vitest-environment jsdom
import React from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  RuntimeConnectionGate,
  RuntimeConnectionProvider,
  useRuntimeConnection,
  type RuntimeConnectionValue,
} from './RuntimeConnectionProvider.tsx';
import type { PermissionsLike } from './localNetworkPermission.ts';

const REALM = { realm_id: 'realm-1', display_name: 'Direct Journey' };
const STORAGE_KEY = 'reigh.runtime.connectedBefore';

type Route = () => Response | Promise<Response>;

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
}

/** A fetch whose answers can be swapped between probes; records every URL it was asked for. */
function fakeGateway() {
  const calls: string[] = [];
  const routes: Record<string, Route> = {
    '/v1/health': () => json({ status: 'ok', protocol: 'workspace.v1' }),
    '/v1/realm': () => json(REALM),
  };
  const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    calls.push(url);
    const path = Object.keys(routes).find((candidate) => url.endsWith(candidate));
    if (!path) throw new Error(`unexpected request ${url}`);
    return routes[path]!();
  }) as unknown as typeof fetch;
  const down = () => {
    routes['/v1/health'] = () => {
      throw new TypeError('Failed to fetch');
    };
  };
  const up = () => {
    routes['/v1/health'] = () => json({ status: 'ok', protocol: 'workspace.v1' });
  };
  const unavailable = (error: string) => {
    routes['/v1/health'] = () => json({ error }, 503);
  };
  return { calls, fetchImpl, routes, down, up, unavailable };
}

function fakePermissions(initial: string) {
  const status: { state: string; onchange: ((this: unknown, event: Event) => unknown) | null } = { state: initial, onchange: null };
  const permissions: PermissionsLike = { query: vi.fn(async () => status) };
  return {
    permissions,
    status,
    change(next: string) {
      status.state = next;
      status.onchange?.call(status, new Event('change'));
    },
  };
}

let latest: RuntimeConnectionValue;
function Probe() {
  latest = useRuntimeConnection();
  return <span data-testid="status">{latest.state.status}</span>;
}

function renderProvider(
  gateway: ReturnType<typeof fakeGateway>,
  permissions: PermissionsLike | undefined,
  props: Partial<React.ComponentProps<typeof RuntimeConnectionProvider>> = {},
) {
  return render(
    <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={permissions} pollIntervalMs={10} {...props}>
      <Probe />
    </RuntimeConnectionProvider>,
  );
}

const status = () => screen.getByTestId('status').textContent;

beforeEach(() => {
  window.localStorage.clear();
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.resetModules();
});

describe('granted', () => {
  it('probes health then realm at once and connects, exposing the realm name', async () => {
    const gateway = fakeGateway();
    const onConnected = vi.fn();
    renderProvider(gateway, fakePermissions('granted').permissions, { onConnected });

    await waitFor(() => expect(status()).toBe('connected'));
    expect(latest.state).toEqual({ status: 'connected', realm: REALM });
    expect(latest.realmName).toBe('Direct Journey');
    expect(latest.isBooting).toBe(false);
    expect(gateway.calls.map((url) => url.replace(/^.*\/api\/runtime/, ''))).toEqual(['/v1/health', '/v1/realm']);
    expect(onConnected).toHaveBeenCalledTimes(1);
    expect(window.localStorage.getItem(STORAGE_KEY)).toBe('1');
  });

  it('is booting, not cant_reach, until the first probe has answered', async () => {
    const gateway = fakeGateway();
    let release: (response: Response) => void = () => {};
    gateway.routes['/v1/health'] = () => new Promise<Response>((resolve) => { release = resolve; });
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(gateway.calls).toHaveLength(1));
    expect(latest.isBooting).toBe(true);
    expect(status()).toBe('connecting');
    release(json({ status: 'ok' }));
    await waitFor(() => expect(status()).toBe('connected'));
  });

  it('a network error is cant_reach, first-time without the connected-before flag', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(status()).toBe('cant_reach'));
    expect(latest.state).toEqual({ status: 'cant_reach', firstTime: true });
    expect(latest.isBooting).toBe(false);
  });

  it('a network error is cant_reach for a returning visitor when the flag is set', async () => {
    window.localStorage.setItem(STORAGE_KEY, '1');
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(status()).toBe('cant_reach'));
    expect(latest.state).toEqual({ status: 'cant_reach', firstTime: false });
  });

  it.each([
    ['runtime_unavailable', 'runtime_stopped'],
    ['realm_changed', 'realm_changed'],
    ['runtime_discovery_invalid', 'runtime_stopped'],
    ['runtime_identity_mismatch', 'identity_mismatch'],
    ['a_code_the_page_has_never_heard_of', 'unknown'],
  ])('a 503 %s (the gateway\'s real codes, scripts/reigh-loopback-gateway.ts) is not_ready with reason %s', async (code, reason) => {
    const gateway = fakeGateway();
    gateway.unavailable(code);
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(status()).toBe('not_ready'));
    expect(latest.state).toEqual({ status: 'not_ready', reason });
  });

  it('a 503 with no readable body is not_ready with reason unknown, never "starting"', async () => {
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => new Response('<html></html>', { status: 503 });
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(status()).toBe('not_ready'));
    expect(latest.state).toEqual({ status: 'not_ready', reason: 'unknown' });
  });

  it('an answer that is not a Reigh gateway (wrong status or body) is cant_reach', async () => {
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => json({ error: 'hosted_origin_required' }, 403);
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('cant_reach'));

    const other = fakeGateway();
    other.routes['/v1/health'] = () => new Response('<html></html>', { status: 200 });
    renderProvider(other, fakePermissions('granted').permissions);
    await waitFor(() => expect(screen.getAllByTestId('status').every((node) => node.textContent === 'cant_reach')).toBe(true));
  });

  it('recovers by the interval, with no reload, and stops probing once connected', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('cant_reach'));

    gateway.up();
    await waitFor(() => expect(status()).toBe('connected'));
    const settled = gateway.calls.length;
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 60)); });
    expect(gateway.calls).toHaveLength(settled);
  });

  it('recovers on window focus when the interval is far away', async () => {
    const gateway = fakeGateway();
    gateway.unavailable('runtime_unavailable');
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(status()).toBe('not_ready'));

    gateway.up();
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(status()).toBe('connected'));
  });
});

describe('app entry preference', () => {
  const PREFERENCE_KEY = 'astrid:prefers-app';

  it('is remembered once the gate connects, so the next visit to the bare domain goes straight in', async () => {
    const gateway = fakeGateway();
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('connected'));
    expect(window.localStorage.getItem(PREFERENCE_KEY)).toBe('1');
  });

  it('is not remembered while the Runtime cannot be reached, or before Connect is pressed', async () => {
    const gateway = fakeGateway();
    gateway.down();
    const { unmount } = renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('cant_reach'));
    expect(window.localStorage.getItem(PREFERENCE_KEY)).toBeNull();
    unmount();

    renderProvider(fakeGateway(), fakePermissions('prompt').permissions);
    await waitFor(() => expect(latest.awaitingConnect).toBe(true));
    expect(window.localStorage.getItem(PREFERENCE_KEY)).toBeNull();
  });

  it('is not set by a same-origin build, which has no gate', async () => {
    const { RuntimeConnectionProvider: Provider } = await import('./RuntimeConnectionProvider.tsx');
    render(<Provider permissions={{ query: vi.fn() }}><div /></Provider>);
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 20)); });
    expect(window.localStorage.getItem(PREFERENCE_KEY)).toBeNull();
  });

  it('still connects when storage refuses the write', async () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    renderProvider(fakeGateway(), fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('connected'));
  });
});

describe('prompt', () => {
  it('sends nothing until connect(), then connects', async () => {
    const gateway = fakeGateway();
    renderProvider(gateway, fakePermissions('prompt').permissions);

    await waitFor(() => expect(latest.isBooting).toBe(false));
    expect(latest.awaitingConnect).toBe(true);
    expect(latest.state).toEqual({ status: 'cant_reach', firstTime: true });
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 50)); });
    window.dispatchEvent(new Event('focus'));
    expect(gateway.fetchImpl).not.toHaveBeenCalled();

    act(() => latest.connect());
    await waitFor(() => expect(status()).toBe('connected'));
    expect(latest.awaitingConnect).toBe(false);
  });

  it('shows connecting while the browser prompt is open, and ignores a second connect()', async () => {
    const gateway = fakeGateway();
    let release: (response: Response) => void = () => {};
    gateway.routes['/v1/health'] = () => new Promise<Response>((resolve) => { release = resolve; });
    renderProvider(gateway, fakePermissions('prompt').permissions);
    await waitFor(() => expect(latest.isBooting).toBe(false));

    act(() => latest.connect());
    await waitFor(() => expect(status()).toBe('connecting'));
    expect(latest.isBooting).toBe(false);
    expect(latest.isChecking).toBe(true);
    act(() => latest.connect());
    expect(gateway.fetchImpl).toHaveBeenCalledTimes(1);

    release(json({ status: 'ok' }));
    await waitFor(() => expect(status()).toBe('connected'));
  });

  it('connect() with nothing listening stays on the first-time panel and keeps offering Connect', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('prompt').permissions);
    await waitFor(() => expect(latest.isBooting).toBe(false));

    act(() => latest.connect());
    await waitFor(() => expect(latest.isChecking).toBe(false));
    expect(latest.state).toEqual({ status: 'cant_reach', firstTime: true });
    expect(latest.awaitingConnect).toBe(true);
  });

  it('the browser granting the permission starts probing without a click', async () => {
    const gateway = fakeGateway();
    const permission = fakePermissions('prompt');
    renderProvider(gateway, permission.permissions);
    await waitFor(() => expect(latest.awaitingConnect).toBe(true));
    expect(gateway.fetchImpl).not.toHaveBeenCalled();

    act(() => permission.change('granted'));
    await waitFor(() => expect(status()).toBe('connected'));
  });

  it('a grant while the Connect probe is pending under the prompt aborts it and probes again, then connects', async () => {
    const gateway = fakeGateway();
    const permission = fakePermissions('prompt');
    let attempts = 0;
    const signals: (AbortSignal | undefined)[] = [];
    // The first health request is the one Chrome holds open behind its prompt: it settles only when aborted.
    gateway.routes['/v1/health'] = () => json({ status: 'ok', protocol: 'workspace.v1' });
    const base = gateway.fetchImpl;
    const fetchImpl = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      signals.push(init?.signal ?? undefined);
      if (String(input).endsWith('/v1/health') && attempts++ === 0) {
        return new Promise<Response>((_resolve, reject) => {
          init?.signal?.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')));
        });
      }
      return (base as unknown as (i: RequestInfo | URL) => Promise<Response>)(input);
    }) as unknown as typeof fetch;
    renderProvider({ ...gateway, fetchImpl }, permission.permissions);
    await waitFor(() => expect(latest.awaitingConnect).toBe(true));

    act(() => latest.connect());
    await waitFor(() => expect(status()).toBe('connecting'));
    expect(fetchImpl).toHaveBeenCalledTimes(1);

    act(() => permission.change('granted'));
    await waitFor(() => expect(status()).toBe('connected'));
    expect(signals[0]?.aborted).toBe(true);
    expect(latest.state).toEqual({ status: 'connected', realm: REALM });
  });

  it('a Permissions API that throws counts as prompt: nothing is sent', async () => {
    const gateway = fakeGateway();
    const throwing: PermissionsLike = { query: vi.fn(async () => { throw new TypeError('unknown permission name'); }) };
    renderProvider(gateway, throwing);

    await waitFor(() => expect(latest.isBooting).toBe(false));
    expect(latest.awaitingConnect).toBe(true);
    expect(gateway.fetchImpl).not.toHaveBeenCalled();
  });

  it('a refusal during connect() is read from the permission: denied becomes blocked', async () => {
    const gateway = fakeGateway();
    gateway.down();
    const permission = fakePermissions('prompt');
    renderProvider(gateway, permission.permissions);
    await waitFor(() => expect(latest.isBooting).toBe(false));

    permission.status.state = 'denied'; // the browser's answer, before it reports a change
    act(() => latest.connect());
    await waitFor(() => expect(status()).toBe('blocked'));
  });
});

describe('denied', () => {
  it('is blocked and sends nothing, and connect() does nothing', async () => {
    const gateway = fakeGateway();
    renderProvider(gateway, fakePermissions('denied').permissions);

    await waitFor(() => expect(status()).toBe('blocked'));
    expect(latest.awaitingConnect).toBe(false);
    act(() => latest.connect());
    window.dispatchEvent(new Event('focus'));
    expect(gateway.fetchImpl).not.toHaveBeenCalled();
  });

  it('allowing it in site settings connects without a reload', async () => {
    const gateway = fakeGateway();
    const permission = fakePermissions('denied');
    renderProvider(gateway, permission.permissions);
    await waitFor(() => expect(status()).toBe('blocked'));

    act(() => permission.change('granted'));
    await waitFor(() => expect(status()).toBe('connected'));
  });
});

describe('storage', () => {
  it('still renders, connects and stays first-time when localStorage throws', async () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('blocked'); });
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('cant_reach'));
    expect(latest.state).toEqual({ status: 'cant_reach', firstTime: true });

    gateway.up();
    await waitFor(() => expect(status()).toBe('connected'));
  });
});

describe('gate', () => {
  it('mounts nothing below it, so no Runtime query can run, until connected', async () => {
    const gateway = fakeGateway();
    gateway.down();
    const mounted = vi.fn();
    function RuntimeQueryOwner() {
      React.useEffect(mounted, []);
      return <div data-testid="app" />;
    }
    render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={fakePermissions('granted').permissions} pollIntervalMs={10}>
        <RuntimeConnectionGate>
          <RuntimeQueryOwner />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );

    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'cant_reach'));
    expect(screen.queryByTestId('app')).toBeNull();
    expect(mounted).not.toHaveBeenCalled();

    gateway.up();
    await waitFor(() => expect(screen.getByTestId('app')).toBeInTheDocument());
    expect(screen.queryByTestId('runtime-not-connected')).toBeNull();
  });

  it('the placeholder panel shows the state name and nothing else', async () => {
    const gateway = fakeGateway();
    gateway.unavailable('runtime_unavailable');
    render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={fakePermissions('granted').permissions} pollIntervalMs={600_000}>
        <RuntimeConnectionGate>
          <div data-testid="app" />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );
    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveTextContent(/^not_ready$/));
  });

  it('takes a panel and a pill as render props', async () => {
    const gateway = fakeGateway();
    gateway.down();
    render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={fakePermissions('granted').permissions} pollIntervalMs={10}>
        <RuntimeConnectionGate
          panel={({ state }) => <p data-testid="custom-panel">{state.status}</p>}
          pill={({ realmName }) => <p data-testid="custom-pill">{realmName}</p>}
        >
          <div data-testid="app" />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );
    await waitFor(() => expect(screen.getByTestId('custom-panel')).toHaveTextContent('cant_reach'));
    expect(screen.queryByTestId('custom-pill')).toBeNull();

    gateway.up();
    await waitFor(() => expect(screen.getByTestId('custom-pill')).toHaveTextContent('Direct Journey'));
    expect(screen.getByTestId('app')).toBeInTheDocument();
    expect(screen.queryByTestId('custom-panel')).toBeNull();
  });
});

describe('same-origin build', () => {
  it('is not gated: children render at once and nothing is probed', async () => {
    const fetchSpy = vi.fn();
    vi.stubGlobal('fetch', fetchSpy);
    const permissionsQuery = vi.fn();
    const { RuntimeConnectionGate: Gate, RuntimeConnectionProvider: Provider } = await import('./RuntimeConnectionProvider.tsx');
    render(
      <Provider permissions={{ query: permissionsQuery }}>
        <Gate>
          <div data-testid="app" />
        </Gate>
      </Provider>,
    );

    expect(screen.getByTestId('app')).toBeInTheDocument();
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 20)); });
    expect(fetchSpy).not.toHaveBeenCalled();
    expect(permissionsQuery).not.toHaveBeenCalled();
    vi.unstubAllGlobals();
  });

  it('is gated once a Runtime origin is configured, and probes that origin', async () => {
    const connection = await import('./connection.ts');
    connection.setRuntimeOrigin({ VITE_RUNTIME_ORIGIN: 'http://127.0.0.1:17340' });
    // The module was reloaded, so the hook must come from the same copy as the provider.
    const { RuntimeConnectionProvider: Provider, useRuntimeConnection: useFresh } = await import('./RuntimeConnectionProvider.tsx');
    function FreshProbe() {
      latest = useFresh();
      return <span data-testid="status">{latest.state.status}</span>;
    }
    const gateway = fakeGateway();
    render(
      <Provider fetchImpl={gateway.fetchImpl} permissions={fakePermissions('granted').permissions} pollIntervalMs={10}>
        <FreshProbe />
      </Provider>,
    );

    await waitFor(() => expect(status()).toBe('connected'));
    expect(latest.gated).toBe(true);
    expect(gateway.calls[0]).toBe('http://127.0.0.1:17340/api/runtime/v1/health');
  });
});

describe('useRuntimeConnection', () => {
  it('throws outside its provider', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => render(<Probe />)).toThrow('useRuntimeConnection must be used within a RuntimeConnectionProvider');
  });
});
