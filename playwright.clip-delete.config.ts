import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-delete-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-delete',
});
