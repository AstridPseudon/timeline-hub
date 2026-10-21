import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

export default defineConfig({
  ...threeProducts,
  testMatch: 'public-trim-mounted-fixture.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/public-trim-mounted-fixture',
});
