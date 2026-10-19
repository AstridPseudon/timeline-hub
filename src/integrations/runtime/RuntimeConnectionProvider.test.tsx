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
import { autoConnectRequested, requestAutoConnect } from './autoConnectRequest.ts';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx';
import { RUNTIME_SCHEMA_DIGEST } from './contract-metadata.ts';

const REALM = { realm_id: 'realm-1', display_name: 'Direct Journey' };
const STORAGE_KEY = 'astrid.runtime.connectedBefore';

type Route = () => Response | Promise<Response>;

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
}

/** A fetch whose answers can be swapped between probes; records every URL it was asked for. */
function fakeGateway() {
  const calls: string[] = [];
  const routes: Record<string, Route> = {
    '/v1/health': () => json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST }),
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
    routes['/v1/health'] = () => json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
  };
  const gatewayDown = (error: string, status = 503) => {
    routes['/v1/health'] = () => json({ error }, status);
  };
  return { calls, fetchImpl, routes, down, up, gatewayDown };
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

class MemoryStorage {
  private values = new Map<string, string>();
  getItem(key: string) { return this.values.get(key) ?? null; }
  setItem(key: string, value: string) { this.values.set(key, String(value)); }
  removeItem(key: string) { this.values.delete(key); }
  clear() { this.values.clear(); }
}

