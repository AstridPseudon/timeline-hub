# U3b exact live upstream refresh: BLOCKED / HOLD

Node **v22.22.0**. Worktree `/home/user/work/wt/app-U3b-live-refresh-sol-2013`. Read PLAN U3/A2 and Runtime commit-v2 contract. Stopped at first ordinary qualification failure as required; no test expectations changed, no additional semantic fix, and no integration request.

## Exact merge state and changes

- HEAD remains base `e2e75b38e29ef0f5f628d0fdab988d701205b758`, tree `81171cb2740e7a4003c93e86576a4aa2c7cdea1e`.
- Read manager's absolute `MERGE_READY` before edits. Actual git-path `/home/user/banodoco/reigh-app/.git/worktrees/app-U3b-live-refresh-sol-2013/MERGE_HEAD` contains exact live `65c1771b78ab972295d4bea91c93970e5bb65e74`. Common ancestor `6b1b337cc3ef479318853709c97514c0d90efb6b`.
- One textual conflict: `src/tools/video-editor/hooks/useTimelineCommit.ts`. Conflict markers removed; index still unmerged because staging/committing belongs to the harness. No final commit/tree/parents or upstream-ancestor result can be claimed yet.
- Worker edited only that hook and `src/tools/video-editor/lib/timeline-mutation-engine.ts`. Hook adopts upstream's new `serializeResolvedConfigForSave`; helper keeps upstream's derived-label filtering and invokes retained `serializeResolvedTimelineEdit` with current authored/resolved bases, preserving opaque roots/output. No speculative abstraction, new writer, executor removal, waiver, test change, pin regeneration or generated-file change.
- Exact scope audit: **84 changed paths with rename detection off, all 84 from the actual upstream delta**. No outside-delta or untracked path. Git's rename-aware stat reports 82 paths. Detailed path list below.

## Qualification failures requiring a scoped follow-up

1. **Retained mounted test:** `src/tools/video-editor/hooks/useTimelineCommit.test.tsx:185`, `splits the original raw seed without authoring display defaults (label p1-video.mp4)`. Expected both halves to retain explicit raw `label: 'p1-video.mp4'`; received both without it. Upstream's label cleanup treats a stored label equal to an asset filename as derived. The entire retained test file remains baseline bytes.
2. **New upstream test:** `src/tools/video-editor/lib/timeline-data.test.ts:637`, `treats a label saved before this rule (equal to the current derived name) as unset`. Expected `second take.mp4` after save/reload with a renamed asset; received `first take.mp4`. Retained `rowsToConfig` carries authored raw labels. The upstream test remains exact upstream bytes.
3. **App typecheck:** `src/app/onboarding/BrowserTourEditor.tsx(17,31): error TS2307: Cannot find module '@/tools/video-editor/components/AgentChat/TourChatPanel.tsx' or its corresponding type declarations.` New welcome host imports a component absent in the retained base. That component exists unchanged at common ancestor and live upstream, SHA256 `b9e61ca2f0c5db8259474cdd5247a0f336a87551f528758f0d4172eb6e78e274`; Git kept the base's removal during the clean merge. No replacement was invented or restored after qualification failed.

Evidence against simply carrying upstream cleanup unchanged: it removes an explicitly authored field from the original mounted split behavior. A policy decision is needed to reconcile that with upstream's legacy-cleanup intent. I did not choose a policy or weaken either expectation. No expected-failure annotation was added.

## Commands and results

Run from the assigned worktree, scratch/logs in `/tmp/w-64c5a933cf`. Shared node_modules resolves to `/home/user/work/app/node_modules`; no shared dependency/cache writes. Owned preload `/tmp/w-64c5a933cf/vitest-preload.cjs` sets `globalThis.__dirname` to this worktree's `config/testing` directory.

```sh
TSX_DISABLE_CACHE=1 node --require "$TMPDIR/vitest-preload.cjs" node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts
```

**Exit1: 280 pass, 2 fail, 282 tests; 10 passing files, 2 failing files.** The previous eight-file **210-test cohort all passes** in this combined run (36+3+11+19+1+32+86+22); added mounted/serialization neighbors contribute 72 tests with the two failures above. Existing React act warnings are in `logs/vitest-core.log`.

```sh
TSX_DISABLE_CACHE=1 node --import tsx --test --test-reporter=spec tests/e2e/local/p1-diagnostic-safety.test.ts tests/e2e/local/support/public-trim-preflight.test.ts tests/e2e/local/support/playwrightSkipGuard.test.ts tests/e2e/local/support/selected-param-credential.test.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/auto-real-proxy-observation.test.mjs tests/e2e/local/support/native-transition-clear.contract.test.mjs
```

**Exit0: 39 pass, zero failed/cancelled/skipped/todo**, including diagnostic12/public-trim8/skip-guard5/support14. Expected negative-control NOT RUN/undeclared-skip/zero-pass messages remain asserted. Log `logs/node-targeted.log`.

```sh
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
```

**Exit2:** single TS2307 above. Log `logs/tsc-app.log`. Node/root typechecks were not started after the first-failure return condition.

