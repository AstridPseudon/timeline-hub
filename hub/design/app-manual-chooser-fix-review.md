# App manual chooser fix review — APPROVE

Reviewed the exact fix SHA `bcd610db8e530454da7029e0479fe81e52bbd156` (`tl/app-m2-manual-chooser-unique-bindings`) against exact base SHA `c297c7a9071ebd222f9920b78866b776255ff2fb` (`tl/app-m2-runtime-manual-chooser-destinations`).

## Verdict

**APPROVE** the exact fix SHA for the duplicate-selection defect. The fix prefixes each chooser option's display/selection value with a local ordinal while retaining the existing frozen raw binding and ID lookup. `ShotSelector` remains name-valued for cmdk, so every option now has a unique selection value without parsing presentation text into authority.

The fix diff is limited to:

- `runtimeRecoveryDestinations.ts`: ordinal prefix only; raw occurrence, shot, revision, parent lane, child track, and media basis bindings remain unchanged.
- `RuntimeRecoveryChooser.test.tsx`: the two original keyboard regressions and suffix-safe display assertions.

`RuntimeRecoveryChooser.tsx` is byte-identical between the two reviewed SHAs. Exact diff check passed; no product files were changed in this review worktree.

## Re-review evidence

All commands ran against a disposable archive of the exact fix SHA, with the shared App `node_modules` symlinked read-only, a private cache directory, `--cache=false`, `--no-file-parallelism`, and `--maxWorkers=1`.

1. Original duplicate keyboard cases, isolated by name:

   ```sh
   vitest run --config /tmp/timeline-app-chooser-review.fOVWX8/config/testing/vitest.config.ts --configLoader bundle --no-file-parallelism --maxWorkers=1 --cache=false --reporter verbose --testNamePattern='keyboard selection of duplicate' /tmp/timeline-app-chooser-review.fOVWX8/src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx
   ```

   **2 passed, 30 skipped; exit 0.** The within-occurrence duplicate child label routed to `alternate-child-track`; the cross-occurrence duplicate name routed to occurrence `Scene · Main` and `alternate-child-track`.

2. Focused neighboring suite:

   ```sh
   vitest run --config /tmp/timeline-app-chooser-review.fOVWX8/config/testing/vitest.config.ts --configLoader bundle --no-file-parallelism --maxWorkers=1 --cache=false /tmp/timeline-app-chooser-review.fOVWX8/src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx /tmp/timeline-app-chooser-review.fOVWX8/src/features/tasks/components/TasksPane/RuntimeTaskRecovery.test.tsx /tmp/timeline-app-chooser-review.fOVWX8/src/features/tasks/components/TasksPane/TasksPane.test.tsx /tmp/timeline-app-chooser-review.fOVWX8/src/integrations/runtime/timelineCommit.test.ts
   ```

   **118 passed across 4 files; exit 0.** This includes pointer and keyboard selection, source/media pin preservation, stale head/draft retention, unmount/disposal cancellation, explicit-scope wiring, honest unavailable native ADD presentation, and Runtime authority neighbors. The combined run showed no callback flakiness, so no additional broad loop was warranted.

3. Prior review's eight private authority controls, rerun against the fix with only literal display-name assertions changed to ordinal-prefix-safe suffix matching in the disposable test copy:

   ```sh
   vitest run --config /tmp/timeline-app-chooser-review.fOVWX8/review-vitest.config.mjs --configLoader bundle --no-file-parallelism --maxWorkers=1 --cache=false /tmp/timeline-app-chooser-review.fOVWX8/authority-controls.test.tsx
   ```

   **8 passed; exit 0.** This covers duplicate raw occurrence refusal, duplicate child-track refusal, absent revision/publication refusal, raw control-like names rendered as text, duplicate child-track keyboard routing, cross-occurrence pointer and keyboard routing, stale-head draft retention with no placement traffic, and independent checks of all five original media-pin fields.

4. `git diff --check c297c7a9071ebd222f9920b78866b776255ff2fb..bcd610db8e530454da7029e0479fe81e52bbd156`: **exit 0**; exactly two files changed, as listed above.

The installed Vitest 4.1.5 rejects the brief's older `--minWorkers` flag, and its `--configLoader runner` path fails on this repository config's `__dirname` under the current runner. Those invocations failed before test collection; the supported bundle loader with one worker and `--cache=false` produced the results above. No full suite, build, browser, socket, TypeScript check, install, activation, legacy writer, default timeline, or native API work was run.

## Authority boundary

The exact Runtime authority read, immutable basis/media pin, stale-head checks, draft retention/disposal guards, and honest unavailable native ADD presentation remain intact. The callback is still only a local routing seam; this review does not qualify native command capture, commit acceptance, undo, matched App/Agent/Runtime semantics, or browser/manual acceptance.

## Next step

Integrate the exact fix SHA, then separately qualify the orchestrator-selected native ADD port and real commit/undo path. Keep the ordinal as presentation-only routing disambiguation; do not parse it or any raw displayed name into canonical ownership.
