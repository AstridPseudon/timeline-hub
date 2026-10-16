import { runtimeOrigin, type RuntimeConnectionState, type RuntimeNotReadyReason } from '@/integrations/runtime/connection.ts';

/**
 * Every word the hosted build's connection gate shows (Plan A, design D3; card CP3). The panel, the pill, the
 * Reload message and the disabled compose controls render from this object and nothing else, so the wording is
 * reviewed in one place.
 *
 * Rules for this file:
 * - Headings never say "Runtime" or "gateway"; body sentences may name the Runtime where it helps.
 * - Straight apostrophes only: the journey matches `Reigh isn't running` exactly.
 * - One heading per not-ready reason, and a heading never contradicts the sentence under it.
 * - Each phrase the journey looks for (`tests/e2e/local/direct-journey.spec.ts`) appears in one element of its
 *   panel only, so a text locator finds exactly one match: "Already installed? Start it", "browser blocked",
 *   "local network access", "Reigh needs to be started again", "Runtime has stopped", "Runtime restarted".
 * - No gateway literal (`127.0.0.1:<port>`, `/api/...`): those live in `connection.ts`.
 */

/** Commands and paths the copy names. Plain strings, so a test or the panel can show them as code. */
const COMMANDS = {
  runtime: 'banodoco-local up --profile astrid',
  app: 'npm run dev:local',
  /** The installer guide, in the astrid-agent repository: a full URL, so a reader without the repo can open it. */
  installUrl: 'https://github.com/peteromallet/astrid-agent/blob/main/docs/setup/local-source-install.md',
  /** The line `dev:local` prints once the loopback gateway this page talks to is starting (`scripts/dev-local-workspace.mjs`). */
  gatewayLine: 'loopback gateway starting on 127.0.0.1:<port> for',
} as const;

/** A sentence made of text and inline code, so a command can be shown as `<code>` and still read as plain text. */
export type Segment = string | { readonly code: string };

/** The plain text of `segments`, for the pill's description and tests. */
export function segmentsText(segments: readonly Segment[]): string {
  return segments.map((segment) => (typeof segment === 'string' ? segment : segment.code)).join('');
}

/** What the panel and pill show; `restarted` is the Runtime restart message, which sits outside the gate's states. */
export type RuntimeConnectionDisplay = RuntimeConnectionState | { status: 'restarted' };

/** A heading and the one sentence under it. */
interface Message {
  readonly title: string;
  readonly sentence: string;
}

/** A heading and the sentence under it, where the sentence may name a command. */
interface RichMessage {
  readonly title: string;
  readonly sentence: readonly Segment[];
}

const REALM_CHANGED_TITLE = 'A different workspace is open';

export interface RuntimeConnectionCopy {
  readonly commands: typeof COMMANDS;
  /** Accessible name for the panel region. */
  readonly panelLabel: string;
  /** While the first probe is in flight. */
  readonly connecting: Message;
  /** Permission `prompt`: shown before anything is sent, with the Connect button. */
  readonly permission: {
    readonly title: string;
    /** The two-line explainer shown before Chrome's prompt. */
    readonly explainer: readonly [string, string];
    readonly connect: string;
    /** Button label while Chrome's prompt is open. */
    readonly connectPending: string;
  };
  /** How to install, shown with the first-time and permission panels; `linkText` links to `COMMANDS.installUrl`. */
  readonly install: { readonly before: string; readonly linkText: string; readonly after: string };
  /** Nothing answers. */
  readonly cantReach: {
    readonly firstTime: Message & { readonly alreadyInstalled: string };
    readonly returning: Message;
  };
  /** Permission `denied`. */
  readonly blocked: Message & {
    readonly fixTitle: string;
    readonly fixSteps: readonly string[];
    /** The lead-in to `settingsAddress`. */
    readonly settingsHint: string;
    /** A direct route to this site's Chrome settings. A page cannot link to chrome://, so it is shown to select and paste. */
    readonly settingsAddress: (pageOrigin: string) => string;
  };
  /** The gateway answered 503. Each reason has its own heading and its one sentence. */
  readonly notReady: { readonly reasons: Readonly<Record<RuntimeNotReadyReason, RichMessage>> };
  readonly connected: { readonly sentence: (realmName: string | null) => string };
  /** The Runtime restart message (`client.ts` fences the session), with Reload. */
  readonly restarted: Message & { readonly realmChanged: Message; readonly reload: string };
  readonly pill: {
    readonly label: (state: RuntimeConnectionDisplay) => string;
    /** Tooltip / accessible description. */
    readonly description: (state: RuntimeConnectionDisplay) => string;
  };
  readonly agent: {
    readonly copy: string;
    readonly copied: string;
    /** Inline, not a toast: the text is shown for copying by hand. */
    readonly copyFailed: string;
    readonly fieldLabel: string;
    readonly showInstructions: string;
    readonly hideInstructions: string;
    /** One block an agent can act on. `pageOrigin` is `window.location.origin`, the origin the gateway must accept. */
    readonly instructions: (pageOrigin: string) => string;
  };
  /** Next to the compose controls the hosted build disables (card A2.X). */
  readonly composeDisabled: string;
}

