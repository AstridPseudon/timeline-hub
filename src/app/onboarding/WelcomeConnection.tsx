import { RuntimeConnectionProvider, RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { requiresLocalNetworkPermission } from '@/integrations/runtime/localNetworkPermission.ts';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx';
import { StarterProjectHandoff } from './StarterProjectHandoff.tsx';
import { completeWelcome, returnTargetFor } from './welcomeProgress.ts';
import { useEffect } from 'react';
import { useRuntimeGateOpen } from '@/integrations/runtime/runtimeGateOpen.tsx';

/** Connected on a step an editor page sent the person to: go back to that page, not to a starter project. */
function ReturnToEditor({ target }: { readonly target: string }) {
  // The card's "Connected" moment plays first: the gate opens once the panel has left.
  const open = useRuntimeGateOpen();
  useEffect(() => {
    if (!open) return;
    completeWelcome();
    window.location.replace(target);
  }, [open, target]);
  return null;
}

export default function WelcomeConnection({ onBack }: { readonly onBack: () => void }) {
  // The durable welcome phase is the handoff into a new app window and across reloads. Its gate is armed in this
  // window; a sessionStorage flag from the installing tab cannot follow the app into its own window.
  const returnTo = returnTargetFor(new URL(window.location.href));
  const runtime = runtimeOrigin();
  const hosted = runtime !== '';
  const needsLocalNetworkPermission = requiresLocalNetworkPermission(runtime, typeof window === 'undefined' ? '' : window.location.origin);
  return <RuntimeConnectionProvider gated requireLocalNetworkPermission={needsLocalNetworkPermission}><RuntimeConnectionGate connectOnEntry={hosted}
    panel={(connection, exit) => <RuntimeConnectionPanel connection={connection} exit={exit} onBack={exit || returnTo ? undefined : onBack} />}>
    {returnTo ? <ReturnToEditor target={returnTo} /> : <StarterProjectHandoff onContinueWithoutProject={() => window.location.replace(completeWelcome())} onReady={selection => window.location.replace(completeWelcome(selection))} />}
  </RuntimeConnectionGate></RuntimeConnectionProvider>;
}
