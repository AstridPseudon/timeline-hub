import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

export default defineConfig({
  ...threeProducts,
  testMatch: 'track-label-command.spec.ts',
});
