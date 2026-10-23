# G3/R2 corrected join schema restore

Completed against base `ecea7d8563c93059283ef9475ecb41a37e628a38`.

Restored only `astrid/core/timeline/schema/edit-command.schema.json`, specifically the approved `timeline.inverse.args.steps` property. The resulting bytes are identical to reviewed current R2/U4a parent `7d356202826ce60ff676d6e46151187aad9f4a70` (also `fc515591b`/`cedc07280`). SHA-256 is exactly `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.

Evidence:

- Exact reference diff: pass; `git diff --check`: pass.
- Exact published-floor assertion: `1 passed`.
- Compound `test_provider_manifest_reload_undo_and_redo`: `1 passed in 1.33s`.
- Ruff: `current=2150 baseline=2150`.
- Private mypy: `current=1915 baseline=1915`.
- `tests/sdk/test_r2_schema_floor.py` is absent.
- The broader schema-floor/composed invocation had `36 passed, 4 failed`: three frozen current-union equality fixtures omit the restored approved `InverseArgs.steps`, and the composed-schema fixture inventory omits registered `doc.patch`. No tests were changed.

The final tracked diff contains only the canonical schema. No generated hand edits, dependency writes, lock/pin changes, deletions, full/browser/farm/native14/P4HTTP tests, or test weakening were performed.
