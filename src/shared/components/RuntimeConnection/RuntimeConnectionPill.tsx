import { useLayoutEffect } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { setRecoveryCardShowing } from '@/integrations/runtime/recoveryCard.ts';
import { CopyInstallCommand } from './CopyInstallCommand.tsx';
import { UI_Z_LAYERS } from '@/shared/lib/uiLayers.ts';
import { RUNTIME_CONNECTION_COPY as COPY, withCommandShell } from './copy.ts';
import { useRuntimeRestartWatch } from './useRuntimeRestartWatch.ts';

export interface RuntimeConnectionPillProps {
  readonly connection: RuntimeConnectionValue;
  /** Override for tests; reloading the page is how the person picks up the restarted Astrid. */
  readonly onReload?: () => void;
  /** Overrides for tests of the restart watch; the defaults are the production interval and `fetch`. */
  readonly restartCheckIntervalMs?: number;
  readonly fetchImpl?: (input: string, init?: RequestInit) => Promise<Response>;
}

/** Fixed bottom-right with a 16px gutter; on a phone it sits above the floating lock/gallery toolbar. */
const CARD_CLASS = 'fixed bottom-20 right-4 w-[calc(100%-2rem)] max-w-sm space-y-3 rounded-2xl border border-border bg-card p-5 text-center text-card-foreground shadow-md sm:bottom-4';

const CARD_STYLE = { zIndex: UI_Z_LAYERS.RUNTIME_RECOVERY_CARD } as const;

function CardText({ title, sentence }: { title: string; sentence: string }) {
  return (
    <div className="space-y-1">
      <h2 className="font-serif font-theme-heading text-base text-foreground">{title}</h2>
      <p className="text-balance text-sm text-muted-foreground">{sentence}</p>
    </div>
  );
}

/**
 * What the connected page says about Astrid, bottom-right. While Astrid is up it says nothing visible: the
 * editor already shows the project, and a "Connected" badge went stale the moment Astrid stopped. Two cards replace it:
 * "Astrid stopped" (it clears itself when Astrid is back) and "Astrid restarted" (Reload). The editor stays mounted with
 * its draft either way. Renders nothing while not connected (the gate shows the panel then).
 */
export function RuntimeConnectionPill({
  connection,
  onReload = () => window.location.reload(),
  restartCheckIntervalMs,
  fetchImpl,
}: RuntimeConnectionPillProps) {
  const restart = useRuntimeRestartWatch(connection.isConnected, { intervalMs: restartCheckIntervalMs, fetchImpl });
  const cardShowing = connection.isConnected && restart !== 'ok';

  // The editor's own technical messages about the same failure stay quiet while the card is the one thing to read.
  // A layout effect, so the flag flips in the same commit that shows the card: no frame shows both.
  useLayoutEffect(() => {
    setRecoveryCardShowing(cardShowing);
    return () => setRecoveryCardShowing(false);
  }, [cardShowing]);

  if (!connection.isConnected) return null;

  if (restart === 'ok') {
    return (
      <div data-testid="runtime-connection-status" data-state="connected" className="sr-only">
        {COPY.connected.sentence}
      </div>
    );
  }

  if (restart === 'stopped') {
    return (
      <div data-testid="runtime-connection-status" data-state="stopped" role="alert" className={CARD_CLASS} style={CARD_STYLE}>
        <CardText title={COPY.stopped.title} sentence={withCommandShell(COPY.stopped.sentence)} />
        <CopyInstallCommand mode="install" />
      </div>
    );
  }

  return (
    <div data-testid="runtime-connection-status" data-state="restarted" role="alert" className={CARD_CLASS} style={CARD_STYLE}>
      <CardText title={COPY.restarted.title} sentence={COPY.restarted.sentence} />
      <Button type="button" className="w-full sm:w-auto" onClick={onReload}>{COPY.restarted.reload}</Button>
    </div>
  );
}
