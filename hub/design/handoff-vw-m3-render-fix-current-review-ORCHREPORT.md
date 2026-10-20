# Current App render download qualification

Qualified the bounded seven-file unit on current-at-start App integration **382d54079741fc0318d5f0d702b0e4df36d5baee**, tree **a803e0f4184eaa0ced270db8e7a045dfae007088**, preserving D03 and all later changes present in that snapshot. Read PLAN first, predecessor final report/ORCHREPORT/manager REVIEW, and verified predecessor final exit 0 and committed source **f536b4267d6d73feb674120954b7e21648b6d04d**. No settled decision challenged.

Candidate branch: `tl/vw-m3-render-fix-current-review`. Qualified candidate source tree: **d38ff675e65b2c5101b5cf07c4d770c441d126b0** (computed from Git tree encoding and worktree file bytes, with the algorithm first reproducing the base tree). The candidate commit SHA cannot exist until the harness commits after worker exit; retrieve it from that branch then and verify this tree. No commit/ref/index mutation was performed.

Exact seven-file diff from the recorded current base: `current-candidate.patch`, SHA-256 **63c9eaceef8cbc7ce3594dcdbadb8b78043466e7daa05b811aae97e66651c2be**. The exact original seven-file transplant is `original-seven-file.patch`; review-only additions relative to the completed predecessor's seven paths are `lifecycle-review.patch`. `source-snapshot.json` records file hashes and source identities. Nothing from the old branch outside these seven paths was adopted.

## Findings and changes

The predecessor patch applied exactly with no conflicts: all seven original path blobs were identical between its base c8566f12d and current-at-start integration. Its original 86 direct tests passed on this current source before review edits.

Reviewed task/project binding, exact output identity, the existing projectObjects.read implementation, its authenticated generated-client object/location reads, size and SHA-256 verification, local Blob fallback, pending-click deduplication, error retry, retained revision/result, and object URL disposal. The predecessor's authorized binary path and product catalog default remain intact. Download Blob URLs use the existing utility's deferred revocation; no output Blob URL is allocated on failed verification. The project's existing binary-read tests are included in the five-file run. This is source/unit qualification, not a new physical confirmation of the earlier native-navigation Origin diagnosis.

Three concrete lifecycle defects required changes, confined to the render hook/control and their direct tests:

- A verified pending binary read could still trigger a download after unmount or project/timeline/provider replacement. Scope cleanup now invalidates that read and polling, clears the obsolete result/revision and active render UI, and releases the old operation identity. Four new regressions failed before this fix.
- A pending admission could resume after scope disposal, allocate a fresh polling generation and publish the old task. A separate scope generation now fences asynchronous admission/save/import continuations and routing. Four additional regressions failed before this fix. An already submitted server task is not cancelled or rewritten; its obsolete UI continuation is ignored.
- An old download's rejection/finally could set an error or clear the pending state for a newer result. The control now resets per-result download state and ignores settled obsolete attempts. Its new regression failed before this fix and also proves the new result can download while the old attempt is pending.

No prior passing assertion was removed, changed to expect missing behavior, skipped, or marked expected-to-fail. A line-multiset check confirms all predecessor `expect(...)` lines remain. Existing original behavior tests, including local/exporter Blob downloads and retry after read failure, pass. The only modifications to predecessor test setup support changing runtime scope and deferring render start.

## Exact validation commands and results

All commands ran in `/home/user/work/wt/vw-m3-render-fix-current-review`. In the commands below:

```sh
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
```

Absolute manager QUIET was absent before each CPU command; no pause/ACK was needed. All Vitest commands used local mocks/jsdom; no live service, browser, render, install, socket suite, full suite, or central request was run.

Original final direct replay, exact transplant before lifecycle changes:

```sh
"$NODE" node_modules/vitest/vitest.mjs run src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx --maxWorkers=1
```

PASS exit0: **2 files / 86 tests**, 3.82s (`transplant-direct-86.log`).

Necessary failing regression demonstrations:

