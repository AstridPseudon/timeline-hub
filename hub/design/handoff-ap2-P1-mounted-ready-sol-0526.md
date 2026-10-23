# P1 mounted readiness diagnosis — no faithful fixture correction

The pre-split expectation is consistent with the actual mounted save lifecycle. An empty owner is persisted eagerly during session creation, not lazily on the first intent. The production storage query is correct. Leave both original positive browser cases unchanged; no known-red body retry is justified by this investigation.

Actual 23041 remains red at the App mounted-readiness seam. Its log does not distinguish an absent owner from existing non-idle owners. The exact mounted error/inflight state cannot be identified without its missing browser artifacts. This is a diagnostic blocker, not proof that a particular App error caused that run.

## Source identity

- Assigned worktree: `/home/user/work/wt/ap2-P1-mounted-ready-sol-0526`.
- Resolved base and current HEAD: `ec8e8a25cf7ac29247d06bc5a224b94145ee71c3` (`tl/ap2-P1-project-seed-return-0514`).
- Current tree: `25140dfd23eeea6e731a4168fce10fa4bff87d8f`, exactly the tree in actual 23041's `snap`; `git diff --stat 25140dfd23eeea6e731a4168fce10fa4bff87d8f HEAD` is empty.
- No tracked or untracked worktree changes. No new source SHA/tree is claimed; no git commit/checkout/merge/rebase was run.
- Service result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P1-project-seed-return-0514-ap2-P1-chain-h6-1023052046-23041/`: terminal `fail`, exit 1, both original cases time out after 90 seconds in `openChain:122`, before either split.

## Actual caller → session → storage

1. `useTimelineSave.ts:82` enables the local document path only with `loadTimelineCommandBasis`, `commitTimeline`, and `getRecoverableIdentity`. The mounted production `RuntimeDataProvider` implements all three (`src/integrations/runtime/dataProvider.ts:739,871` and its commit method).
2. `useTimelineSave.ts:114-212` waits for a loaded head and a clean original document. `readTimelineOriginalSaveBasis` (`timelineLocalSaveHandoff.ts:93-106`) reads the original physical closure, checks revision/publication identity, constructs the authoring bundle, and checks the displayed source against the production load/build projection. This original read can still be pending or fail while track controls are visible.
3. Only after that read and the recovery identity succeed does the hook call `createLocalSaveSession` (`useTimelineSave.ts:158-169`). Cancellation, changed local edit sequence, identity/retirement failure, or source/closure validation failure prevent reaching the claim. The catch at lines 206-208 reports an App local-save error; Runtime connection status alone does not establish save readiness.
4. `createLocalSaveSession` checks the basis, lists existing owners, and calls `claim()` immediately when there are no recoverable nonempty/pending owners (`localSaveSession.ts:241-244`). `claim` starts `storage.create`, reads the claimed record, publishes `saved` with its owner ID, then resolves session readiness (`207-238`). None of this waits for `append` or a gesture.
5. `createCommitOutbox.own` (`commitOutbox.ts:252-276`) stores `{ scope, ownerId, generation: 1, intents: [] }` in a strict readwrite IndexedDB transaction BEFORE invoking the claimed callback. Its primary key is JSON of `[realmId, actorId, projectId, timelineId, ownerId]`; row values carry `scope.timelineId`.
6. `commandOutboxes` (`tests/e2e/local/support/app.ts:195-218`) reads database `astrid.command-outbox`, store `owners`, with a readonly `getAll()`, filters row values by `record.scope.timelineId`, and transports JSON bytes to preserve opaque keys. Those are the actual production names and shape; it does not mistakenly compare the composite storage key with the timeline ID.
7. Therefore `openChain`'s requirement that at least one owner has no pending request and no intents is reachable before the first gesture. Its presence is necessary but does not prove every later recovery stage has completed; capture still awaits the product-owned `localOwner.ready` promise. Removing the wait or accepting `[]` would conceal the current first-seam failure.

## Offline witness and verification

All commands below ran from the assigned worktree. No live browser, local service, HTTP call, original test body, build, full suite, or service retry was run.

The worker-local `node_modules` symlink was pointed at the SAME existing read-only graph used by actual 23041: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules` (Composition 0.0.14). No dependency or shared cache was changed. Vite's cache directory is private and the runner config loader was used.

