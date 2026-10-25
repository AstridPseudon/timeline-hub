# D88b whole-path P4 source report

## Finding

The current Runtime caller can reuse D88b’s replay memo across requests only while the same `RuntimeService` remains alive:

- `RuntimeService._timeline_commits()` caches one `TimelineCommitStore` and coordinator per service (`runtime_protocol/service.py:2413-2423`).
- The request-local `verification_scope` is recreated per request, but the process-level `_replay_memo` persists (`timeline_commit_store.py:225-279`, `441-451`).
- Successful acceptance preserves prior proofs; exceptions/refusals clear them (`timeline_commit_store.py:252-262`, `service.py:434-443`).
- Every daemon restart constructs a new `RuntimeService` (`daemon.py:244-250`), resetting the memo.

The original P4 fixture explicitly restarts before the undo loop (`test_p4_ten_note_v2_runtime.py:422-426`). Therefore the first `step-1` undo in retained run `14151` used a cold memo. This is a source lifetime finding, not a measured cause of the 45-second result.

## Exact P4 path and shape

The original fixture:

- Uses the pinned `astrid` provider and real Runtime daemon (`test_native_batch_ingress.py:43-68`).
- Uses `daemon.token`, actor `owner`, and the owner credential scopes provisioned in `runtime_protocol/daemon.py:132-136`; the separate executor-token helper is not used.
- Replaces only the socket transport with an in-process `MemorySocket` that invokes the real `RuntimeHandler` (`test_native_batch_ingress.py:70-88`).
- Seeds real `tiny.png`, creates the internal timeline owner, and uses `seed_trusted_parent`; that seed directly calls Runtime acceptance as trusted setup, while the ten-note commit and undo/redo use the genuine Agent provider (`test_p4_ten_note_v2_runtime.py:110-134`, `trusted_seed.py:76-111`).
- Builds one v2 commit containing 10 `doc.patch` commands and 10 steps with ordinal mapping `0..9` (`test_p4_ten_note_v2_runtime.py:305-350`).
- After restart, sends ten separate inverse requests, one per step, followed by ten redo requests (`:428-456`).

Trace:

`TimelineSession.undo` → generated client → fixture transport → `RuntimeHandler` (`server.py:294-319`, route `:525-526`) → `RuntimeService.commit_timeline` (`service.py:2447-2513`) → coordinator/provider (`timeline_commit_execution.py:69-107`) → Agent provider inverse selection (`commit.py:1238-1295`) → `RequestCommitPort` history/CAS reads (`timeline_commit_port.py:210-216`) → `TimelineCommitStore.accept` (`timeline_commit_store.py:1521-1589`) → history/CAS publication (`:1732-1763`) → receipt envelope (`:694-701`) → HTTP response (`server.py:321-335`).

Retained XML evidence for `14151` shows the first post-restart undo reaching this production path and timing out at the 45-second gate. It does not establish which layer dominated.

## Comparison with passing four-R2 source 732

The retained `29429` result used Runtime `732c48…` and had:

- Four helper selectors passing in 7.360–11.308 seconds.
- The P4 ten-note selector failing at 45.314 seconds.
- The helper path’s generated adapter called `case.submit()` directly on the Runtime service (`test_timeline_element_publication_runtime.py:364-421`), rather than the P4 in-process HTTP handler.
- Helper requests contained two or three element commands, then one later head change, one inverse, one redo, and an ABA refusal (`:473-559`).
- The helper also explicitly rebuilt `RuntimeService` after restart (`:514-518`), so its retry path was cold as well.

Thus the passing R2 cases differ in request cardinality, ordinal shape, HTTP boundary, and service lifetime. They are useful source controls but cannot attribute the P4 timeout to the HTTP layer or terminal stack.

## Remaining N-scaling seam

D88b memoization skips full `_verify_accepted_replay`, but it does not memoize:

- Fresh source/base closures, continuations, inverse history, event rows, and realm data used to form the replay key (`timeline_commit_store.py:553-584`).
- The full predecessor history/ledger prefix queried and hashed through `project_seq <= ordinal` (`:586-603`).
- Fresh SQL/CAS input checks (`:204-215`, `:314-325`).
- Provider-side inverse step selection and history traversal.

The important ordinal distinction is that P4’s `command_ordinals` are Agent step ordinals inside one accepted publication; Runtime memo keys and `_history_chain` use accepted-publication `project_seq`. Therefore ten notes do not equal ten Runtime history nodes.

The retained D88b source curve measured the remaining seam at N=2/4/8:

- `_verify_accepted_record`: 4 / 11 / 37
- `revision_closure`: 8 / 22 / 74
- digest bytes: 448,680 / 1,154,193 / 3,717,293
- each new acceptance still performed one full replay

This is prior source-derived measurement, not a current-14151 measurement. No claim is made that it explains the 45 seconds.

## Tests and limits

No tests, collection, fixtures, services, profiles, browsers, or measurements were run, per task restrictions.

Worktree remained unchanged. Commit message was written to the assigned path, and `DONE` was created.