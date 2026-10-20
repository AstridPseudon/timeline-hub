import { useEffect, useState } from 'react';
import { CheckCircle2, CircleAlert, Loader2 } from 'lucide-react';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { useRuntimeConnection } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import type { Health, Realm, ServiceStatus } from '@/integrations/runtime/generated.ts';
import { Button } from '@/shared/components/ui/button';
import { SetupStatusLine } from '@/shared/components/OnboardingModal/components/SetupStatusLine.tsx';
import { RUNTIME_CONNECTION_COPY, withCommandShell } from '@/shared/components/RuntimeConnection/copy.ts';
import { connectionStatus } from './ConnectionSection.tsx';
import { ASTRID_HELP_URL } from '@/integrations/astrid/help.ts';
import { Card } from '@/shared/components/ui/card';
import { CopyInstallCommand } from '@/shared/components/RuntimeConnection/CopyInstallCommand.tsx';
import { ASTRID_STATUS_COPY as COPY, connectionStatusCopy } from './astridStatusCopy.ts';

const POLL_INTERVAL_MS = 5_000;

type RuntimeService = ServiceStatus;
type RuntimeDetails = { health: Health; realm: Realm };

function isRuntimeService(value: unknown): value is RuntimeService {
  if (!value || typeof value !== 'object') return false;
  const service = value as Partial<RuntimeService>;
  return typeof service.name === 'string'
    && ['starting', 'running', 'restarting', 'failed'].includes(String(service.state))
    && (typeof service.last_exit === 'number' || service.last_exit === null)
    && typeof service.restart_count === 'number';
}

function statusIcon(status: string) {
  if (status === 'connected') return <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-500" aria-hidden />;
  if (status === 'connecting') return <Loader2 className="h-4 w-4 animate-spin" aria-hidden />;
  return <CircleAlert className="h-4 w-4 text-muted-foreground" aria-hidden />;
}

function StatusRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between gap-4 text-sm">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className="min-w-0 break-all text-right font-medium">{value}</dd>
    </div>
  );
}

function serviceMetadata(service: RuntimeService): string[] {
  return [COPY.restartCount(service.restart_count)].filter((value): value is string => value !== null);
}

export function AstridStatusSection({ isOpen }: { isOpen: boolean }) {
  const connection = useRuntimeConnection();
  const [details, setDetails] = useState<RuntimeDetails | null>(null);
  const [loadFailed, setLoadFailed] = useState(false);
  const connected = connection.state.status === 'connected';

  useEffect(() => {
    if (!isOpen || !connected) {
      setDetails(null);
      setLoadFailed(false);
      return undefined;
    }

    let active = true;
    let reading = false;
    const runtimeClient = new AstridRuntimeClient();
    const refresh = async () => {
      if (reading) return;
      reading = true;
      try {
        const current = await runtimeClient.readStatus();
        if (active) {
          setDetails(current);
          setLoadFailed(false);
        }
      } catch {
        if (active) {
          setDetails(null);
          setLoadFailed(true);
        }
      } finally {
        reading = false;
      }
    };
    setDetails(null);
    setLoadFailed(false);
    void refresh();
    const timer = window.setInterval(() => void refresh(), POLL_INTERVAL_MS);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [isOpen, connected]);

  const summary = connectionStatus(connection);
  const status = connection.state.status;
  const rawServices = details?.health.services;
  const hasServiceDetails = Array.isArray(rawServices) && rawServices.every(isRuntimeService);
  const services = Array.isArray(rawServices) ? rawServices.filter(isRuntimeService) : [];
  const needsRepair = details?.health.status === 'degraded' || services.some((service) => service.state === 'failed');
  const statusText = summary.updateNeeded
    ? COPY.updateNeeded
    : connected
    ? loadFailed ? COPY.unavailable : needsRepair ? COPY.degraded : details ? COPY.connected : COPY.checking
    : connectionStatusCopy(status);

  return (
    <section className="mb-6" aria-labelledby="astrid-status-title">
      <Card className="p-4">
        <div className="flex items-start gap-3">
          {statusIcon(summary.updateNeeded ? 'update_needed' : connected ? needsRepair ? 'degraded' : 'connected' : status)}
          <div className="min-w-0 flex-1 space-y-3">
            <div>
              <h2 id="astrid-status-title" className="text-base font-semibold">{COPY.title}</h2>
              <p className="mt-1 text-sm text-muted-foreground">{COPY.description}</p>
              <p className="mt-2 text-sm font-medium" role="status" aria-live="polite">{statusText}</p>
            </div>

            {summary.checks && <SetupStatusLine checks={summary.checks} mink={false} announce={false} />}
            {(!connected || summary.updateNeeded) && summary.detail && <p className="text-xs text-muted-foreground [overflow-wrap:anywhere]">{summary.updateNeeded ? withCommandShell(summary.detail) : summary.detail}</p>}
            {summary.updateNeeded && <CopyInstallCommand label={RUNTIME_CONNECTION_COPY.agent.copy} mode="update" />}
            {summary.connect && <Button type="button" variant="retro-secondary" size="retro-sm" onClick={() => connection.connect()}>{RUNTIME_CONNECTION_COPY.permission.connect}</Button>}
            {connected && details && needsRepair && (
              <>
                <CopyInstallCommand label={RUNTIME_CONNECTION_COPY.agent.copy} mode="install" />
                <a className="text-sm text-muted-foreground underline underline-offset-4" href={ASTRID_HELP_URL} target="_blank" rel="noreferrer">Get help</a>
              </>
            )}

            {(loadFailed || !connected && status !== 'set_up' && status !== 'connecting') && (
              <a className="text-sm text-muted-foreground underline underline-offset-4" href={ASTRID_HELP_URL} target="_blank" rel="noreferrer">Get help</a>
            )}

            {connected && details && (
              <div className="space-y-4 border-t pt-3">
                <div>
                  <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{COPY.workspace}</h3>
                  <dl className="space-y-1.5">
                    <StatusRow label={COPY.workspaceName} value={details.realm.display_name} />
                  </dl>
                </div>
                <div>
                  <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{COPY.connectionDetails}</h3>
                  <dl className="space-y-1.5">
                    <StatusRow label={COPY.protocol} value={details.health.protocol} />
                    <StatusRow label={COPY.schema} value={details.health.schema_digest} />
                  </dl>
                </div>
                <div>
                  <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{COPY.running}</h3>
                  {loadFailed || !hasServiceDetails ? (
                    <p className="text-sm text-muted-foreground">{COPY.detailsUnavailable}</p>
                  ) : services.length === 0 ? (
                    <p className="text-sm text-muted-foreground">{COPY.noServices}</p>
                  ) : (
                    <ul className="space-y-2">
                      {services.map((service) => {
                        const metadata = serviceMetadata(service);
                        return (
                          <li key={service.name} className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1 text-sm">
                            <span className="font-medium">{COPY.serviceName(service.name)}</span>
                            <span className={service.state === 'failed' ? 'text-destructive' : 'text-muted-foreground'}>
                              {COPY.serviceStates[service.state]}
                            </span>
                            {metadata.length > 0 && (
                              <span className="basis-full text-xs text-muted-foreground">{metadata.join(' · ')}</span>
                            )}
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </Card>
    </section>
  );
}
