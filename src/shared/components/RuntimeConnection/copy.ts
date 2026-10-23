import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { installBrowserName } from '@/pages/Home/installScenario.ts';
import { detectPlatform } from '@/shared/hooks/platformInstall/platformDetection.ts';

/**
 * Every word the hosted build's connection gate shows. The panel, the restart cards,
 * the status container and the disabled compose controls render from this object and nothing else, so the wording is
 * reviewed in one place.
 *
 * Rules for this file:
 * - Screen headings, body text, command lines and Copy labels live here.
 * - Routine recovery text says Astrid; first-run explanation names Runtime so people understand what they are connecting.
 * - Straight apostrophes only: the journey matches `Astrid isn't running` exactly.
 * - Gate states name their screens: connecting, blocked, set_up, not_running, update_needed and connected.
 *   Permission, pending and phone screens come from browser context. Polling never adds a checking indicator.
 * - The setup, repair and update screens all show the command that matches the state and OS, and nothing about opening a terminal.
 * - Each phrase the journey looks for (`tests/e2e/local/direct-journey.spec.ts`) appears in one element of its
 *   panel only, so a text locator finds exactly one match.
 * - The browser a card names is a `{browser}` placeholder, filled by `withBrowser` from the landing page's browser detection.
 * - No gateway literal (`127.0.0.1:<port>`, `/api/...`): those live in `connection.ts`.
 */

/** The browser's name goes where a card says `{browser}`: the one the landing page's install dialog detected. */
const BROWSER_PLACEHOLDER = '{browser}';

/** `text` with every `{browser}` filled in (Chrome or Edge); the browser is detected once per call unless given. */
export function withBrowser(text: string, browser: string = installBrowserName()): string {
  return text.split(BROWSER_PLACEHOLDER).join(browser);
}

/** Product install and update commands. */
export const ASTRID_COMMANDS = {
  macLinux: 'curl -fsSL https://astrid.haus/install | sh',
  windows: 'irm https://astrid.haus/install.ps1 | iex',
  /** For an agent in Git Bash or another non-PowerShell shell on Windows. */
  windowsAgent: 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astrid.haus/install.ps1 | iex"',
  macLinuxUpdate: 'curl -fsSL https://astrid.haus/install | sh -s -- --update',
  windowsUpdate: '& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update',
} as const;

export type CommandMode = 'install' | 'update';

export function installCommand(mode: CommandMode): string {
  const windows = detectPlatform() === 'windows';
  if (mode === 'update') return windows ? ASTRID_COMMANDS.windowsUpdate : ASTRID_COMMANDS.macLinuxUpdate;
  return windows ? ASTRID_COMMANDS.windows : ASTRID_COMMANDS.macLinux;
}

const SETUP_GUIDE_URL = 'https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md';

/** The two ways to update, since this page can't tell an installer install from source checkouts. */
export const UPDATE_ROUTES = {
  installer: (command: string) => `If you installed Astrid with the installer: ${command}`,
  source: "If you run Astrid from source checkouts: update those checkouts to their main branches and restart Astrid. Don't run the installer over them.",
} as const;

