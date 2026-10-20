import { defineConfig } from '@playwright/test';
import direct from './playwright.direct.config.ts';

// Source-stage direct journey. The owner-supplied Runtime guard and native
// historical fixture adapter are prerequisites for running this config.
export default defineConfig({
  ...direct,
  testMatch: 'headless-bootstrap-safety.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/headless-bootstrap-safety',
  timeout: 180_000,
  workers: 1,
});
