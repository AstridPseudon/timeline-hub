# App M0 baseline evidence

Date: 2026-10-19. Source checkout: `/home/user/work/wt/app-m0-baseline-full`, branch `tl/app-m0-baseline-full`, based on `tl/integration`.

## Environment evidence

- Node `v22.22.0`; npm `10.9.4`.
- Shared App dependencies installed at `/home/user/work/app/node_modules` (`510M`). The first `npm ci` attempt hit npm-cache `EROFS`; the retry succeeded, adding 575 packages in 29s. No package update or audit fix was run.
- `npm run test:contracts`: 1 file / 1 test passed. Full log: `/tmp/app-m0-env-logs/npm-test-contracts.log`.
- Explicit `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` Chromium launch/page evaluation passed with Chromium `141.0.7390.37`, title `timeline-m0-probe`, text `ok`, and sum `42`: `/tmp/app-m0-env-logs/chromium-probe-explicit.log`.
- Playwright-managed browser lookup failed because `/opt/pw-browsers/chromium_headless_shell-1223/...` is absent: `/tmp/app-m0-env-logs/chromium-probe.log`. No browser install was run.
- The earlier plain `npm test` remains preserved and incomplete (`/tmp/app-m0-env-logs/npm-test.log`, exit 130 after 624 tests / 2 governance failures). The earlier bounded 2-worker diagnostic also remains preserved and incomplete (`/tmp/app-m0-env-logs/vitest-bounded-diagnostic-2workers.log`, exit 124).

## Complete default suite

Command:

```text
npm test -- --maxWorkers=2 --reporter=verbose
```

This retained npm's two prechecks and the default Vitest selection. Only worker count and reporter differed from plain `npm test`; no bail, skip, filter, or additional exclusion was used.

- Wall time: `2026-10-19T18:01:39Z`–`2026-10-19T18:41:27Z` (39m48s).
- Vitest duration: `2384.29s`; exit code `1`; 60-minute ceiling not reached.
- Test files: 1,432 passed, 15 failed, 0 skipped, 1,447 total.
- Tests: 17,954 passed, 56 failed, 0 skipped, 18,010 total.
- Vitest reported 24 errors, primarily loopback/listener and child-process `EPERM` errors.
- Full verbose log: `/tmp/app-m0-baseline-full/npm-test-maxWorkers2-verbose.log`.
- Every named failure and representative reason is retained in the full verbose log above. The worker report is a summary, not an independent full failure index.

The 1,451 source test files include three checkout-lane tests and one explicit `astridSceneComposition.test.tsx` exclusion with its own config; these four were not selected by the default run. App did not run the three-products e2e journey; the initial env probe lacked App dist and the checkout-local Runtime venv path. Runtime owns subsequent journey feasibility/fixtures in journey-preflight.md and journey-runtime-env.md; this baseline makes no live-journey claim. The App worktree is clean (`git diff --check` passed).

## Socket-enabled targeted rerun

Date: 2026-10-19. Source checkout: `/home/user/work/wt/app-m0-loopback`, branch `tl/app-m0-loopback`, HEAD `850763dfc269a34edf8dcdf38c630033c26ecdd8` (`test(app): reject local server listen failures`), based on the reviewed listener-fix branch. No tracked files changed.

Required preflight probes, run before Vitest, all passed:

- Local HTTP bind and loopback round-trip: `127.0.0.1` bound an ephemeral port and returned HTTP 200 with body `loopback-ok`.
- `execFileSync("node", ["--version"])`: `v22.22.0`.
- `execFileSync("git", ["--version"])`: `git version 2.43.0`.
- Probe output: `/tmp/app-m0-loopback/probes.log`.

The shared installed dependencies were used through this worktree's `node_modules` symlink to `/home/user/work/app/node_modules`; no package installation or update was run.

