# App2 M2 live producer ownership safety review

## Verdict

**HOLD — do not approve candidate `bb71ff7414555a730169ebac14a36cc0194f104c`** (parent/base `692765846fef511047445fecef3e55ec8bb6a5bf`). The focused negatives are directionally correct, but the candidate does not prove, and in the active local route does not preserve, ownership metadata for newly created producer clips.

## What was checked

- Read the settled PLAN, App2 status/inbox, worker 0200 brief/report, and the old canary templates at `692765846^:src/tools/video-editor/lib/compiler-canary.test.ts` (the foreign-owned/user-authored remove cases around 681/712, foreign update around 800, and non-owned recompilation around 1337).
- Reviewed the exact candidate diff. It changes only the two producer implementations, their focused tests, and the two approved stale-canary references. No new DTO, store, writer, public shape, or legacy writer was added.
- Confirmed the candidate’s RED/GREEN report: RED had two expected failures (transcript non-owned deterministic-ID update and Scene Phase foreign/user alignment); GREEN was 8 files / 492 tests. Targeted ESLint and `git diff --check` passed. No browser, socket, localhost, or full suite was run.
- Confirmed Scene Phase positive fixtures were changed to explicitly owned clips and that the new alignment guard emits no operations for foreign/user clips. The transcript positives still cover owned stale removal; the new negative covers foreign/user stale removal and deterministic-ID collision.

## Precise gap

The new guards require canonical reader ownership (`managed === true` and `managedBy === extensionId`):

- transcript: candidate `extension.ts:430` and `:465`;
- Scene Phase: candidate `extension.ts:702-705` and `:837-855`.

However, fresh transcript output is added at candidate `extension.ts:431-455`: `clip.add` has no ownership metadata, and `clip.update` writes `app: { __generated__: generatedMeta }` but no `app.managedBy`. The reader derives clip ownership from `app.managedBy`, an extension-namespaced app key, or `source_uuid` (`src/tools/video-editor/lib/timeline-reader.ts:129-153`); generated metadata is extracted separately (`:651-654`) and is not itself ownership.

The Scene Phase candidate adds `app.managedBy` to `clip.add` (`:561-568`, `:640-647`), but the active route is not proven to preserve it. `useTimelineOps` first routes every classification other than `unsupported` to the generic capture port (`src/tools/video-editor/hooks/useTimelineOps.ts:267-275`). These producer patches contain non-scalar `clip.update` members, so they classify as mixed and `captureGenericPatch` refuses the unsupported member (`src/tools/video-editor/commands/genericPatchCapture.ts:517-535`). If the generic port is absent and the fallback compiler is used, `compileTimelinePatch` creates a clip with only id/at/track/clipType and drops the add payload’s `app` (`src/tools/video-editor/lib/timeline-patch.ts:1121-1143`); the following Scene `clip.update` has no app payload. Either way, this candidate’s direct patch fixtures can be owned while the normal accepted/reloaded path is unproven (and the fallback path can remain unmanaged).

This means a newly generated transcript clip can be skipped on the next regenerate, and a newly generated Scene clip can be skipped on the next alignment; the active generic path may instead refuse the mixed producer patch before acceptance. The new tests construct already-owned snapshots; none exercises create -> active apply/accept -> reload/read -> second producer operation. This is a normal-path correctness gap alongside the requested data-loss negatives, not a reason to weaken the new guards.

## Required repair and route proof before approval

Carry the existing ownership metadata through a compiler-preserved mutation for each fresh producer output (for transcript, alongside `__generated__`; for Scene, do not rely on `clip.add` metadata alone), then add a regression covering accepted/reloaded ownership and the next owned update. No new writer, DTO, store, or public shape is needed.

The actual route gate still needed is:

1. Through the mounted `/tools/video-editor` route and the active transcript-lane and Scene Phase producers, create fresh owned outputs and reload/read the raw accepted timeline. Assert each fresh output has `managed === true` and the active `managedBy` value, then run a second regenerate/alignment and assert the owned output receives the intended update.
2. In the same live timeline, include one foreign-owned and one user-authored clip in each relevant lane. Capture the normal command/session submission and accepted revision; assert no submitted operation targets either protected clip.
3. Reload the accepted raw timeline and deep-compare every authored field of both protected clips (identity, track, timing, type, payload/app/generated metadata, and order). Repeat through the normal retry/reload path and verify there is no partial deletion or update. Do not substitute a direct builder call or test-only provider.

This browser/Runtime route proof was not run by this review worker, as required by the task’s no-browser/socket/full-suite boundary.

## Tests reported by worker 0200

Exact targeted command (reported GREEN, 492 passed):

```text
TMPDIR="$PWD/.tmp-test" node --require /tmp/ap2-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts
```

Targeted ESLint (reported passed):

```text
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 src/tools/video-editor/dev/transcript-lane/extension.ts src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx eslint.strict-debt.js
```

Independent static checks: candidate `git diff --check` passed; candidate commit identity and six changed paths matched the report. No tests were run by this review worker because the candidate worktree was finalized/removed before the review, and the task forbids broad route/browser suites.

## Decision

The RED/GREEN negatives correctly identify the intended protected targets, and the owned positive assertions are retained. The exact candidate SHA is nevertheless **not approved** until fresh producer ownership survives the active accepted/reload route and the required live protected-clip route proof passes.
