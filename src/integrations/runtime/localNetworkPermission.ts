/**
 * Chrome's local-network permission, as the hosted build sees it.
 *
 * The permission name is `local-network-access` (checked in Chromium 141; `local-network` and
 * `loopback-network` throw). `granted` means probe at once, `prompt` means send nothing until the
 * person presses Connect, `denied` means the browser blocked it. Browsers without the Permissions API
 * or this permission name have no local-network permission to ask about, so they probe as `granted`.
 */

export type LocalNetworkPermissionState = 'granted' | 'prompt' | 'denied';

export const LOCAL_NETWORK_PERMISSION_NAME = 'local-network-access';

/** The slice of `PermissionStatus` the gate needs; `onchange` drives re-checks. */
export interface LocalNetworkPermissionStatus {
  state: string;
  onchange: ((this: unknown, event: Event) => unknown) | null;
}

export interface PermissionsLike {
  query(descriptor: { name: string }): Promise<LocalNetworkPermissionStatus>;
}

function normalize(state: unknown): LocalNetworkPermissionState {
  return state === 'granted' || state === 'denied' ? state : 'prompt';
}

function defaultPermissions(): PermissionsLike | undefined {
  return typeof navigator === 'undefined' ? undefined : (navigator.permissions as unknown as PermissionsLike | undefined);
}

/** Resolves the status object, or `undefined` when it cannot be obtained. Never throws. */
export async function queryLocalNetworkPermissionStatus(
  permissions: PermissionsLike | undefined = defaultPermissions(),
): Promise<LocalNetworkPermissionStatus | undefined> {
  try {
    if (!permissions || typeof permissions.query !== 'function') return undefined;
    return (await permissions.query({ name: LOCAL_NETWORK_PERMISSION_NAME })) ?? undefined;
  } catch {
    return undefined;
  }
}

/** The current state: `granted`, `prompt` or `denied`. Missing or unsupported permission queries mean no prompt exists. */
export async function queryLocalNetworkPermission(
  permissions?: PermissionsLike,
): Promise<LocalNetworkPermissionState> {
  const status = await queryLocalNetworkPermissionStatus(permissions);
  return status ? normalize(status.state) : 'granted';
}

/**
 * Calls `listener` with the new state whenever the browser changes the permission (the person
 * answers the prompt, or changes it in site settings). Returns an unsubscribe function; a status
 * that cannot be obtained yields a no-op.
 */
export async function watchLocalNetworkPermission(
  listener: (state: LocalNetworkPermissionState) => void,
  permissions?: PermissionsLike,
): Promise<() => void> {
  const status = await queryLocalNetworkPermissionStatus(permissions);
  if (!status) return () => {};
  status.onchange = () => listener(normalize(status.state));
  return () => {
    status.onchange = null;
  };
}