```sh
"$NODE" node_modules/vitest/vitest.mjs run src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx --maxWorkers=1 --testNamePattern='pending read after|older download failure'
"$NODE" node_modules/vitest/vitest.mjs run src/tools/video-editor/hooks/useRenderState.test.tsx --maxWorkers=1 --testNamePattern='pending admission after'
```

Expected development failures: first **5 failed / 86 filtered**, exit1 (`lifecycle-before-fix.log`); second **4 failed / 82 filtered**, exit1 (`admission-before-fix.log`). Filtering only selected new regressions for red-phase verification; final commands below ran all original tests unchanged.

Original five-file target set on final source:

```sh
"$NODE" node_modules/vitest/vitest.mjs run src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/browser/hooks.test.tsx src/integrations/runtime/dataProvider.test.ts --maxWorkers=1
```

PASS exit0: **5 files / 231 tests**, 13.24s (`targeted-tests.log`). This retains the original 221 targets, the predecessor's final extra stale-read test, and all 9 new lifecycle regressions.

Final direct replay:

```sh
"$NODE" node_modules/vitest/vitest.mjs run src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx --maxWorkers=1
```

PASS exit0: **2 files / 95 tests**, 3.32s (`final-direct-tests.log`); all original 86 plus 9 new regressions.

Scoped ESLint, baseline and final:

```sh
"$NODE" node_modules/eslint/bin/eslint.js src/tools/video-editor/components/TimelineRenderControls.test.tsx src/tools/video-editor/components/TimelineRenderControls.tsx src/tools/video-editor/hooks/timelineStore.ts src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/hooks/useRenderState.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts --max-warnings 0
```

PASS exit0 on both: **zero diagnostics** (`baseline-lint.log`, `lint.log`). Baseline checks ran after temporarily reversing the exact original transplant in this assigned worktree; a finally block restored it before any review edits. No other worktree was modified.

TypeScript, baseline and final:

```sh
"$NODE" node_modules/typescript/bin/tsc --project tsconfig.app.json --noEmit --incremental false
```

Both exit2, with **byte-identical diagnostics**, no changed-file diagnostic (`baseline-typecheck.log`, `typecheck.log`):

- `src/integrations/runtime/RuntimeConnectionProvider.tsx(90,53)` TS7053: string cannot index `Readonly<Record<RuntimeRefusalCode, "restart" | "down">>`.
- `src/tools/video-editor/components/AgentChat/AgentChatNewChatButton.tsx(80,23)` TS2550: `replaceAll` unavailable under the configured ES2020 library.

```sh
git diff --check
git status --short
```

PASS exit0; exactly the seven assigned files changed, no build output/temp/report in the repo. All report/patch/log artifacts are in this worker's ORCH directory.

## Merge readiness and limits

**Unit-qualified, ready for manager review and the narrow integration merge.** No provider/client/auth/source/compiler/package-pin changes; no broad harness adoption. D03 and shared opaque remap changes remain byte-untouched.

During this review integration advanced to **5912bfc3284da03112ef6c235447cfbeffb678bd**, tree **1e21df7d1ebb18cda1c08d08f1e761337a581a3d**, by deleting the unrelated unused writer in `useTimeline.ts` and its tests (131 lines). A read-only diff proves none of the seven candidate paths changed between our base and that newer head. The saved seven-file patch therefore applies to those latest path blobs unchanged; merge the bounded unit so those newer deletions are retained. Tests here qualify the recorded **382d54079** base plus this patch; the combined latest merge tree has not been executed here. If integration changes any candidate path again, reconcile/recheck that overlap rather than replacing a whole branch.

No blocker for this bounded task. Candidate commit SHA remains a harness output after exit. Next: manager reviews the lifecycle delta, harness commits, then integration queue takes the small unit. The separate download-blob-proof/MP4 worker must use the final current-source candidate and freshly approved peer tuple, retain all original artifact/provenance/auth/negative/parity assertions, and perform its authorized physical four-case run. No actual MP4 download/decode, pixel/audio parity, Gate 6 closure, browser or full-suite pass is claimed here.
