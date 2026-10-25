# OPS staging final review validation

## Source and protected-input checks

- Reviewed original `rt-OPS-staging-tool-2209`, `rt-OPS-staging-review-2217`, and `rt-OPS-staging-return-2223` briefs/reports/evidence.
- Reviewed the settled `PLAN.md` before source inspection.
- Reviewed exact return commit `9524356e2ca603f444eda451a502438ef9110d3b`, tree `93ba9e7a6f96ea4d2b9bb31460d01832fcb5945a`; parent is the rejected review base `017bd30c33f88c2e4bed8fb03e910ee1cde6f7db`.
- `git status --short` — clean after moving only the locally generated pycache into the worker tmpdir.
- `git diff --check` — PASS.

## Required author/reviewer controls

- `PYTHONDONTWRITEBYTECODE=1 python3 ops-drop-staging/test_drop_staging.py` — PASS, 14 tests (the original 8 actual-CLI cases plus 6 return regressions).
- `/home/user/work/venv-agent/bin/ruff check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff format --check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py` — PASS, 2 files already formatted.
- `PYTHONPYCACHEPREFIX=/tmp/w-14f7993cf1/drop-staging-pycache-review2235 python3 -m py_compile ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py ops-drop-staging/drop-staging` — PASS.
- `git diff --check` — PASS.

## Additional finite private adversarial controls

Command:

`python3 /tmp/w-14f7993cf1/drop-staging-final-review-2235.py`

Result:

```json
{"archive_symlink_race": {"archive_symlink": true, "outcome": "packed", "outside_unchanged": true, "staging_exists": false}, "evidence_symlink_race": {"evidence_raw_is_symlink": true, "outcome": "packed", "outside_unchanged": true, "staging_exists": false}, "late_lease_race": {"lease_exists": true, "outcome": "packed", "staging_exists": false}, "late_marker_fallback_race": {"archive_exists": false, "error": "protected marker appeared in quarantined tree: KEEP", "nested_payload_exists": false, "staging_exists": true}, "worker_rename_race": {"detached_staging_exists": false, "outcome": "packed", "replacement_exists": true}}
```

These are private in-process fixture controls that invoke the production CLI implementation (`preflight`/`execute`) and inject deterministic changes at the identified boundaries. They are not synthetic real-child acceptance. No full suite, live worker, install, acquisition, browser, provider, or D130 work was run.

## Decision

`FAIL_SOURCE`. The passing baseline and return regressions do not qualify the source for cleanup authorization. The original four findings are not reopened as absent fixes; the five residual races above must be addressed and independently reviewed.
