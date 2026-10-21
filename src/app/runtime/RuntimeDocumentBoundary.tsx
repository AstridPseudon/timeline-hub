import React, { useEffect, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { CheckCircle2 } from 'lucide-react';
import { CONNECTED_HOLD_MS, RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider';
import { EmptyEditorShell } from '@/shared/components/RuntimeConnection/EmptyEditorShell';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel';
import { RuntimeConnectionPill } from '@/shared/components/RuntimeConnection/RuntimeConnectionPill';
import { RUNTIME_CONNECTION_COPY } from '@/shared/components/RuntimeConnection/copy';
import { RuntimeAuthorityProvider } from './RuntimeAuthorityProvider';
import { resolveRuntimeAuthority } from './runtimeAuthority';
import { RuntimeDocumentNormalizationGate } from './RuntimeDocumentNormalizationGate';
import { isWorkspaceRoute } from './runtimeDocument';

/** The moment between "Astrid answered" and the app opening: the same empty editor, a check, then a fade. */
function ConnectedMoment() {
  const [fading, setFading] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setFading(true), CONNECTED_HOLD_MS - 300);
    return () => clearTimeout(timer);
  }, []);
  return (
    <div role="status" className="relative grid min-h-screen place-items-center overflow-hidden bg-background text-foreground">
      <EmptyEditorShell />
      <div className={`relative z-10 flex w-full max-w-lg flex-col items-center gap-4 rounded-2xl border border-border bg-card p-8 shadow-xl transition-opacity duration-300 ${fading ? 'opacity-0' : 'opacity-100'}`}>
        <span className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10">
          <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-500" aria-hidden />
        </span>
        <h1 className="font-serif text-2xl text-foreground">{RUNTIME_CONNECTION_COPY.connected.sentence}</h1>
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
