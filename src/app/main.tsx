import {
  classifyBrowserEntry,
  prefersAppEntry,
  resolveInstallerConnectEntry,
  resolveReturningAppEntry,
} from '@/app/entryClassification.ts';
import { setRuntimeOrigin } from '@/integrations/runtime/connection.ts';
import { releaseBootLayerWhenReady } from '@/app/bootLayer.ts';
import { migrateAstridBrowserStorage } from '@/migrations/astridRenameBrowserMigration.ts';

function loadInstalledAppTypography(): void {
  if (import.meta.env.VITE_DISABLE_REMOTE_FONTS === '1') return;
  if (document.querySelector('[data-installed-app-fonts]')) return;
  // Offline browser-test mode (see config/vite/remoteFonts.ts): no remote-font request may be
  // initiated by the document or by this runtime injection.
  if (import.meta.env.VITE_DISABLE_REMOTE_FONTS === '1') return;

  const fonts = [
    {rel: 'preconnect', href: 'https://fonts.googleapis.com'},
    {rel: 'preconnect', href: 'https://fonts.gstatic.com', crossOrigin: 'anonymous'},
    {
      rel: 'stylesheet',
      href: 'https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Inter:wght@400;500;700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap',
    },
  ];

  for (const font of fonts) {
    const link = document.createElement('link');
    link.rel = font.rel;
    link.href = font.href;
    if ('crossOrigin' in font && font.crossOrigin) link.crossOrigin = font.crossOrigin;
    link.dataset.installedAppFonts = '';
    document.head.append(link);
  }
}

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

  loadInstalledAppTypography();

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
