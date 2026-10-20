## Report

Implemented the scoped recovery port on `f82da322`:

- Added native `TimelineSession.restore(...)` using `timeline.restore`.
- Updated catalog recover to forward canonical timeline ID, original `version`, `expected_version`, and idempotency key.
- Added focused native, retry, CLI-output, and real HTTP qualification assertions.
- Preserved canonical-image/source-carrier code and made no CLI production changes.

Tests:

- `pytest -q tests/sdk/test_timeline_sync.py tests/sdk/test_native_timeline_facades.py tests/sdk/test_timeline_sync_native.py tests/v10/test_domain_cli_projects_timelines.py`
  - **221 passed, 1 skipped**
- Ruff syntax subset: **passed**
- Real HTTP gate: **not run** per instruction; exact remaining node:
  `tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`

The real gate still requires pairing with the exact reviewed Runtime SHA; no positive restore qualification is claimed.

Created `commit-msg` and `DONE`.