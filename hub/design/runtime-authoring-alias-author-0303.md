Implemented **F-authoring-shared-alias** in `authoring_commit.py` plus one new focused test file.

- Authenticates provenance before capturing registered `occurrence.fork` commands.
- Emits payload patches against verified successor roots, with separate structural, payload, and media steps.
- Preserves the untouched sibling’s exact pins and raw images. Generic contradictory-root guard remains strict.
- Original fixture and all 11 assertions remain untouched.

Validation used `/home/user/work/venv-agent/bin/python`, with `PYTHONPATH=.:/home/user/work/runtime` and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`:

```bash
python -m pytest -q tests/timeline/test_authoring_shared_alias_commit.py tests/sdk/test_timeline_public_command.py::test_public_free_edit_cannot_broadcast_one_shared_alias --tb=short --basetemp "$TMPDIR/authoring-checks/pytest-final"
```

**21 passed**, covering either selected alias, exact preservation, preview, acceptance, replay, stale/idempotency refusal, forged sources, mutated reads, and missing media authority.

```bash
python -m pytest -q tests/timeline/test_authoring_publication_migrations.py::test_removed_occurrence_uses_registered_delete_and_preserves_shared_sibling tests/timeline/test_authoring_publication_migrations.py::test_unplaced_local_copy_is_filtered_but_reachable_edit_is_published --tb=short --basetemp "$TMPDIR/authoring-checks/pytest-neighbors"
```

**3 passed.**

- `python -m ruff check astrid/sdk/timeline/authoring_commit.py tests/timeline/test_authoring_shared_alias_commit.py` — passed.
- `python scripts/vendor_lock.py check runtime.lock.json` — passed.
- `python scripts/artifact_manifest.py --check` — passed.
- `git diff --check` — passed.
- Focused parent/final mypy — clean. Repository parent/final comparison with `--python-version 3.13 --no-incremental --cache-dir /dev/null`: **1,934 findings each; zero new or removed normalized identities/multiplicities**. Default configuration stopped on installed NumPy stub syntax.

No implementation blocker. Commit message and `DONE` written; no Git writes performed.

Next: independent Agent review, current-only join, then authorize the original shared-alias fixture body. No original live body, full suite, browser, or journey was run.