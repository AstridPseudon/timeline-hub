import { useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { CheckCircle2 } from 'lucide-react';
import { useRuntimeConnection } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { CopyInstallCommand } from '@/shared/components/RuntimeConnection/CopyInstallCommand.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser, withCommandShell } from '@/shared/components/RuntimeConnection/copy.ts';
import { DialogHeader, DialogTitle } from '@/shared/components/ui/dialog';
import { Button } from '@/shared/components/ui/button';
import type { OnboardingStepProps } from '@/shared/components/OnboardingModal/types';

/** A readable project list, including an empty one, confirms setup without probing creative tools. */
function useSetupReady(): boolean {
  const connection = useRuntimeConnection();
  // Same-origin builds bypass the connection gate; the read-only client still negotiates their session.
  const canRead = !connection.gated || connection.isConnected;
  const { isSuccess } = useQuery({
    queryKey: ['runtime', 'onboarding-projects'],
    enabled: canRead,
    queryFn: () => new AstridRuntimeClient({ readOnly: true }).listProjects(),
    retry: false,
    gcTime: 0,
    refetchInterval: query => query.state.status === 'success' ? false : 4000,
  });
  return canRead && isSuccess;
}

/** How long "Connected to Astrid" stays up before onboarding moves on by itself. */
const CONNECTED_PAUSE_MS = 1200;

/** Setup and reconnect use the same install line as the connection screen. */
export function AstridSetupStep({ onNext, reconnect = false }: OnboardingStepProps & { reconnect?: boolean }) {
  const ready = useSetupReady();
  const copy = reconnect ? COPY.notRunning : COPY.setUp;
  const connection = useRuntimeConnection();
  // Already connected when onboarding opened: there is nothing to set up, so the step is skipped.
  const connectedAtOpen = useRef(!reconnect && connection.gated && connection.isConnected);
  const onNextRef = useRef(onNext);
  onNextRef.current = onNext;

  useEffect(() => {
    if (connectedAtOpen.current) onNextRef.current();
  }, []);

  useEffect(() => {
    if (!ready || connectedAtOpen.current) return undefined;
    if (reconnect) {
      onNextRef.current();
      return undefined;
    }
    const timer = setTimeout(() => onNextRef.current(), CONNECTED_PAUSE_MS);
    return () => clearTimeout(timer);
  }, [ready, reconnect]);

  return (
    <div className="space-y-5 text-center">
      <DialogHeader className="space-y-3">
        {ready && (
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10">
            <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-500" aria-hidden />
          </div>
        )}
        <DialogTitle className="text-center text-2xl font-bold">
          {ready ? COPY.connected.sentence : copy.title}
        </DialogTitle>
      </DialogHeader>
      {ready ? (
        <Button variant="retro" size="retro-sm" onClick={onNext} className="w-full sm:w-auto">
          {reconnect ? 'Back to Astrid' : 'Continue'}
        </Button>
      ) : (
        <>
          <p className="text-muted-foreground">{withCommandShell(copy.sentence)}</p>
          <CopyInstallCommand mode="install" />
          {reconnect ? null : (
            <p className="text-sm text-muted-foreground">{withBrowser('If {browser} asks about devices on your network, choose Allow. This step moves on by itself once Astrid is connected.')}</p>
          )}
        </>
      )}
    </div>
  );
}
