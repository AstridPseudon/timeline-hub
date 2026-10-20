# Manual native ADD submit boundary fix

Fixed the independent review's pre-enqueue HOLD on App base `ace8a84e075c5967605d0c27d61f19df5afef454`. Ready for independent re-review; source-only, not production qualification.

## Exact product delta and decision

Two product paths, **+5/-2 lines, net +3**:

- `runtimeRecoveryPlacement.ts`: set the existing reservation's `submitted` flag only through the session's `onEnqueued` callback, replacing the unconditional pre-handoff assignment.
- `commitSession.ts`: add that required local callback to the existing manual ADD input and invoke it synchronously immediately after successful `enqueue`, before persistence/pump awaits.

The boundary is transfer to the existing owner's pending append, not attempted capture or an ACK. Cancellation, missing/busy owner, stale head/bundle and atomic native capture refusal occur before the callback, so a corrected choice can retry; an unchanged choice reuses its reserved child ID. Once enqueue succeeds the owner retains the original capture, including when append storage fails before any durable intent exists. Only owner Retry continues it. No catch-reset, new queue/journal/wire, native contract change, production binding, optimistic preview or Placed notification.

Durability is not overstated: an append failure leaves the existing in-memory pending append, not a crash-safe persisted intent. No wire body/key exists until normal outbox dispatch. After dispatch/ACK-storage or network uncertainty the original durable request body/key/IDs remain unchanged. This preserves the existing storage-failure semantics rather than introducing another journal.

The only test helper change exposes its existing fake IndexedDB factory. Both required-success reviewer tests were copied verbatim into the normal adapter suite; original tests/expectations remain intact. Two additional cases cover append failure and ACK-storage failure, unchanged and corrected chooser attempts after transfer, retained capture, and owner Retry. **Test delta +69/-2, net +67; total three paths +74/-4, net +70.** Native recipes, fixtures, owner/head/pin checks, all chooser source/positives, outbox and hook source are unchanged. The review's frozen S2/905 complete native execution proof is preserved; no new native parity claim is made.

## Exact commands and results

Working directory: `/home/user/work/wt/app-m2-manual-native-add-submit-boundary-fix`.

```sh
WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-submit-boundary-fix
VITEST=/tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs
node "$VITEST" run --config "$WORKER/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.test.ts
```

Before product edits, after adding the unchanged required-success tests: **30 passed / 2 failed; exit 1; 1.90s** (`required-success-before.log`). Both fail with the exact reviewed already-submitted latch error despite empty intents.

```sh
node "$VITEST" run --config "$WORKER/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.test.ts \
  src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx \
  src/tools/video-editor/commands/occurrenceMediaCapture.test.ts \
  src/tools/video-editor/commands/occurrenceMediaPrimitives.test.ts \
  src/tools/video-editor/commands/occurrenceMediaOwnKeysCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
```

After the final source edits: **8 files / 365 passed; exit 0; 23.46s** (`targeted.log`). Includes the permanent two unchanged regressions, both new storage cases, native goldens, every original chooser positive, session/outbox and close/switch controls. Transport is mocked; no socket/browser/live Runtime.

```sh
node "$VITEST" run --config "$WORKER/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  "$WORKER/adapter-controls.test.ts" "$WORKER/authority-controls.test.tsx"
```

Reviewer control files are byte-identical copies. **41 passed / 1 failed; exit 1; 8.24s** (`controls.log`). All **34 adapter controls pass**, including both formerly failing required-success cases, closed owner and actual busy owner. Authority controls were 7/8: the control-like raw-name case could not find its popup row; the DOM had a closed combobox. No adapter/session path is exercised by that authority case.

```sh
node "$VITEST" run --config "$WORKER/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  "$WORKER/authority-controls.test.tsx"
```

Immediate isolated diagnostic rerun, unchanged source/config/tests: **8/8 passed; exit 0; 4.39s** (`authority-isolated.log`). The first combined failure is retained, not hidden or represented as a clean combined run. No further broad/repeat runs.

```sh
node /tmp/app-coherent-deps12/node_modules/eslint/bin/eslint.js \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.ts \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.test.ts \
  src/tools/video-editor/commands/commitSession.ts --max-warnings 0
git diff --check
```

Both **exit 0**, lint has zero warnings (`lint.log`). Python byte-comparison also confirms both scratch control files exactly equal the original reviewer files and the permanent two tests contain the verbatim original reviewer block.

Environment: this worktree's own ignored dependency symlink and the worker scratch dependency link point to `/tmp/app-coherent-deps12/node_modules`. Runner, config and test imports use that same tree (Vitest 4.1.5). Config is copied from the review config with this worktree's root/aliases/setup, private worker cacheDir, private control include and private12 runner. `--configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism` throughout. No shared dependency/runtime/venv/cache writes. No full/build/tsc/browser/socket/install or git mutation. No worktree build/temp output; private controls/config/logs retained for re-review.

## Limits, blockers and next steps

No blocker to the bounded fix. An append failure cannot survive restart until storage recovers; the existing owner retains the pending capture and exposes Retry. This patch does not add durability machinery.

Independent re-review should verify the exact enqueue callback and the two unchanged success regressions, plus original uncertain Retry/storage cases. The original review's generated-client/pin adoption, authenticated production owner binding, real Runtime acceptance, raw reload, inverse/redo, restart/retry, mixed edits and zero-legacy qualification remain OPEN. No production connection or native contract change was attempted. `KEEP` requests retention of this worktree for re-review; `DONE` marks this bounded worker task complete.
