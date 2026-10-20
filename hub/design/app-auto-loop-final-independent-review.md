# App automatic-placement requester loop — final independent source review

## Identity and verdict

- Worktree: `/home/user/work/wt/app-m2-auto-loop-final-independent-review`
- HEAD: `c34cf6ae40927f5e2b8845d723da75a5496060b4`
- Tree: `9e8e48c32808d052f2ee79e7fbac65029993af9c`
- Worktree status: clean; no product files were changed by this review.
- Verdict: **APPROVE — source-level production loop installed; automatic placement remains unqualified end to end.**

The former source blocker is closed. The production session receives the bound host from `useTimelineCommandSession.ts:115-117`, and the claimed session constructs the requester from the bound operation at `commitSession.ts:71-100`. This is a real installed path, not a factory-only source claim.

## Source findings

### Installed completion path

- `VideoEditorProvider.tsx:912-925` creates and publishes one operation-bound host, installs the existing task-event poller/cursor barrier, and exposes cache updates as wakeups.
- `commitSession.ts:99-100` creates `createSessionPlacementRequester` from the session's same `RuntimeOperation` and existing outbox.
- `sessionPlacement.ts:9-29` installs the requester capture callback. The callback invokes the existing native `readNativePlacementCapture` at `:15`, then limits the production result to one occurrence image command at `:16-18`.
- `commitSession.ts:160-180` calls `requester.resume(box)` from the normal session pump before ordinary commit dispatch. `:182-227` dispatches the captured intent through the same outbox and pump; no parallel commit coordinator exists.

### Completion/reconnect wakeups

- Admission reservation invokes the session callback only after the durable reservation transaction and current-session fence: `editorImagePlacement.ts:119-127`; the session callback reads the claim and wakes `resumePlacements` at `commitSession.ts:473-484`.
- Task completion wakes that same pump through the installed query-cache subscription: `VideoEditorProvider.tsx:920-924`, `useRuntimeTaskEvents.ts:17-23`, and `commitSession.ts:485`.
- Canonical reconnect/observe wakes it even when the head is unchanged: `commitSession.ts:539-543`.
- Explicit owner recovery claims the saved outbox and runs the same pump: `useTimelineCommandSession.ts:232`, `commitSession.ts:495-500`.
- The task-event cache is only a wakeup; authoritative reads use the bound operation in `placementRequester.ts:161-194`.

### Required invariants

- Same outbox/pump: `commitSession.ts:99-100,175-192`; `deferCommit: true` is set by `sessionPlacement.ts:12`, so capture links an intent and the normal session pump owns commit.
- Original approval, occurrence owner, lane, anchor, fallback, basis, reserved IDs, and exact task request bytes/key are persisted and revalidated in `editorImagePlacement.ts:68-87,101-124` and `commitOutbox.ts:347-381`.
- Operation lifetime is pinned to the session: `commitSession.ts:71-100,558-576`; retirement occurs before claim release, and operation callbacks fence both before and after network work at `:72-75,85-97`.
- Completion pin precedes capture/commit: `commitOutbox.ts:393-433` stores `mediaPin` before the native callback and only then appends the placement intent.
- Exact replay precedes any stale re-read: `placementRequester.ts:211-247` reuses the saved task locator/request and saved continuation; `commitOutbox.ts:443-499` retains the exact pending commit request/key for retry.
- Cancellation/refusal/retirement fences are present in `placementRequester.ts:207-277`, `commitOutbox.ts:409-425`, and `commitSession.ts:558-576`. Failed, cancelled, and cancel-requested tasks become visible conflicts without native capture or commit.
- Accepted completion uses the normal Runtime receipt path: `commitSession.ts:194-215` records the accepted closure, projects it after the receipt, and updates the existing publication Undo stack. `commitSession.ts:515-537` sends Runtime-owned `timeline.inverse` for Undo.
- Scope is current occurrence-image only: `sessionPlacement.ts:16-18`; native capture reuses Agent's exact occurrence completion builder and five-field media pin, with the source closure at `:22-27`.
- No new store/coordinator/`producer.guard`/private S3 schema was added. The only new production adapter is `sessionPlacement.ts`; changed source otherwise extends the existing host, task-event, session, and outbox seams.

### Actual Runtime/Agent signature confirmation

- Agent frozen ref `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` exposes `auto_place_completion(bundle, owner, clip_id, media, *, ownership, verified_media, anchor=None, duration=None, preferred_track=None, fallback_at=None, fallback_track=None)` and `capture_placement_create(..., *, ownership, verified_media, consumed=())`. The App callback supplies the corresponding saved values and exact media pin.
- Runtime frozen ref `2c4ac180c2220bdad966bc01e95ad230e99ce26a` requires the five-field verified selector in `runtime_protocol/server.py:52-60` and exposes `get_project_verified_media(project_id, selection, *, authorize)` in `runtime_protocol/service.py:2538-2541`; the App generated/operation clients match these signatures at `generated.ts:180-181` and `operationHost.ts:249-252`.

## Remaining scope boundary / exact lines

No uncalled production completion edge remains for a live, current operation: completion is woken by the task subscription and reconnect/observe, and both reach `requester.resume`.

One explicit boundary remains for the real proxy gate. `RuntimeOperationHost.reconnect()` exists at `src/integrations/runtime/operationHost.ts:70`, but this change has no non-test production caller that automatically invokes it after a retired Runtime operation. The provider binds once at `VideoEditorProvider.tsx:918-925`; a retired operation therefore depends on the existing remount/rebind/explicit recovery path, as documented by the settled design. The real gate must exercise operation rebinding and then prove the saved continuation resumes without a new capture or stale read.

Also, the production adapter calls `readNativePlacementCapture` directly (`sessionPlacement.ts:15`) rather than the older `createNativePlacementCapture` factory. The factory remains non-test-unused by design; the actual installed callback is the lower-level native read/capture API and is invoked from the session requester, so this is not the prior factory-only blocker.

## Independent controls

Private Composition 0.0.12 copy, private Vitest cache, and private preload were used. No install, full suite, browser, socket, build, `tsc`, or central test request was run.

1. `node --import /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-loop-final-independent-review/notes/preload.mjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-loop-final-independent-review/notes/vitest.config.mjs --configLoader=runner --no-cache src/tools/video-editor/commands/commitSession.placement.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx`

   **PASS — 6 files, 261 tests, exit 0, 30.92s.**

2. `node --import /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-loop-final-independent-review/notes/preload.mjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-loop-final-independent-review/notes/vitest.config.mjs --configLoader=runner --no-cache src/integrations/runtime/clientLocalAdapter.test.ts src/integrations/runtime/operationHost.test.ts src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`

   **PASS — 4 files, 88 tests, exit 0, 12.78s.**

The previously reported 426-test result was not repeated wholesale; these are independent nearest controls (349 tests total).

## Next REAL proxy gate

Compose this tree onto the final App `tl/integration` snapshot and verify the required launcher pair before launch:

```text
TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2
TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a
ASTRID_CHECKOUT=/home/user/work/agent
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
npm exec -- playwright test --config playwright.auto-real-proxy.config.ts
```

The gate must use the real Agent executor and Runtime, observe native completion capture, managed-output/verified-media reads, accepted image projection, exact lost-admission/lost-commit replay, Runtime-owned Undo, and Vite/Runtime operation rebinding. This source review does not claim those browser/proxy assertions passed.
