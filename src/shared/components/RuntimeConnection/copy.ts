import hostedOrigin from '../../../../config/hosted-origin.json';
import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { installBrowserName } from '@/pages/Home/installScenario.ts';

/**
 * Every word the hosted build's connection gate shows (Plan A, design D3; card CP3). The panel, the restart cards,
 * the status container and the disabled compose controls render from this object and nothing else, so the wording is
 * reviewed in one place.
 *
 * Rules for this file:
 * - Visible text says Astrid and never names a Runtime, workspace, port or command. Commands appear only in the agent block.
 * - Straight apostrophes only: the journey matches `Astrid isn't running` exactly.
 * - One screen per thing a person can do: states a person cannot tell apart share one message.
 * - Each phrase the journey looks for (`tests/e2e/local/direct-journey.spec.ts`) appears in one element of its
 *   panel only, so a text locator finds exactly one match.
 * - The browser a card names is a `{browser}` placeholder, filled by `withBrowser` from the landing page's browser detection.
- No gateway literal (`127.0.0.1:<port>`, `/api/...`): those live in `connection.ts`.
 */

/** The browser's name goes where a card says `{browser}`: the one the landing page's install dialog detected. */
export const BROWSER_PLACEHOLDER = '{browser}';

/** `text` with every `{browser}` filled in (Chrome or Edge); the browser is detected once per call unless given. */
export function withBrowser(text: string, browser: string = installBrowserName()): string {
  return text.split(BROWSER_PLACEHOLDER).join(browser);
}

/** Commands and paths the agent block names. Plain strings. */
const COMMANDS = {
  runtime: 'astrid-runtime up --profile astrid',
  app: 'npm run dev:local',
  /** The installer guide, in the astrid-agent repository: a full URL, so a reader without the repo can open it. */
  installUrl: 'https://github.com/peteromallet/astrid-agent/blob/main/docs/setup/local-source-install.md',
} as const;

/** The origin `npm run dev:local` opens for by default (`config/hosted-origin.json`); any other needs `ASTRID_APP_LOOPBACK_ORIGIN`. */
const DEFAULT_HOSTED_ORIGIN: string | null = hostedOrigin.origin;

/** Which of the two agent blocks to copy: the page has never reached Astrid, or Astrid changed under a connected page. */
export type AgentInstructionsVariant = 'start' | 'restart';

/** A heading and the one sentence under it. */
interface Message {
  readonly title: string;
  readonly sentence: string;
}

export interface RuntimeConnectionCopy {
  readonly commands: typeof COMMANDS;
  /** Accessible name for the panel region. */
  readonly panelLabel: string;
  /** While the first probe is in flight (and while Astrid is still starting): the one line under the mark. */
  readonly connecting: { readonly sentence: string };
  /** Permission `prompt`: shown before anything is sent, with the Connect button. */
  readonly permission: Message & {
    readonly connect: string;
    /** The browser's prompt is open: nothing to press, so no button. */
    readonly pending: Message & { readonly pointer: string };
  };
  /** Permission `denied`: two steps in the browser, then the page opens by itself. */
  readonly blocked: Message & {
    readonly steps: readonly [string, string];
    readonly footer: string;
  };
  /** Nothing answers and this page has never connected: the install path. */
  readonly setUp: Message & {
    readonly button: string;
    /** `linkText` links to `COMMANDS.installUrl`. */
    readonly footer: { readonly before: string; readonly linkText: string; readonly after: string };
  };
  /** Nothing answers on a return visit, or Astrid answered but is not ready: a person does the same thing for each. */
  readonly notRunning: Message & { readonly button: string };
  /** The Astrid running is not the one this page was set up with: only a restart helps. */
  readonly restartNeeded: Message & { readonly button: string };
  /** A phone can never reach Astrid on a computer: the link goes there instead. */
  readonly phone: Message & { readonly button: string; readonly copied: string };
  /** Screen-reader text of the status container while connected; nothing else says it. */
  readonly connected: { readonly sentence: string };
  /** Connected, and the health check stopped answering. The card clears itself when Astrid is back. */
  readonly stopped: Message;
  /** Connected, and Astrid restarted (or changed) under the page. */
  readonly restarted: Message & { readonly reload: string };
  /** The timeline (or the engine connection behind it) would not load on the hosted build: replaces every engineer-worded error. */
  readonly loadFailed: Message & { readonly button: string; readonly retrying: string };
  readonly agent: {
    /** The set-up state's button. */
    readonly copySetup: string;
    /** The button everywhere else. */
    readonly copy: string;
    readonly copied: string;
    /** The line under the button once the steps are copied. */
    readonly pasteNext: string;
    /** Shown with the steps in a text box, only when the clipboard write failed. */
    readonly copyFailed: string;
    /** One block an agent can act on. `pageOrigin` is `window.location.origin`, the origin the gateway must accept. */
    readonly instructions: (pageOrigin: string, variant: AgentInstructionsVariant) => string;
  };
  /** Next to the compose controls the hosted build disables (card A2.X); followed by `openApp` when the app address is known. */
  readonly composeDisabled: string;
  /** In place of agent chat on the hosted build, which the loopback gateway does not serve (design D2). */
  readonly agentChatDisabled: string;
  /** The link text after `composeDisabled` / `agentChatDisabled`; it never shows the address. */
  readonly openApp: string;
}

