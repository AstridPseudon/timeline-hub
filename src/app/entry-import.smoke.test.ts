/**
 * Entry-import smoke test.
 *
 * Guards the real entry graph against module-evaluation crashes:
 * `bootstrap.tsx` -> `App.tsx` -> `routes.tsx` -> `VideoEditorPage` ->
 * `VideoEditorProvider` -> `createProcessManager`.
 *
 * This test `await import()`s the real entry composition root,
 * `@/app/bootstrap` (which statically imports the real `@/app/App`, with
 * nothing in the video-editor import chain mocked away), and asserts the
 * import resolves without throwing. It does not call `renderApp()`: a
 * module-evaluation-time throw surfaces on the bare `import()` itself.
 *
 * Scope: Vitest resolves `node:*` specifiers through Node.js itself, so a
 * static `node:` import would not fail here. The Node-builtin class is guarded
 * by the `no-restricted-imports` ESLint rule in `eslint.config.js`. This test
 * catches the broader class: any module reachable from the entry root that
 * throws when evaluated under a DOM-shaped runtime.
 *
 * No mocks are used: `src/test/setup.ts` already stubs the browser APIs
 * (matchMedia, IntersectionObserver, ResizeObserver) that jsdom lacks and
 * that components in this graph rely on, and the pattern of importing
 * `@/app/App` / `@/app/routes` unmocked under jsdom is already proven safe by
 * `src/moduleImportCoverage.test.ts`.
 */
import { describe, expect, it } from 'vitest';

describe('entry composition root import smoke', () => {
  it('imports bootstrap -> App -> routes -> VideoEditorPage without throwing at module-load time', async () => {
    const bootstrapModule = await import('@/app/bootstrap');

    expect(bootstrapModule).toBeTruthy();
    expect(typeof bootstrapModule.renderApp).toBe('function');
  }, 60_000);
});
