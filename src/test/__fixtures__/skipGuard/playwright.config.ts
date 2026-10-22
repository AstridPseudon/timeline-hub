import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: import.meta.dirname,
  testMatch: '*.pwfixture.ts',
  forbidOnly: true,
  workers: 1,
  reporter: [['line'], ['../../../../config/testing/playwrightSkipGuard.ts']],
});
