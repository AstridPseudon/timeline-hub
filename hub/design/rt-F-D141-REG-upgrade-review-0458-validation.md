# D141 REG upgrade validation

## Targeted tests

Exact unchanged 13 selectors from author `fix.json` / independent `reg.json`, run directly with the required interpreter and Agent checkout:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-28e56cac /home/user/work/venv-runtime/bin/python -m pytest -q --basetemp=/tmp/w-d5878b7f26/rt-F-D141-REG-upgrade-review-0458.wMVSyO/basetemp -o cache_dir=/tmp/w-d5878b7f26/rt-F-D141-REG-upgrade-review-0458.wMVSyO/pytest-cache \
  tests/test_runtime_upgrade.py::test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[False] \
  tests/test_runtime_upgrade.py::test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[True] \
  tests/test_runtime_upgrade.py::test_upgrade_repairs_missing_historical_object_indexes \
  tests/test_runtime_upgrade.py::test_upgrade_is_not_repeatable_and_refuses_live_owner \
  tests/test_runtime_upgrade.py::test_upgrade_archives_wal_before_activation \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-checkpoint] \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-publication_flush] \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-checkpoint] \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-publication_flush] \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-checkpoint] \
  tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-publication_flush] \
  tests/test_runtime_upgrade.py::test_upgrade_and_compaction_flush_owned_files_through_writable_handles[upgrade] \
  tests/test_runtime_upgrade.py::test_upgrade_post_publication_failure_restores_archived_sqlite_sidecars
```

Result: `13 passed in 7.77s`, exit 0; failures/errors/skips/xfails all zero. The first attempt using the prescribed worker `tmpdir` failed at pytest setup because that path is a regular harness marker file, not a directory; no test body ran in that attempt. The successful rerun used a private harness `/tmp` directory and did not modify source or tests.

## Static and scoped checks

- `ast.parse` on `runtime_protocol/upgrade.py`: PASS.
- `git diff --check base..actual -- runtime_protocol/upgrade.py`: PASS.
- Exact selector-set comparison between author `fix.json` and independent `reg.json`: PASS, 13 == 13.
- Contract/client/conformance/test path comparison against Runtime6a011d58: PASS, unchanged.
- Ruff: exit 1 with five diagnostics, exactly the same diagnostics as the Runtime6a baseline; no new diagnostic. Existing diagnostics are import ordering, datetime alias, ValueError/TypeError, and two closure warnings.
- Mypy: exit 1 with 270 existing diagnostics across 23 files; project has no mypy configuration and no new source edit was made outside the three required assignments/import. The changed source line is within a pre-existing untyped `object.__new__` inspector pattern.
- No project `Makefile`; no project lint/typecheck configuration in `pyproject.toml`; no install performed.

## Applicability and scope

`astrid_runtime/operator_upgrade.py:275` calls `upgrade_realm` for v23 production upgrades, so the source delta reaches the production operator path. The actual retained P5 tests call `migrate_canonical_to_current` at `tests/test_timeline_commit_crash.py:81`; that function body has no `_validate_candidate` call. The prior P5 receipt remains historical. No service, full suite, live socket, provider body, or new-head P5 run was performed.

