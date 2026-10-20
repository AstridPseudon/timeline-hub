# App automatic placement production requester loop

Status: production call path installed; targeted unit evidence passes. **Automatic placement is not yet qualified end to end.** The actual13c real proxy/browser gate remains the next central proof after source review.

## Exact source

- Worktree: `/home/user/work/wt/app-m2-auto-production-requester-loop`, branch `tl/app-m2-auto-production-requester-loop`.
- Base commit: `13c0934b46277524c4b6947f1803947f0184f0af`; base tree: `b80b1dfb15523160b6501e3b4b8e5c1b70dfe0cf`.
- Prospective complete source tree, including both new files: `9e8e48c32808d052f2ee79e7fbac65029993af9c`.
- Computed without writing Git objects/index/refs; the tree-hash calculation was checked against the base tree. `workers/app-m2-auto-production-requester-loop/notes/source-tree.json` contains each changed/new file's SHA256. The harness still owns the commit.
- No integration worktree, shared dependency, branch/ref or production wire schema was changed.

## Installed production callers

1. `clientLocalAdapter.ts:createEditorImagePlacementHost` now exposes the already-bound Runtime operation alongside the unchanged local task client. `VideoEditorProvider.tsx` installs `subscribeRuntimeTaskUpdates` and acquires a reference to the existing shared Runtime task-event poller. Admission awaits the existing `readyRuntimeTaskEvents` cursor barrier and rechecks retirement afterward, closing the fast-settlement startup gap. Closing the task pane therefore does not remove completion discovery. Cached task data only wakes the continuation; authoritative reads still use the bound operation.
2. `commitSession.ts:99` instantiates the requester through the 30-line `sessionPlacement.ts` adapter. Its installed capture callback invokes the existing **`readNativePlacementCapture`** API, retaining the native returned authored bundle plus the original display closure in the normal session payload. It restricts this production caller to occurrence images. The commands-only `createNativePlacementCapture` API remains unchanged for its existing direct consumers.
3. The durable admission reservation calls the session's `reserved` callback only after the original reservation transaction and lifecycle checks. This wakes the same pump. The requester resumes the claimed outbox at `commitSession.ts:175`, using saved task body/key/locator, managed outputs, exact five-field media selection, verified-media lookup, original approval/owner/lane/anchor/read closure and reserved IDs. It does not load today's basis to recapture commands.
4. Requester `deferCommit: true` is additive; existing direct requester request/resume/recover contracts still behave as before. In the editor it stops after linking the captured intent. `commitSession.ts:192` dispatches it through the **existing same outbox and normal command pump**, with the unchanged commit envelope. Placement transmission uses the original operation's exact-byte `transmit`; ordinary commands retain `options.send(request, key)`.
5. Accepted completion enters the existing receipt-consumption block: exact canonical closure and graph, Runtime publication registered in the normal Undo stack, projection awaited, then saved. Placement projects the receipt closure even when a different head was observed during the task. No client rebase or refreshed guards are introduced.
6. The existing explicit owner recovery and retry paths invoke that pump. Canonical `observe` wakes it even on an unchanged head; the Runtime task subscription also wakes it. A wake during a running pump schedules one trailing pass, without another polling framework. Unknown commit ACKs still wait for explicit exact retry/recovery.
7. Cancellation/accepted continuation checks run before requester effects; task failed/cancelled/cancel_requested states retain a visible conflict. The session, operation and IDB claim fence capture and transmission. Disposal unsubscribes and retires the host before releasing the claim; it retains the existing IDB-only append drain and never waits for task/media/commit network acknowledgement.

## Decisions and limits

