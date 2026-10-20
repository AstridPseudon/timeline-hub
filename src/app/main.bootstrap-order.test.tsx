import { beforeEach, describe, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const bootstrapMocks = vi.hoisted(() => ({
  initializeVideoEditorExtensionRuntime: vi.fn(),
  initializeWorkspaceRuntimeIdentity: vi.fn(),
  migrateAstridBrowserStorage: vi.fn(),
  renderApp: vi.fn(),
}));

const indexHtml = readFileSync(resolve(process.cwd(), 'index.html'), 'utf8');
const indexDocument = new DOMParser().parseFromString(indexHtml, 'text/html');
const bootMarkup = indexDocument.getElementById('boot');
const bootStyles = Array.from(indexDocument.querySelectorAll('style')).find((style) => style.textContent?.includes('#boot {'));

// Mock both supported import paths to the same initializer. This keeps
// the test focused on the real entry's initialization-before-render sequence.
vi.mock('@/tools/video-editor/browser', () => ({
  initializeVideoEditorExtensionRuntime: bootstrapMocks.initializeVideoEditorExtensionRuntime,
}));

vi.mock('@/tools/video-editor/browser/initializeVideoEditorExtensionRuntime', () => ({
  initializeVideoEditorExtensionRuntime: bootstrapMocks.initializeVideoEditorExtensionRuntime,
}));

vi.mock('@/app/bootstrap', () => ({
  renderApp: bootstrapMocks.renderApp,
}));

vi.mock('@/integrations/runtime/client.ts', () => ({
  initializeWorkspaceRuntimeIdentity: bootstrapMocks.initializeWorkspaceRuntimeIdentity,
}));

vi.mock('@/migrations/astridRenameBrowserMigration.ts', () => ({
  migrateAstridBrowserStorage: bootstrapMocks.migrateAstridBrowserStorage,
}));

describe('main entry bootstrap order', () => {
  beforeEach(() => {
    vi.resetModules();
    bootstrapMocks.initializeVideoEditorExtensionRuntime.mockReset();
    bootstrapMocks.initializeWorkspaceRuntimeIdentity.mockReset();
    bootstrapMocks.migrateAstridBrowserStorage.mockReset();
    bootstrapMocks.renderApp.mockReset();
    document.body.replaceChildren();
    document.head.querySelectorAll('link[data-installed-app-fonts]').forEach((link) => link.remove());
    // The web root is the public landing entry; the app bootstrap only runs on an app route.
    window.history.replaceState({}, '', '/tools/video-editor?localTest=1');
  });

  it('initializes the extension runtime before rendering the app', async () => {
    bootstrapMocks.migrateAstridBrowserStorage.mockResolvedValue({ success: true });
    const order: string[] = [];
    bootstrapMocks.initializeVideoEditorExtensionRuntime.mockImplementation(() => { order.push('initialize'); });
    bootstrapMocks.renderApp.mockImplementation(() => { order.push('render'); });
    const root = document.createElement('div');
    root.id = 'root';
    document.body.append(root);

    await import('@/app/main');
    await vi.waitFor(() => expect(bootstrapMocks.renderApp).toHaveBeenCalledOnce());
    expect(order).toEqual(['initialize', 'render']);
    expect(bootstrapMocks.renderApp).toHaveBeenCalledWith(root);
  });

  it('blocks app initialization on migration failure and renders after a successful retry', async () => {
    bootstrapMocks.migrateAstridBrowserStorage
      .mockResolvedValueOnce({ success: false, store: 'IndexedDB astrid.timeline-drafts', error: new Error('diverged') })
      .mockResolvedValueOnce({ success: true });

    const root = document.createElement('div');
    root.id = 'root';
    expect(bootMarkup).not.toBeNull();
    expect(bootStyles).toBeDefined();
    const boot = document.importNode(bootMarkup!, true);
    document.head.append(document.importNode(bootStyles!, true));
    document.body.append(boot, root);

    await import('@/app/main');
    await vi.waitFor(() => expect(root.textContent).toContain('IndexedDB astrid.timeline-drafts'));

    expect(bootstrapMocks.renderApp).not.toHaveBeenCalled();
    expect(bootstrapMocks.initializeVideoEditorExtensionRuntime).not.toHaveBeenCalled();
    expect(bootstrapMocks.initializeWorkspaceRuntimeIdentity).not.toHaveBeenCalled();
    await vi.waitFor(() => expect(boot.classList.contains('boot-done')).toBe(true));
    expect(getComputedStyle(boot.querySelector('.boot-paper')!).opacity).toBe('0');
    const retry = Array.from(root.querySelectorAll('button')).find((button) => button.textContent === 'Retry migration');
    expect(retry).toBeDefined();
    expect(retry?.isConnected).toBe(true);
    expect(getComputedStyle(retry!).visibility).toBe('visible');
    retry?.click();

    await vi.waitFor(() => expect(bootstrapMocks.renderApp).toHaveBeenCalledOnce());
    expect(bootstrapMocks.migrateAstridBrowserStorage).toHaveBeenCalledTimes(2);
    expect(bootstrapMocks.renderApp).toHaveBeenCalledWith(root);
  });

  it.each([
    ['injects the remote font links by default', undefined, true],
    ['injects no remote font link when VITE_DISABLE_REMOTE_FONTS=1', '1', false],
  ])('%s', async (_name, flag, expectLinks) => {
    bootstrapMocks.migrateAstridBrowserStorage.mockResolvedValue({ success: true });
    bootstrapMocks.initializeVideoEditorExtensionRuntime.mockResolvedValue(undefined);
    vi.stubEnv('VITE_DISABLE_REMOTE_FONTS', flag ?? '');
    try {
      const root = document.createElement('div');
      root.id = 'root';
      document.body.append(root);

      await import('@/app/main');
      await vi.waitFor(() => expect(bootstrapMocks.renderApp).toHaveBeenCalledOnce());

      const hrefs = [...document.querySelectorAll('link[data-installed-app-fonts]')]
        .map((link) => link.getAttribute('href'));
      if (expectLinks) {
        expect(hrefs.some((href) => href?.startsWith('https://fonts.googleapis.com/css2'))).toBe(true);
      } else {
        expect(hrefs).toEqual([]);
      }
    } finally {
      vi.unstubAllEnvs();
    }
  });
});
