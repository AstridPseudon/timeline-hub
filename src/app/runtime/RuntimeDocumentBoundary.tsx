import React, { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { CheckCircle2 } from 'lucide-react';
import { RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel';
import { RuntimeConnectionPill } from '@/shared/components/RuntimeConnection/RuntimeConnectionPill';
import { RUNTIME_CONNECTION_COPY } from '@/shared/components/RuntimeConnection/copy';
import { RuntimeAuthorityProvider } from './RuntimeAuthorityProvider';
import { resolveRuntimeAuthority } from './runtimeAuthority';
import { RuntimeDocumentNormalizationGate } from './RuntimeDocumentNormalizationGate';
import { isWorkspaceRoute } from './runtimeDocument';

/** The moment between "Astrid answered" and the app opening. */
function ConnectedMoment() {
  return (
    <div role="status" className="grid min-h-screen place-items-center bg-background text-foreground">
      <div className="flex flex-col items-center gap-4">
        <span className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10">
          <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-500" aria-hidden />
        </span>
        <h1 className="text-2xl font-bold">{RUNTIME_CONNECTION_COPY.connected.sentence}</h1>
      </div>
    </div>
  );
}

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
      connected={() => <ConnectedMoment />}
    >
      <RuntimeDocumentNormalizationGate>{content}</RuntimeDocumentNormalizationGate>
    </RuntimeConnectionGate>
  );
}
