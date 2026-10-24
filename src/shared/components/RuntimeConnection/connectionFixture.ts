import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import type { RuntimeConnectionState } from '@/integrations/runtime/connection.ts';

/**
 * A gate value in `state`, as `RuntimeConnectionProvider` would publish it, for the panel and pill tests. `connect`
 * is a no-op unless a test passes its own (a spy, when it asserts the click).
 */
export function connectionFor(state: RuntimeConnectionState, overrides: Partial<RuntimeConnectionValue> = {}): RuntimeConnectionValue {
  return {
    gated: true,
    state,
    isConnected: state.status === 'connected',
    connectedBefore: true,
    isBooting: false,
    isChecking: false,
    realmName: state.status === 'connected' ? state.realm.display_name : null,
    schemaDigest: null,
    localServiceOutOfDate: false,
    setLocalServiceOutOfDate: () => {},
    connect: () => {},
    ...overrides,
  };
}

export const CONNECTED_REALM = { realm_id: 'realm-1', display_name: 'Direct Journey' } as const;
