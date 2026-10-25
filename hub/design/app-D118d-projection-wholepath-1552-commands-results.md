# D118d read-only commands and results

## Source custody and conservation

- `git rev-parse e02180ced^{commit}` — `e02180cedafa581bc8105d77341456b8b1c50b5b`.
- `git rev-parse e02180ced^{tree}` — `b83fcf6cbb2b9bd8620a8b203ba8d0419fa8c354`.
- Finalized test blob — `cadb75166a0fa8eace677554564cea352bf51a7d`; SHA-256 `8747fa62ef628a9c25455fe30876a008ebf54b3b22d575c697c2f6893ca276da`.
- `git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf..e02180ced -- tests/sdk/test_timeline_capture_projection.py` — one modified assigned test file.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf..e02180ced -- tests/sdk/test_timeline_capture_projection.py` — PASS.
- Independent AST comparison — PASS for all 11 `test_*` functions; only `_saved_document` differs. Canonical shot/internal field tuples equal the current `read_document()` caller.
- Worktree status — clean; no repository delta.

## Static checks

- Finalized writer evidence: Ruff PASS, mypy PASS, py_compile PASS, and `git diff --check` PASS on `e02180ced` (writer report/evidence).
- This unchanged audit worktree: `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py` — PASS; mypy with private cache — PASS; private-cache py_compile — PASS.
- Pair file: Ruff PASS; mypy with private cache PASS; private-cache py_compile PASS.
- `git show e02180ced:tests/sdk/test_timeline_capture_projection.py | ruff check -` — PASS. Stdin attempts for mypy (`mypy -`, unsupported) and py_compile (the module API has no `source=` argument) were not valid finalized-file checks; no e021 source copy was created because that branch has no separate worktree and this task forbids applying the source delta. The writer's exact finalized-source mypy/py_compile PASS evidence is retained above.

## Pair-16 accounting audit

- Parsed `handoff-agt-F-D118-core-D89a-1024-outcomes.json` — PASS.
- Exact rows for `tests/editing_conformance/test_current_pair_reader.py` — 16; all outcome `passed`; every row carries source Agent commit `120d71202a9ebafa99011aec417cfca6d67fafc2` and tree `9a65a32e4462464825df6cfe4d913408694ad4c5`.
- Current pair file SHA-256 — `6a0787475f0b032500e769379a2e3f556a4ba5cabc07fa3996350200083a1284`.
- Captured source at Agent `120d71202a9ebafa99011aec417cfca6d67fafc2` SHA-256 — `6a0787475f0b032500e769379a2e3f556a4ba5cabc07fa3996350200083a1284`; byte-exact match — PASS.
- Historical result retained: immutable service `30693`, Agent `120d71202a9ebafa99011aec417cfca6d67fafc2`, Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`, 16 PASS. Current Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` remains unverified; no fresh 16-node body or new core count was run.

## Behavioral execution

- No pytest, own9 rerun, service, browser, acquisition, full suite, or original rerun was run by this worker.
