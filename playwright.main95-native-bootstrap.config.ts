import { defineConfig } from '@playwright/test';
import direct from './playwright.direct.config.ts';

/** One committed Main95 native bootstrap proof; central runner supplies the frozen Agent/Runtime tuple. */
export default defineConfig({
  ...direct,
  testMatch: 'main95-native-bootstrap.integration.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/main95-native-bootstrap',
  timeout: 300_000,
  workers: 1,
});