- `node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p1-chain.spec.ts` — PASS, exactly 2 original cases, 1 file. Log `/tmp/w-d2c48244bb/mounted-ready/list.log`.
- `NODE_OPTIONS=--max-old-space-size=6144 node node_modules/typescript/bin/tsc --project tsconfig.app.json --noEmit` — PASS, exit 0, actual application project checked; `/tmp/w-d2c48244bb/mounted-ready/tsc-app.log` is empty.
- `NODE_OPTIONS=--max-old-space-size=6144 node node_modules/typescript/bin/tsc --project tsconfig.node.json --noEmit` — PASS, exit 0; `/tmp/w-d2c48244bb/mounted-ready/tsc-node.log` is empty. Unlike the root solution config's `tsc --noEmit`, these commands actually check included files. The browser spec itself is outside these project includes; no separate spec typecheck is claimed.
- `node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS, exit 0; `/tmp/w-d2c48244bb/mounted-ready/eslint.log` is empty.
- `git diff --check` — PASS, exit 0. `git status --porcelain=v1 --untracked-files=all` — empty.
- `node node_modules/vitest/vitest.mjs run --config /tmp/w-d2c48244bb/mounted-ready/vitest.config.ts --configLoader runner --no-cache --testTimeout 10000` — PASS, 1 test in 1 file, no skips/xfails, 3.28 seconds total. Log `/tmp/w-d2c48244bb/mounted-ready/lifecycle-final.log`; scratch source `/tmp/w-d2c48244bb/mounted-ready/lifecycle.test.tsx`.

The smallest witness mounts the REAL `useTimelineSave`, which calls the REAL `createLocalSaveSession` and `createCommitOutbox`. It uses P1's seed payload shape and the production `withDefaultTimelineOutput` + `buildTimelineData` projection. Its original verified read is held: no owner or recovery identity is observable before release. After release, the mounted state is ready and the exact unmodified `commandOutboxes` function (extracted and transpiled from current source to avoid loading Playwright fixtures) reads an empty persisted owner with the same owner ID/scope; another timeline reads empty, and the send function is never called. The storage is the repository's in-memory fake IndexedDB with scratch-only standard `databases()` and event-property adapters; this is an offline lifecycle/storage-shape witness, not browser evidence or proof of the live mounted state in 23041.

Scratch setup attempts before the final passing witness exposed runner `__dirname`, hoisted-import, duplicate QueryClient-context, and fake IndexedDB event-property limitations. One incomplete scratch load omitted production output defaults and produced `upstream source differs from the verified authored parent`; adding the production defaults eliminated it. That scratch error is NOT attributed to actual 23041. The incomplete event-property attempt was interrupted (exit 130), and its log is `lifecycle.log`. Final witness expectations were kept positive; no repository behavior test was changed.

## Changes and preserved scope

No product, spec, fixture, test helper, dependency, generated client, suite row, source hash, timeout, port, executor, session wiring, outcome, or browser read was changed. No fixture correction was justified. Reports and a requested P1 commit message were written outside the worktree. The harness decides whether a no-source-change diagnosis needs a commit.

Unchanged hashes:

- `useTimelineSave.ts`: `d56fb2c9c3ae4055d9c7a913f927da5e0381399b49593a69bf3bbf1a2bedcfd6`.
- `localSaveSession.ts`: `aad778d1744c521d207c49c0786ef16e65d6651940443662eab6c22c798ae081`.
- `tests/e2e/local/support/app.ts`: `8e89e2e887032d7e520e5929d60ed9f85f7a2c83eac8573abb8e53f0a6e1a28c`.
- P1 spec: `926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`.
- Agent pin: `f894c3c9dda25ab03527eeb7f52da5da31d627c1`; Runtime pin: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Composition artifact: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- `suites.conf`: `589985b8fe8a338f06773eca0ee2c5dcafb83611efccb3a00fd7abe72225a2c8` (read only; existing P1 row, other rows, source hashes, pins, and 6144 setting untouched).

All original C0v2 request scope/base pair/commands/label/steps with patch and reads/merge/declared reads/dry-run/key assertions remain byte-for-byte intact. So do complete accepted/merged canonical/head/digest/receipt/steps/dependencies/history, conflict/invalid, created IDs, original guards/dependents, raw/opaque/order, lost ACK/exact retry/restart, rollback/recovery/undo, and persisted outbox assertions after the first gesture. None were reached by actual 23041, and they are NOT claimed green.

## Missing evidence / next action

The requested actual service worktree `/home/user/work/wt/.test-ap2-P1-project-seed-return-0514-ap2-P1-chain-h6-1023052046-23041` is absent. The service result directory retains only exit/ext/log/request/runner.log/snap/status/summary, no trace or error context. Searches for `*trace.zip` and `*error-context.md` under `/home/user/work` and ORCH found no P1 chain artifacts. `bin/test-run:44` unconditionally removes the snapshot worktree after execution, explaining the lost paths. The log's artifact links alone are not retained artifacts. An asynchronous request for an alternate retained artifact path was sent; no path was available when this report was prepared.

Manager: independent review of this diagnosis, then obtain the original 23041 artifacts from any external retention. The App lane should inspect the actual original-read/session error or outstanding work, including cancellation/identity/storage failures, before changing product code. A dependency-driven re-render can cancel the original-read effect, but that is only a source-level candidate here, not the established cause. Do not rerun the unchanged known-red body, remove the wait, seed an owner, or invent readiness. Retry the original two cases only after a reviewed correction and artifact retention are in place. Marked BLOCKED because the specifically required actual browser trace/error context is unavailable; classification excludes a lazy-owner/query-shape fixture correction, but exact live cause remains unverified.