```sh
node node_modules/eslint/bin/eslint.js --no-cache --report-unused-disable-directives --max-warnings 0 <all 60 changed existing TS/TSX paths>
```

**Exit0, zero warnings.** Exact ordered paths in `logs/lint-files.txt` were passed as individual Python subprocess argv elements, selected from `git diff HEAD --name-only --diff-filter=ACMR`; `logs/eslint.log` empty.

`git diff --check`: exit0. Changed-source conflict-marker scan: zero markers. No full suite, browser, hosted build, localhost/live-socket run, or original body run. Pinned running P1 untouched. Playwright discovery P1/P3/P2 **not run after the first-failure stop**; required future discovery remains 2/1/8, preflight only. Changed welcome/client/tour targeted suites and Node/root types also remain unverified.

## Frozen-source/provenance audit

Audit logs `logs/source-audit.log` and `logs/scope-audit.log` record the checks:

- Runtime lock is exact base blob `2800842c772228b508ca1b7a53d799bc22df29b9`, pin `34eac0041b0891e9011966b39bcbd26053fde5bc`, producer `sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572`. Independently hashed **all78** producer artifacts from `git show` at that pin against `contract/artifacts.json`; all match. **All13 App mappings** match their lock hashes and exact pinned producer bytes. No schema/DTO regeneration.
- Composition archive exact baseline bytes, SHA256 **819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234**, package0.0.14, retained path `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`. SHA512 SRI matches lock: `sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`. Archive identity is not live renderer/body proof.
- `git diff HEAD -- runtime.lock.json package.json package-lock.json vendor` empty. No ba8585 instrumentation, b221 artifact or popup17324 imported.
- Mounted `useTimelineSave.test.tsx` exact base blob **0bd79ea18c3fc522852e4444c8479da91d58ef69**. Production `useTimelineSave.ts`, `localSaveSession.ts`, `commitOutbox.ts` exact base. Existing full request/reply DTOs and commit transport unchanged. Client's only incoming HEAD diff adds `createProject` through existing mutation wrapper. Door/direct-harness source/config unchanged by this worker.
- Entire original P1 file exact base blob **feb26946d62db9a4a02dab8dca1c0dc7320f2681**, so its original first/second bodies remain byte-identical to approved base. Diagnostics exact base source/test **a49f6bfb20c21b01bc709db79d3fa3cd47b216c3 / 3b72ee8fff59b6d7e9919aa936f0ac3e6d9a4ff5**. Gate5 whole source exact **37caf28577d42fbe98afd2320dffa3c72e6e74b1**.
- Public-trim preflight source/test exact base **51dc979958f140dfbb649e799363c5e0a747a2c5 / bdd3cda7e117d794f264b6c42d0b31e82fe4d573**; all8 strict controls passed.
- Central quick-descriptor result1772 reused only for unchanged source/test **521baa4383de5b743afc40f562d296d15ea27ff7 / 458c2fd469fbf25c26067d355e64e0bd977ba6d1**. Read existing summary: `env TSX_DISABLE_CACHE=1 node --import tsx --test tests/e2e/local/support/quick-descriptor.test.ts`, **8 pass/exit0**. No duplicate service/socket run. This does not qualify the complete refresh.

## Explicit changed paths and reasons

All paths are incoming upstream delta; upstream exact includes named retired files. Only the two source-resolution paths above were edited by this worker. No files were manually deleted. Composed/retained paths preserve earlier draft-only code in clean merges or the resolution.

