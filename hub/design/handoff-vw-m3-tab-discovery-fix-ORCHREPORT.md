# Timeline tab-audio fixture discovery fix

## Result

Fixed the Playwright fixture-loader syntax failure in
`tests/e2e/timeline/tab-audio-capture.probe.ts`: the unused first fixture
argument is now an object-destructuring pattern (`{}`), with the repository's
existing targeted `no-empty-pattern` suppression. The standalone Chrome155
probe, two-tone fixture, native per-stream PTS assertions, cleanup, and
controller/source guards are unchanged.

Only one tracked product file changed:

```diff
-  fixtureUrl: async (fixtures, provide) => {
-    void fixtures;
+  // Playwright reads fixture dependencies from the destructuring pattern; this fixture has none.
+  // eslint-disable-next-line no-empty-pattern
+  fixtureUrl: async ({}, provide) => {
```

The setup script and controller are byte-for-byte unchanged. No grant, old
marker, listener, browser, socket, network, install, full suite, or central
test-service run was used. The prior pre-browser failure is treated only as a
fixture-loader defect; this work makes no backend capability claim.

## Evidence

All logs are flat and absolute under this directory:

- `handoff-vw-m3-tab-discovery-fix-targeted.log`
- `handoff-vw-m3-tab-discovery-fix-typecheck.log`
- `handoff-vw-m3-tab-discovery-fix-playwright-list.log`

Commands and results:

```text
node --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs
PASS: 2 file-level subtests, 2 pass, 0 fail.

npm exec -- eslint tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts tests/e2e/timeline/tab-audio-capture.analysis.mjs tests/e2e/timeline/tab-audio-capture.analysis.test.mjs --max-warnings 0
PASS: exit 0.

node --check tests/e2e/timeline/tab-audio-capture.controller.mjs
node --check tests/e2e/timeline/tab-audio-capture.controller.test.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
git diff --check
PASS: all exit 0.

npm exec -- tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --allowJs --resolveJsonModule --types node tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts
PASS: exit 0.

/tmp/vw-m3-agent-gate-node20.19.4/bin/node --version
v20.19.4

/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/playwright/cli.js test --config tests/e2e/timeline/tab-audio-capture.config.ts --project=native-codec-chrome155-tab-audio --list
PASS: exit 0; exactly 1 test in 1 file discovered. --list only; no listener or browser execution.
```

## Handoff

The source is ready for the manager to review and issue a fresh source grant.
Do not reuse the consumed old grant or run the live capability probe from this
worker. The central run remains unverified here.
