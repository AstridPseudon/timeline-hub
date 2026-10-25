## Verdict: PASS_SOURCE

Reviewed `f32a890e3b` independently. The seven-line test-only change correctly asserts:

- `ABSENT → present(row)` then `present(row) → ABSENT`
- `created == [created]`
- final boundary remains net-zero/absent

All parameters, branches, opaque row fields, retry, reservation, redo, restart, history, no-write, and replace-existing predicates remain preserved. Production source confirms sequential inverse recording and restoration allocation.

Checks:

- `py_compile`: passed
- Scoped Ruff: passed
- AST predicate/assertion conservation: passed
- Mypy baseline/candidate: identical pre-existing NumPy Python-3.12 diagnostic; no target difference
- `git diff --check`: passed
- No tests, collection, helpers, fixtures, services, builds, browsers, renders, or probes executed

Merge requested with:

`request-merge agt-F-netzero-oracle-0210`

Merged into `/home/user/work/agent` at `cef8a5be53`; verified exact target blob `a6056ae9…`.

Functional qualification remains unverified. Main must still run the one exact net-zero original proof; replace-existing remains the separate Runtime/D90 seam.