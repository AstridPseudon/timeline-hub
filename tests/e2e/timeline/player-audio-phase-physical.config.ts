import { defineConfig } from '@playwright/test';
import base from './player-audio.config';

// One diagnostic only. It cannot silently select the original capture matrix.
export default defineConfig({
  ...base,
  testMatch: 'player-audio-phase-physical.probe.ts',
  webServer: (Array.isArray(base.webServer) ? base.webServer : []).map((server, index) => ({
    ...server,
    // The central launcher keeps Vite's cache outside read-only dependencies.
    command: index === 0 ? process.env.PLAYER_AUDIO_PHASE_VITE_COMMAND ?? server.command : server.command,
  })),
  fullyParallel: false,
  repeatEach: 1,
  workers: 1,
  retries: 0,
  projects: [{ name: 'player-audio-phase-amplified' }],
});
