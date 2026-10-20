# App release12 / Runtime 0.2.9 / Gate 5 composed source candidate

Source composition is complete; **actual Agent 0.2.9 + public12 pair SHA: PENDING**. The live paired gate is held. This is one exact source candidate, not release qualification or blanket approval to integrate the inherited 174-file cohort. No old frozen tuple was relabeled.

Worktree: `/home/user/work/wt/app-m3-release12-029-gate5-compose`; branch `tl/app-m3-release12-029-gate5-compose`. Final App commit SHA is assigned by the harness after exit, not yet available here. No project git commit/merge/rebase/checkout/push/ref mutation was performed.

## Exact lineage and delta

Base **`be499a7f0c421563bf4072b80415cd6b1d265035`**, the reviewed normal Runtime 0.2.9 App pin, whose parent is **`080a5743a4e38847e0cc84dd07ccada67adb27f1`** (current public12/render + SDK + shot-safety composition). The normal be499 pin supersedes the historical 0.2.8 placeholder language in the 080/source-only reports; those historical files were not edited.

Only these three reviewed commit diffs were applied with `git apply` (no whole-branch import):

| Reviewed source | Applied delta |
| --- | --- |
| `04346844f194909146d67d2f126640ba7edd6776` | Four-file after-ACK scheduling, original session regressions/helper update, isolated M2 Gate 5 helper/case and exact source guards |
| `e3a3b5a5bf287b60ab764bdf2bb2eff0135422b4` | Two-line ACP `/events` fixture response correction |
| `125515780d1745194d28b639874c1bdc323102af` | 45-line positive shared-placement regression coverage |

Six tracked paths, **+353/-13** total; the only product edit is `commitSession.ts`, **+8/-2** (net six lines). Patch SHA-256: `ce66343a1849f5818f5d5cd525e6de777a67c2865e3354a973ea61c46cee2c8d`. The four first-source blobs and two test-fix blobs are byte-identical to their reviewed commits. New B queueing calls `pump(false)`; a persisted uncertain A remains pending without automatic retransmission. Explicit retry/flush/recovery retains existing authority. B retains its original guards and suffix tokens.

All **21 original helpers and six original journey bodies** are byte-identical to be499. `prepareDependentMoves` and `faultFirstCommit` are unchanged; the new M2 case uses its separate `prepareAfterAckLossMoves`. Original session expectations and the current helper's external-edit/inverse suffix are byte-identical. No added skip/todo/fails/only marker or weakened behavior expectation.

No continuation/requester/bootstrap/PARAM/None/additional ordinary ports, a103 enlargement, native writer activation, or other worker changes are included. The strict six-file diff preserves all other SDK/shot/opaque/history/transition/accepted-projection/render download/capture source and tests, as well as default fixture timing and frozen bundles.

## Preserved tuple

| Field | Exact value |
| --- | --- |
| Runtime producer checkout | `/home/user/work/wt/app-m3-runtime029-producer-source` (read only) |
| Runtime source | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` |
| Contract/client version | `0.2.9` |
| Schema digest | `sha256:8d7f29873ff3417cda746e243ebc81cb9d54e41c972596d4d3ae591fc1de00cf` |
| Producer artifact manifest version | `sha256:e02a71b5b77479bdc8035a8a8d75ec57e9f1962b7f9195126739ab0d1ed063ac` |
| Component manifest digest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Composition | Immutable public `0.0.12` artifact, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |
| Actual matching Agent 0.2.9/public12 SHA | **PENDING** |

The unchanged 13-file Runtime vendor allowlist equals BOTH working and committed producer bytes and matches each recorded hash. Both normal vendor-lock check modes pass. No generated file or digest was edited. All 77 installed Composition files equal the artifact. Package/lock/vendor/contract bytes are unchanged from be499. Full individual hashes are in `notes/tuple-audit.json`.

Only this worker's ignored `node_modules` symlink selects the existing `/tmp/app-coherent-deps12/node_modules`; no dependency was installed/copied/modified. All77 file hashes, six peer manifests, and recursive shared/private cache metadata are identical before and after (`deps-before.json` equals `deps-after.json`). Shared dependencies/runtimes/venvs remained read only. Vitest used the worker-owned runner preload with `--configLoader=runner --no-cache --maxWorkers=1`; all Playwright cache/output paths were worker-owned. No build output or temp files were created in the worktree.

## Executed checks

Working directory for all commands: `/home/user/work/wt/app-m3-release12-029-gate5-compose`. Node `v22.22.0`, Vitest `4.1.5`. **31 files / 1,322 tests passed**, no failed/skipped assertions: session/recovery **307**, necessary SDK/ACP/auto **642**, current render/history/transport guards **373**. Exact commands and results:

`core` — **120 passed**, exit 0. Full log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/core.log`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts
```

`neighbors` — **187 passed**, exit 0. Full log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/neighbors.log`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/components/TimelineCommandRecovery.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts
```

`sdk-acp-auto` — **642 passed**, exit 0. Full log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/sdk-acp-auto.log`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/sdk/examples-governance.test.ts src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx src/shared/lib/placement/__tests__/documentPlacement.test.ts
```

`current-render-guards` — **373 passed**, exit 0. Full log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/current-render-guards.log`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/hooks/useTimelineHistory.test.ts src/tools/video-editor/hooks/useTimelineHistory.remote-boundary.test.tsx src/integrations/runtime/opaqueRootWriters.test.tsx src/tools/video-editor/lib/timeline-domain.transition.test.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/runtime/deterministicCapture.test.ts src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx src/integrations/runtime/recordedResponses.test.ts src/integrations/runtime/timelineCommit.test.ts
```

Scoped lint, source preservation, producer/artifact checks, and whitespace: all exit 0. Playwright discovery: exactly seven cases in one file; **list only**, no browser/server/global setup executed.

`source`:

```sh
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/audit-source.cjs
```

`producer-lock`:

```sh
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime029-producer-source
```

`local-lock`:

```sh
node scripts/vendor-lock.mjs check runtime.lock.json
```

`producer-artifact`:

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/audit-tuple.py
```

