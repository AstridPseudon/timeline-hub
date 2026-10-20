import React, { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel';
import { RuntimeConnectionPill } from '@/shared/components/RuntimeConnection/RuntimeConnectionPill';
import { RuntimeAuthorityProvider } from './RuntimeAuthorityProvider';
import { resolveRuntimeAuthority } from './runtimeAuthority';
import { RuntimeDocumentNormalizationGate } from './RuntimeDocumentNormalizationGate';
import { isWorkspaceRoute } from './runtimeDocument';

/** Holds data providers until Runtime is connected and the opening document identity is canonical. */
export function RuntimeDocumentBoundary({ children }: { children: React.ReactNode }) {
  const { pathname, search } = useLocation();
  const authority = useMemo(
    () => resolveRuntimeAuthority(search, pathname),
    [pathname, search],
  );
  const content = <RuntimeAuthorityProvider value={authority}>{children}</RuntimeAuthorityProvider>;
  if (!isWorkspaceRoute(pathname)) return content;
  return (
    <RuntimeConnectionGate
      panel={(connection) => <RuntimeConnectionPanel connection={connection} />}
      pill={(connection) => <RuntimeConnectionPill connection={connection} />}
    >
      <RuntimeDocumentNormalizationGate>{content}</RuntimeDocumentNormalizationGate>
    </RuntimeConnectionGate>
  );
}
