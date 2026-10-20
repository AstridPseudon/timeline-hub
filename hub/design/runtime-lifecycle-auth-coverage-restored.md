# Runtime lifecycle authority coverage restored

Worker: `rt-m2-lifecycle-keep-auth-family-coverage`  
Base: `8f105c26e3b62f9c2683f717a9773a12bc775a8e`

## Changes

- Kept `archive_timeline` and `recover_timeline` out of the retired `FAMILIES` matrix.
- Added HTTP auth/no-write coverage for both existing visibility routes across tracked, fresh, and unused timeline IDs. Unauthenticated and read-only callers must receive 401, with unchanged Runtime state and `total_changes`.
- Expanded historical-recover refusal coverage across tracked, fresh, and unused IDs. Tracked/fresh are archived first, then target valid positive historical version 1 (current version 2), expecting visible 410 `timeline_restore_required`; the absent unused ID expects visible 404 `not_found`. A failing `_command_replay` hook proves refusal precedes accepted-retry lookup, and state/write assertions remain.
- Narrowed the existing `test_runtime_domains.py` strict xfail to a scoped `_RetiredTimelineUpdate` sentinel requiring exactly 410 / `retired_route` / `timeline_commit_required`. Setup and unrelated `ApiError` exceptions rethrow normally.
- Existing current/absent visibility unarchive and exact new-visibility replay coverage was left unchanged.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_legacy_authority.py::test_service_historical_recover_refuses_before_legacy_replay_or_writes tests/test_timeline_legacy_authority.py::test_service_exact_new_visibility_replay_survives_catalog_version_change tests/test_timeline_legacy_authority.py::test_service_visibility_receipt_proof_refuses_malformed_evidence` — **12 passed**.
- Central scoped `restore-integration` with the actual Agent checkout, targeting the two changed/new cases plus the scoped xfail — **12 passed, 1 expected xfailed** in 15.78s. Result: `rt-m2-lifecycle-keep-auth-family-coverage-restore-integration-1020194109-71`.
- `git diff --check` — **passed**.
- A direct local HTTP attempt was blocked at listener creation by the sandbox (`PermissionError: [Errno 1] Operation not permitted`); the central socket-capable run passed. No full suite was run.

No product, schema, client, metadata, or other test files were changed.
