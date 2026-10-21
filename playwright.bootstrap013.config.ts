import { defineConfig } from '@playwright/test';
import direct from './playwright.direct.config.ts';

// Dedicated current013 source gate: the central runner supplies the frozen App/Agent/Runtime tuple.
export default defineConfig({
  ...direct,
  testMatch: 'bootstrap013-real-http.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/bootstrap013-real-http',
});
