import { Badge } from '@/shared/components/ui/badge.tsx';
import { Button } from '@/shared/components/ui/button.tsx';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, type RuntimeConnectionDisplay } from './copy.ts';
import { useRuntimeRestartWatch, type RuntimeRestartStatus } from './useRuntimeRestartWatch.ts';

export interface RuntimeConnectionPillProps {
  readonly connection: RuntimeConnectionValue;
  /** Override for tests; reloading the page is how the person picks up the restarted Runtime. */
  readonly onReload?: () => void;
  /** Overrides for tests of the restart watch; the defaults are the production interval and `fetch`. */
  readonly restartCheckIntervalMs?: number;
  readonly fetchImpl?: (input: string, init?: RequestInit) => Promise<Response>;
}

function RestartMessage({ kind, onReload }: { kind: Exclude<RuntimeRestartStatus, 'ok'>; onReload: () => void }) {
  const restarted = COPY.restarted;
  const message = kind === 'realm_changed' ? restarted.realmChanged : restarted;
  return (
    <div role="alert" className="w-full max-w-sm space-y-2 rounded-lg border border-border bg-card p-4 text-card-foreground shadow-md">
      <h2 className="text-sm font-medium">{message.title}</h2>
      <p className="text-xs leading-5 text-muted-foreground">{message.sentence}</p>
      <Button type="button" size="sm" onClick={onReload}>{restarted.reload}</Button>
    </div>
  );
}

/**
 * The connection pill, fixed to the bottom-right while connected, and the Runtime restart message above it (Plan A,
 * D3). The pill names the realm; after a restart or a realm change the message replaces nothing: the editor stays
 * mounted with its draft until Reload. Renders nothing while not connected (the gate shows the panel then).
 */
export function RuntimeConnectionPill({
  connection,
  onReload = () => window.location.reload(),
  restartCheckIntervalMs,
  fetchImpl,
}: RuntimeConnectionPillProps) {
  const restart = useRuntimeRestartWatch(connection.isConnected, { intervalMs: restartCheckIntervalMs, fetchImpl });
  if (!connection.isConnected) return null;

  const display: RuntimeConnectionDisplay = restart === 'ok' ? connection.state : { status: 'restarted' };
  return (
    <div
      data-testid="runtime-connection-status"
      data-state={display.status}
      className="pointer-events-none fixed bottom-3 right-3 z-50 flex flex-col items-end gap-2"
    >
      {restart !== 'ok' && <div className="pointer-events-auto"><RestartMessage kind={restart} onReload={onReload} /></div>}
      <Badge
        variant="outline"
        title={COPY.pill.description(display)}
        className="pointer-events-auto cursor-default select-none bg-card px-3 py-1 text-xs text-foreground shadow-sm"
      >
        {COPY.pill.label(display)}
      </Badge>
    </div>
  );
}
