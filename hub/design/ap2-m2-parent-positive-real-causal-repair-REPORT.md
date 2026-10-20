# Parent positive-drop causal repair

**Partial repair; original browser refusal remains blocked, not qualified.**
The exact central32057 trace and error-context were deleted by runner EXIT
cleanup. No browser/socket/central/full rerun was authorized or performed.
The candidate fixes a separately reproduced placement error and makes the
next committed-source gate identify the missing first failure.

## Evidence and limits

- Base: `9de0e009f5c50d45de402727b8eb889ee4cb7199`, tree
  `9afa27b7ba22074dce31d670970007a9eecd6920`.
- Read central result directory
  `tests/ap2-m2-parent-positive-drop-first-post-fix-ap2-m2-parent-drop-real-central-qualification-1020211823-32057/`
  and `design/ap2-m2-parent-exact-candidate-central-gate-REPORT.md`.
  Its snapshot tree, successful hosted build, and logged App snapshot
  `2aff048ddb82277ad738618a493e28a2f83de5ba` establish the exact candidate
  source. There are no retained downloaded chunk bytes for independent
  served-asset comparison.
- `/tmp/timeline-normal014-app.mdDJlZ/browser-output/.../trace.zip` and its
  error-context no longer exist. The only retained manual-drop trace found,
  `/tmp/timeline-normal014-app.91b9YO/browser-output/three-products-M2-real-mou-0d47b--undo-preserves-opaque-data/trace.zip`,
  is the older malformed-digest negative run (422); it is **not** evidence
  of corrected32057's positive refusal. Cancelled23889 was not used.
- **Correction to the prior report's premise:** `faultFirstCommit` increments
  `attempts` before `route.fetch()`, but appends to `posts` only after fetching
  and JSON-decoding the response (`three-products.spec.ts:712–719`). Therefore
  the retained `posts.length === 0` failure proves zero completed observations,
  not zero native POST attempts. Neither a valid-input 422 nor its absence is
  established by that counter alone.
- The existing positive assertion proves the original five-field verified GET
  was requested. In this producer, that call follows `port.capture`, so the
  native port, initial legacy-clean guard and displayed-head check were reached.
  It does **not** prove GET success, `finish`, or `submit`. The old test awaited
  only the ordinary selection response. The exact first positive UI/console/
  capture error, original epoch across that await, and negative draft contents
  cannot be recovered from the retained log.
- Ordinary standalone prerequisite: this test explicitly calls
  `enableTimelineAuthoring(ASTRID_PYTHON)` before opening; the harness restarts
  Runtime with `--authoring-profile astrid`, then waits for a durable owner.
  Missing profile is not supported as the cause. No protected draft was
  cleared, replaced, or silently recovered. No shared Provider/session/core
  patch is justified by the available evidence; those sources were not edited.

## Own producer and fixture repair

1. A clean real command-session/service test reaches native capture, outbox and
   transport. Adding the actual transient uploading row shifts the requested
   20s placement: the one-second focused case emits 19s, and an offline replay
   using the retained older trace's unchanged compound fixture and 12s media
   emits 25s. This is caused by both placement planners treating the temporary
   five-second placeholder as an authored collision. It is a proven additional
   bug, **not proof of the original zero-response cause**.
2. `useTimelineCommandsService.ts` excludes `uploading-` actions only from a
   detached placement-planning view, matching existing `rowsToConfig`
   semantics. Capture still uses the original displayed data; its row retains
   `from`, `to`, and `hold`. Actual skeleton/data objects remain untouched.
3. `useAssetManagement.ts` preserves the boolean refusal and no-fallback behavior
   while showing the existing service error through the normal error toast.
   Previously `.then(result => result.ok)` swallowed the only capture message.
4. The mounted journey now awaits verified HTTP 200 and exact selected identity,
   then separately checks POST attempts (including alerts, session notice and
   read-only draft diagnostics on failure) and completed responses. Existing
   negative, retry/restart, undo, opaque, position and legacy assertions remain.

No API/schema/pin/dependency change, shared install mutation, or guard weakening.

## Exact validation

One private source-copy path, `.causal-overlay`, with EXIT cleanup. Shared
node_modules was only symlinked/read; Vitest used runner loading and no cache.
The reproducible driver is:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-positive-real-causal-repair/validate.sh
```

Before product repair, new/extended behavior tests on base source:

```sh
node --require ./vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommandsService.parentMedia.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx
```

**Expected exit 1: 6 passed / 2 failed** (wrong position; missing refusal toast).
Original refusal expectation and skeleton preservation were retained.

After repair, same private copy:

```sh
node --require ./vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommandsService.parentMedia.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/mediaImport.test.ts
node node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/useTimelineCommandsService.parentMedia.test.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx tests/e2e/local/three-products.spec.ts
node node_modules/typescript/bin/tsc --noEmit --pretty false --incremental false
git diff --check
```

**10 files / 274 tests passed; ESLint, TypeScript and diff check exit 0.**
Logs: worker `regression-before.log`, `regression-after.log`, `eslint.log`,
`typecheck.log`. Overlay removed. No browser collection/run or central request.

## Required next step (orchestrator, after harness commit)

Recover corrected32057's trace if another retained copy exists; otherwise the
next authorized committed-source gate must supply its first error. Do not label
this the repaired zero-POST cause. Retain that gate's browser artifacts before
normal014 EXIT cleanup, or its failed assertion now exposes the verified
response/attempt/UI/session/draft stage in the central log.

The exact existing named-suite command, **not executed here**, is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-positive-real-causal-repair ap2-m2-parent-drop-real-central-qualification) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

If the negative leaves a valid protected draft, resolve it through normal user
controls or run the positive in an independent normal fixture; do not clear its
storage. If a shared-session defect is then proven, request its exact minimal
patch from the App owner. Native acceptance/recovery tail remains unverified.
