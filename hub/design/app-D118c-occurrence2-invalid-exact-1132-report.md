# D118c occurrence2 report

Changed only [test_commit_runtime_occurrence_create.py](/home/user/work/wt/app-D118c-occurrence2-invalid-exact-1132/tests/editing_conformance/test_commit_runtime_occurrence_create.py).

- Migrated stale `409` expectation to `422`.
- Added authoritative `details.status == "invalid"` and `details.code == "unsupported_timing"`.
- Preserved `1e308`, reason, rejection, no-write, history, inverse/redo, and retry assertions.
- AST conservation: 29 → 31 assertions; all other assertions byte-exact.
- Ruff, mypy, py_compile, and `git diff --check`: PASS.
- Both exact pinned Runtime nodes reached the new assertions successfully, then failed at unrelated Runtime guards:
  - `[False]`: inverse stage materialization guard.
  - `[True]`: grouped physical-promotion guard.
- Full original tail is not green and is unverified. Runtime owner must address those guards; no Runtime or production changes were made.

Pinned Runtime verified clean: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`.

Evidence: [facts.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118c-occurrence2-invalid-exact-1132/evidence/facts.json), [facts.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118c-occurrence2-invalid-exact-1132/evidence/facts.md).