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
 * - Gate states name their screens: connecting, blocked, set_up, not_running, restart_needed and connected.
 *   Permission, pending and phone screens come from browser context. Polling never adds a checking indicator.
 * - One screen per thing a person can do: setup finds an install first; start never installs again.
 * - Each phrase the journey looks for (`tests/e2e/local/direct-journey.spec.ts`) appears in one element of its
 *   panel only, so a text locator finds exactly one match.
 * - The browser a card names is a `{browser}` placeholder, filled by `withBrowser` from the landing page's browser detection.
 * - No gateway literal (`127.0.0.1:<port>`, `/api/...`): those live in `connection.ts`.
 */

/** The browser's name goes where a card says `{browser}`: the one the landing page's install dialog detected. */
export const BROWSER_PLACEHOLDER = '{browser}';

/** `text` with every `{browser}` filled in (Chrome or Edge); the browser is detected once per call unless given. */
export function withBrowser(text: string, browser: string = installBrowserName()): string {
  return text.split(BROWSER_PLACEHOLDER).join(browser);
}

/** Commands and paths the agent block names. Plain strings. */
const COMMANDS = {
  app: 'npm run dev:local',
  /** The installer guide, in the astrid-agent repository: a full URL, so a reader without the repo can open it. */
  installUrl: 'https://github.com/banodoco/astrid-agent/blob/main/docs/setup/local-source-install.md',
} as const;

/**
 * How an agent finds an Astrid that is already set up, before anything is installed. A browser only knows it hasn't
 * found Astrid: a cleared browser, a private window or another browser looks like a new computer.
 * - `install`: the installer's folder (agent, Runtime and the app's launcher), the setup that serves the hosted page.
 *   Its install.json carries `"schema": "astrid.local-source-install.v1"`; `-exec grep {} +` survives spaces in paths.
 * - `checkout`: a developer checkout of astrid-app (package.json's name is generic, so the launcher file marks it).
 *   Searched only when there is no install, because every install holds a copy of the app under sources/app.
 * - `runtimeDataFolder`, `runtimeCommand`: signs that Astrid has run here without either (the Runtime's default data
 *   folder on macOS, and its command). Neither starts the bridge the page needs, and a fresh install would open an
 *   empty workspace beside the person's work, so the setup block asks instead of installing.
 */
export const AGENT_SEARCHES = {
  install: 'find ~ -maxdepth 6 -name install.json -not -path "*/node_modules/*" -exec grep -l astrid.local-source-install {} + 2>/dev/null',
  checkout: 'find ~ -maxdepth 6 -path "*/scripts/dev-local-workspace.mjs" -not -path "*/node_modules/*" 2>/dev/null',
  runtimeDataFolder: '~/Library/Application Support/Astrid Runtime',
  runtimeCommand: 'astrid-runtime',
} as const;

/** The origin `npm run dev:local` opens for by default (`config/hosted-origin.json`); any other needs `ASTRID_APP_LOOPBACK_ORIGIN`. */
const DEFAULT_HOSTED_ORIGIN: string | null = hostedOrigin.origin;

