import React, { createContext, useState, useContext, ReactNode, useEffect, useMemo } from 'react';
import { LOCAL_USER_ID, probeBridgeSession } from '@/shared/auth/bridgeSession';
import { queryClient } from '@/app/providers/queryClient';
import { isRuntimeQueryKey } from '@/integrations/runtime/connection';
import { RuntimeConnectionProvider, useRuntimeConnection } from '@/integrations/runtime/RuntimeConnectionProvider';
import { requireContextValue } from './contextGuard';
import { isLocalTestMode } from '@/app/localTestRuntime';
import { isRuntimeDocumentMode } from '@/app/runtime/runtimeDocument';
import { hasLocalModeUrlParams } from '@/shared/dev/devSession';

interface AuthContextType {
  userId: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/** Boot/auth seam: one health probe of the Astrid bridge (`astridBase()`) per boot IS the session
 * (doc 27 §local-trust). A healthy bridge resolves the fixed local user;
 * failure degrades to alive-but-unauthenticated with exactly one probe.
 * The per-boot request token lives at the vite-proxy layer and never
 * reaches browser code.
 *
 * On the hosted build (a Runtime origin is configured) the boot gate owns the probe instead:
 * the session is "the gate is connected" (`RuntimeConnectionProvider`), the permission is
 * checked before anything is sent, and `isLoading` holds until the gate has an answer. */
export const AuthProvider = ({ children }: { children: ReactNode }) => (
  <RuntimeConnectionProvider onConnected={invalidateRuntimeQueries}>
    <AuthSession>{children}</AuthSession>
  </RuntimeConnectionProvider>
);

/** Marks whatever the Runtime queries cached before the connection came up as stale. */
function invalidateRuntimeQueries() {
  void queryClient.invalidateQueries({ predicate: (query) => isRuntimeQueryKey(query.queryKey) });
}

const AuthSession = ({ children }: { children: ReactNode }) => {
  const connection = useRuntimeConnection();
  const gated = connection.gated;
  const localTestMode = isLocalTestMode();
  const localAstridMode = hasLocalModeUrlParams(
    typeof window === 'undefined' ? '' : window.location.search,
  );
  const runtimeDocumentMode = isRuntimeDocumentMode();
  const sessionlessDocument = !gated && (localTestMode || localAstridMode || runtimeDocumentMode);
  const [userId, setUserId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(!gated && !sessionlessDocument);

  useEffect(() => {
    if (gated) return;
    if (sessionlessDocument) {
      setUserId(null);
      setIsLoading(false);
      return;
    }
    let cancelled = false;
    void probeBridgeSession().then((probe) => {
      if (cancelled) return;
      setUserId(probe.ok ? probe.userId : null);
      setIsLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [gated, sessionlessDocument]);

  const { isConnected, isBooting } = connection;
  const value = useMemo(
    () => gated
      ? { userId: isConnected ? LOCAL_USER_ID : null, isAuthenticated: isConnected, isLoading: isBooting }
      : { userId, isAuthenticated: !!userId, isLoading },
    [gated, isConnected, isBooting, userId, isLoading],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => requireContextValue(useContext(AuthContext), 'useAuth', 'AuthProvider');
const NO_AUTH = Object.freeze({ userId: null, isAuthenticated: false, isLoading: false });
export const useAuthSafe = (): AuthContextType => useContext(AuthContext) ?? NO_AUTH;
