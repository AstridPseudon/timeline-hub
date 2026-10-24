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

// Shown before the app's CSS loads: keep in step with index.html's fallback
function showFailureCard(rootElement: HTMLElement, { title: titleText, sentence, button: buttonText, onClick }: {
  title: string;
  sentence: string;
  button: string;
  onClick: () => void;
}): HTMLButtonElement {
  const container = document.createElement('main');
  container.setAttribute('role', 'alert');
  container.style.cssText = 'min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;text-align:center;color:var(--boot-ink,#2b2724);font-family:Inter,system-ui,-apple-system,sans-serif';
  const width = document.createElement('div');
  width.style.maxWidth = '420px';
  const icon = document.createElement('img');
  icon.src = '/astrid-app-icon-192.png';
  icon.alt = '';
  icon.width = 76;
  icon.height = 76;
  icon.style.cssText = 'display:block;margin:0 auto';

  const title = document.createElement('h1');
  title.textContent = titleText;
  title.style.cssText = "margin:10px 0 4px;font:400 25px/1.2 Georgia,'Times New Roman',serif";

  const detail = document.createElement('p');
  detail.textContent = sentence;
  detail.style.cssText = 'margin:0 0 16px;font-size:14px;line-height:24px;opacity:.72';

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = buttonText;
  button.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;height:44px;padding:0 28px;border-radius:12px;background:var(--boot-ink,#2b2724);color:var(--boot-background,#faf8f5);font-size:14px;font-weight:500;text-decoration:none;border:0;cursor:pointer;font-family:inherit';
  button.addEventListener('click', onClick);

  width.append(icon, title, detail, button);
  container.append(width);
  rootElement.replaceChildren(container);
  return button;
}

function showStartupFailure(rootElement: HTMLElement, error: unknown): void {
  console.error('Astrid failed to start', error);
  showFailureCard(rootElement, {
    title: 'Astrid could not start',
    sentence: 'It may have just been updated. Reload to try again.',
    button: 'Reload',
    onClick: () => window.location.reload(),
  });
}

function showMigrationFailure(rootElement: HTMLElement, store: string, retry: () => Promise<void>): void {
  const button = showFailureCard(rootElement, {
    title: 'Astrid could not prepare browser storage',
    sentence: `Migration failed for ${store}. Your existing browser data is preserved. Retry to try again.`,
    button: 'Retry migration',
    onClick: () => {
      button.disabled = true;
      button.textContent = 'Retrying…';
      void retry();
    },
  });
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
