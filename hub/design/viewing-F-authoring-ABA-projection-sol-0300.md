**PASS — bounded Agent repair and required checks.** End-to-end Runtime qualification remains incomplete.

Changed only `_commit_patch.py` and new `test_authoring_undo_projection.py`. Changed functions: `CommitPatch.after`, `CommitPatch.finish`, `rebase_patch`, `_materialization_sites`, `inverse_address_resolver`.

The repair captures single-command v2 inverses, projects the completed final stage with its authenticated manifest, and keeps transient-root authority in source-bound effect ranges. Legacy materializations remain supported. Production flow exercised: `RuntimeCommitService.commit` → `execute` → private capture → `accept`/`preview`.

Old HEAD with capture alone produced **2 expected failures**: invalid stage successor projection and incorrect parent revision. New controls pass, including input/ref/history/boundary/owner/digest/range/ABA corruption refusals.

All commands used `PYTHONPATH="$PWD:/home/user/work/runtime"` and `PYTHONDONTWRITEBYTECODE=1`; the shared Agent environment lacks `runtime_protocol` by itself.

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_authoring_undo_projection.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_payload_still_guards_all_other_input
```

**55 passed in 6.98s.**

Additional commands/results:

- Same pytest options with `test_transient_root_baseline.py test_doc_patch_v2.py`: **112 passed in 8.53s**.
- `python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_commit_preview.py tests/editing_conformance/test_authoring_undo_projection.py`: passed.
- `python -m mypy --cache-dir "$TMPDIR/mypy" --follow-imports=silent astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_commit_preview.py`: zero diagnostics.
- `python scripts/vendor_lock.py check runtime.lock.json`: passed.
- `python scripts/artifact_manifest.py --check`: passed.
- `git diff --check`: passed.

Local Runtime source validation at `f3208b26…` accepted the retained-input undo/redo roundtrip and refused **16 corrupted carriers**. These used reproducible fixture history, not retained remote packet custody.

**Additional Runtime probes failed:** transient create/edit redo reports an occurrence alias outside its boundary; existing-child multi-stage redo reports incomplete native-effect coverage. Runtime guards were unchanged. No live/original/full/browser/service run occurred.

Next: independent review, reorder-history overlap review before porting, then Agent’s authorized changed-original qualification. Commit message and `DONE` are written; no Git mutation was performed.