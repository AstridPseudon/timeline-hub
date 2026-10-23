# G5 SDK checkout/history ports — agt-G5-sdk-history-ports-1528

PASS for the scoped test source port; Runtime integration witness remains pending.

Changed only:

- `tests/sdk/test_timeline_checkout_history_runtime.py`: `redo --publication` → `redo --commit` with the same exact receipt.
- `tests/sdk/test_timeline_checkout_history_boundaries.py`: direct `_commit_document` fixture with its supported keyword-only signature; all existing reset, local undo/redo, history, failure, and no-write assertions retained.

Evidence: boundary tests **9 passed**; central targeted assigned-file lane **9 passed, 4 integration nodes deselected**; assigned files **13 collected**; `py_compile`, `git diff --check`, vendor-lock, and artifact-manifest checks passed. Private checks report Ruff **2148 vs 2149 baseline** and Mypy **1911 vs 1912 baseline**, zero added findings and one inherited improvement each; no baseline files were modified.

Source: base `f57d283d2d4946bbb09d7b68da89422f2d3bfd77`, tree `fb4385a20361ab4af88d5baa92a3517da5faa56a`. Current file SHA-256 values are recorded in the worker report.

The four live Runtime nodes remain unverified because the central targeted service deselects `pytest.mark.integration`; no local live-socket run was performed. G5 remains draft-only/P1-gated as directed.
