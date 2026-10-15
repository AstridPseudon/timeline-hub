import { afterEach, describe, expect, it, vi } from 'vitest';
import { ReighRuntimeClient, RUNTIME_CLIENT_SCOPES } from './client.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from './contract-metadata.ts';

// The browser default transport is `fetch`; the App builds clients ad hoc, so
// every client on one base URL must negotiate health/handshake/realm once.
const REALM = 'realm-shared';
const INSTANCE = 'instance-shared';

function stubRuntime(counts: Record<string, number>, instance = () => INSTANCE) {
  const handler = vi.fn(async (input: RequestInfo | URL) => {
    const path = new URL(String(input), 'http://localhost').pathname.replace(/^\/api\/[^/]+/, '');
    counts[path] = (counts[path] ?? 0) + 1;
    const body = path === '/v1/health'
      ? { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: instance() }
      : path === '/v1/handshake'
        ? { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 's', actor_id: 'reigh-product', realm_id: REALM, scopes: [...RUNTIME_CLIENT_SCOPES], capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] }
        : path === '/v1/realm'
          ? { realm_id: REALM, display_name: 'r', version: 1, created_at: '2026-01-01T00:00:00Z' }
          : { items: [], next_cursor: null };
    return new Response(JSON.stringify(body), { status: 200, headers: { 'Content-Type': 'application/json' } });
  });
  vi.stubGlobal('fetch', handler);
  return handler;
}

afterEach(() => vi.unstubAllGlobals());

describe('shared Runtime session', () => {
  it('negotiates one handshake for every concurrent client on a base URL', async () => {
    const counts: Record<string, number> = {};
    stubRuntime(counts);
    const clients = Array.from({ length: 6 }, () => new ReighRuntimeClient({ baseUrl: '/api/shared-a' }));
    await Promise.all(clients.map((client) => client.ensureSession()));
    await Promise.all(clients.map((client) => client.listProjects()));
    expect(counts['/v1/handshake']).toBe(1);
    expect(counts['/v1/health']).toBe(1);
    expect(counts['/v1/realm']).toBe(1);
  });

  it('keeps separate base URLs separate', async () => {
    const counts: Record<string, number> = {};
    stubRuntime(counts);
    await Promise.all([
      new ReighRuntimeClient({ baseUrl: '/api/shared-b' }).ensureSession(),
      new ReighRuntimeClient({ baseUrl: '/api/shared-c' }).ensureSession(),
    ]);
    expect(counts['/v1/handshake']).toBe(2);
  });

  it('reconnect on one client renegotiates for all of them', async () => {
    const counts: Record<string, number> = {};
    stubRuntime(counts);
    const a = new ReighRuntimeClient({ baseUrl: '/api/shared-d' });
    const b = new ReighRuntimeClient({ baseUrl: '/api/shared-d' });
    await a.ensureSession();
    await a.reconnect();
    await b.ensureSession();
    expect(counts['/v1/handshake']).toBe(2);
  });

  it('a failed negotiation is not cached for later clients', async () => {
    const counts: Record<string, number> = {};
    let healthy = false;
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const path = new URL(String(input), 'http://localhost').pathname.replace(/^\/api\/[^/]+/, '');
      counts[path] = (counts[path] ?? 0) + 1;
      if (!healthy) return new Response('down', { status: 503 });
      const inner: Record<string, number> = {};
      stubRuntime(inner);
      return (globalThis.fetch as typeof fetch)(input);
    }));
    await expect(new ReighRuntimeClient({ baseUrl: '/api/shared-e' }).ensureSession()).rejects.toBeTruthy();
    healthy = true;
    await expect(new ReighRuntimeClient({ baseUrl: '/api/shared-e' }).ensureSession()).resolves.toBeTruthy();
  });
});
