import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';

// Raw native-browser control: no App, fixture server or shared config imports.
export default defineConfig({
  testDir: fileURLToPath(new URL('.', import.meta.url)),
  testMatch: 'player-audio-platform.probe.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? '/tmp/timeline-player-platform-results',
  timeout: 30_000,
  workers: 1,
  retries: 0,
  repeatEach: 3,
  reporter: 'list',
  projects: [{ name: 'native-audio-platform' }],
  use: {
    headless: true,
    viewport: { width: 1440, height: 900 },
    launchOptions: {
      executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
      ignoreDefaultArgs: ['--mute-audio'],
      args: [
        '--no-sandbox',
        '--host-resolver-rules=MAP supabase.co 127.0.0.1:1, MAP *.supabase.co 127.0.0.1:1, '
          + 'MAP *.supabase.in 127.0.0.1:1, MAP openrouter.ai 127.0.0.1:1, MAP *.openrouter.ai 127.0.0.1:1, '
          + 'MAP api.openai.com 127.0.0.1:1, MAP api.anthropic.com 127.0.0.1:1, '
          + 'MAP huggingface.co 127.0.0.1:1, MAP *.huggingface.co 127.0.0.1:1',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
      ],
    },
  },
});
