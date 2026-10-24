import { RuntimeConnectionProvider, RuntimeConnectionGate } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { RuntimeConnectionPanel } from '@/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx';
import { StarterProjectHandoff } from './StarterProjectHandoff.tsx';
import { completeWelcome } from './welcomeProgress.ts';
import type { WindowMode } from '@/shared/components/RuntimeConnection/copy.ts';

export default function WelcomeConnection({ windowMode }: { windowMode: WindowMode }) {
  return <RuntimeConnectionProvider><RuntimeConnectionGate
    panel={(connection, exit) => <RuntimeConnectionPanel connection={connection} exit={exit} windowMode={windowMode} />}>
    <StarterProjectHandoff onContinueWithoutProject={() => window.location.assign(completeWelcome())} onReady={selection => window.location.assign(completeWelcome(selection))} />
  </RuntimeConnectionGate></RuntimeConnectionProvider>;
}
