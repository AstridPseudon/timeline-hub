# U3b final current-live refresh independent review

## Verdict

**PASS for the scoped source qualification; integration remains HOLD.**

Reviewed `/home/user/work/wt/app-U3b-live-final-review-2038` at `14d4acd749b663231b3099767dd3dec247d911d0`, tree `2a31fc488645ca77e51f320c77b37832f947a4c1`, against the settled PLAN/U3/A2/C0/D24 obligations and upstream `65c1771b78ab972295d4bea91c93970e5bb65e74`. No source, test, generated file, pin, branch, or ref was changed by this review. Worktree is clean.

The target has the expected ancestry: `7978ed829e8c12ca4058676f43208a882e381966` has parents `e2e75b38e29ef0f5f628d0fdab988d701205b758` and `65c1771b78ab972295d4bea91c93970e5bb65e74`; both are ancestors of the reviewed child and of the reviewed HEAD.

## Findings

- The required original 282 core assertions are an exact byte prefix of the current `useTimelineCommit.test.tsx`; only three append-only mounted regression cases follow them. No passing expectation was rewritten, skipped, weakened, or marked expected-failure.
- Mounted production-path coverage passes for absent labels, filename-equal authored labels, asset-ID-equal raw labels, explicit writes, and prepared-media additions. The implementation preserves authored raw labels through `rowsToConfig`/`withAuthoredClipLabels` and the mounted local-save/outbox handoff. The upstream legacy row-projection cleanup remains unchanged and passes.
- No equality-based authored clear is introduced. Equality checks remaining in `assembleTimelineData`/projection code only establish non-enumerable derived display labels or preserve unchanged raw basis; explicit enumerable writes, including explicit clear, remain edits. Wire-level label-clear support is not claimed.
- `TourChatPanel.tsx`, `NewChatMenu.tsx`, and `NewChatMenu.test.tsx` are byte-exact with upstream 65c1771 (SHA-256 `b9e61c…e274`, `624f4e…1635`, `246d22…7576`). The retained AgentChatMenu/NewChatModels/ChatUpdateNeeded adapters preserve retained callers and their tests. No cloud, development-extension, M5, popup, b221/ba858, or new writer source was imported.
- The 78-artifact audit passes: 65 producer-manifest entries plus 13 runtime-mapped App artifacts match declared sizes and SHA-256 values. Runtime producer pin `34eac0041b0891e9011966b39bcbd26053fde5bc`, stamp `sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572`, edit schema identity `d106…`, and Composition archive SHA-256 `819acf…40234`/package-lock SRI remain frozen.
- Frozen runtime/client/outbox/provider/capture/undo/door sources, package files, vendor bytes, P1 source (`feb269…f2681`), Gate-5 source (`37caf…74b1`), diagnostics, public-trim controls, and quick-descriptor sources are unchanged from the task base. The central quick-descriptor result `1772` remains 8/8 PASS and was reused, not rerun.

## Verification

All commands ran from the reviewed worktree with Node `v22.22.0`, Vitest `4.1.5`, shared `node_modules` read-only, Vitest `--configLoader=runner --no-cache --maxWorkers=2`, and owned temporary preload/output under `/tmp/w-5c7eb8f92a`.

```sh
TSX_DISABLE_CACHE=1 node --require /tmp/w-5c7eb8f92a/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts
# exit 0 — 12 files, 285/285 tests
```

The focused 22-file Vitest command from the qualification design passed **380/380** (exit 0). The exact seven-file Node command from the design passed **39/39** (7/7 files, exit 0). It included only static/control tests; no browser body, localhost service, HTTP, seed, benchmark, build, or live preflight run was performed.

```sh
TSX_DISABLE_CACHE=1 node --require /tmp/w-5c7eb8f92a/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 \
  src/app/Layout.test.tsx src/app/hooks/useOnboardingFlow.test.ts src/app/main.bootstrap-order.test.tsx src/app/main.runtime-origin.test.tsx src/app/main.welcome.test.tsx \
  src/app/onboarding/BrowserTourEditor.integration.test.tsx src/app/onboarding/StarterProjectHandoff.test.tsx src/app/onboarding/WelcomeFlow.test.tsx src/app/onboarding/prepareStarterProject.test.ts src/app/onboarding/welcomeProgress.test.ts \
  src/integrations/runtime/client.test.ts src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx \
  src/tools/video-editor/tour/runner/editorTourGate.test.tsx src/tools/video-editor/tour/runner/tourBeats.test.ts src/tools/video-editor/tour/runner/tourFlag.test.ts src/tools/video-editor/tour/runner/useEditorTourHost.test.tsx \
  src/tools/video-editor/tour/timeline/EditorTourScenePresentation.test.tsx src/tools/video-editor/tour/timeline/EditorTourTimelineDriver.test.tsx src/tools/video-editor/tour/timeline/useTourMediaWarmup.test.ts \
  src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatModelLine.test.tsx
# exit 0 — 22 files, 380/380 tests

TSX_DISABLE_CACHE=1 node --import tsx --test --test-reporter=spec \
  tests/e2e/local/p1-diagnostic-safety.test.ts tests/e2e/local/support/public-trim-preflight.test.ts tests/e2e/local/support/playwrightSkipGuard.test.ts \
  tests/e2e/local/support/selected-param-credential.test.ts tests/e2e/local/support/timeline-scope.test.ts \
  tests/e2e/local/support/auto-real-proxy-observation.test.mjs tests/e2e/local/support/native-transition-clear.contract.test.mjs
# exit 0 — 7 files, 39/39 tests
```

```sh
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.node.json --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.json --pretty false
```

All three typechecks passed (exit 0). ESLint passed with `--no-cache --report-unused-disable-directives --max-warnings 0` over the exact 68 existing/added TS/TSX paths selected by `git diff --diff-filter=ACMR e2e75b38..HEAD`; `git diff --check` passed. The raw 87-path scan included 19 deleted files and was not used for linting.

Playwright list-only discovery passed: **P1=2**, **P3=1**, **P2=8**. No journey body or browser ran. The unchanged central quick descriptor is **8/8 PASS**. The initial worker’s unchanged Undo timing failure is retained as historical evidence; this review produced no failure, and the current core run is green.

## Disposition and next steps

No scoped blocker was found. The only decision made during review was to derive the requested 68-path lint set with `--diff-filter=ACMR`, excluding deleted paths as required by “existing/new paths.” No source edits or test changes were needed.

Keep integration, P1/P2/P3 execution, and freeze **HOLD** exactly as directed. The orchestrator/manager should perform the post-harness ancestry check and decide the separate P1/P2/P3/freeze gate; this review is not a merge request and does not authorize integration.
