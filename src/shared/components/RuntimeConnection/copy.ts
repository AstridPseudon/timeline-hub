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

/** The fully local setup: the editor's source, how to start it, and where it serves. */
export const LOCAL_SETUP = {
  macLinuxInstaller: ASTRID_COMMANDS.macLinux,
  windowsInstaller: ASTRID_COMMANDS.windows,
  repoUrl: 'https://github.com/banodoco/astrid-app',
  cloneCommand: 'git clone https://github.com/banodoco/astrid-app.git',
  startCommand: 'npm run dev:local',
  /** The first-open address resumes at connection: `entryFor` sends `?connect=1` straight there. */
  openUrl: 'http://127.0.0.1:5180/tools/video-editor?connect=1',
} as const;

export type WindowMode = 'app-window' | 'browser-tab';

export function localSetupInstructions(): string {
  const L = LOCAL_SETUP;
  return [
    'Please set up Astrid to run fully on this computer, including the editor, so I can change Astrid itself. Do the work yourself and verify the result.',
    `1. Install or repair Astrid with the official installer. Fetch and read the script before running it. macOS/Linux: \`${L.macLinuxInstaller}\`. Windows PowerShell: \`${L.windowsInstaller}\`. Keep my existing workspace, projects, media, credentials, and agent instructions. The installer may open astrid.haus; finish this setup in the local editor below.`,
    `2. Get the editor's code from ${L.repoUrl}. Install Git and Node.js 20.19 or newer in the Node 20 release line if needed. Clone with \`${L.cloneCommand}\`, then \`cd astrid-app\` and \`npm ci\`. If a clone already exists, preserve its changes and update it to \`main\` without discarding work; use \`git pull --ff-only origin main\` when it can fast-forward and resolve any divergence before continuing.`,
    `3. In that clone, run \`${L.startCommand}\` in a terminal that stays open. This starts the source editor on port 5180, checks the installed Runtime and selected workspace, and connects through the editor's own server. Keep the existing hosted door for https://astrid.haus; do not change its origin or turn it off. If the launcher reports a problem, diagnose it and repair through the official installer when needed. Do not delete or replace my workspace or credentials.`,
    `4. Open ${L.openUrl} in my browser and confirm it shows Connected. This first-open address resumes at connection because I already completed the tour. Verify \`/api/runtime/v1/health\` and \`/api/runtime/v1/realm\` through http://127.0.0.1:5180 and confirm the editor uses my existing Runtime workspace. No browser local-network permission is needed for this route. Do not claim success if any check could not be run; tell me the actual result.`,
    `5. Tell me the absolute path of the clone so you or I can edit it. Source edits appear through Vite's normal development workflow. To start later: \`cd\` to that clone and run \`${L.startCommand}\`, then open the local address it prints. To stop the editor: Ctrl+C in its terminal. That stops the editor and proxy, plus any Runtime it started; a Runtime it attached to keeps running for astrid.haus. To update the editor: stop it, save or commit local source changes, then run \`git pull --ff-only origin main\`, \`npm ci\`, and \`${L.startCommand}\`. To update the Runtime and agent: use \`${ASTRID_COMMANDS.macLinuxUpdate}\` on macOS/Linux, or \`${ASTRID_COMMANDS.windowsUpdate}\` in Windows PowerShell, then restart the editor. Read the update script before running it. The local editor can open offline after its dependencies are installed; online models and providers still need internet.`,
  ].join('\n');
}

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
export function agentInstructions(mode: CommandMode, pageOrigin: string, windowMode: WindowMode = 'browser-tab'): string {
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
    `When Astrid is running, open it ${windowMode === 'app-window' ? 'in the installed Astrid app if it exists, otherwise https://astrid.haus in my browser' : 'at https://astrid.haus in my browser'}.`,
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
    readonly allowTitle: string;
    readonly allowDetails: string;
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
  /** Connected, and the health check answers too slowly: Astrid is running under load. The card clears itself. */
  readonly busy: Message;
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
    title: 'Connect to Astrid on this computer',
    sentence: '{browser} will ask to reach your computer. Choose Allow.',
  },
  commands: ASTRID_COMMANDS,

  panelLabel: 'Connect to Astrid',

  waiting: 'Waiting for Astrid on this computer…',

  connecting: {
    sentence: 'Looking for Astrid on this computer…',
  },

  permission: {
    title: 'Connect to Astrid on this computer',
    sentence: '{browser} will ask to reach your computer. Choose Allow.',
    connect: 'Connect',
    allowTitle: 'What does this allow?',
    allowDetails: "This page can talk to Astrid running on your computer, and nothing else. Astrid only lets it work with your Astrid projects, media and jobs. It can't open your other files or apps. Chat messages go to your own agent on this computer. Your work never passes through our servers.",
    pending: {
      title: 'Choose Allow in {browser}',
      sentence: 'The prompt is at the top left of this window.',
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

  busy: {
    title: 'Astrid is busy',
    sentence: "It's still running and will catch up. Your changes are kept.",
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
