import { defineConfig } from '@playwright/test';
import direct from './playwright.direct.config.ts';

// One current-ops producer ownership journey on the normal direct Runtime-door harness.
export default defineConfig({
  ...direct,
  testDir: './tests/e2e/local',
  testMatch: 'producer-ownership-current-pin.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/producer-ownership-current-pin',
  timeout: 300_000,
  workers: 1,
  retries: 0,
});
