import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const boot = vi.hoisted(() => ({ migrate: vi.fn(), release: vi.fn() }));
vi.mock('@/migrations/astridRenameBrowserMigration.ts', () => ({ migrateAstridBrowserStorage: boot.migrate }));
vi.mock('@/app/bootLayer.ts', () => ({ releaseBootLayerWhenReady: boot.release }));

describe('main startup failures', () => {
  const reload = vi.fn();
  beforeEach(() => {
    vi.resetModules();
    localStorage.clear();
    sessionStorage.clear();
    boot.migrate.mockReset();
    boot.release.mockReset();
    reload.mockReset();
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    document.body.innerHTML = '<div id="root"></div>';
    window.history.replaceState({}, '', '/tools/video-editor');
    const { href, origin, pathname, search, hash } = window.location;
    vi.stubGlobal('location', { href, origin, pathname, search, hash, reload });
  });
  afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

  it('shows a Reload screen and releases the boot layer when startup throws', async () => {
    boot.migrate.mockRejectedValue(new Error('Failed to fetch dynamically imported module'));
    await import('@/app/main');
    await vi.waitFor(() => expect(boot.release).toHaveBeenCalledOnce());
    const root = document.getElementById('root')!;
    expect(root.textContent).toContain('Astrid could not start');
    const button = root.querySelector('button')!;
    expect(button.textContent).toBe('Reload');
    button.click();
    expect(reload).toHaveBeenCalledOnce();
  });

  it('reloads once on vite:preloadError and never loops', async () => {
    boot.migrate.mockResolvedValue({ success: false, store: 'x' });
    await import('@/app/main');
    const first = new Event('vite:preloadError', { cancelable: true });
    window.dispatchEvent(first);
    expect(first.defaultPrevented).toBe(true);
    expect(reload).toHaveBeenCalledOnce();
    const second = new Event('vite:preloadError', { cancelable: true });
    window.dispatchEvent(second);
    expect(second.defaultPrevented).toBe(false);
    expect(reload).toHaveBeenCalledOnce();
  });
});