export const RUNTIME_CONNECTION_COPY: RuntimeConnectionCopy = {
  commands: COMMANDS,

  panelLabel: 'Connect to Astrid',

  connecting: {
    sentence: 'Looking for Astrid on this computer…',
  },

  permission: {
    title: 'Connect to Astrid on this computer',
    sentence: '{browser} will ask about devices on your network. Choose Allow so this page can reach Astrid on your computer.',
    connect: 'Connect',
    pending: {
      title: 'Choose Allow in {browser}',
      sentence: '{browser} is asking, at the top left of this window, to let this page reach Astrid on your computer.',
      /** The word on the arrow that points at the prompt, as the install dialog's says "Up here". */
      pointer: 'Up here',
    },
  },

  blocked: {
    title: 'Allow Astrid in {browser}',
    sentence: '{browser} is set to stop this page reaching Astrid on your computer.',
    steps: [
      'Click the icon at the left of the address bar, then Site settings.',
      'Set Local network access to Allow.',
    ],
    footer: 'Come back here and it opens by itself.',
  },

  setUp: {
    title: 'Set up Astrid on this computer',
    sentence: "Astrid runs on your own computer, and it isn't running here yet.",
    button: 'Copy setup steps for your agent',
    footer: {
      before: 'Already installed? Start Astrid and this page opens by itself. Or follow ',
      linkText: 'the install guide',
      after: '.',
    },
  },

  notRunning: {
    title: "Astrid isn't running",
    sentence: 'Start Astrid on this computer and this page opens by itself.',
    button: 'Copy steps for your agent',
  },

  restartNeeded: {
    title: 'Astrid needs a restart',
    sentence: 'Astrid changed on this computer since this page last used it. Restart it and this page opens by itself.',
    button: 'Copy steps for your agent',
  },

  phone: {
    title: 'Open Astrid on your computer',
    sentence: 'Astrid runs on a computer, so open this page there.',
    button: 'Send the link to your computer',
    copied: 'Link copied',
  },

  connected: {
    sentence: 'Connected to Astrid',
  },

  stopped: {
    title: 'Astrid stopped',
    sentence: 'Start it again on this computer and this page carries on. Your changes are kept.',
  },

  restarted: {
    title: 'Astrid restarted',
    sentence: 'Reload to carry on. Your changes are kept.',
    reload: 'Reload',
  },

  loadFailed: {
    title: "Couldn't load this timeline",
    sentence: "Astrid on this computer didn't answer. Start it and try again.",
    button: 'Try again',
    retrying: 'Trying again…',
  },

  agent: {
    copySetup: 'Copy setup steps for your agent',
    copy: 'Copy steps for your agent',
    copied: 'Copied',
    pasteNext: 'Now paste them into your agent.',
    copyFailed: 'Copy these steps and paste them into your agent.',
    instructions: (pageOrigin, variant) => {
      const prefix = pageOrigin === DEFAULT_HOSTED_ORIGIN ? '' : `ASTRID_APP_LOOPBACK_ORIGIN=${pageOrigin} `;
      return [
        `Please start Astrid on this computer so the page open at ${pageOrigin} can connect to it.`,
        'Keep any existing installation, profile, data root and workspace as they are. Do not reset, reinstall over or delete anything.',
        ...(variant === 'restart'
          ? [`Astrid changed since this page connected. If ${COMMANDS.app} is running, stop it before step 2.`]
          : []),
        [
          `1. Start Astrid's Runtime: ${COMMANDS.runtime}`,
          '   If it is already running, leave it running.',
          `   If the command is not found, Astrid is not installed here yet: follow the install guide (${COMMANDS.installUrl}), then come back to this step.`,
          `2. In the Astrid app checkout (the astrid-app repository), run: ${prefix}${COMMANDS.app}`,
          `   If it is already running but never printed "Open ${pageOrigin}", stop it and start it again this way.`,
          '   If it says another program is in the way, do not stop that program; report the details line it prints.',
          `3. Leave both running, and report back once ${COMMANDS.app} prints "Open ${pageOrigin}". The page connects by itself; it does not need a reload.`,
        ].join('\n'),
      ].join('\n\n');
    },
  },

  composeDisabled: "Making new images isn't on this page yet.",

  agentChatDisabled: "Agent chat isn't on this page yet.",

  openApp: 'Open the full editor',
};

/**
 * CP3's compose line on the hosted build (a gateway origin is configured), `null` same-origin. The one rule
 * the compose controls, their submit handlers and the task-creation library all read, so the composer route,
 * which the gateway does not serve, is never requested from the hosted page.
 */
export function composeDisabledReason(): string | null {
  return runtimeOrigin() !== '' ? RUNTIME_CONNECTION_COPY.composeDisabled : null;
}

/**
 * The agent chat line on the hosted build, `null` same-origin. The gateway never serves the ACP routes, so
 * on the hosted page chat is not mounted and its project-chat routes are never requested.
 */
export function agentChatDisabledReason(): string | null {
  return runtimeOrigin() !== '' ? RUNTIME_CONNECTION_COPY.agentChatDisabled : null;
}
