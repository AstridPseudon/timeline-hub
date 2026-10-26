# D141 integrated post-REG validation

Verdict: **PASS — exact 15 REG selectors only** on Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` / tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, with Agent `8585ed9c0404d0187b2ce70242d25114a32747c2` / tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.

## Acceptance

The first invocation could not create its requested private basetemp because the harness-provided worker `tmpdir` is a regular-file marker. It raised 15 pytest setup `NotADirectoryError`s before any test body ran. No source or test file changed.

The exact selector set was then run once with a private `/tmp/rt-F-D141-postREG-integrated-proof-JfAg26` basetemp/cache:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q --basetemp=/tmp/rt-F-D141-postREG-integrated-proof-JfAg26/basetemp -o cache_dir=/tmp/rt-F-D141-postREG-integrated-proof-JfAg26/cache \
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
  tests/test_runtime_upgrade.py::test_upgrade_post_publication_failure_restores_archived_sqlite_sidecars \
  tests/test_typescript_generator.py::test_typescript_conformance_generator_is_byte_stable \
  tests/test_typescript_generator.py::test_typescript_generator_check_rejects_client_and_manifest_mutation
```

Result: **15 passed, 0 failed, 0 errors, 0 skipped, 0 xfailed**. The 38 `NEW_OURS` records remain outside this result and unchanged.

## Static checks

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check` — PASS.
- `node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"` — PASS.
- `node --check tools/generate_typescript_conformance.mjs` — PASS.
- `tsc --noEmit -p conformance/tsconfig.json` — PASS.
- `git diff --check` — PASS.

## Source and scope checks

- Runtime was clean before and after; Agent was clean before and after.
- The three integrated delta blobs equal their reviewed author blobs exactly: the two TypeScript outputs equal `4a66dee1...c3ae3`; `runtime_protocol/upgrade.py` equals `012889c1...ccc7`.
- The corrected upgrade identity is intentional: the prior review's absent `...ccc6` suffix was withdrawn by immutable correction; actual author commit is `...ccc7`.
- C0 was read from `commit-v2.md`; the recorded contract surface includes base revision/publication pair, commands, label, per-step patches/ordinals, `fields|atomic`, declared reads, idempotency key, dry run, accepted/merged/conflict/invalid/preview replies, canonical authenticated closure records, dependencies/history/guarded undo, conflict reason/head, invalid code/path/hint/suggested command, and preview no mutation.
- No product/test/assertion/input/fixture/generated/contract/generator/pin edit, install, registry refresh, source merge, release/tag claim, or generated-product write occurred.

## Limits

No full Runtime suite, P5 rerun, new pristine run, live gate/body, central service request, source registry refresh, or new Runtime consumer pin was run. The original P5 `38 passed` receipt remains the authentic P5 proof; applicability is documented separately in `p5-applicability.json`.
