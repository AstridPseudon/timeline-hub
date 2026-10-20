import { defineConfig } from 'vite';
import baseConfig from './config/vite/vite.config';

export default defineConfig(async (environment) => {
  const base = typeof baseConfig === 'function' ? await baseConfig(environment) : baseConfig;
  return {
    ...base,
    cacheDir: process.env.PRIVATE_VITE_CACHE_DIR ?? '.vite-local-browser-export',
  };
});
