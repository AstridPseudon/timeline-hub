#!/usr/bin/env node
/**
 * `npm run dev:editor` — the timeline in a browser, with no Supabase and no install beyond `npm ci`.
 *
 * Spawns the fake Runtime (`tests/e2e/fake-runtime/launch.mjs --serve`: the demo project and timeline seeded
 * from the same fixtures the e2e suite uses, saves held in memory) plus the Vite dev server, and prints the
 * Runtime-mode editor URL that the e2e specs use. `localTest=1` suppresses unrelated authenticated-service
 * queries, while `timelineOverlayCanary=1` enables the DEV-only rollout gate for the timelineOverlay family so
 * the scene-phase-markers canary is visible out of the box; production never honors either query parameter.
 * The placeholder `VITE_SUPABASE_*` values mirror the ones `playwright.config.ts` injects: the Supabase env
 * getters are lazy, so local mode only needs them to exist.
 */
import { spawn } from 'node:child_process';
import { packageManagerInvocation } from './node-package-manager.mjs';

import { fakeRuntimeEnv } from '../tests/e2e/fake-runtime/launch.mjs';

const PORT = process.env.PORT ?? '2222';
const RUNTIME_PORT = Number(process.env.VITE_ASTRID_BRIDGE_PORT ?? '17334');
const EDITOR_QUERY = new URLSearchParams({
  project: 'demo-project-id',
  timeline: 'demo-timeline',
  localTest: '1',
  timelineOverlayCanary: '1',
});
const EDITOR_URL = `http://127.0.0.1:${PORT}/tools/video-editor?${EDITOR_QUERY}`;

const env = {
  ...process.env,
  PORT,
  // The fake Runtime's port, token file and identity; the Vite proxies read the same values, so the browser
  // never sees the bearer token.
  ...fakeRuntimeEnv({ port: RUNTIME_PORT }),
  // Must stay in step with DEFAULT_DEV_SUPABASE_URL in
  // src/shared/dev/devSession.ts — the dev session's storage key is
  // derived from this URL. (.mjs cannot import the TS module.) This is the
  // local `supabase start` convention, not a fake external domain.
  VITE_SUPABASE_URL: process.env.VITE_SUPABASE_URL ?? 'http://127.0.0.1:54321',
  VITE_SUPABASE_ANON_KEY: process.env.VITE_SUPABASE_ANON_KEY ?? 'test-anon-key',
  // The localTest contract is offline/deterministic.  Remove the declarative
  // Google Fonts links at Vite transform time so the browser cannot even
  // initiate a remote-font request before React bootstraps.
  VITE_DISABLE_REMOTE_FONTS: '1',
};

const children = [
  spawn(process.execPath, ['tests/e2e/fake-runtime/launch.mjs', '--serve'], { stdio: 'inherit', env }),
  (() => {
    const invocation = packageManagerInvocation('npm', ['run', 'dev', '--', '--host', '127.0.0.1', '--port', PORT], { env });
    return spawn(invocation.command, invocation.args, { stdio: 'inherit', env });
  })(),
];

console.log([
  '',
  'Timeline dev environment',
  `  editor : ${EDITOR_URL}`,
  `  runtime: http://127.0.0.1:${RUNTIME_PORT} (fake Runtime, demo project, in-memory saves)`,
  '',
].join('\n'));

let shuttingDown = false;
const shutdown = (signal) => {
  if (shuttingDown) return;
  shuttingDown = true;
  for (const child of children) {
    if (child.exitCode === null) child.kill(signal);
  }
};

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

// If either process dies the other is useless — take the whole thing down.
for (const child of children) {
  child.on('exit', (code) => {
    shutdown('SIGTERM');
    process.exitCode = code ?? 0;
  });
}
