import path from 'node:path';

export const EDITOR_EXTENSION_FIXTURE_ENV = 'ASTRID_APP_E2E_EXTENSION_FIXTURES';
const EDITOR_EXTENSION_CATALOG_IMPORT = '@/tools/video-editor/dev/localExtensions.ts';

/** Resolve the fixed legacy capability-matrix catalog only for a Vite dev server. */
export function editorExtensionFixtureAlias(
  command: string,
  environment: NodeJS.ProcessEnv,
): { find: string; replacement: string } | null {
  if (command !== 'serve' || environment[EDITOR_EXTENSION_FIXTURE_ENV] !== '1') return null;
  return {
    find: EDITOR_EXTENSION_CATALOG_IMPORT,
    replacement: path.resolve(__dirname, '../../src/test/editorExtensionFixtureCatalog.ts'),
  };
}
