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

// Mock both supported import paths to one deferred implementation. This keeps
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
    window.history.replaceState({}, '', '/tools/video-editor?localTest=1');
  });

  it('waits for extension runtime initialization before rendering the app', async () => {
    bootstrapMocks.migrateAstridBrowserStorage.mockResolvedValue({ success: true });
    let resolveInitialization!: () => void;
    bootstrapMocks.initializeVideoEditorExtensionRuntime.mockImplementation(() => new Promise<void>((resolve) => {
      resolveInitialization = resolve;
    }));

    const root = document.createElement('div');
    root.id = 'root';
    document.body.append(root);

    await import('@/app/main');

    await vi.waitFor(() => expect(bootstrapMocks.initializeVideoEditorExtensionRuntime).toHaveBeenCalledOnce());
    expect(bootstrapMocks.renderApp).not.toHaveBeenCalled();

    resolveInitialization();
    await vi.waitFor(() => expect(bootstrapMocks.renderApp).toHaveBeenCalledOnce());
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
});
