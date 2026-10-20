import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import base from '../../../playwright.config';

// Explicitly opt-in. The ordinary timeline projects never collect this probe.
export default defineConfig({
  ...base,
  testDir: fileURLToPath(new URL('.', import.meta.url)),
  testMatch: 'tab-audio-capture.probe.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? '/tmp/timeline-tab-audio-probe',
  workers: 1,
  retries: 0,
  projects: [{ name: 'native-codec-chrome155-tab-audio' }],
  use: {
    ...base.use,
    viewport: { width: 1440, height: 900 },
    launchOptions: {
      ...base.use?.launchOptions,
      // The approved native codec profile is fixed; a browser path from an
      // ambient environment must not silently change the probe identity.
      executablePath: '/opt/google/chrome/chrome',
      ignoreDefaultArgs: ['--mute-audio'],
      args: [
        ...(base.use?.launchOptions?.args ?? []),
        '--auto-accept-this-tab-capture',
        '--enable-usermedia-screen-capturing',
        '--allow-http-screen-capture',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
      ],
    },
  },
});
