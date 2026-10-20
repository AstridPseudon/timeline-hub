import { createRequire } from 'node:module';
import { join } from 'node:path';
import { isolatedEnvironment, privateGraphRoot } from './tab-audio-capture.controller.mjs';
import { fileURLToPath } from 'node:url';

const graphRoot = privateGraphRoot();
const isolated = isolatedEnvironment();
const require = createRequire(join(graphRoot, '../package.json'));
const { defineConfig } = require('@playwright/test');

// Explicitly opt-in. This capability probe has no App or fake Runtime startup.
export default defineConfig({
  testDir: fileURLToPath(new URL('.', import.meta.url)),
  testMatch: 'tab-audio-capture.probe.ts',
  outputDir: isolated.PLAYWRIGHT_OUTPUT_DIR,
  workers: 1,
  retries: 0,
  projects: [{
    name: 'native-codec-chrome155-tab-audio',
    use: {
      viewport: { width: 1440, height: 900 },
      launchOptions: {
        // The approved native codec profile is fixed; a browser path from an
        // ambient environment must not silently change the probe identity.
        executablePath: '/opt/google/chrome/chrome',
        ignoreDefaultArgs: ['--mute-audio'],
        args: [
          '--auto-accept-this-tab-capture',
          '--enable-usermedia-screen-capturing',
          '--allow-http-screen-capture',
          '--disable-background-timer-throttling',
          '--disable-renderer-backgrounding',
        ],
      },
    },
  }],
});