function realmLabel(realmName: string | null): string {
  const name = realmName?.trim();
  return name ? name : '';
}

export const RUNTIME_CONNECTION_COPY: RuntimeConnectionCopy = {
  commands: COMMANDS,

  panelLabel: 'Connect to Reigh on this computer',

  connecting: {
    title: 'Looking for Reigh',
    sentence: 'Checking whether Reigh is running on this computer.',
  },

  permission: {
    title: 'Connect to Reigh on this computer',
    explainer: [
      'This page opens your projects straight from Reigh on your computer; this site only supplies the app.',
      "Chrome will ask to let this site look for and connect to devices on your local network. Choose Allow; it only talks to Reigh on this computer, and won't ask again.",
    ],
    connect: 'Connect',
    // Neutral: Chrome may have answered already while a slow gateway has not.
    connectPending: 'Connecting…',
  },

  install: {
    before: 'New to Reigh? Follow ',
    linkText: 'the install guide',
    after: ', or copy the instructions below for your agent.',
  },

  cantReach: {
    firstTime: {
      title: 'Set up Reigh on this computer',
      sentence: "This page works with Reigh running on your own computer, and we couldn't find it here yet.",
      alreadyInstalled: 'Already installed? Start it, and this page connects by itself.',
    },
    returning: {
      title: "Reigh isn't running",
      sentence: 'Start Reigh on this computer again and this page reconnects by itself, with no reload needed.',
    },
  },

  blocked: {
    title: 'Your browser blocked the connection',
    sentence: 'Chrome is set to stop this site from reaching Reigh on your computer, so nothing was sent.',
    fixTitle: 'To allow it in Chrome',
    fixSteps: [
      'Click the site controls icon at the left of the address bar, then choose Site settings.',
      'Find Local network access and change it to Allow.',
      'Come back to this tab. It connects by itself; if Chrome offers to reload the page, go ahead.',
    ],
    settingsHint: 'Or paste this address into Chrome\'s address bar:',
    settingsAddress: (pageOrigin) => `chrome://settings/content/siteDetails?site=${encodeURIComponent(pageOrigin)}`,
  },

  notReady: {
    reasons: {
      starting: {
        title: 'Reigh is starting up',
        sentence: ['Reigh is still starting up. This page connects as soon as it is ready.'],
      },
      runtime_stopped: {
        title: 'Reigh needs to be started again',
        sentence: [
          'Reigh is open on this computer, but its Runtime has stopped. Start it again with ',
          { code: COMMANDS.runtime },
          ', and this page connects by itself.',
        ],
      },
      realm_changed: {
        title: REALM_CHANGED_TITLE,
        sentence: [
          'Reigh on this computer is now serving a different workspace, so this page paused to keep your projects apart. Start Reigh with the workspace you were using and this page connects by itself.',
        ],
      },
      identity_mismatch: {
        title: "This page can't use this Reigh",
        sentence: [
          "Reigh is running on this computer, but its Runtime isn't the one this page was set up for, so this page paused to keep your projects safe. Start it again with ",
          { code: COMMANDS.runtime },
          ', and this page tries again by itself.',
        ],
      },
      unknown: {
        title: "Reigh isn't ready",
        sentence: [
          "Reigh answered on this computer but isn't ready to use. Start it again with ",
          { code: COMMANDS.runtime },
          ", and if this page doesn't connect, reload it.",
        ],
      },
    },
  },

  connected: {
    sentence: (realmName) => {
      const name = realmLabel(realmName);
      return name ? `Connected to ${name} on this computer.` : 'Connected to Reigh on this computer.';
    },
  },

  restarted: {
    title: 'Reigh restarted',
    sentence: 'The Runtime restarted on this computer, so this page needs a fresh start. Your draft is saved and comes back after you reload.',
    realmChanged: {
      title: REALM_CHANGED_TITLE,
      sentence: 'Reigh on this computer is now serving another workspace. Your draft is saved; reload to continue with the one that is running.',
    },
    reload: 'Reload',
  },

  pill: {
    label: (state) => {
      switch (state.status) {
        case 'connecting': return 'Connecting…';
        case 'connected': {
          const name = realmLabel(state.realm.display_name);
          return name ? `Connected · ${name}` : 'Connected';
        }
        case 'cant_reach': return 'Not connected';
        case 'blocked': return 'Blocked by browser';
        case 'not_ready': return state.reason === 'starting' ? 'Starting…' : 'Not ready';
        case 'restarted': return 'Reload needed';
      }
    },
    description: (state) => {
      switch (state.status) {
        case 'connecting': return 'Looking for Reigh on this computer.';
        case 'connected': return RUNTIME_CONNECTION_COPY.connected.sentence(state.realm.display_name);
        case 'cant_reach': return state.firstTime ? 'Reigh is not set up on this computer yet.' : 'Reigh is not running on this computer.';
        case 'blocked': return 'Chrome is blocking this site from reaching Reigh on this computer.';
        case 'not_ready': return segmentsText(RUNTIME_CONNECTION_COPY.notReady.reasons[state.reason].sentence);
        case 'restarted': return 'Reigh restarted; reload to continue.';
      }
    },
  },

  agent: {
    copy: 'Copy instructions for your agent',
    copied: 'Copied. Paste it into your agent.',
    copyFailed: "Couldn't copy automatically. Select the instructions below and copy them.",
    fieldLabel: 'Instructions for your agent',
    showInstructions: 'Show instructions',
    hideInstructions: 'Hide instructions',
    instructions: (pageOrigin) => [
      `Please start Reigh on this computer so the page open at ${pageOrigin} can connect to it.`,
      'Keep any existing installation, profile, data root and workspace as they are. Do not reset, reinstall over or delete anything.',
      [
        `1. Start the Reigh Runtime: ${COMMANDS.runtime}`,
        '   If it is already running, leave it running.',
        `   If the command is not found, Reigh is not installed here yet: follow the install guide (${COMMANDS.installUrl}), then come back to this step.`,
        `2. In the reigh-app checkout, run: REIGH_LOOPBACK_ORIGIN=${pageOrigin} ${COMMANDS.app}`,
        `   If ${COMMANDS.app} is already running without printing "loopback gateway starting ... for ${pageOrigin}", stop it and start it again this way.`,
        '   If it says its port is already taken, do not stop the process holding it; report the realm it names.',
        `3. Leave both running, and report back once ${COMMANDS.app} prints "${COMMANDS.gatewayLine} ${pageOrigin}". The page connects by itself; it does not need a reload.`,
      ].join('\n'),
    ].join('\n\n'),
  },

  composeDisabled: `Making new images needs Reigh's own app on your computer for now; open the address that ${COMMANDS.app} prints.`,
};

/**
 * CP3's compose line on the hosted build (a gateway origin is configured), `null` same-origin. The one rule
 * the compose controls, their submit handlers and the task-creation library all read, so the composer route,
 * which the gateway does not serve, is never requested from the hosted page.
 */
export function composeDisabledReason(): string | null {
  return runtimeOrigin() !== '' ? RUNTIME_CONNECTION_COPY.composeDisabled : null;
}
