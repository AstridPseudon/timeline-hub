import { createRequire } from 'node:module';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { assertRunMode, isolatedEnvironment, privateGraphRoot } from './tab-audio-capture.controller.mjs';

const graphRoot = privateGraphRoot();
assertRunMode();
const isolated = isolatedEnvironment();
const require = createRequire(join(graphRoot, '../package.json'));
const { defineConfig } = require('@playwright/test');

export default defineConfig({
  testDir: fileURLToPath(new URL('.', import.meta.url)),
  testMatch: 'private-pulse-stereo.probe.ts',
  outputDir: isolated.PLAYWRIGHT_OUTPUT_DIR,
  workers: 1,
  retries: 0,
  projects: [{
    name: 'private-pulse-stereo-chrome155',
    use: {
      viewport: { width: 1440, height: 900 },
      launchOptions: {
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
