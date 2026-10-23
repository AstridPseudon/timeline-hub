import { shouldShowWelcome } from '@/app/onboarding/welcomeProgress.ts';
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
    renderPublicEntry(rootElement);
    releaseBootLayerWhenReady(rootElement);
    return;
  }

  await startApp(rootElement);
}

function showMigrationFailure(
  rootElement: HTMLElement,
  store: string,
  retry: () => Promise<void>,
): void {
  const container = document.createElement('main');
  container.setAttribute('role', 'alert');
  container.style.cssText = 'min-height:100vh;display:grid;place-content:center;gap:12px;padding:24px;font:16px Inter, sans-serif;color:#ededf1;background:#101014';

  const title = document.createElement('h1');
  title.textContent = 'Astrid could not prepare browser storage';
  title.style.cssText = 'margin:0;font-size:20px';

  const detail = document.createElement('p');
  detail.textContent = `Migration failed for ${store}. Your existing browser data is preserved. Retry to try again.`;
  detail.style.cssText = 'max-width:560px;margin:0;line-height:1.5';

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = 'Retry migration';
  button.style.cssText = 'justify-self:start;padding:9px 14px;border:0;border-radius:6px;background:#fff;color:#111;font:inherit;cursor:pointer';
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

  if (shouldShowWelcome(new URL(window.location.href))) {
    const { renderWelcome } = await import('@/app/onboarding/welcomeBootstrap.tsx');
    renderWelcome(rootElement);
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
  renderApp(rootElement);
  releaseBootLayerWhenReady(rootElement);
}

void main();