| Path | vs exact live | Reason |
| --- | --- | --- |
| `docs/structure_detail/shared_utilities.md` | upstream exact | Upstream onboarding/shared-utilities documentation. |
| `docs/video-editor/onboarding-lantern-valley.md` | upstream exact | Upstream onboarding/shared-utilities documentation. |
| `eslint.shared-layer-allowlist.js` | upstream exact | Upstream removes retired wizard allowlist entry. |
| `src/app/Layout.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/Layout.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/hooks/useOnboardingFlow.test.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/app/hooks/useOnboardingFlow.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/app/main.bootstrap-order.test.tsx` | composed/retained | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/main.runtime-origin.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/main.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/main.welcome.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/BrowserTourEditor.integration.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/BrowserTourEditor.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/StarterProjectHandoff.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/StarterProjectHandoff.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/WelcomeConnection.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/WelcomeFlow.test.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/WelcomeFlow.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/prepareStarterProject.test.ts` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/prepareStarterProject.ts` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/welcomeBootstrap.tsx` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/welcomeProgress.test.ts` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/app/onboarding/welcomeProgress.ts` | upstream exact | Upstream welcome-first bootstrap, demo and starter-project handoff/tests. |
| `src/features/tasks/components/TasksPane/TasksPane.tsx` | upstream exact | Upstream shared task-pane surface for welcome-tour chat. |
| `src/features/tasks/components/TasksPane/components/TasksPaneSurface.tsx` | upstream exact | Upstream shared task-pane surface for welcome-tour chat. |
| `src/integrations/runtime/client.test.ts` | upstream exact | Upstream createProject wrapper and test; keep commit transport. |
| `src/integrations/runtime/client.ts` | composed/retained | Upstream createProject wrapper and test; keep commit transport. |
| `src/moduleImportCoverage.test.ts` | upstream exact | Upstream removes retired onboarding module reference. |
| `src/pages/Home/PublicAstridCallouts.scheduling.test.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridCallouts.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridHeroCta.test.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridHeroCta.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridInstallDialog.test.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridInstallDialog.tsx` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/pages/Home/PublicAstridShell.css` | upstream exact | Upstream homepage layout/focus/callout scheduling and tests. |
| `src/shared/components/OnboardingModal/components/OnboardingStepWithContinue.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/SetupStatusLine.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/AstridSetupStep.test.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/AstridSetupStep.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/CommunityStep.test.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/CommunityStep.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/PrivacyDefaultsStep.test.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/PrivacyDefaultsStep.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/components/steps/TimeOfDayStep.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/hooks/useOnboardingSteps.test.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/hooks/useOnboardingSteps.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/lib/onboardingColors.test.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/lib/onboardingColors.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/OnboardingModal/types.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx` | upstream exact | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/RuntimeConnection/RuntimeConnectionPanel.tsx` | upstream exact | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/RuntimeConnection/SetupStatusLine.tsx` | upstream exact | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/RuntimeConnection/copy.ts` | upstream exact | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/SettingsModal/sections/AstridStatusSection.tsx` | upstream exact | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/SettingsModal/sections/ConnectionSection.tsx` | composed/retained | Upstream connection copy/status-line move; keep existing schema guards. |
| `src/shared/components/modals/OnboardingModal.tsx` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/hooks/__tests__/useOnboarding.test.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/shared/hooks/useOnboarding.ts` | upstream exact | Upstream retires competing wizard/tests; status-line component moves. |
| `src/tools/video-editor/commands/runner.ts` | composed/retained | Upstream resolved-config effect serialization; retained executor stays. |
| `src/tools/video-editor/components/TimelineEditor/ClipAction.tsx` | upstream exact | Upstream displayName/persisted-label distinction and round-trip tests. |
| `src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx` | upstream exact | Upstream sequence presentation and regression coverage. |
| `src/tools/video-editor/compositions/TimelineRenderer.tsx` | upstream exact | Upstream sequence presentation and regression coverage. |
| `src/tools/video-editor/hooks/useTimelineCommit.ts` | composed/retained | Textual conflict resolution; preserve mounted handoff/held sources and adopt upstream save helper. |
| `src/tools/video-editor/lib/clipDisplayNames.ts` | upstream exact | Upstream displayName/persisted-label distinction and round-trip tests. |
| `src/tools/video-editor/lib/timeline-data.test.ts` | upstream exact | Upstream displayName/persisted-label distinction and round-trip tests. |
| `src/tools/video-editor/lib/timeline-data.ts` | composed/retained | Upstream displayName/persisted-label distinction and round-trip tests. |
| `src/tools/video-editor/lib/timeline-mutation-engine.ts` | composed/retained | Combine upstream derived-label filter with retained authored-root serializer; exposes policy conflict. |
| `src/tools/video-editor/pages/VideoEditorPage.tsx` | upstream exact | Upstream explicit onboarding/tour integration. |
| `src/tools/video-editor/tour/card/TourCard.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/editorTourGate.test.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/tourBeats.test.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/tourBeats.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/tourFlag.test.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/tourFlag.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/useEditorTourHost.test.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/useEditorTourHost.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/useEditorTourTrigger.test.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/runner/useEditorTourTrigger.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/timeline/EditorTourScenePresentation.test.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/timeline/EditorTourTimelineDriver.test.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/timeline/EditorTourTimelineDriver.tsx` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/timeline/useTourMediaWarmup.test.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `src/tools/video-editor/tour/timeline/useTourMediaWarmup.ts` | upstream exact | Upstream welcome-tour entry and media/frame presentation; retires old trigger test. |
| `tests/e2e/video-editor-workflow-parity.spec.ts` | upstream exact | Upstream journey stops interacting with retired automatic wizard. |

## Recommended next steps and limitations

1. Orchestrator scopes the authored-label/legacy-cleanup policy resolution and precise upstream TourChatPanel dependency follow-up. Preserve behavior tests; do not choose a new contract or infer a pin tuple.
2. Resume branch-only source work, repeat affected tests, then complete changed upstream suites, App/Node/root types under flock/4096MB, scoped lint and P1=2/P3=1/P2=8 list-only discovery. Request manager central execution if necessary support/browser sources change; do not duplicate pinned P1.
3. After harness staging/commit, manager must verify actual two parents (base e2e75 first, exact65c177 second) and run `git merge-base --is-ancestor 65c1771b78ab972295d4bea91c93970e5bb65e74 HEAD`. Future parent/ancestry results are unverified here.
4. **HOLD integration** until original P1/P2/P3 GO/freeze. No live-body credit. No original tests weakened; no full request; no Git fetch/merge/add/commit/rebase/reset/checkout/push run by worker.

Wrote ordinary worker report, absolute orchestrator design report, conventional commit-message draft and BLOCKED. No DONE because qualification is incomplete. Logs are small copies of owned TMPDIR results; no fixtures/dependencies in worker folder.
