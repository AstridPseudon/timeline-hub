# Staged single-parent split on current029/public12

Worktree: `/home/user/work/wt/app-m2-parent-split029-source-slice`. Base: `c866da88e6acb92e6f7194324e0a29bfacab3b4b`.

**Complete as a source staging task; actual UI writer retirement and real-pair qualification remain open.** No full suite, build, browser, project typecheck, install, socket, push or git mutation was run. No KEEP or queued test.

- Ported the reviewed `b8ff1f59b` / `92cec8da6` parent-only native recorder, exact fixture and parity cases. `clipSplitCapture.ts` matches the reviewed 92 source with only its extra trailing blank line removed. Ported only the single-parent session/gesture delta from `2f9458297` / `e4d7ce82e`, using raw parent ownership as reviewed in the `4f79aea85` ingress map. No batch, ordinary/media/placement bundle was imported.
- Caller supplies one explicit parent clip, original cut seconds and one already-reserved right ID before any preview. Original complete claims and created IDs survive persistence, dependent suffixes, recovery and exact retry. Source windows, speed, literal `for`, null/absent values, rational FPS, half-open geometry, registry and opaque values follow the native recipe.
- Reused the one existing prepared map, durable outbox, commit pump, inverse request and `MoveRecording.compile()`. The internal `TimelinePatch` carries complete native left/right rows through existing `assembleTimelineData`; it adds no timing/compiler implementation. The hook installs the candidate once using `commitData(save:false, skipHistory:true)` and uses the same adapter on recovery. Existing label/move compilation stays in place.
- Exposed only the needed `clipSplit` editor operation and `clipSplitPort` hook surface. The mounted ingress test exercises the gesture adapter through the real command-session hook and local commit pipeline. **No existing context-menu, keyboard, inspector or SDK facade split producer is switched.** Existing old split writers remain byte unchanged, as required for staging; no global zero-legacy claim.
- Raw parent rows determine ownership; arbitrary authored `app.canonical` remains opaque. No suffix rewriting, source-asset guessing, new DTO/public operation/schema/guard protocol, or fallback writer. Group, occurrence, multi, new-track and compound contracts remain separate. Existing grouped/multi positives and all pre-existing tests are unchanged; no new failure markers.

The reviewed imported tests needed two already-reviewed `4f79aea85` fixture corrections: recompute literal `for` when changing source-window/speed, and clone a frozen command before testing forgery. Their success/refusal expectations are unchanged. Initial failures and the corrected runs are retained in worker logs. No settled plan decision was contradicted.

## Exact verification

Commands ran in the assigned worktree. The own, ignored `node_modules` symlink points to the pre-existing `/tmp/app-coherent-deps12/node_modules`; shared dependencies were never written. Node `v22.22.0`, Vitest `4.1.5`, Composition `0.0.12`, Remotion `4.0.509`. Vite runner bootstrap is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/vitest-runner.cjs` and only sets `globalThis.__dirname` to the existing config directory. Every Vitest run used one worker, runner config loading and disabled caches.

Native Agent used read-only `/home/user/work/agent`, head `c456b3281497653cecf44f61acd6fa30565d83c8`, with the existing dependencies-only venv. Bytecode writes were disabled. The portable fixture is unchanged from the reviewed source. Exact native command, complete record and authored after document match; native inverse restores the original bundle and redo restores the split:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_split_parity.py
```

PASS, exit 0: `1/1 native split command, complete record, authored after, inverse and redo verified`. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/native-parity.log`.

Targeted split plus neighbors:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/components/TimelineEditor/ClipAction.test.tsx
```

PASS, exit 0: **18 files / 564 tests**, 38.84s. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/targeted-tests.log`. Covers the new native capture/gesture/session/mounted boundary; existing move, track label, outbox, opaque/remap/source guards, mounted projection, generic operations and grouped/multi split behavior.

After a type-only annotation cleanup in the split preview and its test, reran all affected split files:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
```

PASS, exit 0: **4 files / 76 tests**, 6.41s. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/final-core-tests.log`. This overlaps the 564 distinct passing tests; it is not an additional 76 distinct cases.

Coverage includes exact created IDs/claims; dependent unacknowledged split suffix and reload; identical pending bytes/key; refusal retaining draft; abandoning an unsubmitted capture/prepared preview; duplicate finish and duplicate submit fencing; one accepted-publication undo request; opaque parent identity fields; wrong head/group/occurrence/collision refusal; altered preview refusal; a single mounted local install with no snapshot scheduling; and capture/finish/submit fencing behind earlier snapshot saves.

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipSplitCapture.ts src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts
git diff --check
```

PASS, exit 0, no diagnostics. Lint log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/final-lint.log`.

## Dependency closure and growth

No package or lock change, install, copied dependency, public export, generated client or Runtime contract change. Product additions depend only on current Runtime type exports, current `clipMovePrimitives` (`MoveRecording` / `AuthoredState` / JSON helpers), existing authoring bundle conversion, existing TimelineData assembly and the existing durable session/outbox. Local preview resolves the two native rows with the existing resolved asset entry; it does not register/select/guess media. The Python parity verifier additionally imports native capture/execute/bundle conversion and the main conformance inverse helper; no App inverse writer was added.

Six product files: **+520 / -4 = +516 lines**. Two new modules contribute 446 lines; four existing files contribute net 70. Five test/verifier files: +892 lines. One unchanged reviewed golden: +2524 lines / 57,241 bytes. Total patch growth: +3936 / -4 = +3932 lines. Exact per-file census: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/growth.json`.

`git diff --quiet` against the assigned base confirms byte unchanged root manifests/locks/config, all `src/sdk`, all `src/integrations/runtime` (official 0.2.9 / 14-op contract), settings, render/runtime closure, original split hooks/facade, generic patch compiler, pre-existing after-ACK/M2 tests and source/remap helpers. Needed host ports are the only timeline-state edits. Original tests were not changed. Package/artifact/client SHA-256 values: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/dependency-hashes.txt`.

## Remaining qualification and handoff

No blocker for this staging deliverable. Real Runtime/Agent atomic acceptance, publication-history guarding, process restart, actual UI event routing, no-legacy HTTP traffic and Player/export source-clock/pixel/audio parity were **not exercised**. Native inverse semantics are proved by the native verifier; the App undo/session transport tests use deterministic in-process transport doubles, not a real server. The mounted test is a React command-session adapter ingress, not a browser/context-menu journey. No TypeScript compiler was run per the brief.

Next: orchestrator reviews this bounded source delta, then assigns the real current029/public12 single-parent UI/Runtime journey before switching a producer or retiring its old writer. Keep group/occurrence/nonmedia/multi/new-track/compound positive behavior on its existing path until its own complete native contract is qualified. Do not claim M2, Gate 5/6 closure or zero legacy from this task.
