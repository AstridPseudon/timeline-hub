import { RuntimeConnectionProvider, RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx';
import { StarterProjectHandoff } from './StarterProjectHandoff.tsx';
import { completeWelcome } from './welcomeProgress.ts';

export default function WelcomeConnection() {
  // The durable welcome phase is the handoff into a new app window and across reloads. Its gate is armed in this
  // window; a sessionStorage flag from the installing tab cannot follow the app into its own window.
  const connectOnEntry = runtimeOrigin() !== '';
  return <RuntimeConnectionProvider><RuntimeConnectionGate connectOnEntry={connectOnEntry}
    panel={(connection, exit) => <RuntimeConnectionPanel connection={connection} exit={exit} />}>
    <StarterProjectHandoff onContinueWithoutProject={() => window.location.assign(completeWelcome())} onReady={selection => window.location.assign(completeWelcome(selection))} />
  </RuntimeConnectionGate></RuntimeConnectionProvider>;
}
