**P3’s failing boundary is established; its root cause remains unproven. Repeated history GETs alone do not explain the 5000 ms failure.** No source, tests, waits, guards, dependencies or retained artifacts changed.

| Retained service command / result ID | Actual outcome |
|---|---|
| `ap2-P1-chain-h6` / `18792`, App f8b15af / Agent7873804 / Runtime2a9e347 | PASS: 2 tests, 56.3s; service exit 0, 141s |
| `full-e2e-three-products` / `12221`, App804134d / Agent079580c / Runtime37eb6c7 | Mounted readiness PASS in 17.4s; originals: 3 FAIL, 5 NOTRUN; exit 1, 501s |
| `ap2-P3-gate5-h6-0348` / `3362`, same App804/079/37eb tuple | Bootstrap outbox readiness FAIL; exit 2, 147s. Original Gate 5 NOTRUN |

P3’s bootstrap helper reached connection and track visibility before its outbox poll failed. The readiness leaf’s subsequent `connected-selection` and fresh-owner checks were NOTRUN. This distinction resolves the apparent disagreement between cause0309 and review0309. See [bootstrap helper](/home/user/work/wt/app-readiness-whole-path-sol-0332/tests/e2e/local/support/app.ts:124) and [failing assertion](/home/user/work/wt/app-readiness-whole-path-sol-0332/tests/e2e/local/three-products.mounted-readiness.spec.ts:301).

The independently traced path is:

- Mounted [save hook](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/tools/video-editor/hooks/useTimelineSave.ts:186) awaits the [original-basis reader](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:110).
- The [basis loader](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/integrations/runtime/dataProvider.ts:885) reads history and pagination, then immutable parent, shots and internals, validates the canonical closure and builds the graph. The handoff subsequently checks the original head, builds the authoring bundle and checks the displayed source.
- History uses [`withSession`](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/integrations/runtime/client.ts:696). The [door](/home/user/work/wt/rt-pin-37eb6c7b/runtime_protocol/door.py:530) authenticates its product credential and dispatches to the [Runtime history handler](/home/user/work/wt/rt-pin-37eb6c7b/runtime_protocol/server.py:545).
- Runtime37eb performs locked, authorized [_read_history](/home/user/work/wt/rt-pin-37eb6c7b/runtime_protocol/timeline_commit_store.py:468), authenticating stored receipts, events, closures and sequential execution evidence. This reads provider evidence; it does not execute a new semantic commit.
- Only after the original basis resolves does the hook obtain recovery identity and [create the session](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/tools/video-editor/hooks/useTimelineSave.ts:211). The session lists scoped recovery owners or [claims a durable owner](/home/user/work/wt/app-readiness-whole-path-sol-0332/src/tools/video-editor/commands/localSaveSession.ts:215).

Supported mechanisms and limits:

- **History verification cost is real.** [Runtime0138](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-readiness-server-probe-0138.md) measured slow schema/authentication work under the mutex on Runtime2a9. All 18 diagnostic requests completed; it reproduced no deadlock. Runtime37eb already contains the qualified operation-local authentication reduction. Those measurements do not establish changed-pair P3 causality.
- **P3 restarted before session creation.** Retained lifecycle records show owner 1, generation 0 basis-read at 4041.2ms, cleanup at 8116.6ms (`sessionPresent=false`, `closed=false`), then generation 1 basis-read at 8121.2ms. No basis-ready, identity-read, session-created or rejection event was retained; no diagnostic loss was reported.
- **The two P3 GETs did not overlap.** [Trace0325](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-readiness-D42-trace-sol-0325/report.md) establishes GET1 HTTP 200 in 3555.827ms and GET2 starting **140.328ms after GET1 ended**. GET2 is unfinished in the trace; server completion is UNKNOWN. Generation/request aliases and a lifecycle-to-trace clock anchor are absent.
- No observed head mismatch exists: the completed history head matched both mounted pairs. Config/registry comparison outcomes and the exact unresolved await remain UNKNOWN. The exact dependency triggering cancellation—including P2 lifecycle triggers—is UNKNOWN.

P1 is a valid passing comparison with different scope: explicit timeline selection, a 90-second owner wait, and a simpler parent fixture. Native readiness seeds parent/shot/internal images and declares whole-timeline reads at request and step boundaries. Both seed implementations submit command arrays as one commit; command count is **not** history-entry count. P2’s readiness pass also cannot explain its later, separate `native-none` gesture failures. Source comparisons found the inspected loader/client/support/P1 spec unchanged between Appf8 and App804; hook and handoff differ.

Source custody remains qualified only to retained observations: installed Runtime bytes matched37eb, while actual failed-run daemon imports/provider attachment remain UNKNOWN. [Scope0302](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-readiness-proof-scope-review-0302.md) certifies 145 passes/60.12s on Agent4151; the 59.37s run’s Agent provenance is UNKNOWN.

**One finite next action:** have existing diagnostic0318 owner review/complete the missing generation→await→request/clock join, including the authoring-bundle await, before another P3 experiment. Runtime memo0322 and App coalescing0325 retain sole fix ownership.

Executed checks: `git diff --check` PASS; `git status --porcelain=v1 --untracked-files=all` empty; `git rev-parse HEAD HEAD^{tree}` confirmed App804134d74782d40855146aa568ff289200b79142/tree8437e47666853b62e03a58af3716235346316fba. No tests, services or browsers launched. Investigation complete; causal attribution remains limited above. Required `commit-msg` and `DONE` created.