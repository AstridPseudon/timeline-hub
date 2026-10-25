# Validation

- PASS: source manifests were independently recomputed from `git show <historical-ref>:<path>`; all seven byte counts, line counts, and SHA-256 values matched the completed census manifest.
- PASS: Python `ast.parse` accepted all six historical Runtime files and Agent `astrid/sdk/timeline/commit.py` from exact Git streams.
- PASS: flat census JSON artifacts and retained JSON artifacts parsed; safe arithmetic reproduced 32016 handler/provider/dispatch boundaries and 15200 handler/provider/dispatch boundaries.
- PASS: source enumeration confirmed every ranked waiter and the full Runtime → Agent provider → Runtime return chain. Nested `timeline_commit_port.py:875` and `timeline_commit_store.py:264` are reentrant under already-ranked outer locks.
- PASS: D112 is statically reachable only conditionally through DB/WAL identity change, with `RLock` at `timeline_commit_store.py:315`, reopen at `:333-338`, and SQLite connect/busy timeout at `store.py:1230-1246`.
- PASS: static source scan found no reachable sleep, selector, Event/Condition wait, or subprocess wait in the provider chain; unrelated routes remain excluded.
- PASS: Composition worktree remained clean; current integration was not used as behavioral evidence.
- NOT RUN by explicit task scope: product tests, targeted tests, full suites, browser/live sockets, provider body, authoring, qualification, retry, benchmark/profile/collector, child/acquisition, alternative route, live request body, or D130-held SWAP/WAL transfer.

One source-label correction is recorded, not applied: the census call-path text labels `timeline_commit_store.py:1792/1834` as `store.py`. The source manifest and waiter entries otherwise match the historical objects.
