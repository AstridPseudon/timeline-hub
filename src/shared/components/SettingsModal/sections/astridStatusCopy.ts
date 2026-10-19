/** User-facing copy for the Astrid status section in App Settings. */
export const ASTRID_STATUS_COPY = {
  title: 'Astrid on this computer',
  description: 'Your connected workspace and what is running on this computer.',
  connecting: 'Connecting to Astrid…',
  connected: 'Connected',
  degraded: 'Runtime is degraded',
  checking: 'Checking Runtime details…',
  unavailable: 'Runtime details are unavailable right now.',
  setUp: 'Not set up',
  notRunning: 'Not running',
  updateNeeded: 'Needs an update',
  blocked: 'Connection permission is blocked',
  restartNeeded: 'Restart needed',
  workspace: 'Connected workspace',
  versions: 'Versions',
  versionsUnavailable: 'Installed app, Runtime, and agent versions are not reported by this Runtime connection.',
  connectionDetails: 'Connection details',
  protocol: 'Protocol',
  schema: 'Schema identifier',
  running: "What's running",
  noServices: 'No long-running services are declared.',
  detailsUnavailable: 'Service details are unavailable.',
  serviceStates: {
    starting: 'Starting',
    running: 'Running',
    restarting: 'Restarting',
    failed: 'Failed',
  },
  restartCount: (count: number) => `Restarts: ${count}`,
  lastExit: (code: number) => `Last exit: ${code}`,
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
