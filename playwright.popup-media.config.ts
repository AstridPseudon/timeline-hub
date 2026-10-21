import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

// One committed-source popup ADD journey through the existing timeline drop
// control. The central runner supplies the exact App/Agent/Runtime/public
// Composition cohort.
export default defineConfig({
  ...threeProducts,
  testMatch: 'popup-media-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/popup-media-command',
});

