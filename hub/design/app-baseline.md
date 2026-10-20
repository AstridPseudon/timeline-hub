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

## Final M1 product + approved relay-test batch — 2026-10-19T21:24Z
Central app-full-1019210225-20828, npm test -- --maxWorkers=3, tree706101f52dc180d3eaac7fd7cd18d1bfc5a841a7 (integration2d8eac72e; all final product changes plus approved04ffb3c20 relay-test). Exit1,1263s wall.1453filesPASS/4FAIL;18,286testsPASS/6FAIL/3audited expected-fail (18,295total). All6failures are the original recorded baseline: PanelFrameAnchor/PanelPreviewService import coverage(2), HoverScrubVideo.gateway CORS(2), hosted AuthContext permission loading(1), useAgentSession.proposal-vertical absent bridge refusal(1). No new product/unit failures, no unhandled error section. Exact6new local-door-only relay assertions nowPASS (1944filecases) with paired product policy unchanged. No baseline assertion skipped/weakened.
Later integrationdd376d5e0 differs from this full tree only in the4journey/e2e support files. Its reviewed worker source tree dbcd92f45bed96990fa25a5a5878057e57d2e72b passed BOTH REAL M1 browser cases in app-m1-journey-python-basis-e2e-m1-gesture-1019210718-13326 (34.7s +27.6s,3.0min browser; normal Agent a8eb28af/Runtime82df3cf/Composition7aa384a unchanged). Independent Agent reads its own scoped pinned raw closure before capture; original hashes remain checked, no product numeric/schema bypass. Actual main durability loss/retry/restart/inverse/readback +retained conflict/reload identities passed. Real committed preview target label observed; composed pixels/audio not claimed. Runtime main integrated qualification requested ondd376d5e0. Whole neutral3products/fullTimeline/macOS unrun this batch.

## Restored five-journey + public package integrated batch — 2026-10-19T22:18Z
App integration85be65a0a6fcf5dbf3575d95fecfdc445e2edc02, exact tree0b115750bdc4981af72bb9b5a5e64ceb1b5a2ee7, clean/unchanged throughout both final requests. app-full-1019215846-15801, **npm test -- --maxWorkers=3**: exit1,1061s wall/1055.75s Vitest; **1453filesPASS/4FAIL;18286testsPASS/6FAIL/3expected (18295total)**. Both prechecksPASS: no placeholder smoke tests; EXACT3authorized expected-failure markers/0forbidden. Manager compared all final FAIL node headings against prior full app-full-1019210225-20828: IDENTICAL; no unhandled-error/rejection/exception section. Four failing test files are byte-unchanged from original main60aa26b95. Exact causes unchanged: two example imports missing PanelFrameAnchor/PanelPreviewService coverage; two gateway CORS `null` vs `anonymous`; hosted auth loading `true` vs `false`; absent bridge proposal refusal `bridge_contract_violation` vs `session_not_owned`. No new App product/unit failures, no skipped/weakened baseline assertions. Repo full remains RED, not all gates green.

Same-tree **integration:app e2e-m1-closure app-e2e-m1-closure-1019215846-11716 PASS5/259s**: unfiltered npm run test:e2e:three-products with normal shared Runtime/Agent source/Python env, renderer OFF. Restores BOTH original named positive journeys (track/transition conflict+retained draft, open-App Runtime restart+unsent draft recovery) alongside original Agent→App and BYTE-IDENTICAL two real mouse M1 helpers/cases. Stronger Keep/recover/originalCAS/UseLatest/nativeIDB/exactly1save assertions pass. All actual native guard/outbox/exact retry/Runtime restart/undo/immutable closure/history/opaque+transition preservation/nativeinputs visualization/accepted preview label/0legacy move+inverse assertions pass. Captured tupleAgentddc1bac3/Runtimeff0ae58/Composition7aa384a: service completed22:03:10; App mirror Agent reflog advanced to4ffbb8b0 at22:03:19, AFTER completion (filemtime same), so no source overlap. Main's historic two-case qualification remains separate evidence. Full and browser snapshots both match App tree0b115750 exactly.

