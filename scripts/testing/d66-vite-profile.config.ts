import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, loadConfigFromFile } from 'vite';

const appRoot = process.env.D66_APP_CHECKOUT;
const profileRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const compositionRoot = process.env.D66_COMPOSITION_PACKAGE_ROOT;

if (!appRoot || !compositionRoot) {
  throw new Error('D66 private Vite profile requires the pinned App root and staged Composition package');
}

const publicExports = {
  '': 'index.js',
  '/evaluation': 'evaluation.js',
  '/theme-api': 'theme-api.js',
  '/registry.generated': 'registry.generated.js',
  '/effects.generated': 'effects.generated.js',
  '/animations.generated': 'animations.generated.js',
  '/transitions.generated': 'transitions.generated.js',
  '/registries': 'registries.js',
};

export default defineConfig(async ({ command, mode }) => {
  const loaded = await loadConfigFromFile(
    { command, mode },
    path.join(profileRoot, 'config/vite/vite.config.ts'),
  );
  if (!loaded) throw new Error('D66 private Vite profile could not load the pinned App Vite config');

  const existing = loaded.config.resolve?.alias;
  const aliases = Array.isArray(existing)
    ? existing
    : Object.entries(existing ?? {}).map(([find, replacement]) => ({ find, replacement }));
  const compositionAliases = Object.entries(publicExports).map(([suffix, file]) => ({
    find: new RegExp(`^@banodoco/timeline-composition${suffix.replaceAll('.', '\\.')}$`),
    replacement: path.join(compositionRoot, 'dist', file),
  }));

  return {
    ...loaded.config,
    resolve: {
      ...loaded.config.resolve,
      alias: [...compositionAliases, ...aliases],
    },
  };
});
