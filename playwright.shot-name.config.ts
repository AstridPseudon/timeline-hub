import { defineConfig } from '@playwright/test';
import direct from './playwright.direct.config.ts';

// Dedicated source gate: the central runner supplies the frozen App/Agent/Runtime/Composition tuple and private caches.
export default defineConfig({
  ...direct,
  testMatch: 'shot-name-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/shot-name-command',
  timeout: 300_000,
  workers: 1,
});