Reserved root fix consumes EXACT0.0.8 tarballSHA25693bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa with React18.3.1/Remotion4.0.509 public exports; all77installedfiles byte-equal, freshconsumer8publicexports+5exactpeersPASS,6config-resolution casesPASS, final hostedbuildPASS81s. Granted exact bundledtheme assertion3PASS; specialized existing scene tests2PASS through config-only ESM-inline/peer resolution. No evaluator/preview/editing product changes in this preservation batch, no artifact rebuild/version change, old vendor deletion explicitly held for M3 callers. Actual App tsc command npm exec tsc -- --noEmit -p tsconfig.app.json reports EXACT original2errors (RuntimeConnectionProvider90TS7053,AgentChatNewChatButton80TS2550),0new diagnostics.

App M1 evidence READY; overall M1 recording waits orchestrator deep audit/final cross-manager classification. M2 DESIGN ONLY until that record. Frame/audio parity, all-writers/popup0legacy, full unfiltered Timeline suite, owner film and macOS UNRUN/not claimed. Initial preserved-only attempt failed before browser on old0.0.2 build; first combined diagnostic1PASS/1setupFAIL/3notrun corrected normal clip selection after reload without changing transition-value assertion; candidate thenPASS5/203s before final integratedPASS5/259s. No extra final/full request was submitted.

### Postrestore full — 2026-10-19T23:05Z
`app-full-1019224105-27715`, integration9d0a383a1/tree d27f9992672c2c5d54d4dbe6fa0d9328cea5971a: `npm test -- --maxWorkers=3` => **18291PASS/6FAIL/3expected**,1453filesPASS/4FAIL,1391s. Exactly5new restoreguard tests pass versus prior18286. Manager compared complete FAILnodeheadings: exactsame6 as app-full-1019215846-15801; all4failingfiles byte-identical to original60aa26b95. NoUnhandledErrorssection. Both prechecksPASS/exact3authorized0forbidden. Full remainsREDbaseline, **0new**. NewM1mixedcase is E2Eonly and originalsrc/unitinputs unchanged; exactpassing browsercandidate b5c6aab85/treea6d1a0c6 gets separateintegrationmerge and onepostbatchfull perqueuepolicy.

### Final quiet full on unchanged App source — 2026-10-20 01:35Z
Lead replacement `app-full-m1-bounded-integration-1020011705-2755` completed `env ASTRID_CHECKOUT=/home/user/work/agent npm test -- --maxWorkers=2` on final2bfde69ea/tree dd1fe6a725cf20015f7b8cb4a966bdf507319653: **18301PASS /6EXACTBASELINEFAIL /3original expected**,1454PASS/4FAIL files,1458executed,1068s wall/1007.12s Vitest. Exact failed-node set equals27715; both prechecks pass, no unhandled worker error. Retained cache (mtime01:35:46Z) proves ProjectTimelineSelectors18tests ran/pass2823.704481ms; Home lifecycle3225.534543ms and EmptyWorkspaceGuidance2508.00912ms also pass. Manager captured machine-readable nodes+cache evidence in managers/app/notes/quiet-final-2755.json before another suite could overwrite it.
Prior24066 readiness extras do not recur at low load. Classifier finds no causal App JS delta: relevant runtime imports emit identical JS, target implementations unchanged, current config unchanged from qualified9d0; original/candidate16/16 wholefile passes twice. Exact scheduler cause of24066 is unproven; this is not a blanket pre-existing/flaky classification. 12729 also completed identical Vitest result but shell postprocessing failed; authoritative final run is2755, no additional full requested. App M1 evidence ready; global record now awaits Agent opaque-item remap fix and orchestrator decision.

### Authorized SDK example correction — 2026-10-20 08:26Z (branch, merge held for settings safety)

Candidate8846d7189ddc3f24e8fc7186d5f55e8949efae90 changes ONLY the granted transcript-panel-example.ts and examples-governance.test.ts. All original624 governance cases/assertions stay; one new hover contract case is added. Exact old failures `public export "PanelFrameAnchor" is imported by at least one example` and `public export "PanelPreviewService" is imported by at least one example` now pass through actual public service/DOM-anchor/disposal usage. Governance625/625PASS; neighboring real TranscriptPanel.hover5/5PASS, combined630/630PASS. Narrow real TypeScript program rooted at the actual example/current SDK barrel PASS; scoped lint/diff-check PASS. Commands/report: design/app-sdk-preview-example-authorized-fix.md. Manager reviewed81-line two-file delta. No test exclusion or original expectation change. Current integration still1be and retains six historical full failures until the bounded candidate is merged; this branch fixes two, it does not relabel the full11559 result or claim a new full. Settings safety must merge FIRST.