`diff`:

```sh
git diff --check
```

`lint`:

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts tests/e2e/local/three-products.spec.ts src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx src/shared/lib/placement/__tests__/documentPlacement.test.ts
```

`discovery`:

```sh
env PWTEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/playwright-cache PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/playwright-output node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
```

Read-only dependency audit commands (both exit 0; `cmp` exit 0):

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/deps-before.json
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/deps-after.json
cmp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/deps-before.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/deps-after.json
```

No full suite was requested; FULL21209 was left alone. No install/build/browser/project tsc/socket/live gate/heavy run was performed. Unit transport mocks and discovery do not certify the actual Agent/Runtime pair or render/frame/audio parity. Prior normal-pin vendor-lock temporary-fixture sandbox failures were not re-run or claimed green; the real producer-aware and local lock checks pass here.

## Decisions, pending work and future commands

No settled decision changed; no contradictory evidence found. Routine choices: apply exact approved diffs rather than their historical parent cohorts; keep all reports outside the repository; use the existing read-only private12 dependency tree. The bounded source task has no blocker. **Integration/adoption remains held for the actual published Agent pair and paired gate**.

Manager next steps: obtain the published full Agent 0.2.9/public12 SHA and frozen checkout, retain the Runtime941 producer lease, let the harness assign the composed App SHA, then review this exact candidate. Run ONE composed-source project typecheck later under the existing manager serialization rule (not run here):

```sh
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit
```

The manager must register the actual pair and exact composed hosted build in the central service before requesting any live suite. The historical `e2e-m1-gesture` definition currently uses moving integration paths and lacks the mandatory source pins/prebuilt-dist selector. Do not submit that unchanged lane or substitute old Bundle1/2 values. The following is a FUTURE service command template only; its Agent/build inputs are deliberately required:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  TIMELINE_BUNDLE_AGENT_HEAD="${FINAL_AGENT_PUBLIC12_SHA:?published full 40-character Agent SHA required}" \
  TIMELINE_BUNDLE_RUNTIME_HEAD=94114269d1ce23ab3224d7eca5a85138ce2b5fed \
  ASTRID_CHECKOUT="${FINAL_AGENT_CHECKOUT:?frozen matching Agent checkout required}" \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime029-producer-source \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_APP_DIRECT_DIST="${PAIRED_HOSTED_DIST:?hosted build from exact harness-assigned composed App SHA required}" \
  PWTEST_CACHE_DIR="$PWD/.gate5-playwright-cache" \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/browser-artifacts/${PWD##*/} \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M1 real'
```

`M1 real` selects preserved exact-retry/restart/undo, the new post-loss M2 Gate 5, and the preserved relevant-conflict case. The new case asserts mounted B capture only after A acceptance/lost ACK, no implicit A retransmission, original request body/key, reload/Runtime restart and explicit recovery, original B guards/new key at HA, independent Agent C rebase/retention, raw closure/history/undo, opaque/transition retention, Agent show/preview identity, and zero legacy POSTs. A source/prerequisite guard refusal is not a semantic pass.

Only AFTER the manager registers that exact pair/build/cache-safe command in the existing central lane:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-release12-029-gate5-compose e2e-m1-gesture) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

On wait exit 124, wait again on the same R, never resubmit. Preserved concurrent-edit/restart qualification can separately use `e2e-m1-preserved` only after the manager updates that lane to the same pair/build. No full old ordinary cohort is authorized by this report.

## Absolute handoff paths

- Design/report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-release12-029-gate5-compose.md`
- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/report.md`
- Notes/report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes/report.md`
- Exact commands/results, source/tuple/dependency audits and patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/notes`
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/commit-msg`
- Completion marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/DONE`
- Retention marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-029-gate5-compose/KEEP`

Retain this candidate and its source inputs until manager review and actual paired qualification. No integration request was made.
