import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// One committed-source parent-trim journey. The central runner supplies the exact App/Agent/Runtime/public13 tuple.
export default defineConfig({
  ...threeProducts,
  testMatch: 'parent-trim-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/parent-trim-command',
});
