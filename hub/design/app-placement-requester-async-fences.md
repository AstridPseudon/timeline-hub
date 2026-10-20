# Placement requester async fences — inactive source

Completed in `/home/user/work/wt/app-m2-placement-requester-async-fences`, base `07f64b46f`. Read PLAN and the independent review/counterexample patch first. No settled decision changed. Product changes are limited to requester and the narrow capture check below; only direct requester tests were added.

## Changes and composition handoff

- Requester authorization reads through the existing live `ClaimedOutbox.read()` after awaited authenticated identity. That reader already rejects released claims and superseded persisted generations. Task POST, task/output reads, capture and transmission reuse it; no cached generation becomes authority.
- Capture checks authenticated identity and the live claim before callback dispatch and after callback success **or failure**, before storage can link a payload or persist a capture refusal.
- Transmission awaits its result and checks identity/claim in `finally` before returning any accepted/rejected/retry outcome to ordinary dispatch. Interruption keeps the exact saved request/body/key and intent; dispatch records transport uncertainty. A later pass under the original identity replays that request rather than rebuilding it.
- Requester semantic/API refusal persistence also rechecks identity and claim. Identity-service failures are normalized to lifecycle errors, including a transient identity-service `ApiError(403)`, so they cannot become permanent task rejection. Existing genuine first-conflict retention remains intact.
- Kept the inherited post-reservation identity-mismatch rejection behavior; no test expectation changed. No new ID allocation or task rearming was added.

**Unavoidable narrow outbox API change:** `capturePlacement(id, mediaPin, capture, check?: () => Promise<void>)`. The optional check runs immediately before invoking capture and after its success/error catch, outside that catch and before the final storage access. Existing three-argument calls retain their behavior. A thrown requester lifecycle check must escape without being converted into `placement_capture_failed`; otherwise a requester-only wrapper cannot prevent the existing capture catch from permanently rejecting an interrupted approval. Composition must preserve both check locations and their placement outside the semantic-error catch, plus the existing persisted generation checks. No outbox schema, database, journal, coordinator, timer, protocol, authority field, dispatch ACK algorithm or other continuation behavior changed. The parallel composition branch/worktree was not edited.

## Exact executed evidence

Commands ran from the assigned worktree. Logs are under:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-placement-requester-async-fences/notes/`.

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/commands/placementRequester.test.ts -t 'review fences'
```

