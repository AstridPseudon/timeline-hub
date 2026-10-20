import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { installBrowserName } from '@/pages/Home/installScenario.ts';
import { detectPlatform } from '@/shared/hooks/platformInstall/platformDetection.ts';

/**
 * Every word the hosted build's connection gate shows (Plan A, design D3; card CP3). The panel, the restart cards,
 * the status container and the disabled compose controls render from this object and nothing else, so the wording is
 * reviewed in one place.
 *
 * Rules for this file:
 * - Screen headings, body text, command lines and Copy labels live here.
 * - Visible text says Astrid and never names a Runtime, workspace, port or command outside the code block.
 * - Straight apostrophes only: the journey matches `Astrid isn't running` exactly.
 * - Gate states name their screens: connecting, blocked, set_up, not_running, update_needed and connected.
 *   Permission, pending and phone screens come from browser context. Polling never adds a checking indicator.
 * - The setup, repair and update screens all show the command that matches the state and OS.
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

/** Product install and update commands. */
export const ASTRID_COMMANDS = {
  macLinux: 'curl -fsSL https://astrid.haus/install | sh',
  windows: 'irm https://astrid.haus/install.ps1 | iex',
  macLinuxUpdate: 'curl -fsSL https://astrid.haus/install | sh -s -- --update',
  windowsUpdate: '& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update',
} as const;

export type CommandMode = 'install' | 'update';

export function installCommand(mode: CommandMode): string {
  const windows = detectPlatform() === 'windows';
  if (mode === 'update') return windows ? ASTRID_COMMANDS.windowsUpdate : ASTRID_COMMANDS.macLinuxUpdate;
  return windows ? ASTRID_COMMANDS.windows : ASTRID_COMMANDS.macLinux;
}

/** The short shell-opening hint shown beside every install, repair and update line. */
export function terminalOpeningHint(): string {
  switch (detectPlatform()) {
    case 'mac': return 'Open Terminal from Applications → Utilities.';
    case 'windows': return 'Open Start and type PowerShell.';
    case 'linux': return 'Open Terminal from your applications menu.';
    default: return 'Open a terminal on your computer.';
  }
}

/** Names the shell that matches the command shown on setup, repair and recovery cards. */
export function withCommandShell(sentence: string): string {
  return detectPlatform() === 'windows' ? sentence.replace('in a terminal', 'in PowerShell') : sentence;
}

/** A heading and the one sentence under it. */
interface Message {
  readonly title: string;
  readonly sentence: string;
}

export interface RuntimeConnectionCopy {
  readonly commands: typeof ASTRID_COMMANDS;
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
  readonly setUp: Message;
  /** Nothing answers on a return visit, or the gateway answered on this page. */
  readonly notRunning: Message;
  readonly updateNeeded: Message;
  /** A phone can never reach Astrid on a computer: the link goes there instead. */
  readonly phone: Message & { readonly button: string; readonly copied: string };
  /** Screen-reader text of the status container while connected, and the line App settings shows then. */
  readonly connected: { readonly sentence: string };
  /** Connected, and the health check stopped answering. The card clears itself when Astrid is back. */
  readonly stopped: Message;
  /** Connected, and Astrid restarted (or changed) under the page. */
  readonly restarted: Message & { readonly reload: string };
  /** The timeline (or the engine connection behind it) would not load on the hosted build: replaces every engineer-worded error. */
  readonly loadFailed: Message & { readonly button: string; readonly retrying: string };
  readonly agent: {
    readonly copy: string;
    readonly copied: string;
    readonly pasteNext: string;
    /** Shown with the command in a text box, only when the clipboard write failed. */
    readonly copyFailed: string;
    readonly note: string;
  };
  /** Next to the compose controls the hosted build disables (card A2.X). */
  readonly composeDisabled: string;
}

export const RUNTIME_CONNECTION_COPY: RuntimeConnectionCopy = {
  commands: ASTRID_COMMANDS,

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
    sentence: "This browser hasn't found Astrid here yet. Run this line in a terminal to set it up, or to start it if it's already installed.",
  },

  notRunning: {
    title: "Astrid isn't running",
    sentence: 'Run this line in a terminal to start it again. It keeps your work as it is. This page opens by itself.',
  },

  updateNeeded: {
    title: 'Update Astrid',
    sentence: 'Astrid on this computer needs an update to work with this page. Run this line in a terminal to update it. It backs up your work first.',
  },

  /** Lead-in above the shared update screen when a chat reply from this computer's Astrid is out of date. */
  chatNeedsUpdate: 'Chat needs this update.',

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
    sentence: 'Run this line in a terminal to start it again. Your changes are kept.',
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
    copy: 'Copy',
    copied: 'Copied',
    pasteNext: 'Steps copied. Paste them into your agent.',
    copyFailed: "Copying didn't work. Select the text below and copy it.",
    note: 'Or paste it into a coding agent to run for you.',
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
