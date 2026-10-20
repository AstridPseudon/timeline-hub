import { defineConfig } from '@playwright/test';
import nativeCodec from './playwright.viewing-parity.native-codec.config';

export default defineConfig({
  ...nativeCodec,
  globalSetup: './tests/e2e/timeline/viewing-parity/global-setup.ts',
  testMatch: 'player-export-normal-profile-native1920.spec.ts',
});
