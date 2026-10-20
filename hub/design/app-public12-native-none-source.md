# App public12 native transition None — source unit complete, qualification HELD

Worktree: `/home/user/work/wt/app-m2-public12-native-none-source`.
Base: `080a5743a4e38847e0cc84dd07ccada67adb27f1`.
Reviewed source authority: `90f39e080ded099a0c73893f26c91b51b2abcc74` only for the logical clear delta and its dependency closure. PLAN and `design/app-native-none-review.md` were read first. No ancestor merge, root/pin/generated-client changes, integration writes, branch/ref operations or Git commits were performed.

## Result and bounded dependency closure

Single None/Remove submits official `clip.set` v1 with exactly `{values:{}, clear:['transition']}` through the existing durable session/outbox. Bulk None/Remove captures every selected clip before finishing all commands and enqueueing one atomic intent/request. Failed capture, unsupported fields, mixed preview operations, mismatched owners/bases or missing targets preserve the prior draft/outbox and issue a visible refusal; there is no partial preview/write or snapshot fallback on a supplied native capture path. Mixed selection placeholder remains inert.

The base lacked the scalar implementation. Reused the reviewed `clipScalarCapture.ts` (379 lines), `clipScalarGesture.ts` (64), `clip-scalar-preview.ts` (41), and `useClipScalarControl.ts` (25) byte-for-byte. Added only their session owner/prepare/submit closure, legacy-save fences, clear preview metadata/validation and inspector plumbing. This is **509 unchanged reviewed product lines plus 207 net integration lines = 716 net product lines**. Retained the complete reviewed scalar module, including its hold/asset validation, to preserve exact golden parity and avoid inventing a second capture engine. Hold/asset UI migration, trim, params, track-create, popup, renderer and other ordinary cohorts were not imported. `clipMovePrimitives.ts` remains identical to base: the unrelated old params own-key setter hardening was unnecessary for this closure.

Owner binding uses the raw parent row or explicit projector occurrence binding, checked against project, parent, raw clip, occurrence, shot/internal revisions and stable output identity. No display-ID ownership shortcut or new guards are invented. Original captured claims execute against current authored bytes without refreshing on ACK. Native clear records ABSENT and removes the own leaf from both raw parent mirrors. Exact null/absence/opaque/prototype-looking keys/order are covered. The reused preview is local leaf removal metadata inside the existing patch compiler; no server operation, wire schema, endpoint, compiler authority or client field was introduced.

The shared inspector's single clear callback also checks read-only state, as bulk already did. Installed and shared hosts pass the complete selection. Detached presentation callbacks remain compatible; this source staging does not declare production legacy writer retirement.

## Preservation and review repair

- The original TransitionPreservation describe block (21 cases), rawClip fixture and authored/published assertion helper bodies are byte-identical to this base. No original behavior test was rewritten, skipped, removed or marked expected-to-fail. Revision/opaque/reset/default/known-None semantics from the integrated safety source stay intact.
- Both original raw-removal fixture expectations remain ordinary positive native publication tests. `parent.clips` and `parent.config.clips` are compared exactly, including JSON order; no assertions were replaced by refusal expectations.
- Repaired the readonly review's concrete test defect: nativeEditor.project now replays recovered previews. The refused-batch recovery test additionally asserts **both displayed clip planes stay cleared after recovery**, while **both accepted raw mirrors stay unchanged**. Existing stored request/intent and no-retransmit rejection assertions remain.
- Existing `commitSession.test.ts` is byte-identical to base. Existing session hook bodies are unchanged; three reviewed scalar/bulk fence cases were appended intact. Scalar capture/gesture/session suites and the native golden are byte-identical to reviewed source.
- Added the five applicable old inspector cases with unchanged bodies in `ClipPanel.nativeNone.test.tsx`: None, Remove, visible failed removal, unsupported mixed fields atomically, SET/duration retaining their callback. Only shared test support was copied; old hold editing UI cases were not imported.
- The old **543** and readonly **209** counts were overlapping selections on a larger old cohort, not counts of source changes or an additive target. All applicable available neighboring files were run here. `commitSession.mixed.test.ts` depends on unported params/trim; old `ClipPanel.scalar.test.tsx` also includes unported hold authoring. They were not imported/disabled. The applicable None bodies were retained as above, and reviewed batch-clear → newer move suffix remains in TransitionPreservation.

Golden SHA256: `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06`, unchanged from the reviewed native Agent fixture. This is frozen native contract parity, not proof that the final deployed provider/client pair accepts the commands.

## Exact changed-path allowlist and growth

**26 paths: 17 product (+726/−10, net +716), 8 test/support (+1266/−15, net +1251), 1 unchanged copied golden fixture (+6317). Total +8309/−25, net +8284.** The large fixture is test data, outside authored product growth. No other tracked or untracked source path changed. No root/package/lock/generated/Runtime pins changed.

