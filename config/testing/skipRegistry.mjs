// The one registry of skips this repo allows ("we shouldn't have invisible skips").
//
// A skip is visible only when ALL hold:
//   1. it is declared here, with a reason and the exact condition;
//   2. the run reports it by test name (vitest: config/testing/skipGuardReporter.ts; Playwright:
//      config/testing/playwrightSkipGuard.ts; node:test: scripts/quality/node-skip-guard-reporter.mjs),
//      and fails on any skip whose reason does not carry a registered `[declared:NAME]` tag;
//   3. some CI job runs the test where the condition holds (`ci`, checked against .github/workflows by
//      scripts/quality/check-skip-registry.mjs). `ci: []` plus `manual` says, in words, that no job does.
//
// Tests never call .skip / .only / .fixme / .todo / skipIf / runIf themselves
// (scripts/quality/check-no-raw-skips.mjs). They use `skipWhen` (src/test/declaredSkip.ts, vitest),
// `skipUnlessLane` (tests/e2e/support/declaredSkip.ts, Playwright) or `declaredSkip` (scripts/quality/declared-skip.mjs, node:test).
// Share this definition with the Runtime (tests/lanes.py) and Astrid agent repos.

/**
 * Skips reported at run time. `ci` = CI jobs (job ids in .github/workflows) where the skip condition is
 * false, so the test runs. `requireInLane`: in a job that sets ASTRID_REQUIRE_LANES to include this value,
 * the condition is a failure, never a skip (the lane's job provides the dependency).
 */
export const SKIP_REGISTRY = {
  'direct-journey-harness': {
    skipWhen: 'harnessUnavailableReason() !== null: no Runtime venv, no hosted dist/ build, or no openssl',
    reason: 'the direct journey needs a Runtime venv, a production build and openssl on the machine',
    ci: ['direct-journey'],
    requireInLane: 'direct-journey',
  },
  'direct-journey-ffmpeg': {
    skipWhen: '!harness.seed.video.decodable: ffmpeg is not installed, so stock Chromium cannot decode the fallback MP4',
    reason: 'the video-load case needs ffmpeg to make a decodable clip',
    ci: ['direct-journey'],
    requireInLane: 'direct-journey',
  },
  'provider-no-checkpoint-api': {
    skipWhen: 'the provider under test sets skipCheckpoints: it has no saveCheckpoint / loadCheckpoints (optional in DataProvider.ts)',
    reason: 'the provider has no checkpoint API (RuntimeDataProvider keeps composition revisions; the testing InMemoryDataProvider has none); the browser in-memory provider runs these',
    ci: ['vitest'],
  },
  'posix-owner-only-modes': {
    skipWhen: "process.platform === 'win32'",
    reason: 'owner-only file modes (chmod 0644 refusal) are a POSIX permission model',
    ci: ['vitest'],
  },
  'macos-lockf-broker': {
    skipWhen: "process.platform !== 'darwin' || !existsSync('/usr/bin/lockf')",
    reason: 'the broker-election reaping case exercises macOS /usr/bin/lockf',
    ci: [],
    manual: 'no CI job runs on macOS, and no job runs scripts/release tests; run `npm run test:extension-ship-verifier` on a Mac',
  },
  'symlink-creation-permitted': {
    skipWhen: 'fs.symlinkSync throws (no symlink privilege in this environment)',
    reason: 'the symlink-escape case needs permission to create symlinks',
    ci: [],
    manual: 'no CI job runs scripts/quality node tests; run `node --test scripts/quality/check-extension-family-conformance.test.mjs` locally',
  },
};

/**
 * Config-level lanes: specs and tests a config leaves out of the default run (testIgnore, exclude, grep,
 * env-gated projects). They are not "skipped" in a report, so each is declared here with the command that
 * runs it and the CI job that does, or `manual` saying that none does.
 */
