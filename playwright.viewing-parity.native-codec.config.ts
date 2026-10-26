import { defineConfig } from '@playwright/test';
import baseline from './playwright.viewing-parity.config';

// Explicit additional environment; the original four-case Chromium 141 config stays runnable.
export default defineConfig({
  ...baseline,
  projects: [{
    name: 'native-codec-chrome155',
    metadata: { viewingParityBrowserProfile: 'native-codec-chrome155' },
  }],
});
