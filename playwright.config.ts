import { defineConfig, devices } from '@playwright/test';
import { DEFAULT_DEV_SUPABASE_URL } from './src/shared/dev/devSession.ts';
import { fakeRuntimeEnv } from './tests/e2e/fake-runtime/launch.mjs';
import { astridOnboardedStorageState } from './tests/e2e/fixtures/astridOnboardedStorageState';
import {
  allocateIsolatedPort,
  readCanonicalBaseUrl,
  resolveCanonicalBaseUrl,
} from './tests/e2e/timeline/isolated-port.mjs';

const allocatedPorts = new Set<number>();
// Timeline gates are intentionally isolated even when invoked from a shell
// that has no CI marker.  Explicit ports are validated by the allocator;
// omitted ports are fresh per run.
const inheritedRunPorts = process.env.ASTRID_APP_TIMELINE_PORTS_ALLOCATED === '1';
const configuredBaseURL = readCanonicalBaseUrl();
if (configuredBaseURL && !process.env.PLAYWRIGHT_PORT) process.env.PLAYWRIGHT_PORT = String(configuredBaseURL.port);
const readInheritedPort = (envName: string): number => {
  const value = Number(process.env[envName]);
  if (!Number.isInteger(value) || value < 1 || value > 65_535) {
    throw new Error(`${envName} was marked run-allocated but is invalid: ${process.env[envName] ?? ''}`);
  }
  return value;
};
const port = inheritedRunPorts
  ? readInheritedPort('PLAYWRIGHT_PORT')
  : allocateIsolatedPort('PLAYWRIGHT_PORT', allocatedPorts);
const baseURL = resolveCanonicalBaseUrl(port);
process.env.BASE_URL = baseURL;
process.env.PLAYWRIGHT_BASE_URL = baseURL;
// Concurrent acceptance lanes must not clean or overwrite each other's traces.
const outputDir = process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results';

// Browser-level network blocking for the timeline browser lane: Chromium resolves
// every provider/Supabase host to a closed loopback port so a stray remote
// fetch fails fast inside the browser (the local dev Supabase is the raw IP
// 127.0.0.1:54321, which resolver MAP cannot cover — the origin audit in
// tests/e2e/timeline/support.ts `openEditor` covers that leg). Applied on
// EVERY launchOptions branch so no executable path skips the blackhole.
const BROWSER_DNS_BLACKHOLE_ARGS = [
  '--no-sandbox',
  // NOTE: no shell-style quotes around the value — Playwright passes argv
  // verbatim (no shell), and Chromium rejects every rule if the value carries
  // literal quote characters (proven: quoted form leaves supabase.co reachable,
  // unquoted form fails fast at 127.0.0.1:1).
  '--host-resolver-rules=MAP supabase.co 127.0.0.1:1, MAP *.supabase.co 127.0.0.1:1, '
    + 'MAP *.supabase.in 127.0.0.1:1, MAP openrouter.ai 127.0.0.1:1, MAP *.openrouter.ai 127.0.0.1:1, '
    + 'MAP api.openai.com 127.0.0.1:1, MAP api.anthropic.com 127.0.0.1:1, '
    + 'MAP huggingface.co 127.0.0.1:1, MAP *.huggingface.co 127.0.0.1:1',
] as const;
const chromiumExecutablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
const launchOptions = chromiumExecutablePath
  ? { executablePath: chromiumExecutablePath, args: [...BROWSER_DNS_BLACKHOLE_ARGS] }
  : { args: [...BROWSER_DNS_BLACKHOLE_ARGS] };

// Timeline device specs need a live dev server plus the fake Runtime (both booted by `webServer` below).
// Their opt-in script owns their collection.
// See `npm run test:e2e:timeline`.
const TIMELINE_DEVICE_SPECS = /tests[\\/]e2e[\\/]timeline[\\/].*\.spec\.ts$/;
const RENDERER_OWNED_TIMELINE_SPECS = /(?:caption-render-export|caption-render-matrix)\.spec\.ts$/;
const includeTimelineDevices = process.env.PLAYWRIGHT_TIMELINE_DEVICES === '1';
const EXTENSION_HARNESS_SETUP_SPEC = /extension-harness\.setup\.ts$/;
// These specs have dedicated configs which provision their browser, fake Runtime and
// raster policy. The default device matrix must not collect them a second time
// under a different topology (in particular, mobile WebKit is not a pixel gate).
const DEDICATED_EXTENSION_SPECS = /extension-(?:accessibility|cross-browser|visual-regression)\.spec\.ts$/;
// The fake Runtime port is run-isolated too, so a stale Runtime from another
// checkout cannot answer this run's requests.
const fakeRuntimePort = inheritedRunPorts
  ? readInheritedPort('FAKE_RUNTIME_PORT')
  : allocateIsolatedPort('FAKE_RUNTIME_PORT', allocatedPorts);
