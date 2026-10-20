import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// Source-only until the staged footer consumer is composed and centrally qualified.  This lane
// must keep the exact ordinary 0.2.3 pair; it must not silently select integration checkouts.
for (const [variable, expected] of [
  ['TIMELINE_BUNDLE_AGENT_HEAD', '027bd16d96010544331c953c0e1014e161786e71'],
  ['TIMELINE_BUNDLE_RUNTIME_HEAD', '4c145dc62192f0e942e3ee3922a11488aefe9b41'],
]) {
  if (process.env[variable] !== expected) throw new Error(`${variable} must equal frozen ordinary 0.2.3 ${expected}`);
}
for (const variable of ['ASTRID_CHECKOUT', 'ASTRID_RUNTIME_CHECKOUT', 'ASTRID_PYTHON', 'ASTRID_RUNTIME_PYTHON']) {
  if (!process.env[variable]) throw new Error(`${variable} must explicitly select the frozen source/shared dependencies`);
}

export default defineConfig({
  ...threeProducts,
  testMatch: 'track-create-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/track-create',
});
