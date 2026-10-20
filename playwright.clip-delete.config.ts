import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

/**
 * The real-delete lane is deliberately source-pinned by its caller.  A list or
 * run without the approved paired checkouts and heads is not qualification
 * evidence, so fail at config load rather than silently selecting sibling
 * defaults.
 */
for (const name of [
  'ASTRID_CHECKOUT',
  'ASTRID_RUNTIME_CHECKOUT',
  'TIMELINE_BUNDLE_AGENT_HEAD',
  'TIMELINE_BUNDLE_RUNTIME_HEAD',
]) {
  if (!process.env[name]) throw new Error(`clip-delete qualification requires ${name}`);
}

export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-delete-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-delete',
});
