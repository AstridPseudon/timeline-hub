import { defineConfig } from '@playwright/test';
import directConfig from './playwright.direct.config.ts';

// This descriptor-bound, imported-realm acceptance stays out of the regular direct CI suite.
export default defineConfig({
  ...directConfig,
  testMatch: ['timeline-transfer.spec.ts'],
  globalSetup: './tests/e2e/local/n4-global-setup.ts',
  workers: 1,
  fullyParallel: false,
  retries: 0,
  forbidOnly: true,
});
