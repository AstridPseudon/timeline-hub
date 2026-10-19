import { DEMO_PROJECT_ID, DEMO_TIMELINE_ID } from '@/shared/dev/devSession.ts';

export type BrowserEntryOwner = 'public' | 'app';

const PUBLIC_WEB_PATHS = new Set(['/', '/home']);
/** Public pages served by the dedicated public entry in every build. */
const PUBLIC_PAGE_PATHS = new Set(['/', '/home', '/vision']);

export function isRecognizedOAuthCallbackUrl(url: URL): boolean {
  if (!PUBLIC_WEB_PATHS.has(url.pathname)) {
    return false;
  }
  const hash = url.hash.startsWith('#') ? url.hash.slice(1) : url.hash;
  if (!hash) {
    return false;
  }
  const parameters = new URLSearchParams(hash);
  return Boolean(parameters.get('access_token') && parameters.get('refresh_token'));
}

export function classifyBrowserEntry(
  url: URL,
): BrowserEntryOwner {
  if (isRecognizedOAuthCallbackUrl(url)) {
    return 'app';
  }
  if (PUBLIC_PAGE_PATHS.has(url.pathname)) {
    return 'public';
  }
  return 'app';
}

/**
 * The hosted build is the one compiled with a Runtime origin (`VITE_RUNTIME_ORIGIN`, `connection.ts`). It talks to the
 * visitor's own Runtime, which has no `demo-project`: the demo slug there is a stale explicit URL and shows "Project
 * not found". The bare editor route lets the editor pick the last-opened (or newest) project by itself.
 */
function isHostedBuild(): boolean {
  const origin = (import.meta.env as { VITE_RUNTIME_ORIGIN?: unknown }).VITE_RUNTIME_ORIGIN;
  return typeof origin === 'string' && origin.trim() !== '';
}

/**
 * Where a returning visitor lands once they have chosen the app over the landing page: the local
 * editor. Other app routes send anyone without a signed-in session back to /home, so they would
 * bounce straight back here.
 */
export const APP_ENTRY_PATH = isHostedBuild()
  ? '/tools/video-editor'
  : `/tools/video-editor?project=${DEMO_PROJECT_ID}&timeline=${DEMO_TIMELINE_ID}`;

/** Installer links arrive on the public root, but `?connect=1` must reach the app's Runtime gate. */
export function resolveInstallerConnectEntry(url: URL): string | null {
  if (url.pathname !== '/' || url.searchParams.get('connect') !== '1') return null;
  const target = new URL(APP_ENTRY_PATH, url.origin);
  const incomingKeys = new Set(url.searchParams.keys());
  for (const key of incomingKeys) target.searchParams.delete(key);
  url.searchParams.forEach((value, key) => target.searchParams.append(key, value));
  return `${target.pathname}${target.search}${url.hash}`;
}
const APP_ENTRY_PREFERENCE_KEY = 'astrid:prefers-app';

/** Remember that this browser chose the app (installed it, or asked to use it here). */
export function rememberAppEntryPreference(): void {
  try {
    localStorage.setItem(APP_ENTRY_PREFERENCE_KEY, '1');
  } catch {
    // Storage can be unavailable (private windows, blocked site data); the landing page still works.
  }
}

function isRunningInstalled(): boolean {
  try {
    return window.matchMedia('(display-mode: standalone)').matches
      || window.matchMedia('(display-mode: fullscreen)').matches
      || (navigator as Navigator & { standalone?: boolean }).standalone === true;
  } catch {
    return false;
  }
}

export function prefersAppEntry(): boolean {
  if (isRunningInstalled()) return true;
  try {
    return localStorage.getItem(APP_ENTRY_PREFERENCE_KEY) === '1';
  } catch {
    return false;
  }
}

/**
 * Installing from the browser doesn't open the app at its start page: Chrome moves the tab being viewed
 * (usually the landing page) into the new app window, with no reload. When a public page finds itself
 * running as the installed app this way, it hands over to the editor.
 */
export function followIntoInstalledApp(): void {
  let query: MediaQueryList;
  try {
    query = window.matchMedia('(display-mode: standalone)');
  } catch {
    return;
  }
  query.addEventListener('change', () => {
    if (!isRunningInstalled()) return;
    rememberAppEntryPreference();
    window.location.replace(APP_ENTRY_PATH);
  });
}

/**
 * Once someone has installed Astrid or chosen to use it in the browser, the site root opens the app
 * instead of the landing page. /home always shows the landing page.
 */
export function resolveReturningAppEntry(url: URL, prefersApp: boolean): string | null {
  if (!prefersApp || url.pathname !== '/' || isRecognizedOAuthCallbackUrl(url)) return null;
  return APP_ENTRY_PATH;
}
