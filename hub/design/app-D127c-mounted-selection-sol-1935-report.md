Corrected D127c within the two permitted Runtime test files:

- Selects the first real App `doc.patch` element insertion.
- Requires traced `_dispatch` and bounded prefetch provenance.
- Adds structural, forged-prefetch, mixed/dry-run/retry controls.
- Fixes optional pstats typing; preserves profiler output schema and original predicates.

Validation: central `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py` — **61 passed in 3.62s**. Ruff, Python 3.11 compilation and diff/AST audits passed. Helper Pyright: zero errors. Scoped typechecks: zero new errors; existing baseline diagnostics remain.

Helper SHA-256: `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`  
Tested tree: `8d5683702f36034f27ee7f49737665d66dbc2b75`

[Validation and exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-mounted-selection-sol-1935/evidence/validation.md) and the six requested safe evidence files are published. Commit message and `DONE` are ready; final commit SHA awaits the harness.

No product edits or live element/browser/full/tour runs. Next gate: App validator adaptation plus one coupled independent review. Normal/home/body remains held.