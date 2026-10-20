import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// Source only until the manager qualifies the composed controls, normal 0.2.3 pin and public 0.0.10 root.
// Explicit source identities prevent accidentally qualifying the integration checkouts or Bundle 1.
for (const [variable, expected] of [
  ['TIMELINE_BUNDLE_AGENT_HEAD', '027bd16d96010544331c953c0e1014e161786e71'],
  ['TIMELINE_BUNDLE_RUNTIME_HEAD', '4c145dc62192f0e942e3ee3922a11488aefe9b41'],
]) {
  if (process.env[variable] !== expected) throw new Error(`${variable} must equal frozen ordinaryBundle2 ${expected}`);
}
for (const variable of ['ASTRID_CHECKOUT', 'ASTRID_RUNTIME_CHECKOUT', 'ASTRID_PYTHON', 'ASTRID_RUNTIME_PYTHON']) {
  if (!process.env[variable]) throw new Error(`${variable} must explicitly select the frozen source/shared dependencies`);
}

export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-scalar-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-scalar',
});
