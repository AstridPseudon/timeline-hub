import { RUNTIME_ACCEPTED_SCHEMA_DIGESTS } from '@/integrations/runtime/contract-metadata.ts';
import { type RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { type SetupChecks } from '@/shared/components/OnboardingModal/components/SetupStatusLine.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser } from '@/shared/components/RuntimeConnection/copy.ts';

interface ConnectionStatus {
  readonly title: string;
  readonly detail?: string;
  /** Onboarding's Runtime and Workspace marks; left out while the browser's permission is the step, as nothing is checked then. */
  readonly checks?: SetupChecks;
  /** The one step this page can take itself: asking the browser for permission. */
  readonly connect?: boolean;
  /** Astrid on this computer is older than this page: the Update Astrid command belongs under the status. */
  readonly updateNeeded?: boolean;
}

const REACHED: SetupChecks = { runtime: 'pass', workspace: 'pass', ready: true };
/** The provider keeps looking until Astrid answers, so these spin rather than fail. */
const LOOKING: SetupChecks = { runtime: 'checking', workspace: 'checking', ready: false };

/** Same digests the Runtime client accepts: anything else, and the page can't open a session with this Astrid. */
function needsUpdate(schemaDigest: string | null): boolean {
  return schemaDigest !== null && !(RUNTIME_ACCEPTED_SCHEMA_DIGESTS as readonly string[]).includes(schemaDigest);
}

/** Each gate state's title and one line: the connection screens' own words, without their buttons and guides. */
export function connectionStatus(connection: RuntimeConnectionValue): ConnectionStatus {
  const { state } = connection;
  switch (state.status) {
    case 'connected':
      if (needsUpdate(connection.schemaDigest) || connection.localServiceOutOfDate) {
        return { title: COPY.updateNeeded.title, detail: COPY.updateNeeded.sentence, checks: REACHED, updateNeeded: true };
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
      return { title: COPY.setUp.title, detail: COPY.setUp.sentence, checks: LOOKING };
    case 'update_needed':
      return { title: COPY.updateNeeded.title, detail: COPY.updateNeeded.sentence, checks: LOOKING, updateNeeded: true };
    case 'not_running':
      return { title: COPY.notRunning.title, detail: COPY.notRunning.sentence, checks: LOOKING };
  }
}

