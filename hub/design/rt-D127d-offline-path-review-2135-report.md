# D127d Report

- Read plan and independently traced the full commit path through server, service, coordinator, Agent provider, port, store, auth, and lifecycle guards.
- Confirmed `timeline_commit_auth.py` is production-path scope; no production changes made.
- Reviewed artifact custody and retained benchmark limits. Verdict remains **UNAPPLIED; actual performance UNPROVED**.
- Evidence: `/tmp/.../workers/rt-D127d-offline-path-review-2135/evidence/`

Tests:

- `pytest ... tests/test_timeline_offline_cost.py` — **8 passed**
- Benchmark `--repeats 1` — **UNAPPLIED**, retained warm median 123.629 ms
- AST seam census — **PASS**
- Source hashes / JSON evidence / `git diff --check` — **PASS**
- Ruff — **FAIL**, 5 inherited findings; unchanged due read-only scope

Smallest next replay: existing `tests/test_timeline_commit_integration.py::editing` fixture with the registered Agent provider; run real `capture_move`, disjoint same-base rebase, dry-run, and exact-key replay.

Actual 21.74 s element cost, 13.78 s provider cost, and 1.75 s native control remain incomparable and unexplained. No full or live suite was run.