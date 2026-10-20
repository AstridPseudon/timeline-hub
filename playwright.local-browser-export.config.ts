import { defineConfig } from '@playwright/test';
import baseline from './playwright.config';

const privateViteConfig = 'playwright.local-browser-export.vite.config.ts';
const webServer = Array.isArray(baseline.webServer)
  ? baseline.webServer.map((server, index) => index === 0
    ? {
      ...server,
      command: server.command.replace(
        'npm run dev --',
        `node_modules/.bin/vite --config ${privateViteConfig}`,
      ),
    }
    : server)
  : baseline.webServer;

export default defineConfig({
  ...baseline,
  webServer,
});
