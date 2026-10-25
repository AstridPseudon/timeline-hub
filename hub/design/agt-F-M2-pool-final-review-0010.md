## PASS_SOURCE — F-D85

Reviewed `tl/agt-F-M2-pool-return-0005` at `e911171b5b`.

- Verified `add-second` and `remove-middle` seed prior pool membership through genuine Runtime `commitTimeline` receipts.
- Confirmed provider bootstrap, full v2 request fields, authenticated history boundaries, source custody, and all six Runtime-backed cases.
- AST conservation passed: 17 test functions; original assertions, raises, branches, and bodies preserved. Only intended Runtime fixture/marker deltas exist.
- Scope: only `tests/editing_conformance/test_recipe_m2_shot_pool.py`.
- Candidate SHA-256: `7fbdd2f08dc1c772ce57500705a46a8b4a012d50ccd76918c50f1d45ae020b7e`.

Checks passed:

```text
ruff check --config pyproject.toml: baseline and candidate
mypy --no-incremental: baseline and candidate
in-memory compile/AST audit: pass
git diff --check: pass
```

No pytest, Runtime service, build, render, or function execution was run per D85. Functional qualification remains for the later MAIN affected-node batch.

Request normal merge of original return worker `agt-F-M2-pool-return-0005`, not the failed branch. `DONE` marker and review commit message were created.