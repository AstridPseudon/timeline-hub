import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';
import { assertCurrentQualificationSources } from './tests/e2e/local/support/currentQualification.ts';

// The current lane is explicit and source-pinned. This source-only branch does
// not select the historical frozen parent-delete spec.
assertCurrentQualificationSources();

export default defineConfig({
  ...threeProducts,
  testMatch: 'current-qualification.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/current-qualification',
});