export const LANES = {
  'vitest-checkout': {
    what: 'src/tools/video-editor/{data/portableVisualSeamIntent,runtime/astridSceneAuthoring,dev/localExtensions.catalog}.test.ts (config/testing/lanes.ts)',
    command: 'npm run test:checkout',
    ci: [],
    manual: 'needs sibling Runtime and Astrid checkouts; not run by any job yet',
  },
  'vitest-astrid-composition': {
    what: 'src/tools/video-editor/runtime/astridSceneComposition.test.tsx',
    command: 'npm run test:astrid-composition',
    ci: [],
    manual: 'needs ASTRID_CHECKOUT; not run by any job yet',
  },
  'vitest-sdk-boundary': {
    what: 'src/sdk/__tests__/*.test.{ts,tsx} (vitest.boundary.config.ts)',
    command: 'npm run test:sdk-boundary',
    ci: ['vitest'],
  },
  'playwright-default': {
    what: 'tests/e2e/*.spec.ts (chromium-desktop/condensed/mobile projects)',
    command: 'playwright test --config playwright.config.ts',
    ci: [],
    manual: 'no job runs playwright.config.ts; known failures exist (public A03/A08/A11/A12, extension-harness)',
  },
  'playwright-timeline': {
    what: 'tests/e2e/timeline/*.spec.ts (timeline-devices and timeline-chrome-export projects, PLAYWRIGHT_TIMELINE_DEVICES=1)',
    command: 'npm run test:e2e:timeline',
    ci: [],
    manual: 'no job runs the timeline specs; known failures exist (layout-geometry, extension-performance-budget)',
  },
  'playwright-extension-a11y-visual-cross-browser': {
    what: 'tests/e2e/extension-{accessibility,visual-regression,cross-browser}.spec.ts',
    command: 'npm run test:e2e:extension-accessibility | extension-visual | extension-cross-browser',
    ci: [],
    manual: 'no job runs them; extension visual and a11y fail on main',
  },
  'playwright-quick-descriptor': {
    what: 'tests/e2e/local/three-products.spec.ts "quick: Astrid edit then App edit" (grepInvert unless ASTRID_QUICK_DESCRIPTOR)',
    command: 'ASTRID_QUICK_DESCRIPTOR=... npm run test:e2e:three-products',
    ci: [],
    manual: 'needs an adopted Runtime realm descriptor from the owner; no job has one',
  },
  'playwright-direct': {
    what: 'tests/e2e/local/{direct-journey,settings-persist}.spec.ts',
    command: 'npm run test:e2e:direct',
    ci: ['direct-journey'],
  },
  'playwright-three-products': {
    what: 'tests/e2e/local/three-products.spec.ts (all but the quick case)',
    command: 'npm run test:e2e:three-products',
    ci: ['three-products'],
  },
};

export const DECLARED_TAG = /\[declared:([a-z0-9-]+)\]/;

export function declaredTag(name) {
  if (!Object.hasOwn(SKIP_REGISTRY, name)) throw new Error(`skip "${name}" is not declared in config/testing/skipRegistry.mjs`);
  return `[declared:${name}] ${SKIP_REGISTRY[name].reason}`;
}

/** The registered name carried by a skip reason, or null when the skip is undeclared. */
export function declaredName(reason) {
  const match = DECLARED_TAG.exec(String(reason ?? ''));
  return match && Object.hasOwn(SKIP_REGISTRY, match[1]) ? match[1] : null;
}

/** True when the job running now provides the lane, so a missing dependency must fail, not skip. */
export function laneIsRequired(name) {
  const lane = SKIP_REGISTRY[name]?.requireInLane;
  return Boolean(lane) && (process.env.ASTRID_REQUIRE_LANES ?? '').split(',').map((part) => part.trim()).includes(lane);
}

/** Splits `{ name, reason }` skip entries into declared and undeclared, and formats the report. */
export function classifySkips(entries) {
  const declared = [];
  const undeclared = [];
  for (const entry of entries) (declaredName(entry.reason) ? declared : undeclared).push(entry);
  return { declared, undeclared };
}

export function formatSkipReport({ declared, undeclared }) {
  const lines = [];
  if (declared.length) {
    lines.push(`declared skips (${declared.length}):`);
    for (const entry of declared) lines.push(`  SKIP ${entry.name}: ${entry.reason}`);
  }
  for (const entry of undeclared) lines.push(`UNDECLARED SKIP ${entry.name}: ${entry.reason || '(no reason)'}`);
  return lines.join('\n');
}