/** Setup finds an install first; start is for Astrid we already know is installed. */
export type AgentInstructionsVariant = 'setup' | 'start';

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
  /**
   * Nothing answers and this browser has never connected. The browser can't tell a new computer from a cleared
   * browser, a private window or another browser, so the screen never says Astrid isn't installed.
   */
  readonly setUp: Message & {
    /** The second line under the title, for someone who is set up: as prominent as the sentence. */
    readonly installed: string;
    /** The quiet line under the button: the other way to set up. `linkText` links to `COMMANDS.installUrl`. */
    readonly footer: { readonly before: string; readonly linkText: string; readonly after: string };
  };
  /** Nothing answers on a return visit, or the gateway answered on this page. */
  readonly notRunning: Message;
  /** Astrid changed while it was running: only a restart helps. */
  readonly restartNeeded: Message;
  /** A phone can never reach Astrid on a computer: the link goes there instead. */
  readonly phone: Message & { readonly button: string; readonly copied: string };
  /** Screen-reader text of the status container while connected, and the line App settings shows then. */
  readonly connected: { readonly sentence: string };
  /**
   * Connected, but Astrid on this computer and this page speak different versions, so the page can't use it (App
   * settings). A schema digest has no direction, so the sentence never says which one is older.
   */
  readonly updateNeeded: Message;
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
    /** The line under the button once the steps are copied; stays until the screen changes. */
    readonly pasteNext: string;
    /** Shown with the steps in a text box, only when the clipboard write failed. */
    readonly copyFailed: string;
    /** One block an agent can act on. `pageOrigin` is `window.location.origin`, the origin the gateway must accept. */
    readonly instructions: (pageOrigin: string, variant: AgentInstructionsVariant) => string;
  };
  /** Next to the compose controls the hosted build disables (card A2.X). */
  readonly composeDisabled: string;
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
    sentence: '{browser} is blocking this page from reaching Astrid on your computer.',
    steps: [
      'Click the icon at the left of the address bar, then Site settings.',
      'Set Local network access to Allow.',
    ],
    footer: 'Come back here and it opens by itself.',
  },

  setUp: {
    title: 'Set up Astrid on this computer',
    sentence: "This browser hasn't found Astrid here, so it looks like you might not be set up yet.",
    installed: 'Already installed? Start Astrid and this page opens by itself.',
    footer: {
      before: 'Or set it up yourself with ',
      linkText: 'the install guide',
      after: '.',
    },
  },

  notRunning: {
    title: "Astrid isn't running",
    sentence: 'Start Astrid on this computer and this page opens by itself.',
  },

  restartNeeded: {
    title: 'Astrid needs a restart',
    sentence: 'Astrid on this computer changed while it was running. Restart it and this page opens by itself.',
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

  updateNeeded: {
    title: 'Astrid needs an update',
    sentence: "Astrid on this computer doesn't match this page. Ask your agent to update it.",
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
    // No promise that it loads by itself: the automatic retries stop after a few tries, and the button is the way on.
    // A stopped Astrid shows the stopped card instead of this one, so the sentence doesn't ask anyone to start it.
    sentence: "Astrid on this computer didn't answer in time.",
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
        variant === 'setup'
          ? `Please start Astrid on this computer so the page open at ${pageOrigin} can connect to it. It may already be set up here, so look before you install anything, and never reset, reinstall over or delete what you find.`
          : `Please start Astrid on this computer so the page open at ${pageOrigin} can connect to it. It's already set up here, so don't install it again, and never reset or delete what you find.`,
        '',
        '1. Look for an Astrid install:',
        `     ${AGENT_SEARCHES.install}`,
        '   Each result is <folder>/install.json. Start that install with:',
        `     ${prefix}<folder>/start`,
        "   or, if it's an older install with no start file:",
        `     ${prefix}<folder>/with-env npm --prefix <folder>/sources/app run dev:local`,
        "2. Only if there's no install, look for a developer checkout of astrid-app:",
        `     ${AGENT_SEARCHES.checkout}`,
        '   Each result is <checkout>/scripts/dev-local-workspace.mjs. Start that checkout by running this inside it:',
        `     ${prefix}${COMMANDS.app}`,
        variant === 'setup'
          ? `3. If you find more than one, ask me which to start. If you find neither, but ${AGENT_SEARCHES.runtimeDataFolder} exists or ${AGENT_SEARCHES.runtimeCommand} is on your PATH, Astrid has run here before: ask me how I start it. Otherwise install Astrid by following ${COMMANDS.installUrl}. Its last step starts it.`
          : '3. If you find more than one, ask me which to start. If you find neither, ask me where Astrid is.',
        `4. Astrid keeps running until it's stopped, so start it where it can keep running and don't wait for it to exit. Once it prints "Open ${pageOrigin}", tell me. The page connects by itself.`,
        '5. If it says another Astrid is already running, stop that one and run the command again. If it stops with any other message, tell me that message and the "Details:" line under it.',
      ].join('\n');
    },
  },

  composeDisabled: "Making new images isn't on this page yet.",
};

/**
 * CP3's compose line on the hosted build (a gateway origin is configured), `null` same-origin. The one rule
 * the compose controls, their submit handlers and the task-creation library all read, so the composer route,
 * which the gateway does not serve, is never requested from the hosted page.
 */
export function composeDisabledReason(): string | null {
  return runtimeOrigin() !== '' ? RUNTIME_CONNECTION_COPY.composeDisabled : null;
}
