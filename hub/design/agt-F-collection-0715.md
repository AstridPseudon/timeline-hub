# F-agent-full collection

PASS: current integration tree `4edc4b321cae5cfc58252d7ed89e3f0408238646` had a collection-only regression in `tests/test_dev_journey_quick.py` because `6c5b616a4` intentionally deleted the dormant `astrid/core/extensions` package, while later upstream integration retained the test's old `from astrid.core.extensions.scopes import contribution_roots` import. Upstream `431681a6d3cfa0bba2c8c9baa03f152d33032df1` includes that package, so the defect is downstream integration-only.

The one-file patch removes the missing import and uses the already-established current journey binding `Path(env["ASTRID_USER_PACKS"])`. The original six test functions and assertions are unchanged. Current production uses `astrid.core.pack.discovery.discover_pack_metadata` and `astrid.core.pack.source_setup.active_source_inventory`; no production caller uses `core.extensions.scopes`.

Evidence:

- Exact collector before patch: FAIL, `ModuleNotFoundError`, `0` collected.
- Exact collector after patch: PASS, `6 tests collected`.
- Exact file body after patch: PASS, `6 passed in 0.40s`.
- Scoped Ruff: PASS.
- Normal Ruff baseline: PASS, `2149/2149`.
- Artifact manifest: PASS.
- Vendor lock: FAIL, unrelated shared Runtime checkout is `a5d4258312c979024865ee704da2d632ca5b2730` instead of locked `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Private mypy baseline: FAIL before comparison because `types-PyYAML` is absent and NumPy stubs require Python 3.12 under a Python 3.13 venv; scoped mypy additionally reports the pre-existing line-88 test annotation error.

No full/journey-heavy run was requested; no service env, generated files, package pins, or other worktrees were changed.