/** A complete handoff: retain an existing workspace and diagnose failures before retrying. */
export function agentInstructions(mode: CommandMode, pageOrigin: string): string {
  const windows = detectPlatform() === 'windows';
  const command = installCommand(mode);
  return [
    `Please ${mode === 'update' ? 'update my existing Astrid installation' : 'set up or restart Astrid on this computer'} so the page at ${pageOrigin} can connect. Do the work yourself and verify the result.`,
    'First inspect the existing installation, running services, profile, selected workspace and data root. Preserve my projects, media, credentials and agent instructions. Do not reset or delete my workspace, or replace it with an empty one.',
    "Use the current official Astrid installer; read it before running it. The installer adopts an existing workspace itself; don't run workspace or migration commands by hand. Do not bypass ownership guards or overwrite a directory just because the installer refuses it.",
    windows && mode === 'install'
      ? `The command offered by this page, in PowerShell:\n${command}\nFrom Git Bash or another shell:\n${ASTRID_COMMANDS.windowsAgent}\nInstall from Windows, not inside WSL.`
      : `${mode === 'update' ? 'If you installed Astrid with the installer, the command offered by this page is' : 'The command offered by this page is'}:\n${command}${windows ? '\nInstall from Windows, not inside WSL.' : ''}`,
    mode === 'update'
      ? `${UPDATE_ROUTES.source} Before running the installer, check whether this computer runs Astrid from source checkouts (for example, a running runtime_protocol from a git checkout). If it does, update those checkouts instead of running the installer.`
      : null,
    'If installation or startup fails, read the log path printed by the installer, diagnose the actual cause and resolve it before retrying. Keep the existing workspace selection and data root connected; do not infer that no installation exists merely because the browser cannot reach it.',
    `The installer verifies Astrid and opens astrid.haus. Tell me to choose Allow if Chrome or Edge asks, and confirm Astrid shows Connected. Setup guide: ${SETUP_GUIDE_URL}`,
  ].filter((part): part is string => part !== null).join('\n\n');
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
  readonly firstRun: { readonly title: string; readonly sentence: string };
  readonly commands: typeof ASTRID_COMMANDS;
  /** Accessible name for the panel region. */
  readonly panelLabel: string;
  /** The quiet status line along the bottom of a card that waits for something done elsewhere; it becomes `connected`. */
  readonly waiting: string;
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
  /** Lead-in above the update screen when a chat reply from this computer's Astrid is out of date. */
  readonly chatNeedsUpdate: string;
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
    readonly commandCopy: string;
    readonly commandCopied: string;
    readonly terminalAlternative: string;
    /** Update only, where the installer is one of two routes. */
    readonly terminalAlternativeUpdate: string;
  };
  /** Next to the compose controls the hosted build disables. */
  readonly composeDisabled: string;
}

export const RUNTIME_CONNECTION_COPY: RuntimeConnectionCopy = {
  firstRun: {
    title: 'Connect your machine',
    sentence: "Astrid's Runtime runs on your machine. Connect it to work with your files and generate using your own GPU or connected providers.",
  },
  commands: ASTRID_COMMANDS,

  panelLabel: 'Connect to Astrid',

  waiting: 'Waiting for Astrid on this computer…',

  connecting: {
    sentence: 'Looking for Astrid on this computer…',
  },

  permission: {
    title: 'Connect to Astrid on this computer',
    sentence: '{browser} will ask about devices on your network. Choose Allow so this page can reach Astrid.',
    connect: 'Connect',
    pending: {
      title: 'Choose Allow in {browser}',
      sentence: '{browser} is asking at the top left of this window.',
      /** The word on the arrow that points at the prompt, as the install dialog's says "Up here". */
      pointer: 'Up here',
    },
  },

  blocked: {
    title: 'Allow Astrid in {browser}',
    sentence: '{browser} is blocking this page from reaching Astrid.',
    steps: [
      'Click the icon at the left of the address bar, then Site settings.',
      'Set Local network access to Allow.',
    ],
    footer: 'Come back here and it opens by itself.',
  },

  setUp: {
    title: 'Connect Astrid on this computer',
    sentence: 'Your coding agent can set Astrid up, or reconnect the one you have.',
  },

  notRunning: {
    title: "Astrid isn't running",
    sentence: 'Give these instructions to your coding agent to start it again. Your work is kept.',
  },

  updateNeeded: {
    title: 'Update Astrid',
    sentence: 'This page needs a newer Astrid. Give these instructions to your coding agent to update it.',
  },

  /** Lead-in above the shared update screen when a chat reply from this computer's Astrid is out of date. */
  chatNeedsUpdate: 'Chat on this computer is older than this page.',

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
    sentence: 'Give these instructions to your coding agent to start Astrid again. Your changes are kept.',
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
    copy: 'Copy agent instructions',
    copied: 'Copied. Paste them into your agent.',
    pasteNext: 'Steps copied. Paste them into your agent.',
    copyFailed: "Copying didn't work. Select the text below and copy it.",
    commandCopy: 'Copy command',
    commandCopied: 'Command copied',
    terminalAlternative: 'Or run this yourself in a terminal:',
    terminalAlternativeUpdate: 'If you installed Astrid with the installer, run this in a terminal:',
  },

  composeDisabled: "Making new images isn't on this page yet.",
};

/**
 * The compose line on the hosted build (a gateway origin is configured), `null` same-origin. The one rule
 * the compose controls, their submit handlers and the task-creation library all read, so the composer route,
 * which the gateway does not serve, is never requested from the hosted page.
 */
export function composeDisabledReason(): string | null {
  return runtimeOrigin() !== '' ? RUNTIME_CONNECTION_COPY.composeDisabled : null;
}