- Used the existing native **read/capture** API because the session needs its returned authored bundle, not only commands. Its commands-only wrapper and all normal public call signatures remain intact.
- Added an internal defer-commit option so acceptance/history/projection has one session owner. No parallel coordinator, outbox, store, journal, `producer.guard` guess or new wire field.
- While a production automatic continuation is outstanding, new ordinary semantic captures are held behind it. Reopening the same saved generation approval remains possible before a commit prefix exists; changed target/prompt still refuses without rewriting the original. Existing admission-only host fixtures and all their passing behavior tests are preserved unchanged.
- A true clash keeps the continuation, captured commands, request bytes/key and original display basis. It is never silently reauthored at a newer head.
- Parent automatic policy remains deferred to the next official union. The operation must still be current; a retired operation needs an existing remount/rebind/recovery path, and this change does not invent an alternate transport.
- Runtime source reviewed: `runtime_protocol/server.py:VERIFIED_READS` requires the complete five-field verified-media selector. Agent source reviewed: `astrid/sdk/timeline/native_placement_commands.py:placement_create/capture_placement_create` and `native_auto_placement.py`; no command or guard DTO was invented.

## Tests — exact final commands

Run from the worktree above. The private configuration preserves the repository's test setup/plugins, aliases Composition to this worker's private extraction of the repository's immutable 0.0.12 archive, sets cacheDir beneath this worker's notes, and disables Vitest caches. Archive SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. No install or shared dependency/cache writes.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-production-requester-loop
node --import "$W/notes/preload.mjs" node_modules/vitest/vitest.mjs run \
  --config "$W/notes/vitest.config.mjs" --configLoader=runner --no-cache \
  src/tools/video-editor/commands/commitSession.placement.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/nativePlacementCapture.test.ts \
  src/tools/video-editor/commands/placementRequester.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/integrations/runtime/clientLocalAdapter.test.ts \
  src/integrations/runtime/operationHost.test.ts \
  src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.test.tsx \
  src/tools/video-editor/components/EditorImageGeneration.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
```

**PASS: 12 files, 426 tests, exit 0, 56.61s.** Log: `workers/app-m2-auto-production-requester-loop/notes/targeted-final.log`.

```sh
node_modules/.bin/eslint --no-cache \
  src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.ts \
  src/integrations/runtime/clientLocalAdapter.ts \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/sessionPlacement.ts \
  src/tools/video-editor/commands/commitSession.placement.test.ts \
  src/tools/video-editor/commands/editorImagePlacement.ts \
  src/tools/video-editor/commands/placementRequester.ts \
  src/tools/video-editor/commands/nativePlacementCapture.ts \
  src/tools/video-editor/contexts/VideoEditorProvider.tsx
git diff --check
```

**Both PASS, exit 0.** ESLint log: `workers/app-m2-auto-production-requester-loop/notes/lint-final.log`.

The 9 added tests exercise production RuntimeOperationHost negotiation and exact-byte transport, local admission adapter, the installed Runtime task-cache subscription, native verified capture, the claimed session pump, normal acceptance projection/Undo registration, lost admission ACK and commit ACK across repeated reopenings, original capture after a newer initial head, retired task/verified-media callbacks with teardown before network completion, cancelled/failed tasks, a true clash retained across retry/reopen, and the startup-cursor barrier with retirement during its wait. Existing ingress tests were neither rewritten nor weakened.

**Evidence boundary:** these are production-call-path unit tests. HTTP Runtime responses/acceptance are fabricated; fake IndexedDB is not browser crash-durability proof. Native parity/requester tests likewise remain unit evidence. No full suite, project tsc, build, browser, socket, install or central test request was run.

## Remaining real gate / recommended next steps

1. Source-review this tree and compose it onto the final App integration snapshot, keeping the real proxy test from base `13c0934b46277524c4b6947f1803947f0184f0af`.
2. Verify the launcher pair from `app-auto-real-proxy-source-review.md`: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (or an explicitly approved successor tuple), and the actual checkout paths.
3. Run the **actual13c real proxy/browser gate centrally**, once authorized for that final tree. It must establish real executor settlement, native capture, accepted image projection, loss/restart exact replay and Runtime-owned Undo, including Vite/Runtime operation rebinding. This worker does not claim those assertions passed.

No implementation blocker remains for this assigned source task. `commit-msg`, `report.md`, `DONE` and `KEEP` are in the worker directory; KEEP preserves the private test environment/logs for review.