Exact command:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/runtime/processes/astridAcpBridge.test.ts src/integrations/paired/pairedTransport.test.ts src/tools/video-editor/examples/extensions/__tests__/process-runtime-canary.integration.test.tsx src/tools/video-editor/runtime/processes/ProcessManager.integration.test.ts src/integrations/runtime/vendorLock.test.ts src/tools/video-editor/runtime/processes/processFixture.test.ts src/tools/video-editor/data/astridBridgeProxyPolicy.test.ts src/tools/video-editor/runtime/project-element-selection.test.ts src/integrations/paired/objectCachePolicy.test.ts src/integrations/astrid/transport.test.ts src/tools/video-editor/runtime/element-admission-build.test.ts
```

Selected files, in command order:

1. `src/tools/video-editor/runtime/processes/astridAcpBridge.test.ts`
2. `src/integrations/paired/pairedTransport.test.ts`
3. `src/tools/video-editor/examples/extensions/__tests__/process-runtime-canary.integration.test.tsx`
4. `src/tools/video-editor/runtime/processes/ProcessManager.integration.test.ts`
5. `src/integrations/runtime/vendorLock.test.ts`
6. `src/tools/video-editor/runtime/processes/processFixture.test.ts`
7. `src/tools/video-editor/data/astridBridgeProxyPolicy.test.ts`
8. `src/tools/video-editor/runtime/project-element-selection.test.ts`
9. `src/integrations/paired/objectCachePolicy.test.ts`
10. `src/integrations/astrid/transport.test.ts`
11. `src/tools/video-editor/runtime/element-admission-build.test.ts`

Result: exit code `0`; Vitest duration `18.33s` (wall time about `19.55s`); test files `11 passed, 0 failed, 0 skipped / 11`; tests `115 passed, 0 failed, 0 skipped / 115`; unhandled errors `0`. Full output: `/tmp/app-m0-loopback/vitest-targeted.log`.

This is a Linux socket/process-enabled result only. No macOS run was performed or claimed. It validates the two-file listener-error fix in `astridAcpBridge.test.ts` and `pairedTransport.test.ts`: both suites pass without the restricted-run listener timeouts.

Restricted full-run classification is unchanged: `17,954 passed / 56 failed / 24 errors` in `1,447` files, `2,384.29s`, exit `1`. The frozen 11-file set contained 50 of those failures: local-listener timeouts in `pairedTransport` (11), `objectCachePolicy` (6), and `astridAcpBridge` (5); direct local-listener `EPERM` in `astrid/transport` (6) and `project-element-selection` (1); child-process/IPC restrictions in `vendorLock` (`spawnSync git EPERM`, 11), `element-admission-build` (`spawnSync /opt/node22/bin/node EPERM`, with tsx IPC `listen EPERM`, 1), and process fixture/canary failures (ProcessManager 3, processFixture 3, canary 2). `astridBridgeProxyPolicy` (1) timed out while its spawned Vite preview/local listener fixture could not complete. All 50 pass in the socket-enabled targeted rerun.

The six excluded baseline failures remain unaddressed and were not rerun here: two `PanelFrameAnchor`/`PanelPreviewService` example-governance coverage assertions, two `HoverScrubVideo` CORS attribute assertions receiving `null` instead of `anonymous`, one hosted `AuthContext` loading assertion receiving `true` instead of `false`, and one `useAgentSession` proposal assertion receiving `bridge_contract_violation` instead of `session_not_owned`. These are unrelated governance/UI/product assertions, not loopback/IPC baseline failures.

## Remote App integrated M1 unit batch — 2026-10-19T20:46Z
Central app-full-1019202612-15847, command npm test -- --maxWorkers=3, App tree6a601fc0340fddec22e5ac5340e6460c938fb761 (integration9a0ff406e before bounded recovery-pin34b9cfc93). Exit1,1195s wall/1189.02s Vitest.1452filesPASS/5FAIL;18,265testsPASS/12FAIL/3audited expected-fail (18,280total); no unhandled error section. Both no-smoke and strict known-failures gates passed (exact3authorized,0forbidden).
Six failures match the recorded real baseline: examples-governance PanelFrameAnchor/PanelPreviewService import coverage(2); HoverScrubVideo.gateway CORS attributes(2); hosted AuthContext permission-loading(1); useAgentSession.proposal-vertical absent bridge capability refusal(1). No change to these files in M1. No baseline failures weakened/skipped.
Six new failures are source-derived pairedRoutePolicy tests: commitTimeline,listTimelineCommits,getProjectMediaSelection each expected allowed through BOTH /api/runtime and /api/astrid, but unchanged paired policy denies them. PLAN2.12 keeps new authoring path on local Runtime door; hosted/paired relay deferred. Test-only scope/correction requested in escalations/app-20261019T2030Z-local-only-relay-tests.md. No relay policy expanded, no blanket assertion removed. All new mounted session/recovery/projection/preview tests in this source batch passed.
Subsequent recovery-pin34b9cfc93 (integrationdc77a3ca6) has74focusedPASS4files; not covered by this earlier full snapshot. Actual browser first attempt failed BEFORE editor with HTTPS navigation reset; this full unit result is NOT real App M1 gate evidence. Linux only; macOS unrun.
