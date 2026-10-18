import { ReactNode } from 'react';
import { useAuth } from '@/shared/contexts/AuthContext';
import { useRuntimeConnection } from '@/integrations/runtime/RuntimeConnectionProvider';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel';

export const AuthGate = ({ children }: { children: ReactNode }) => {
  const { isLoading } = useAuth();
  const connection = useRuntimeConnection();

  // On the hosted build the wait is the Runtime probe (up to its timeout), so show the connecting state, not a blank page.
  if (isLoading) return connection.gated ? <RuntimeConnectionPanel connection={connection} /> : null;

  return <>{children}</>;
};
