# Review: duplicate concrete session patch

## Decisions

- **Proposed code: APPROVE.** The reviewed delta from `f34054c624f78c4f2f3b73551733f9151fc1b930` to `5bb0a9f6383d0598608263644b51af6c69fe325d` wires the already reviewed native `occurrence.duplicate` capture/gesture into the existing command session, outbox, editor-ops context, and canonical document-shot consumer. No unrelated API, pin, DTO, store, dependency, generated, or package change was found.
- **Ownership: HOLD.** This is not a private-copy-only result. The branch commit changes seven tracked App files, all under App-owned/shared paths (`commitSession`, `AstridTimelineEditor`, command-session/state hooks, and focused tests). Do not merge this branch directly or erase its work; route the recovered patch through the App owner.
- **Actual duplicate door/gate: HOLD.** App integration is frozen, and this review did not run browser, localhost, socket, live Runtime-door, or full suites. This is not merge authorization.

## Reviewed behavior

- Capture starts from the session's raw authored bundle and checks project/timeline/head identity against the displayed `TimelineData`; the helper snapshots the original bundle and records the native command basis. Finish replays that immutable basis and re-executes against the session bundle, retaining the original guards and refusing a changed generation.
- The canonical consumer reserves occurrence and shot IDs once, before capture. `occurrenceDuplicateGesture.ts` freezes the arguments/basis and verifies the returned command still has the same owner, IDs, scope, and occurrence ownership. The prepared command is accepted only by the same session generation and bundle identity.
- The duplicate has one outbox intent and no preview patch. The new session test asserts one persisted intent, the exact pending body/key, and an exact second request after a lost acknowledgement, dispose, remount, explicit recovery, and flush.
- Undo is still the existing guarded durable inverse path. The focused session suite covers the accepted-publication inverse and uncertain-commit refusal/recovery barriers; the native helper parity evidence also covers the duplicate record's guarded inverse. A duplicate-specific live-door undo was not run here and remains part of the held gate.
- The canonical consumer no longer imports/calls `duplicateIndependentShot`, `shotComposition.publish`, or `refetchShots`; its path submits the native command only. The focused editor assertion verifies that the legacy `duplicateShotGroup` and reload path are not called for canonical duplication. The non-canonical catalog duplication branch remains intact (`duplicateShotGroup` plus reload), keeping project-catalog duplication outside film history. Static inspection found no task creation call in the canonical path.

## Evidence

Patch artifact:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-duplicate-concrete-session.patch`

It is the exact binary-capable unified diff from base `f34054c624f78c4f2f3b73551733f9151fc1b930` to reviewed result `5bb0a9f6383d0598608263644b51af6c69fe325d` (389 lines, 22,767 bytes). `git apply --check` passed against a fresh private archive of the base.

Targeted test command:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts \
  src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts \
  src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

Result: **8 files passed, 186 tests passed**. `git diff --check f34054c62..HEAD` also passed. No full/browser/socket/live-door suite was run; the worker's earlier 162-test report is not browser evidence.

## Recommended next step

Have the App owner apply the flat patch to the current integration root through the ownership queue, then qualify the real mounted consumer and Runtime door for duplicate commit/reload, guarded undo, exact idempotent retry after restart, and direct rejection/spy evidence for all legacy graph/task traffic. Keep this branch and patch on HOLD until that gate and the integration freeze are lifted.