**RED before product edits:** exit 1, 2 failed assertions, 49 inherited tests outside the filter; 08:22:23 UTC, 1.23s. Stale generation POSTed; changed-actor ACK linked acceptance and pruned pending/intents. `red-before.log` retains the full output. Both tests were copied from `counterexamples.patch` with their exact original setup/assertions, including diagnostic output, and remain verbatim in the final test file.

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/commands/placementRequester.test.ts -t 'identity-service refusal'
```

Additional **RED** before the identity-service normalization: exit 1, 1 failed assertion / 63 outside filter; 08:26:24 UTC, 1.70s. Expected retry, received permanent conflict after an asynchronous identity-service 403 followed by immediately restored authentication. `identity-service-red.log`.

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**Final GREEN using the private dependency overlay:** exit 0, 3 files, **145 passed**, 08:29:11 UTC, 8.07s; `green-private-overlay.log`. All **129 inherited bodies** remain unchanged: original requester file is an exact byte prefix, and outbox/session tests are byte identical to HEAD. Added 16 ordinary test cases (several cover multiple outcomes); none skipped, disabled, weakened or rewritten. Retained review patch equality and inherited source comparisons were also checked with Python against `git show HEAD:<path>`.

Coverage includes both actor/realm changes during capture success/refusal and every transmit outcome; original-identity recovery with exact commit bytes/key, stable original input/created IDs and no recapture/rebuild after pending transmission; release/reclaim and persisted generation loss during capture/transmit; stale callback completion while a newer generation already accepted; capture/transmit/refusal claim loss during awaited identity; changed identity during awaited capture/API refusal checks; first-conflict retention; duplicate accepted recovery; original admission only from the reclaimed generation.

```sh
node_modules/.bin/eslint src/tools/video-editor/commands/placementRequester.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.ts
git diff --check
```

**PASS**, exit 0, no ESLint diagnostics or whitespace errors. Intermediate cohort results are retained: initial fix 130 pass/1 fail (changed inherited rejection behavior, corrected in source); then 131 pass; recovery development 60 pass/1 fail (new fixture expected message lacked generated API error-code prefix, corrected); then 141, 144 and 145 pass. These were targeted runs, not full suites.

**Dependency/tooling incident:** Initial direct runs followed the earlier worker's standard deps8 symlink, `/tmp/app-m2-coherent-deps8/node_modules`. Vite bundled its config under shared `.vite-temp` and Vitest wrote the shared `.vite/vitest/.../results.json`. These incidental tool cache/temp writes violated the shared-folder rule; no dependency package installation/edit/link change was requested or performed. No shared cache files were manually cleaned up or changed afterward. Final qualification instead uses a private overlay at this worker's `deps/node_modules`: package entries point read-only to physical deps8, while `.vite`, `.vite-temp` and `.cache` are private directories; own worktree's ignored `node_modules` symlink points to the overlay. The final command also disables Vitest result caching. A trial with `--configLoader runner --no-cache` failed before collection (`__dirname is not defined` in the existing standard config), so final qualification kept standard bundled config loading, with its temporary files confined to the private overlay. The orchestrator should assess the earlier shared-cache activity against concurrent qualification; the final isolated pass does not undo it. The overlay's `.vite-temp` is empty after the successful run. No worktree build output or temporary files remain.

## Source size

| File | Base lines / bytes | Final lines / bytes | Net lines |
| --- | ---: | ---: | ---: |
| `placementRequester.ts` | 267 / 15113 | 277 / 15741 | +10 |
| `commitOutbox.ts` | 526 / 24388 | 529 / 24581 | +3 |
| Product total | 793 / 39501 | 806 / 40322 | **+13** |
| `placementRequester.test.ts` | 491 / 27984 | 848 / 45366 | +357 |

Product diff: 37 additions / 24 deletions; tests only append. Storage/session test files, session source, generated client, production callers, writers and pins remain unchanged. Shared reports are outside the repository.

## Remaining dependencies and limits

Source-only integration HEADs observed during this task: Agent `408f3ba3f60dda8fcecfcf4384048114c487a5fb`, Runtime `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, App `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff`, Composition `5e06f40146573a529896cc812229eb890c53c81a`. These are **not an executed or qualified current pair/tuple**.

Correction to the older review's source inventory: Agent now registers explicit `placement.create`, `placement.move`, `placement.unplace` and additional native operations. `native_placement_commands.py` explicitly excludes automatic positioning/collision shifting; its creation capture is a bounded occurrence-owned image at caller-supplied absolute time. This does not supply the required automatic completion-placement factory for saved anchor absence/fallback, lane membership/order, start-frame shifts, extent/collision reads, stable media birth IDs and task/attempt commit guards. Those automatic semantics and their real provider/client remain dependencies. No settled plan decision is contradicted.

`rg` still finds no production caller of `createPlacementRequester`/`preparePlacementTask`. Authorized producer preparation, explicit original approval/bindings, authoritative automatic capture, normal commit build/transmit and authenticated finite reconnect/task-read wakeup wiring are still required. Same-store bootstrap/D13/placement composition is separately owned and unverified here.

Tests execute actual outbox logic with fake IndexedDB and generated Runtime client with mocked transport; capture payloads and accepted outcomes are opaque fixtures. Real automatic capture/current-pair task admission or acceptance, Runtime provenance enforcement/rebase, canonical reload, guarded undo/redo, browser durability, closed-editor production recovery and zero legacy-write traffic remain **UNRUN**. No full suite, project tsc, build, browser, install, localhost/socket/server run or central test-service request was executed.

Local task is complete, with no blocker. Keep production activation and writer retirement closed. Next: review these fences and preserve the optional capture check in the separately owned storage composition; supply the real Agent automatic capture and authorized caller, then qualify the supported current pair for success, both lost ACKs/exact restart retries, conflict retention and duplicate completion through later edits/undo. No git commit/merge/rebase/checkout/push/ref mutations were executed. KEEP and conventional commit message are present; DONE marks completion.
