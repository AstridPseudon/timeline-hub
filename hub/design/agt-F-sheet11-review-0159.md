## Report

**Verdict: PASS_SOURCE**

Reviewed `tl/agt-F-sheet11-fps-0154` commit `2b843b27da`.

- Only the permitted test file changed.
- Original XML confirms the invalid fractional `timeline.init` failure.
- Integer initialization plus guarded `doc.patch` restores exact authored `30000 / 1001`; no rounding or synthetic history.
- Seven test-function ASTs, assertions, branches, decorators, topology, identities, opaque fields, and C0 envelope preserved.
- Own-only ancestry: one commit from the integration merge-base.

Checks:

- AST compile/conservation: passed.
- Ruff baseline and candidate: passed.
- `git diff --check`: passed.
- Mypy baseline/candidate: identical NumPy Python-version stub failure at `numpy/__init__.pyi:737`.
- Pytest, collection, fixture/function execution, service, build, browser, render, and probes: not run per restrictions.

Normal original-author merge requested and completed:

- Receipt: `merge-agt-F-sheet11-fps-0154`
- Integration merge: `d265112485cd499ea7cc26dae113af47165e8601`
- Reviewed and integrated file blobs match exactly: `0d02b6e1c30a41348956906e03a76c2d71eb3661`

Later MAIN behavioral proof remains required.