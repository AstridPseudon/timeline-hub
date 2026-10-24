import { entryFor, readWelcomePhase } from '@/app/onboarding/welcomeProgress.ts';
import {
  classifyBrowserEntry,
  prefersAppEntry,
  resolveInstallerConnectEntry,
  resolveReturningAppEntry,
} from '@/app/entryClassification.ts';
import { setRuntimeOrigin } from '@/integrations/runtime/connection.ts';
import { releaseBootLayerWhenReady } from '@/app/bootLayer.ts';
import { migrateAstridBrowserStorage } from '@/migrations/astridRenameBrowserMigration.ts';

async function main(): Promise<void> {
  // First, before any module that can build a Runtime client or media URL is imported: the hosted
  // build points every Runtime and Astrid base at the loopback gateway (`connection.ts`).
  setRuntimeOrigin(import.meta.env);

  const rootElement = document.getElementById('root');
  if (!rootElement) {
    throw new Error("Failed to render app: element with id 'root' was not found.");
  }

  const currentUrl = new URL(window.location.href);
  const installConnectEntry = resolveInstallerConnectEntry(currentUrl);
  if (installConnectEntry) {
    window.history.replaceState(window.history.state, '', installConnectEntry);
  }

  const returningAppEntry = installConnectEntry
    ? null
    : resolveReturningAppEntry(new URL(window.location.href), prefersAppEntry());
  if (returningAppEntry) {
    window.history.replaceState(window.history.state, '', returningAppEntry);
  }

  const owner = classifyBrowserEntry(new URL(window.location.href));
  if (owner === 'public') {
    const { renderPublicEntry } = await import('@/app/publicBootstrap.tsx');
    clearPreloadReloadAfterRender(rootElement);
    renderPublicEntry(rootElement);
    releaseBootLayerWhenReady(rootElement);
    return;
  }

  await startApp(rootElement);
}

const PRELOAD_RELOAD_FLAG = 'astrid:preload-reloaded';
/** A render counts as a good boot only if it stays free of chunk failures this long. */
const PRELOAD_GUARD_SETTLE_MS = 10_000;
let preloadErrorSeen = false;

/**
 * Keep the reload guard until the render has committed AND stayed free of chunk-load failures for a
 * settle period. Clearing at first paint would loop: a lazy chunk that is still missing fails right
 * after the shell renders, so each reload would clear the guard and reload again.
 */
function clearPreloadReloadAfterRender(rootElement: HTMLElement): void {
  const existingChildren = new Set(rootElement.children);
  const observer = new MutationObserver(() => clear());
  const clear = () => {
    const renderedApp = [...rootElement.children].some(
      (child) => !existingChildren.has(child) && child.getAttribute('role') !== 'alert',
    );
    if (!renderedApp) return;
    observer.disconnect();
    window.setTimeout(() => {
      if (preloadErrorSeen) return;
      try {
        sessionStorage.removeItem(PRELOAD_RELOAD_FLAG);
      } catch {
        // Storage can be unavailable; the current page is still usable.
      }
    }, PRELOAD_GUARD_SETTLE_MS);
  };
  observer.observe(rootElement, { childList: true, subtree: true });
  clear();
}

/**
 * A hashed chunk that 404s after a redeploy: reload once for the new build. The session flag keeps a
 * chunk that is still missing after the reload from looping; then the error reaches the error boundary.
 */
function handlePreloadError(event: Event): void {
  preloadErrorSeen = true;
  try {
    if (sessionStorage.getItem(PRELOAD_RELOAD_FLAG)) return;
    sessionStorage.setItem(PRELOAD_RELOAD_FLAG, '1');
  } catch {
    return; // Without storage we cannot guard against a loop, so do not reload.
  }
  event.preventDefault();
  window.location.reload();
}
window.addEventListener('vite:preloadError', handlePreloadError);

function showStartupFailure(rootElement: HTMLElement, error: unknown): void {
  console.error('Astrid failed to start', error);
  const container = document.createElement('main');
  container.setAttribute('role', 'alert');
  container.className = 'grid min-h-screen place-content-center gap-3 p-6 text-foreground';

  const title = document.createElement('h1');
  title.textContent = 'Astrid could not start';
  title.className = 'text-xl font-semibold';

  const detail = document.createElement('p');
  detail.textContent = 'Astrid may have just been updated. Reload to try again.';
  detail.className = 'max-w-prose text-muted-foreground';

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = 'Reload';
  button.className = 'w-fit rounded-md bg-primary px-4 py-2 text-primary-foreground';
  button.addEventListener('click', () => window.location.reload());

  container.append(title, detail, button);
  rootElement.replaceChildren(container);
}

function showMigrationFailure(
  rootElement: HTMLElement,
  store: string,
  retry: () => Promise<void>,
): void {
  const container = document.createElement('main');
  container.setAttribute('role', 'alert');
  container.className = 'grid min-h-screen place-content-center gap-3 p-6 text-foreground';

  const title = document.createElement('h1');
  title.textContent = 'Astrid could not prepare browser storage';
  title.className = 'text-xl font-semibold';

  const detail = document.createElement('p');
  detail.textContent = `Migration failed for ${store}. Your existing browser data is preserved. Retry to try again.`;
  detail.className = 'max-w-prose text-muted-foreground';

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = 'Retry migration';
  button.className = 'w-fit rounded-md bg-primary px-4 py-2 text-primary-foreground';
  button.addEventListener('click', () => {
    button.disabled = true;
    button.textContent = 'Retrying…';
    void retry();
  });

  container.append(title, detail, button);
  rootElement.replaceChildren(container);
}

async function startApp(rootElement: HTMLElement): Promise<void> {
  const migration = await migrateAstridBrowserStorage();
  if (!migration.success) {
    showMigrationFailure(rootElement, migration.store, () => startApp(rootElement));
    releaseBootLayerWhenReady(rootElement);
    return;
  }

  const welcomeEntry = entryFor(new URL(window.location.href), readWelcomePhase());
  if (welcomeEntry !== 'editor') {
    const { renderWelcome } = await import('@/app/onboarding/welcomeBootstrap.tsx');
    clearPreloadReloadAfterRender(rootElement);
    renderWelcome(rootElement, welcomeEntry);
    releaseBootLayerWhenReady(rootElement);
    return;
  }

  const [
    { renderApp },
    { initializeVideoEditorExtensionRuntime },
    { initializeWorkspaceRuntimeIdentity },
  ] = await Promise.all([
    import('@/app/bootstrap'),
    import('@/tools/video-editor/browser/initializeVideoEditorExtensionRuntime.ts'),
    import('@/integrations/runtime/client.ts'),
  ]);
  initializeVideoEditorExtensionRuntime();
  await initializeWorkspaceRuntimeIdentity();
  clearPreloadReloadAfterRender(rootElement);
  renderApp(rootElement);
  releaseBootLayerWhenReady(rootElement);
}

void main().catch((error: unknown) => {
  const rootElement = document.getElementById('root');
  if (!rootElement) {
    console.error('Astrid failed to start', error);
    return;
  }
  showStartupFailure(rootElement, error);
  releaseBootLayerWhenReady(rootElement);
});