// Playwright reloads this config in worker processes after webServer starts;
// carry the values across those reloads without probing our own live servers
// as though they were stale external processes.
process.env.ASTRID_APP_TIMELINE_PORTS_ALLOCATED = '1';
// The Vite env that points the app at the fake Runtime (runtime URL, expected identity, the `/api/astrid`
// bridge port and token, the ACP port and token). It also exports FAKE_RUNTIME_PORT and
// FAKE_RUNTIME_TOKEN_FILE, which the specs read; a config reload in a worker reads the same token file.
const fakeRuntimeViteEnv = fakeRuntimeEnv({ port: fakeRuntimePort });
const fakeRuntimeServeCommand = 'node tests/e2e/fake-runtime/launch.mjs --serve';
const extensionHarnessDependencies = ['extension-harness-setup'];
// The same-machine direct journey needs a Runtime checkout, a gateway and its
// own config (`playwright.direct.config.ts`, `npm run test:e2e:direct`).
const LOCAL_JOURNEY_SPECS = /tests[\\/]e2e[\\/]local[\\/].*\.spec\.ts$/;
const defaultProjectIgnores = [
  TIMELINE_DEVICE_SPECS,
  EXTENSION_HARNESS_SETUP_SPEC,
  DEDICATED_EXTENSION_SPECS,
  LOCAL_JOURNEY_SPECS,
];

export default defineConfig({
  testDir: './tests/e2e',
  // Unit helpers here use Vitest or node:test; only browser specs belong to
  // Playwright. The extension setup project overrides this match explicitly.
  testMatch: '**/*.spec.ts',
  outputDir,
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  fullyParallel: true,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL,
    storageState: astridOnboardedStorageState(baseURL),
    trace: 'retain-on-failure',
    ...(launchOptions ? { launchOptions } : {}),
  },
  // Array form: the default device matrix and the timeline device specs both
  // need the fake Runtime, so it is a second managed server instead of a second
  // terminal. Every server is owned by this run; an existing process is never
  // adopted, which keeps browser evidence tied to the configured checkout.
  webServer: [
    {
      // `--mode test` is the mode the fixtures are gated on (`?transcriptLaneFixture` is honoured only when
      // `import.meta.env.MODE === 'test'`, VideoEditorPage.tsx) and the one that keeps the dev-only debug
      // tooling out of the page. It is still the dev server (`import.meta.env.DEV`), so `localTest=1` works.
      command: `npm run dev -- --mode test --host 127.0.0.1 --port ${port}`,
      url: baseURL,
      // Never adopt a hand-started process for deterministic timeline/local
      // gates.  The allocated port is ours for this run, and a collision was
      // already rejected above.
      reuseExistingServer: false,
      timeout: 120_000,
      env: {
        // The editor capability-matrix E2E suite uses a fixed host-owned
        // fixture catalog; the Vite config only aliases it for `serve`.
        VITE_SUPABASE_URL: process.env.VITE_SUPABASE_URL ?? DEFAULT_DEV_SUPABASE_URL,
        VITE_SUPABASE_ANON_KEY: process.env.VITE_SUPABASE_ANON_KEY ?? 'test-anon-key',
        // Vite removes the declarative Google Fonts links before serving the
        // document, so the origin audit can reject every remote-font attempt
        // without relying on browser runtime interception.
        // Every Playwright server is a deterministic localTest surface. Strip
        // remote-font links before the browser sees HTML; production preview
        // keeps its normal font policy because this env is dev-server-only.
        VITE_DISABLE_REMOTE_FONTS: process.env.VITE_DISABLE_REMOTE_FONTS ?? '1',
        // One deterministic fake Runtime serves the timeline (workspace.v1), the
        // `/api/astrid` bridge routes and the narrow project-chat read. This env
        // points all three at it, behind its token, and overrides whatever
        // Runtime, bridge or ACP listener the developer machine exports.
        ...fakeRuntimeViteEnv,
      },
    },
    {
      command: fakeRuntimeServeCommand,
      // workspace.json is the one open route; every other route needs the token.
      url: `http://127.0.0.1:${fakeRuntimePort}/runtime-config/v1/workspace.json`,
      reuseExistingServer: false,
      timeout: 30_000,
      env: {
        FAKE_RUNTIME_PORT: String(fakeRuntimePort),
        FAKE_RUNTIME_TOKEN_FILE: fakeRuntimeViteEnv.FAKE_RUNTIME_TOKEN_FILE,
      },
    },
  ],
  projects: [
    {
      name: 'extension-harness-setup',
      testMatch: EXTENSION_HARNESS_SETUP_SPEC,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'chromium-desktop',
      testIgnore: defaultProjectIgnores,
      dependencies: extensionHarnessDependencies,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'chromium-condensed',
      testIgnore: defaultProjectIgnores,
      dependencies: extensionHarnessDependencies,
      use: { ...devices['iPad Mini'] },
    },
    {
      name: 'chromium-mobile',
      testIgnore: defaultProjectIgnores,
      dependencies: extensionHarnessDependencies,
      use: { ...devices['iPhone 13'] },
    },
    ...(includeTimelineDevices
      ? [{
          name: 'timeline-devices',
          testMatch: TIMELINE_DEVICE_SPECS,
          // Caption export/matrix specs require a producing render worker plus
          // managed media fixtures and therefore remain renderer-owned until
          // their dedicated command provisions that topology.
          testIgnore: RENDERER_OWNED_TIMELINE_SPECS,
          // Each spec sets its own viewport/touch profile via test.use().
          use: { ...devices['Desktop Chrome'] },
        }]
      : []),
  ],
});
