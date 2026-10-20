import { defineConfig } from '@playwright/test';

// Manager-scheduled central run only, under /tmp/timeline-viewing-browser.lock.
// Requires the Agent-owned launcher bridge in viewing-parity/bootstrap.ts.
export default defineConfig({
  testDir: './tests/e2e/timeline',
  testMatch: 'player-export-frame-parity.spec.ts',
  globalSetup: './tests/e2e/local/global-setup.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/viewing-parity',
  timeout: 300_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  use: { trace: 'retain-on-failure', acceptDownloads: true },
});
