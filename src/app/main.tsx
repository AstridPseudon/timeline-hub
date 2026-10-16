import {
  classifyBrowserEntry,
  prefersAppEntry,
  resolveReturningAppEntry,
} from '@/app/entryClassification.ts';

function loadInstalledAppTypography(): void {
  if (document.querySelector('[data-installed-app-fonts]')) return;

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

/**
 * Lifts index.html's boot layer once the page's first real frame has committed: #root has
 * content and nothing in it holds the boot (`data-boot-hold`, which the video editor renders
 * while its workspace answers, so the paper dissolves straight into the editor's frame rather
 * than into an empty sky). It starts on the next frame, with that frame already painted under
 * it; index.html owns the timing (mink 120ms, paper 260ms).
 */
function releaseBootLayerWhenReady(root: HTMLElement): void {
  const boot = document.getElementById('boot');
  if (!boot) return;
  let lifted = false;
  const ready = () => root.childElementCount > 0 && root.querySelector('[data-boot-hold]') === null;
  const lift = () => {
    if (lifted) return;
    lifted = true;
    observer.disconnect();
    requestAnimationFrame(() => {
      // The mink's own transitions bubble here too; only the paper's end removes the layer.
      boot.addEventListener('transitionend', (event) => {
        if (event.target === boot) boot.remove();
      });
      boot.classList.add('boot-done');
      // Reduced motion turns the transitions off, so no transitionend arrives.
      if (getComputedStyle(boot).transitionDuration === '0s') boot.remove();
    });
  };
  const observer = new MutationObserver(() => {
    if (ready()) lift();
  });
  observer.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['data-boot-hold'] });
  if (ready()) lift();
}

async function main(): Promise<void> {
  const rootElement = document.getElementById('root');
  if (!rootElement) {
    throw new Error("Failed to render app: element with id 'root' was not found.");
  }

  const returningAppEntry = resolveReturningAppEntry(new URL(window.location.href), prefersAppEntry());
  if (returningAppEntry) {
    window.history.replaceState(window.history.state, '', returningAppEntry);
  }

  const owner = classifyBrowserEntry(new URL(window.location.href), {
    VITE_APP_ENV: import.meta.env.VITE_APP_ENV,
  });
  if (owner === 'public') {
    const { renderPublicEntry } = await import('@/app/publicBootstrap.tsx');
    renderPublicEntry(rootElement);
    releaseBootLayerWhenReady(rootElement);
    return;
  }

  loadInstalledAppTypography();

  const [
    { renderApp },
    { initializeVideoEditorExtensionRuntime },
  ] = await Promise.all([
    import('@/app/bootstrap'),
    import('@/tools/video-editor/browser/initializeVideoEditorExtensionRuntime.ts'),
  ]);
  await initializeVideoEditorExtensionRuntime({ development: import.meta.env.DEV });
  renderApp(rootElement);
  releaseBootLayerWhenReady(rootElement);
}

void main();
