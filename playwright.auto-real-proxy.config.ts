import { defineConfig } from '@playwright/test';

/** Central launcher for the bounded real automatic-placement operation-proxy gate. */
export default defineConfig({
  testDir: './tests/e2e/local',
  testMatch: 'auto-real-proxy.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/auto-real-proxy',
  timeout: 300_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: process.env.CI ? [['line'], ['html', { open: 'never' }]] : 'list',
  use: { acceptDownloads: true, trace: 'retain-on-failure' },
});