| Path | Added/deleted lines |
| --- | --- |
| `src/sdk/video/timeline/patch.ts` | +2/−0 |
| `src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts` | +3/−1 |
| `src/tools/video-editor/commands/clipScalarCapture.test.ts` | +184/−0 |
| `src/tools/video-editor/commands/clipScalarCapture.ts` | +379/−0 |
| `src/tools/video-editor/commands/clipScalarGesture.test.ts` | +73/−0 |
| `src/tools/video-editor/commands/clipScalarGesture.ts` | +64/−0 |
| `src/tools/video-editor/commands/commitSession.clipScalar.test.ts` | +468/−0 |
| `src/tools/video-editor/commands/commitSession.ts` | +102/−1 |
| `src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_scalar_fields.json` | +6317/−0 |
| `src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx` | +22/−3 |
| `src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.tsx` | +4/−1 |
| `src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx` | +198/−0 |
| `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx` | +4/−0 |
| `src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx` | +21/−3 |
| `src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx` | +5/−0 |
| `src/tools/video-editor/components/PropertiesPanel/PropertiesPanelBody.tsx` | +11/−0 |
| `src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx` | +222/−14 |
| `src/tools/video-editor/contexts/VideoEditorProvider.tsx` | +1/−0 |
| `src/tools/video-editor/hooks/useClipScalarControl.ts` | +25/−0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx` | +57/−0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts` | +12/−0 |
| `src/tools/video-editor/hooks/useTimelineState.ts` | +8/−1 |
| `src/tools/video-editor/hooks/useTimelineState.types.ts` | +2/−0 |
| `src/tools/video-editor/lib/clip-scalar-preview.test.ts` | +61/−0 |
| `src/tools/video-editor/lib/clip-scalar-preview.ts` | +41/−0 |
| `src/tools/video-editor/lib/timeline-patch.ts` | +23/−1 |

## Exact validation commands and results

All commands ran from the assigned worktree. Own `node_modules` symlink points to existing `/tmp/app-coherent-deps12/node_modules`; there was no install. The private runner only supplies `globalThis.__dirname = require('node:path').join(process.cwd(), 'config', 'testing');` for Vite's runner loader. `--configLoader=runner --no-cache` avoids temporary config bundles and shared Vite caches.

Core: **7 files / 203 passed**, exit 0, 26.57s; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/core.log`:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/lib/clip-scalar-preview.test.ts
```

Neighbors (including transition callbacks, outgoing serializer and patch atomicity): **15 files / 813 passed**, exit 0, 45.21s; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/neighbors.log`:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/SchemaForm/SchemaForm.test.tsx src/tools/video-editor/transitions/catalog.test.ts src/tools/video-editor/transitions/validation.test.ts src/tools/video-editor/lib/timeline-domain.transition.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts
```

Applicable old mounted inspector cases: **1 file / 5 passed**, exit 0, 8.78s; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/mounted-none.log`:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-native-none-source/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx
```

Final distinct coverage: **23 files / 1021 passed**, zero failed/skipped/todo. Core and mounted runs cover final affected source; the neighbor run also covers the final host wiring. No passing test was weakened.

Scoped lint: all exit 0, no warnings (`lint.log`, `lint-state.log`, `lint-mounted-none.log`):

```sh
node node_modules/eslint/bin/eslint.js src/sdk/video/timeline/patch.ts src/tools/video-editor/commands/clipScalarCapture.ts src/tools/video-editor/commands/clipScalarGesture.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts src/tools/video-editor/hooks/useClipScalarControl.ts src/tools/video-editor/lib/clip-scalar-preview.ts src/tools/video-editor/lib/clip-scalar-preview.test.ts src/tools/video-editor/lib/timeline-patch.ts --max-warnings 0
node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineState.ts --max-warnings 0
node node_modules/eslint/bin/eslint.js src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx --max-warnings 0
node scripts/quality/check-known-failures.mjs
git diff --check
```

Known-failure check: **3 original authorized group-drag markers / 0 forbidden**, exit 0. Diff check: pass. Pure source assertions passed for exact reviewed modules/golden, original test bodies and the 26-path boundary (`notes/source-audit.txt`, `notes/source-summary.json`). Metadata snapshots of **35,464 entries each** in private public12 dependencies and shared App dependencies remained identical over the neighbor/mounted checks, including cache directories and symlinks (`notes/dependency-summary.json`). No shared dependency, venv or runtime file was written; core also used runner/no-cache. Snapshot input was removed after comparison. No temporary/build output remains in the worktree.

## Remaining native and paired limits; next steps

**No blocker to this source task; activation remains HELD.** These are in-process App tests using the real session/outbox/provider boundary with a unit transport executing the reused native capture. They do not establish actual Agent registration/acceptance, Runtime transactionality, server inverse guards, browser reload, actual lost-ACK recovery after process restart, final-render parity or zero production legacy traffic.

Native UI coverage in this unit is single and atomic bulk transition None/Remove only. Transition SET, duration, parameter edits and reset keep their integrated callbacks. Other scalar/ordinary/popup consumers and legacy publication remain outside this task. Keep the original production writer retirement condition: real matching current-pair acceptance + reload + undo + exact retry/restart + zero legacy traffic for representative None/Remove journeys.

Orchestrator should review this bounded source delta separately from public12 root adoption, compose the independently owned normal official Runtime **0.2.9** pin and after-ACK delta, freeze the matching Agent/public12 + Runtime tuple, and run the central paired qualification lanes. The existing official primitive is sufficient; this unit adds no custom operation/client fields. No full/build/browser/tsc/socket/install was run or requested. Typecheck and actual server/browser behavior remain unverified, as required by this brief. No current-pair acceptance or legacy writer deletion is claimed. No KEEP is requested; recycle normally after harness capture.
