## Completed

- Refreshed generated Runtime client and `runtime.lock.json` from Runtime `d691ddad` / tree `2fc57ada`.
- Confirmed canonical schema parity: SHA256 `472622c45fa6…`.
- Removed only the 12 schema-gated popup xfails; popup lane now passes `48 passed`.
- Preserved nullable-speed first-add xfail. Cause: Runtime `_fraction()` rejects `None` at `timeline_inspection.py` lines 348/415.
- No Runtime core, materialization, producer.guard, Bundle1, App, or CLI changes.

Pin files:

`runtime.lock.json`, generated client files under `astrid_runtime_client/`, and `tests/editing_conformance/test_commit_runtime_occurrence_media.py`.

## Tests

- Popup direct Runtime qualification: `48 passed`
- Focused generated/client/schema/lock suite: `171 passed`
- Ordinary/PARAM/provider neighbors: `18 passed`
- Identity/inverse/add-delete neighbors: `9 passed`
- Vendor freshness, schema parity, `git diff --check`, Ruff: passed
- M1/first-clip socket tests not qualified; sandbox rejected socket bind (`PermissionError`).

No full, browser, or central suite run.

Commit message written to the required `commit-msg` path.