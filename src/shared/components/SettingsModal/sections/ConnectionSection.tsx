import { Button } from '@/shared/components/ui/button';
import { RUNTIME_ACCEPTED_SCHEMA_DIGESTS } from '@/integrations/runtime/contract-metadata.ts';
import { useRuntimeConnection, type RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { SetupStatusLine, type SetupChecks } from '@/shared/components/OnboardingModal/components/SetupStatusLine.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser } from '@/shared/components/RuntimeConnection/copy.ts';

interface ConnectionStatus {
  readonly title: string;
  readonly detail?: string;
  /** Onboarding's Runtime and Workspace marks; left out while the browser's permission is the step, as nothing is checked then. */
  readonly checks?: SetupChecks;
  /** The one step this page can take itself: asking the browser for permission. */
  readonly connect?: boolean;
}

const REACHED: SetupChecks = { runtime: 'pass', workspace: 'pass', ready: true };
/** The provider keeps looking until Astrid answers, so these spin rather than fail. */
const LOOKING: SetupChecks = { runtime: 'checking', workspace: 'checking', ready: false };

/** Same digests the Runtime client accepts: anything else, and the page can't open a session with this Astrid. */
function needsUpdate(schemaDigest: string | null): boolean {
  return schemaDigest !== null && !(RUNTIME_ACCEPTED_SCHEMA_DIGESTS as readonly string[]).includes(schemaDigest);
}

/** Each gate state's title and one line: the connection screens' own words, without their buttons and guides. */
function connectionStatus(connection: RuntimeConnectionValue): ConnectionStatus {
  const { state } = connection;
  switch (state.status) {
    case 'connected':
      if (needsUpdate(connection.schemaDigest)) {
        return { title: COPY.updateNeeded.title, detail: COPY.updateNeeded.sentence, checks: REACHED };
      }
      return {
        title: COPY.connected.sentence,
        detail: connection.realmName ? `Workspace: ${connection.realmName}` : undefined,
        checks: REACHED,
      };
    case 'connecting':
      if (!connection.awaitingConnect) return { title: COPY.connecting.sentence, checks: LOOKING };
      if (connection.isChecking) {
        return { title: withBrowser(COPY.permission.pending.title), detail: withBrowser(COPY.permission.pending.sentence) };
      }
      return { title: withBrowser(COPY.permission.title), detail: withBrowser(COPY.permission.sentence), connect: true };
    case 'blocked':
      // The steps, not the reason: the title already says what is wrong.
      return { title: withBrowser(COPY.blocked.title), detail: COPY.blocked.steps.join(' ') };
    case 'set_up':
      return { title: COPY.setUp.title, detail: COPY.setUp.installed, checks: LOOKING };
    case 'not_running':
      return { title: COPY.notRunning.title, detail: COPY.notRunning.sentence, checks: LOOKING };
    case 'restart_needed':
      return { title: COPY.restartNeeded.title, detail: COPY.restartNeeded.sentence, checks: LOOKING };
  }
}

/**
 * The top of App settings: where the connection to Astrid stands and whether Astrid needs an update, read from the
 * connection RuntimeConnectionProvider already keeps. Laid out like the Preferences rows: the state on the left, the
 * check marks (or the one button) on the right, one quiet line under them.
 */
export function ConnectionSection({ isMobile }: { isMobile: boolean }) {
  const connection = useRuntimeConnection();
  const { title, detail, checks, connect } = connectionStatus(connection);

  return (
    <section aria-labelledby="settings-connection-title" className="mb-6">
      <h3 id="settings-connection-title" className="mb-3 text-sm font-medium text-muted-foreground">
        Connection
      </h3>
      <div className={`${isMobile ? 'p-3' : 'p-4'} space-y-2 rounded-lg bg-muted/30`} data-connection-state={connection.state.status}>
        <div className={`flex ${isMobile ? 'flex-col items-start gap-2' : 'items-center justify-between gap-4'}`}>
          <p className="font-medium" role="status" aria-live="polite">{title}</p>
          {checks && <SetupStatusLine checks={checks} mink={false} announce={false} />}
          {connect && (
            <Button type="button" variant="retro-secondary" size="retro-sm" className="shrink-0" onClick={() => connection.connect()}>
              {COPY.permission.connect}
            </Button>
          )}
        </div>
        {detail && <p className="text-xs text-muted-foreground [overflow-wrap:anywhere]">{detail}</p>}
      </div>
    </section>
  );
}