beforeEach(() => {
  Object.defineProperty(window, 'localStorage', { configurable: true, value: new MemoryStorage() });
  Object.defineProperty(window, 'sessionStorage', { configurable: true, value: new MemoryStorage() });
  vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue(
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  );
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
    expect(latest.schemaDigest).toBe(RUNTIME_SCHEMA_DIGEST);
    expect(latest.isBooting).toBe(false);
    expect(gateway.calls.map((url) => url.replace(/^.*\/api\/runtime/, ''))).toEqual(['/v1/health', '/v1/realm']);
    expect(onConnected).toHaveBeenCalledTimes(1);
    expect(window.localStorage.getItem(STORAGE_KEY)).toBe('1');
  });

  it.each([
    ['unknown', 'sha256:unknown'],
    ['missing', undefined],
  ])('shows update_needed for a %s health digest', async (_name, digest) => {
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => json({ status: 'ok', ...(digest === undefined ? {} : { schema_digest: digest }) });
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('update_needed'));
    expect(gateway.calls.map((url) => url.replace(/^.*\/api\/runtime/, ''))).toEqual(['/v1/health']);
  });

  it.each(['focus', 'interval'] as const)('a %s re-check between the probe answering and the connected render starts no second probe', async (trigger) => {
    const gateway = fakeGateway();
    // Plain stub answers: their json() settles in microtasks only, so the test controls exactly where the probe resumes.
    const answer = (body: unknown) => ({ ok: true, status: 200, json: async () => body }) as unknown as Response;
    let releaseRealm: (response: Response) => void = () => {};
    gateway.routes['/v1/health'] = () => answer({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
    gateway.routes['/v1/realm'] = () => new Promise<Response>((resolve) => { releaseRealm = resolve; });
    // Capture the provider's own poll (recognised by its distinctive period) so the test can fire it by hand.
    const POLL_MS = 123_456;
    let tick: () => void = () => {};
    const realSetInterval = window.setInterval.bind(window);
    vi.spyOn(window, 'setInterval').mockImplementation(((handler: TimerHandler, ms?: number, ...args: unknown[]) => {
      if (ms !== POLL_MS) return realSetInterval(handler, ms, ...args);
      tick = () => (handler as () => void)();
      return realSetInterval(() => {}, ms);
    }) as typeof window.setInterval);
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: POLL_MS });
    await waitFor(() => expect(gateway.calls).toHaveLength(2));

    // The probe answers. Only microtasks run, so the probe has resumed (and cleared its in-flight guard) while React has
    // not yet rendered the connected outcome, which is the window a slow machine leaves open.
    releaseRealm(answer(REALM));
    for (let i = 0; i < 50; i += 1) await Promise.resolve();
    if (trigger === 'focus') window.dispatchEvent(new Event('focus'));
    else tick();

    await waitFor(() => expect(status()).toBe('connected'));
    expect(gateway.calls.map((url) => url.replace(/^.*\/api\/runtime/, ''))).toEqual(['/v1/health', '/v1/realm']);
  });

  it('fresh profile stays connecting after one silent reading, then two show setup', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    expect(status()).toBe('connecting');
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(status()).toBe('set_up'));
    expect(latest.state).toEqual({ status: 'set_up' });
    expect(latest.isBooting).toBe(false);
  });

  it('keeps the permission prompt for any browser that supports the local-network permission', async () => {
    vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 Firefox/153.0');
    const gateway = fakeGateway();
    const permissions = fakePermissions('prompt');
    renderProvider(gateway, permissions.permissions);
    await waitFor(() => expect(latest.awaitingConnect).toBe(true));
    expect(permissions.permissions.query).toHaveBeenCalled();
    expect(gateway.fetchImpl).not.toHaveBeenCalled();
  });

  it('background polls do not change the rendered panel while a reading is pending', async () => {
    const gateway = fakeGateway();
    gateway.down();
    const permissions = fakePermissions('granted');
    const view = render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={permissions.permissions} pollIntervalMs={10}>
        <RuntimeConnectionGate panel={(connection) => <RuntimeConnectionPanel connection={connection} />}>
          <div data-testid="app" />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );

    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'set_up'));
    const panel = screen.getByTestId('runtime-not-connected');
    const rendered = panel.innerHTML;
    let release: (response: Response) => void = () => {};
    gateway.routes['/v1/health'] = () => new Promise<Response>((resolve) => { release = resolve; });
    const callsAtVerdict = gateway.calls.length;
    await waitFor(() => expect(gateway.calls.length).toBeGreaterThan(callsAtVerdict));
    expect(panel.innerHTML).toBe(rendered);
    expect(screen.queryByText('Looking for Astrid on this computer…')).not.toBeInTheDocument();
    release(new Response('<html></html>', { status: 200 }));
    await waitFor(() => expect(gateway.calls.length).toBeGreaterThan(callsAtVerdict + 1));
    expect(panel.innerHTML).toBe(rendered);
    view.unmount();
  });

  it('connectedBefore: two silent readings show not_running', async () => {
    window.localStorage.setItem(STORAGE_KEY, '1');
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    expect(status()).toBe('connecting');
    await act(async () => { window.dispatchEvent(new Event('focus')); });

    await waitFor(() => expect(status()).toBe('not_running'));
    expect(latest.state).toEqual({ status: 'not_running' });
  });

  it.each([503, 502])('gateway down body at HTTP %i establishes Astrid is installed', async (httpStatus) => {
    const gateway = fakeGateway();
    gateway.gatewayDown('runtime_unavailable', httpStatus);
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('not_running'));
    expect(latest.state).toEqual({ status: 'not_running' });
  });

  it('remembers any gateway down reading even when the second reading is silent', async () => {
    const gateway = fakeGateway();
    gateway.gatewayDown('runtime_unavailable');
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    expect(status()).toBe('connecting');

    gateway.down();
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(status()).toBe('not_running'));
    expect(latest.state).toEqual({ status: 'not_running' });
  });

  it('shows runtime_identity_mismatch as restart_needed immediately', async () => {
    const code = 'runtime_identity_mismatch';
    const gateway = fakeGateway();
    gateway.gatewayDown(code);
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(status()).toBe('restart_needed'));
    expect(latest.state).toEqual({ status: 'restart_needed' });
  });

  it('a 503 with no readable body remains a transient check, not a stopped verdict', async () => {
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => new Response('<html></html>', { status: 503 });
    renderProvider(gateway, fakePermissions('granted').permissions);

    await waitFor(() => expect(status()).toBe('set_up'));
    expect(latest.state).toEqual({ status: 'set_up' });
  });

  it('a foreign Not found error stays silent, so two readings still show setup', async () => {
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => json({ error: 'Not found' }, 404);
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    expect(status()).toBe('connecting');
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(status()).toBe('set_up'));
    expect(latest.state).toEqual({ status: 'set_up' });
  });

  it('recovers by the interval, with no reload, and stops probing once connected', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('set_up'));

    gateway.up();
    await waitFor(() => expect(status()).toBe('connected'));
    const settled = gateway.calls.length;
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 60)); });
    expect(gateway.calls).toHaveLength(settled);
  });

  it('recovers on window focus when the interval is far away', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions, { pollIntervalMs: 600_000 });
    await waitFor(() => expect(gateway.fetchImpl).toHaveBeenCalledTimes(1));
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(status()).toBe('set_up'));

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

  it('is not remembered while Astrid is absent, or before Connect is pressed', async () => {
    const gateway = fakeGateway();
    gateway.down();
    const { unmount } = renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('set_up'));
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
    vi.spyOn(Object.getPrototypeOf(window.localStorage), 'setItem').mockImplementation(() => { throw new Error('blocked'); });
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
    expect(latest.state).toEqual({ status: 'connecting' });
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

    release(json({ status: 'ok', schema_digest: RUNTIME_SCHEMA_DIGEST }));
    await waitFor(() => expect(status()).toBe('connected'));
  });

  it('connect() with nothing listening stays on the first-time panel and keeps offering Connect', async () => {
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('prompt').permissions);
    await waitFor(() => expect(latest.isBooting).toBe(false));

    act(() => latest.connect());
    await waitFor(() => expect(latest.isChecking).toBe(false));
    expect(latest.state).toEqual({ status: 'connecting' });
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
    gateway.routes['/v1/health'] = () => json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
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

  it('an unsupported local-network permission query counts as granted and probes directly', async () => {
    const gateway = fakeGateway();
    const throwing: PermissionsLike = { query: vi.fn(async () => { throw new TypeError('unknown permission name'); }) };
    renderProvider(gateway, throwing);

    await waitFor(() => expect(status()).toBe('connected'));
    expect(latest.awaitingConnect).toBe(false);
    expect(gateway.fetchImpl).toHaveBeenCalled();
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
    vi.spyOn(Object.getPrototypeOf(window.localStorage), 'getItem').mockImplementation(() => { throw new Error('blocked'); });
    vi.spyOn(Object.getPrototypeOf(window.localStorage), 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    const gateway = fakeGateway();
    gateway.down();
    renderProvider(gateway, fakePermissions('granted').permissions);
    await waitFor(() => expect(status()).toBe('set_up'));
    expect(latest.state).toEqual({ status: 'set_up' });

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

    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'set_up'));
    expect(screen.queryByTestId('app')).toBeNull();
    expect(mounted).not.toHaveBeenCalled();

    gateway.up();
    await waitFor(() => expect(screen.getByTestId('app')).toBeInTheDocument());
    expect(screen.queryByTestId('runtime-not-connected')).toBeNull();
  });

  it('the placeholder panel shows the state name and nothing else', async () => {
    const gateway = fakeGateway();
    gateway.down();
    render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={fakePermissions('granted').permissions} pollIntervalMs={10}>
        <RuntimeConnectionGate>
          <div data-testid="app" />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );
    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveTextContent(/^set_up$/));
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
    await waitFor(() => expect(screen.getByTestId('custom-panel')).toHaveTextContent('set_up'));
    expect(screen.queryByTestId('custom-pill')).toBeNull();

    gateway.up();
    await waitFor(() => expect(screen.getByTestId('custom-pill')).toHaveTextContent('Direct Journey'));
    expect(screen.getByTestId('app')).toBeInTheDocument();
    expect(screen.queryByTestId('custom-panel')).toBeNull();
  });
});

