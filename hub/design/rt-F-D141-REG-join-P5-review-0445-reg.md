# D141h actual-result REG join

## Result

The retained cut had 53 bad records. The exact no-cache pristine actual request `rt-pin-fa9cd546-full-d141-pristine-targeted15-1026044256-11121` passed all 15 mapped upstream IDs with zero failures, errors, skips, or xfails. The join is exact: 15 proved REG records plus 38 `NEW_OURS` records. There are no environment-type pristine failures and no unknown exact IDs.

## All 15 exact verdicts

| Original ID | Cut frame/status | Actual | Source basis | Verdict |
|---|---|---|---|---|
| `test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[False]` | AttributeError at `timeline_commit_store.py:261` / FAILURE | PASS | `tests/test_runtime_upgrade.py:130`, body `596585ef...e3bf4` | REG_PROVED |
| `test_upgrade_preserves_canonical_rows_and_retains_backup_only_when_requested[True]` | same | PASS | same | REG_PROVED |
| `test_upgrade_repairs_missing_historical_object_indexes` | same | PASS | `tests/test_runtime_upgrade.py:534`, body `c8007f60...c5d74` | REG_PROVED |
| `test_upgrade_is_not_repeatable_and_refuses_live_owner` | same | PASS | `tests/test_runtime_upgrade.py:638`, body `9399fe21...ee580` | REG_PROVED |
| `test_upgrade_archives_wal_before_activation` | same | PASS | `tests/test_runtime_upgrade.py:686`, body `9361627c...eff2d` | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-checkpoint]` | same | PASS | `tests/test_runtime_upgrade.py:757`, body `fa754f55...87fc` | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[None-publication_flush]` | same | PASS | same | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-checkpoint]` | same | PASS | same | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[before_publication-publication_flush]` | same | PASS | same | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-checkpoint]` | same | PASS | same | REG_PROVED |
| `test_upgrade_restores_after_publication_and_preserves_uncertain_rollback[after_publication-publication_flush]` | same | PASS | same | REG_PROVED |
| `test_upgrade_and_compaction_flush_owned_files_through_writable_handles[upgrade]` | same | PASS | `tests/test_runtime_upgrade.py:795`, body `9107c12d...a0ada` | REG_PROVED |
| `test_upgrade_post_publication_failure_restores_archived_sqlite_sidecars` | same | PASS | `tests/test_runtime_upgrade.py:830`, body `a847338f...201f` | REG_PROVED |
| `test_typescript_conformance_generator_is_byte_stable` | stale artifact AssertionError / FAILURE | PASS | `tests/test_typescript_generator.py:34`, body `e173341d...506e3` | REG_PROVED |
| `test_typescript_generator_check_rejects_client_and_manifest_mutation` | stale artifact AssertionError / FAILURE | PASS | `tests/test_typescript_generator.py:50`, body `09bb60ce...bd7` | REG_PROVED |

The abbreviated IDs in the table are the exact original IDs including module and parameter spelling in `reg.json`.

## Cause and ownership

All 13 upgrade cases retain the same product-facing frame: `_validate_candidate` creates a staged `RealmStore` inspector without `db_path`, and the timeline integrity check reads it at `runtime_protocol/timeline_commit_store.py:261`. The two generator cases retain the stale checked-in `conformance/typescript/contract-metadata.ts` frame. These are the only proved REG causes; no speculative cause is recorded.

The complete handoff and C0v2 closure requirements are in `handoff.md`. P5 custody, all 38 exact node IDs, source hashes, trace, snap, and receipt custody are in `p5-custody.json`.
