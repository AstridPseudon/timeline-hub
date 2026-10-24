import { describe, expect, it, vi } from 'vitest';
import {
  LOCAL_NETWORK_PERMISSION_NAME,
  queryLocalNetworkPermission,
  watchLocalNetworkPermission,
  type LocalNetworkPermissionStatus,
  type PermissionsLike,
} from './localNetworkPermission.ts';

function permissionsWith(state: string) {
  const status: LocalNetworkPermissionStatus = { state, onchange: null };
  const query = vi.fn(async (_descriptor: { name: string }) => status);
  return { permissions: { query } as PermissionsLike, status, query };
}

describe('queryLocalNetworkPermission', () => {
  it.each(['granted', 'prompt', 'denied'] as const)('reports %s', async (state) => {
    const { permissions, query } = permissionsWith(state);
    await expect(queryLocalNetworkPermission(permissions)).resolves.toBe(state);
    expect(query).toHaveBeenCalledWith({ name: LOCAL_NETWORK_PERMISSION_NAME });
    expect(LOCAL_NETWORK_PERMISSION_NAME).toBe('local-network-access');
  });

  it('reports an unsupported permission name as unsupported', async () => {
    const permissions: PermissionsLike = { query: async () => { throw new TypeError('unknown permission name'); } };
    await expect(queryLocalNetworkPermission(permissions)).resolves.toBe('unsupported');
  });

  it('reports a synchronously throwing unsupported query as unsupported', async () => {
    const permissions: PermissionsLike = { query: () => { throw new Error('boom'); } };
    await expect(queryLocalNetworkPermission(permissions)).resolves.toBe('unsupported');
  });

  it('counts an unrecognised state as prompt', async () => {
    const { permissions } = permissionsWith('something-new');
    await expect(queryLocalNetworkPermission(permissions)).resolves.toBe('prompt');
  });

  it('reports a missing Permissions API as unsupported', async () => {
    await expect(queryLocalNetworkPermission({} as PermissionsLike)).resolves.toBe('unsupported');
  });
});

describe('watchLocalNetworkPermission', () => {
  it('reports each change until unsubscribed', async () => {
    const { permissions, status } = permissionsWith('prompt');
    const listener = vi.fn();
    const stop = await watchLocalNetworkPermission(listener, permissions);

    status.state = 'granted';
    status.onchange?.call(status, new Event('change'));
    expect(listener).toHaveBeenLastCalledWith('granted');

    status.state = 'denied';
    status.onchange?.call(status, new Event('change'));
    expect(listener).toHaveBeenLastCalledWith('denied');

    stop();
    expect(status.onchange).toBeNull();
    expect(listener).toHaveBeenCalledTimes(2);
  });

  it('returns a harmless unsubscribe when the query throws', async () => {
    const permissions: PermissionsLike = { query: async () => { throw new Error('no'); } };
    const stop = await watchLocalNetworkPermission(vi.fn(), permissions);
    expect(() => stop()).not.toThrow();
  });
});
