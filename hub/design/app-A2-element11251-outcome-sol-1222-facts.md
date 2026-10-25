# A2 current element11251 outcome propagation

Production caller defect **not demonstrated**. No product source changed. The original Runtime outcome remains **UNKNOWN**; this is not gate or browser credit.

## Retained boundary

Read the exact retained trace and diagnostic locally, without extracting private bodies, URLs, DOM or stacks. There is one scoped commit POST, with trace response status/content size both -1 and no diagnostic response event. The last preclose diagnostic has connection connected, dialog present, original Apply button applying, terminal pending. No timing extraction was repeated.

The diagnostic click listener retains the original button. Its retained read requires that button's closest dialog to equal the currently queried dialog before classifying it as applying. This ties the original DOM button to the current dialog at the observation; it does not expose React fiber identity or the actual adapter promise. A panel replacement before this observation is unsupported by the retained witness.

## Finite source witness

- `ElementsLibraryPanel.tsx:67-105,154`: capture and await execute; then await query invalidation; only then set applied. Failure sets its message. Busy clears in finally; message gates status rendering. No reset effect exists.
- `VideoEditorProvider.tsx:310-379`: actual registration binds the mounted save routes and current head to the adapter; refreshed context updates it.
- `element-adapter.ts:389-497`: capture generation/head, read document, author mutation, await routes.save, return acknowledged result.
- `useTimelineSave.ts:743-801`: capture through the existing owner, adopt preview, await handoff.flush, return current canonical document.
- `timelineLocalSaveHandoff.ts:575-627`: atomic persisted doc.patch; await session.flush, validate adopted head, await history read.
- `localSaveSession.ts:128-208,315-321`: await outbox dispatch/send, adopt acceptance before saved; rejection rolls back and retains intent; unsaved flush rejects.
- `commitOutbox.ts:464-529`: reserve/persist exact request before transmit, consume only returned acceptance.
- `dataProvider.ts:751-768,807-851`, generated client `generated.ts:78-96,202-205`: await HTTP response and body before decoding authoritative acceptance/refusal.

The missing external boundary is the original scoped HTTP response into this generated client/provider/send chain. Source plus a pending request cannot establish server receipt, acceptance, merge, refusal, lost acknowledgement, or actual durable outbox state after close. No source repair is justified by those missing facts. Query invalidation and history are additional awaited steps after receipt, not evidence of a current failure there.

## Mounted controls

Added five controls only to existing `useTimelineSave.currentContract.test.tsx`. They mount the actual `AgentChatProvider`, `VideoEditorProvider`, and `ElementsLibraryPanel`, use the real captured adapter, hook, handoff, session, durable outbox, RuntimeDataProvider and generated response decoder. Only the network response bytes, IndexedDB, exclusive locks and existing renderer invalidation boundary are controlled.

1. Held reply: original execute promise remains unsettled; no status; button disabled; exact body/key persisted. Selection/context rerender preserves the same dialog and one panel mount.
2. Accepted and merged replies: canonical closure adopted, durable intents cleared, captured promise resolves and original panel renders applied. Merged canonical output includes the remote field change.
3. Conflict refusal: same promise rejects, panel shows failure, local preview rolls back and rejected intent remains durable.
4. Panel close/reopen: new panel has fresh local status while canonical/outbox acceptance survives. This expected local lifecycle is not claimed as the original failure.
5. Editor close/lost acknowledgement/restart: original invocation rejects; replacement editor replays identical body/key and adopts canonical acceptance. Replacement panel does not inherit prior success.

The original mounted split test passes unchanged, furnishing the comparison to the shared outbox/canonical path. All original predicates in that test are byte-identical. Protected browser tests, fixtures, locators, budgets, waits, Runtime client, outbox and all product sources are unchanged. No product RED/GREEN was claimed: intermediate failures were new control fixture/assertion errors, documented in JSON.

## Commands and results

Local Node20 `--configLoader=runner --no-cache --maxWorkers=1` startup failed before collection because normal repo config uses undefined `__dirname`. Used the expressly allowed existing normal central targeted route, with no package or config changes:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-A2-element11251-outcome-sol-1222 targeted --files "src/tools/video-editor/hooks/useTimelineSave.currentContract.test.tsx src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/localSaveSession.lifecycle.test.ts"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-A2-element11251-outcome-sol-1222-targeted-1025123228-6804
```

Actual service command:

```sh
npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/hooks/useTimelineSave.currentContract.test.tsx src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/localSaveSession.lifecycle.test.ts
```

Result: **6 files, 105 tests passed, 0 skipped**, tree `5d1247b07c3db77afca0c8369639f945b0005411`. Full log is `targeted.log`. Existing duplicate `effect:text-card` key warnings remain visible; AM Burst controls pass.

```sh
env PATH=/opt/node20/bin:$PATH flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
env PATH=/opt/node20/bin:$PATH ./node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelineSave.currentContract.test.tsx
git diff --check
```

Each exited **0**; actual App typecheck has **0 diagnostics**. No node-config, full, P1/P2/P3, browser, native, live socket or service-probe run was requested or performed.

## Disposition

Return the precise missing response boundary. Obtain correlation of the original scoped HTTP request to its Runtime/provider result and actual client/outbox completion before any product repair or new full tour. No timeout change, speculative caller patch, core outbox proposal or automatic GO. This investigation is complete; actual end-to-end qualification remains unresolved.

Hashes and detailed safe facts are in `facts.json`. Commit message supplied for additive A2 controls; harness owns commit/review/merge. An independent core review is required if a source fix is subsequently produced; none was produced here.
