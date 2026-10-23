import { RuntimeConnectionProvider, RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx';
import { StarterProjectHandoff } from './StarterProjectHandoff.tsx';
import { completeWelcome } from './welcomeProgress.ts';

export default function WelcomeConnection() {
  return <RuntimeConnectionProvider><RuntimeConnectionGate
    panel={(connection, exit) => <RuntimeConnectionPanel connection={connection} exit={exit} firstRun />}>
    <StarterProjectHandoff onContinueWithoutProject={() => window.location.assign(completeWelcome())} onReady={selection => window.location.assign(completeWelcome(selection))} />
  </RuntimeConnectionGate></RuntimeConnectionProvider>;
}
