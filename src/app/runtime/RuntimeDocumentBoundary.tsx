import React, { useEffect, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { RuntimeConnectionGate, type RuntimeConnectionPanelExit, type RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider';
import { connectionStepFor } from '@/app/onboarding/welcomeProgress';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel';
import { RuntimeConnectionPill } from '@/shared/components/RuntimeConnection/RuntimeConnectionPill';
import { RuntimeAuthorityProvider } from './RuntimeAuthorityProvider';
import { resolveRuntimeAuthority } from './runtimeAuthority';
import { RuntimeDocumentNormalizationGate } from './RuntimeDocumentNormalizationGate';
import { isWorkspaceRoute } from './runtimeDocument';

/** States where the person has to do something before Astrid can connect: the onboarding connection step owns those screens. */
const NEEDS_THE_CONNECTION_STEP: ReadonlySet<string> = new Set([
  'needs_permission', 'blocked', 'not_running', 'refused', 'browser_update_needed', 'unsupported',
]);

/**
 * The editor's panel. Until Astrid has connected in this page load, a state that needs the person to act sends the page
 * to the onboarding connection step (which explains the permission, points at Chrome's prompt and asks on entry), with
 * this address as the return. Everything else (looking, a phone, a restart, an update) keeps its own screen, and once
 * connected a later drop is the pill's business, never this.
 */
export function EditorConnectionPanel({ connection, exit }: { connection: RuntimeConnectionValue; exit: RuntimeConnectionPanelExit | null }) {
  const redirect = !exit && NEEDS_THE_CONNECTION_STEP.has(connection.state.status);
  useEffect(() => {
    if (redirect) window.location.replace(connectionStepFor(window.location));
  }, [redirect]);
  // While the page changes, the boot screen stays up rather than flashing a card.
  return <RuntimeConnectionPanel connection={redirect ? { ...connection, state: { status: 'connecting' } } : connection} exit={exit} />;
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
      panel={(connection, exit) => <EditorConnectionPanel connection={connection} exit={exit} />}
      pill={(connection) => <RuntimeConnectionPill connection={connection} />}
    >
      <RuntimeDocumentNormalizationGate>{content}</RuntimeDocumentNormalizationGate>
    </RuntimeConnectionGate>
  );
}
