# AP2 M2 ordinary session patch — independent review

Date: 2026-10-20

## Verdict

- **Source helper: APPROVE.** The exact source base is `05b6b488d1834650c459c5c565f2530d9bea20e9`; the current-root helper source is `f76d61c5cfa222939a6cc77509e5f7c03019c611`. The helper stays bounded to merge-mode parent track labels and finite positive clip holds, uses the existing recorder/outbox types, and has no new store, DTO, API, pin, cohort, or dependency.
- **Concrete session patch: HOLD at the actual door.** The patch applies cleanly to the exact `05b6` base and the native session path is real, but the live `TimelineOps` dispatch bypasses the required retained legacy path for unsupported standalone producers.
- **Browser/row qualification: HOLD.** No browser, localhost, socket, Runtime HTTP, or full suite was run, per the brief.

## Patch identity and application

- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-concrete-session.patch`
- Patch SHA-256: `6bf54301a9f712b097384a6143ee99dfb5543878d7358c2fab46900fdf61a1e5`
- Exact base SHA: `05b6b488d1834650c459c5c565f2530d9bea20e9`
- Current helper-only root SHA: `f76d61c5cfa222939a6cc77509e5f7c03019c611`
- `git -C <private exact-05b6 archive> apply --check handoff-ap2-m2-ordinary-concrete-session.patch`: **passed**.
- The patch was applied only to `/tmp/ap2-m2-ordinary-review.CnlQ2S`; the assigned worktree and shared integration worktrees were not modified.

## What was verified

The private exact-base candidate passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts
```

Result: **7 files, 184 tests passed**.

```text
node_modules/.bin/eslint \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineState.ts --max-warnings 0
node_modules/.bin/tsc --noEmit --pretty false
```

Both commands passed. Existing compiler/source-map producer neighbors also passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts
```

Result: **2 files, 90 tests passed**. This confirms their isolated test doubles remain intact; it does not prove the live hook wiring below.

Fresh current-TypeScript native parity was generated from the private patch and piped directly to the read-only Agent archive:

```text
node --import tsx --input-type=module -e "...captureGenericPatch(...)..." |
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT_ORDINARY" \
  /home/user/work/venv-app2-native/bin/python -c \
  '...validate_command(...); execute(...); ...'
```

Result: Agent validation and execution passed for `clip.set`, `track.set`, ordinals `[0, 1]`, hold `1.23456789`, and label `""`. The private Python environment and source archive were read-only.

## Session-path audit

The actual current-root session wiring is concrete, not pseudocode:

- `commitSession.ts:326-375` captures against the current authored bundle and displayed head, records the original `localBasis`, stores `prepared` under `JSON.stringify(captured.capture.commands)`, requires the same command key and bundle identity at submit, requires the exact combined preview, then calls the existing `enqueue` once.
- `lastIntent ? { after: lastIntent } : { head: known.head }` preserves a dependent B suffix basis over A rather than refreshing B's guards. The existing outbox dispatch serializes the one `commands[]` payload and its persisted idempotency key; the new restart/lost-ack test observed two calls with equal body text and key.
- The all-member preflight in `genericPatchCapture.ts` rejects unsupported mixed batches before owner resolution; the focused test confirms the resolver is not called. No partial command list or post-capture snapshot fallback occurs for that mixed refusal.
- The native projection path is used for recovery and local projection, preserving unrelated display/data-lane state. Existing session undo is publication-based, so one generic batch is one outbox intent/history publication (source audit; no new generic-batch undo test was added under the brief's no-new-tests rule).
- `useTimelineCommandSession.ts` applies the same `legacyClean()` barrier to generic capture, finish, and submit.

## Finding — actual door HOLD

`useTimelineOps.ts:276-281` unconditionally calls `genericPatchPort.capture/finish/submit` whenever the port exists. `useTimelineState.ts:766-770` passes `save.commands.genericPatchPort` into the live hook once the command session is mounted. Therefore the retained legacy branch at `useTimelineOps.ts:283-315` is unreachable for live sessions, including valid unsupported standalone operations.

This is distinct from the required mixed-batch behavior: mixed supported/unsupported input correctly refuses before owners/preview/enqueue. The defect is that an all-unsupported positive patch also refuses instead of preserving the existing snapshot producer until its native migration. A direct affected producer is `compiler-canary.ts:440-441`, whose `project-data.write` source/source-map batch now reaches the bounded native port and refuses before the later proposal/draft path. The source helper itself remains approved; the live consumer needs a narrow dispatch distinction that retains unsupported positive/draft producers while keeping mixed native refusal atomic.

No product change was made in this review.

## Not run / limits

- No full suite, browser, localhost, live socket, Runtime HTTP, package installation, dependency/pin/generated-contract change, or shared worktree edit.
- No new tests, skipped tests, weakened assertions, or source edits.
- The exact native check proves Agent command validation/execution only; Runtime-door acceptance and App browser reachability remain unverified.
