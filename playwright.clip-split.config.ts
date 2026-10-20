import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// Source-only until the manager composes and qualifies the current013 split consumer.
export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-split-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-split',
});
