/** User-facing copy for the Astrid status section in App Settings. */
export const ASTRID_STATUS_COPY = {
  title: 'Astrid on this computer',
  description: "Your workspace and what's running on this computer.",
  connecting: 'Looking for Astrid…',
  connected: 'Connected',
  degraded: "Connected, but part of Astrid isn't working.",
  checking: 'Reading details…',
  unavailable: "Astrid's details aren't available right now.",
  setUp: 'Not found yet',
  notRunning: 'Not running',
  updateNeeded: 'Needs an update',
  blocked: "Blocked by your browser's settings",
  restartNeeded: 'Needs a restart',
  workspace: 'Workspace',
  workspaceName: 'Name',
  versions: 'Versions',
  versionsUnavailable: "Astrid doesn't report its versions here yet.",
  connectionDetails: 'Connection details',
  protocol: 'Protocol',
  schema: 'Schema',
  running: "What's running",
  noServices: 'Nothing else is running with Astrid.',
  detailsUnavailable: "Can't tell what's running right now.",
  serviceStates: {
    starting: 'Starting…',
    running: 'Running',
    restarting: 'Restarting…',
    failed: 'Failed',
  },
  restartCount: (count: number) => `Restarts: ${count}`,
  lastExit: (code: number) => `Last exit code: ${code}`,
  reason: (value: string) => `Reason: ${value}`,
} as const;

export function connectionStatusCopy(status: string): string {
  switch (status) {
    case 'connected': return ASTRID_STATUS_COPY.connected;
    case 'connecting': return ASTRID_STATUS_COPY.connecting;
    case 'set_up': return ASTRID_STATUS_COPY.setUp;
    case 'not_running': return ASTRID_STATUS_COPY.notRunning;
    case 'update_needed': return ASTRID_STATUS_COPY.updateNeeded;
    case 'blocked': return ASTRID_STATUS_COPY.blocked;
    case 'restart_needed': return ASTRID_STATUS_COPY.restartNeeded;
    default: return ASTRID_STATUS_COPY.unavailable;
  }
}
