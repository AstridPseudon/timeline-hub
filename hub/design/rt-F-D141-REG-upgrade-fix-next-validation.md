# D141 Runtime upgrade REG repair validation

## Scope and correction

Base: Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`.

The independent REG join proved 13 upgrade cases fail on the cut because
`_validate_candidate()` creates a staged `RealmStore` inspector without the
production `db_path`; `TimelineCommitStore` then fails during canonical
integrity inspection. After staging `db_path`, the same inspector also needs
the production `threading.RLock` because `TimelineCommitStore` clears replay
memo state under that mutex. The only product change is therefore in
`runtime_protocol/upgrade.py`:

```python
inspector.db_path = root / "realm.sqlite3"
inspector._mutex = threading.RLock()
```

The existing fail-closed quick-check, foreign-key check, canonical integrity
report, schema-v32 migration, archive/journal, publication, rollback, and
recovery paths are unchanged. No contract, test, assertion, fixture, input,
skip, Store, or `timeline_commit_store.py` change was made.

## Exact acceptance

Command, with the production Runtime venv, authenticated Agent checkout, and
private basetemp/cache:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-28e56cac /home/user/work/venv-runtime/bin/python -m pytest -q --basetemp=/tmp/rt-F-D141-REG-upgrade-fix-next.meANQN/basetemp-after -o cache_dir=/tmp/rt-F-D141-REG-upgrade-fix-next.meANQN/pytest-cache-after \
  'tests/test_runtime_upgrade.py::test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[False]' \
  'tests/test_runtime_upgrade.py::test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[True]' \
  'tests/test_runtime_upgrade.py::test_upgrade_repairs_missing_historical_object_indexes' \
  'tests/test_runtime_upgrade.py::test_upgrade_is_not_repeatable_and_refuses_live_owner' \
  'tests/test_runtime_upgrade.py::test_upgrade_archives_wal_before_activation' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-checkpoint]' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-publication_flush]' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-checkpoint]' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-publication_flush]' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-checkpoint]' \
  'tests/test_runtime_upgrade.py::test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-publication_flush]' \
  'tests/test_runtime_upgrade.py::test_upgrade_and_compaction_flush_owned_files_through_writable_handles[upgrade]' \
  'tests/test_runtime_upgrade.py::test_upgrade_post_publication_failure_restores_archived_sqlite_sidecars'
```

Result: `13 passed in 4.12s`, exit 0; 0 failed, 0 errors, 0 skipped, and 0
xfail. `git diff --check` passed. The scoped AST check passed and verified the
only changed path plus both staged assignments.

The first attempted invocation used the harness `tmpdir` marker as a
directory and produced setup-only errors before product code ran. It was
discarded from acceptance; the final command above used a fresh private `/tmp`
directory and is the actual acceptance result.

No configured lint or typecheck tool exists in `pyproject.toml`; none was
installed or run. No full suite was requested or run.

## Source/predicate custody

`runtime_protocol/upgrade.py` changed from SHA-256
`c3f44783b1145877ceec913a4bddeb925e711275296550570fa58a1bc8648cdb` to
`c8787dc29b3fa0097ee7aaa9daa704c1626523498cd2c4574f10e14d7e840d50`.

`tests/test_runtime_upgrade.py` is byte-identical before and after:
`7d1857338a95da5c57f54aa23980c3b8db11a0591a5c7d452f591acac82214a9`.
The relevant test-function AST/source hashes are also identical; see the
absolute `source-manifest.json`.

## P5 applicability boundary

The reviewed P5 route executes `tests/test_timeline_commit_integration.py` and
`tests/test_timeline_commit_crash.py`; neither calls `upgrade_realm` or
`_validate_candidate`. This fix applies to operator upgrade staged-candidate
canonical validation and is not on the executed P5 commit-door/crash path.
The prior P5 receipt remains the authentic cut proof. This worker does not
claim a new-head P5 proof.