describe('gate: the landing page already asked to go in', () => {
  /** A panel that shows the state the gate hands it, so the test sees explainer versus Chrome's prompt. */
  const panel = ({ awaitingConnect, isChecking, connect }: RuntimeConnectionValue) => (
    awaitingConnect && !isChecking
      ? <button type="button" data-testid="explainer" onClick={connect}>Connect</button>
      : <p data-testid="panel-state">{awaitingConnect ? 'pending' : 'other'}</p>
  );
  const renderGate = (gateway: ReturnType<typeof fakeGateway>, permission: string) => render(
    <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={fakePermissions(permission).permissions} pollIntervalMs={10}>
      <RuntimeConnectionGate panel={panel}>
        <div data-testid="app" />
      </RuntimeConnectionGate>
    </RuntimeConnectionProvider>,
  );

  it('connects at once with the flag set and the permission still to be asked, and never shows the explainer', async () => {
    requestAutoConnect();
    const gateway = fakeGateway();
    renderGate(gateway, 'prompt');

    await waitFor(() => expect(screen.getByTestId('app')).toBeInTheDocument());
    expect(screen.queryByTestId('explainer')).toBeNull();
    expect(gateway.fetchImpl).toHaveBeenCalled();
    // One-shot: the flag is used up.
    expect(autoConnectRequested()).toBe(false);
  });

  it('consumes ?connect=1 once, preserves other URL parts, and immediately asks for permission', async () => {
    window.history.replaceState({}, '', '/tools/video-editor?timeline=timeline-7&connect=1#frame-42');
    const gateway = fakeGateway();
    renderGate(gateway, 'prompt');
    await waitFor(() => expect(screen.getByTestId('app')).toBeInTheDocument());
    expect(window.location.href).toContain('/tools/video-editor?timeline=timeline-7#frame-42');
    expect(window.location.search).not.toContain('connect=1');
    expect(gateway.fetchImpl).toHaveBeenCalledTimes(2);
    expect(autoConnectRequested()).toBe(false);
  });

  it('shows the pending screen, not the explainer, while Chrome\'s prompt is open', async () => {
    requestAutoConnect();
    const gateway = fakeGateway();
    gateway.routes['/v1/health'] = () => new Promise<Response>(() => {});
    renderGate(gateway, 'prompt');

    await waitFor(() => expect(screen.getByTestId('panel-state')).toHaveTextContent('pending'));
    expect(screen.queryByTestId('explainer')).toBeNull();
  });

  it('shows the explainer for a direct visit, and asks Chrome only when Connect is pressed', async () => {
    const gateway = fakeGateway();
    renderGate(gateway, 'prompt');

    await waitFor(() => expect(screen.getByTestId('explainer')).toBeInTheDocument());
    expect(gateway.fetchImpl).not.toHaveBeenCalled();
    act(() => screen.getByTestId('explainer').click());
    await waitFor(() => expect(screen.getByTestId('app')).toBeInTheDocument());
  });

  it('with the permission already granted or denied the flag has nothing to do, and does not linger', async () => {
    for (const permission of ['granted', 'denied']) {
      requestAutoConnect();
      const gateway = fakeGateway();
      const view = renderGate(gateway, permission);
      await waitFor(() => expect(autoConnectRequested()).toBe(false));
      view.unmount();
    }
  });

  it('a later permission reset shows the explainer again, because the flag was used up', async () => {
    requestAutoConnect();
    const gateway = fakeGateway();
    gateway.down();
    const permissions = fakePermissions('prompt');
    render(
      <RuntimeConnectionProvider gated fetchImpl={gateway.fetchImpl} permissions={permissions.permissions} pollIntervalMs={10}>
        <RuntimeConnectionGate panel={panel}><div data-testid="app" /></RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );
    await waitFor(() => expect(autoConnectRequested()).toBe(false));
    permissions.change('denied');
    permissions.change('prompt');
    await waitFor(() => expect(screen.getByTestId('explainer')).toBeInTheDocument());
  });

  it('survives storage that refuses to be read', () => {
    vi.spyOn(Object.getPrototypeOf(window.localStorage), 'getItem').mockImplementation(() => { throw new Error('blocked'); });
    vi.spyOn(Object.getPrototypeOf(window.localStorage), 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    expect(() => requestAutoConnect()).not.toThrow();
    expect(autoConnectRequested()).toBe(false);
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
