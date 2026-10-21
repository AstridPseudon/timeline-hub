import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// One committed-source native parent split journey. The central runner supplies
// the exact App/Agent/Runtime/public13 tuple and private dependency overlay.
export default defineConfig({
  ...threeProducts,
  testMatch: 'parent-split-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/parent-split-command',
});
