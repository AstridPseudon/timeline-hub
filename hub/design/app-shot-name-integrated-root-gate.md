# App M2 shot-name integrated root gate

Status: **blocked by the real product path**. The repaired native source is composed onto App root `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` and the final-tree central browser gate reached the production embedded ShotEditor, but no Runtime commit request was emitted after the Unicode name was submitted. Per the integration instruction, work stopped at that product failure; this is not a source-only qualification.

## Final source and tree

- App base/root: `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` (`3599fc49ad76dfdd7847ab4c813fc9317a0304eb^{tree}` = `74130f681f6b0c87a7c61cb33d4ae6a092c03046` before the delta).
- Integrated final worktree tree: `f27821adaa105f7e430112ae9a511d8f90c537ff`.
- Native source chain ported: `a4fb4bbb0` session migration, `04810b121` draft-basis fix, and `09e377adb` hook-retirement fix, relative to the actual root. The real e2e source is from `5d9626a68`.
- Current hydration/recovery readiness and pins remain from root: `useTimelineSave.ts:102` still gates `initialReadReady` on both the initial commit read and `initialRecoveryChecked`; `useTimelineCommandSession.ts` retains the same readiness guard. No settings surface was expanded.
- Key final source hashes: `ShotEditorView.tsx` `3ff46cb026aab47651087762d8169f2b9d4a756f1ebc15bc6a1248342ec76088`; `useNameEditing.ts` `884651d931ea8d22c9fbca844fb2f9b66af0bdc6d127e5fbcf38ce3446942e25`; `commitSession.ts` `ca0224ff5003d4b6e824f01d934654eb2564faec624103cd573f5c057a301730`; `shotSetCapture.ts` `952a0b5e1df128f8c8aa6350cbfe8329e54425f7b66e10f4553f1cae3070cb74`; `shotSetGesture.ts` `2b0c80ab61dddaec5233f789b1026eb2e00c407206b2714b740d45ef201d7a48`; `useTimelineCommandSession.ts` `811b2d8595b3aeaaa7dbc1d33844783c89815e665c5472b0892c267458226ac3`.
- Real gate source/config hashes: `tests/e2e/local/shot-name-command.spec.ts` `eaec1c25793041d42f459c182e88b70370ba9bdfd2dc67f5c4c3a4a268a9648d`; `playwright.shot-name.config.ts` `69cfca264db2961b18d35e8d6fce02056d247353aa4e92ffa00c2fa75c53dc82`; app support `754eba0a62b8e3328d02da579032658a55b412bee750ca6e3a64972bf9061e99` and harness `28715d4b3e8508a5b1b840eb57428946ee32568d445d0bc7c31f9c4f8fe9397a`.

## Actual binding and gate coverage

The source uses the production path:

`AstridTimelineEditor` → `useTimelineState` editor operations → guarded `useTimelineCommandSession` `shotSet` port → `LocalTimelineShotBrowser` → `ShotEditorView`.

The real journey opens the seeded embedded shot through `[data-shot-group-key]`, double-clicks the label `F2 canonical shot`, verifies `[data-canonical-occurrence-id="f2-occurrence"]`, clicks the production `span[title="Click to edit shot name"]`, and fills the first native dialog input. It observes only POST `/v1/projects/.../timelines/.../commit` and rejects POST `/timelines/.../composition-revisions`. Later assertions are wired to the mounted `Undo` button and `Recover saved edits` button scoped by `[data-owner-id="..."]`.

The intended single test covers raw Unicode preservation, `shot.set`, opaque-field preservation, reload, Runtime inverse Undo, lost-ACK retry, restart/recovery, exact request-body/idempotency-key retry, and same-property `409` draft retention. The source helper was corrected to use `harness.seed.projectId` for the raw shot read; `ThreeProductsSeed` has no `projectId` field.

Central suite registered:

`e2e-shot-name-integrated-root3599-treef27821-agent8130-runtime2c4-public12`

It ran with Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public `12`, Chromium 141, short temp `/tmp/tl-shot-name-integrated-f27821`, and unset `ASTRID_PUBLIC_CHECKOUT`/`ASTRID_APP_DIRECT_DIST`. Strict source, peer, cache, and browser/build preflight passed.

Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-shot-name-integrated-root-gate-e2e-shot-name-integrated-root3599-treef27821-agent8130-runtime2c4-public12-1020153124-16620`

The product gate failed at `tests/e2e/local/shot-name-command.spec.ts:150`:

```text
Error expect(received).toBe(expected)
Expected: 1
Received: 0
Timeout 90000ms exceeded while waiting on predicate
await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
```

The trace/error context shows the actual dialog opened, the padded `Édit 🎬` value was entered, and Enter was pressed, but no `/v1/.../commit` request appeared. Consequently Runtime acceptance, raw preservation, Undo, lost-ACK/restart, exact retry, `409`, and legacy-traffic assertions were not reached. Trace: `notes/shot-name-runner/runs/.test-.../browser-artifacts/shot-name-command-M2-real--d8b46-nd-same-name-conflict-draft/trace.zip`; error context is alongside it. Do not claim browser qualification or zero legacy traffic from this run.

## Tests and controls

- Targeted Vitest: `TMPDIR=/tmp/tl-shot-name-targeted node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/components/ShotEditor/hooks/actions/joinSegmentFreshness.test.ts` — **8 files, 149 tests passed**.
- ESLint on all touched App/e2e files, including `tests/e2e/local/shot-name-command.spec.ts`, with `--max-warnings 0` — **passed**.
- `node --test scripts/testing/current013-integration.test.mjs` — **1 passed**.
- `TMPDIR=/tmp/tl-shot-name-discovery PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-shot-name-discovery-output node_modules/.bin/playwright test --config playwright.shot-name.config.ts --list` — **exactly 1 test discovered**.
- `bash -n` on the central runner and `git diff --check` — **passed**.
- No full suite, project `tsc`, install, framePCM, or renderer run was performed.

## Remaining writers and next step

Remaining writers are explicitly bounded: standalone/canonical fallback name writing in `ShotEditorView.tsx` (`enqueueCanonicalShotPublish` / `updateCanonicalShotName`), ordinary legacy fallback there via `useUpdateShotName().mutate`, gallery/list writing in `src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.tsx` via `useUpdateShotName().mutateAsync`, and the separate canonical settings writer in `ShotEditorView.tsx` (`updateCanonicalShotSettings` through the whole-graph CAS callback). These were intentionally not expanded or removed in this gate task, and the failed browser run cannot establish their traffic behavior.

Next step is to diagnose why the production name submit after the real click/input interaction does not call the mounted `shotSet` capture/submit path, then rerun the one registered central suite once the product fix is made. No manager merge or completion-row claim was made.
