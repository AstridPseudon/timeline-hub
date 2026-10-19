import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import base from '../../../playwright.config';

// Opt-in capture experiment; the ordinary device lane keeps its launch policy.
export default defineConfig({
  ...base,
  testDir: fileURLToPath(new URL('.', import.meta.url)),
  testMatch: process.env.PLAYER_AUDIO_CAPTURE === 'tab'
    ? 'player-tab-capture.probe.ts' : 'player-audio-capture.probe.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? '/tmp/timeline-player-audio-results',
  webServer: (Array.isArray(base.webServer) ? base.webServer : []).map(server => ({
    ...server, cwd: fileURLToPath(new URL('../../../', import.meta.url)),
  })),
  workers: 1,
  retries: 0,
  projects: [{ name: 'player-audio-capture' }],
  use: {
    ...base.use,
    viewport: { width: 1440, height: 900 },
    launchOptions: {
      ...base.use?.launchOptions,
      ignoreDefaultArgs: ['--mute-audio'],
      args: [
        ...(base.use?.launchOptions?.args ?? []),
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        ...(process.env.PLAYER_AUDIO_CAPTURE === 'tab' ? [
          '--auto-accept-this-tab-capture',
          '--enable-usermedia-screen-capturing',
          '--allow-http-screen-capture',
        ] : []),
      ],
    },
  },
});
