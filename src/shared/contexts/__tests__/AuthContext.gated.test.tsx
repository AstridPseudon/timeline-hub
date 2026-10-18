// @vitest-environment jsdom
/**
 * AuthContext on the hosted build: the Runtime boot gate is the session, not the bridge probe.
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';

const { probeBridgeSessionMock } = vi.hoisted(() => ({ probeBridgeSessionMock: vi.fn() }));
vi.mock('@/shared/auth/bridgeSession', () => ({
  probeBridgeSession: probeBridgeSessionMock,
  LOCAL_USER_ID: 'local-user',
}));

const GATEWAY = 'http://127.0.0.1:17340';

function stubGateway(health: () => Response) {
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/v1/health')) return health();
    if (url.endsWith('/v1/realm')) return new Response(JSON.stringify({ realm_id: 'r1', display_name: 'Direct Journey' }), { status: 200 });
    throw new Error(`unexpected ${url}`);
  });
  vi.stubGlobal('fetch', fetchMock);
  return fetchMock;
}

function stubPermission(state: string) {
  Object.defineProperty(navigator, 'permissions', {
    configurable: true,
    value: { query: vi.fn(async () => ({ state, onchange: null })) },
  });
}

async function renderHosted() {
  vi.resetModules();
  const connection = await import('@/integrations/runtime/connection');
  connection.setRuntimeOrigin({ VITE_RUNTIME_ORIGIN: GATEWAY });
  const { AuthProvider, useAuth } = await import('../AuthContext');
  const { queryClient } = await import('@/app/providers/queryClient');
  function Consumer() {
    const { userId, isAuthenticated, isLoading } = useAuth();
    return (
      <div>
        <span data-testid="userId">{userId ?? 'null'}</span>
        <span data-testid="isAuthenticated">{String(isAuthenticated)}</span>
        <span data-testid="isLoading">{String(isLoading)}</span>
      </div>
    );
  }
  render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Consumer />
      </AuthProvider>
    </QueryClientProvider>,
  );
  return { queryClient };
}

describe('AuthProvider on the hosted build', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/');
    window.localStorage.clear();
    probeBridgeSessionMock.mockReset();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    Reflect.deleteProperty(navigator, 'permissions');
  });

  it('resolves the local user from the gate when the Runtime is connected, without the bridge probe, and invalidates Runtime queries', async () => {
    stubPermission('granted');
    stubGateway(() => new Response(JSON.stringify({ status: 'ok' }), { status: 200 }));
    const { queryClient } = await renderHosted();
    const invalidate = vi.spyOn(queryClient, 'invalidateQueries');

    await waitFor(() => expect(screen.getByTestId('userId')).toHaveTextContent('local-user'));
    expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('true');
    expect(screen.getByTestId('isLoading')).toHaveTextContent('false');
    expect(probeBridgeSessionMock).not.toHaveBeenCalled();
    expect(invalidate).toHaveBeenCalledTimes(1);
    const { predicate } = invalidate.mock.calls[0]![0] as { predicate: (query: { queryKey: unknown[] }) => boolean };
    expect(predicate({ queryKey: ['runtime', 'generation-variants'] })).toBe(true);
    expect(predicate({ queryKey: ['astrid-bridge', 'health'] })).toBe(true);
    expect(predicate({ queryKey: ['runtime-tasks', 'p1'] })).toBe(true);
    expect(predicate({ queryKey: ['runtime-editor', 'session', 'projects'] })).toBe(true);
    expect(predicate({ queryKey: ['shots', 'p1'] })).toBe(false);
  });

  it('is loading while the permission is read, then anonymous and not loading when the Runtime is not reachable', async () => {
    stubPermission('granted');
    stubGateway(() => { throw new TypeError('Failed to fetch'); });
    await renderHosted();

    await waitFor(() => expect(screen.getByTestId('isLoading')).toHaveTextContent('false'));
    expect(screen.getByTestId('userId')).toHaveTextContent('null');
    expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('false');
    expect(probeBridgeSessionMock).not.toHaveBeenCalled();
  });

  it('sends nothing while the permission is prompt, and does not stay in loading', async () => {
    stubPermission('prompt');
    const fetchMock = stubGateway(() => new Response('{}'));
    await renderHosted();

    await waitFor(() => expect(screen.getByTestId('isLoading')).toHaveTextContent('false'));
    expect(screen.getByTestId('userId')).toHaveTextContent('null');
    expect(fetchMock).not.toHaveBeenCalled();
    expect(probeBridgeSessionMock).not.toHaveBeenCalled();
  });
});
