PASS_SOURCE

Reviewed `358eb966b482ab5432d801cd9735e2237049281e` against `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`.

- Scope is exactly the two authorized files.
- Physical provenance is authenticated against immutable shot/internal IDs, revisions, digests, and empty `item_id_map`.
- Existing-owner lineage, alias-map strictness, fork behavior, unknown/duplicate/missing/retarget refusals, and no-write guards remain intact.
- Production trace reaches the change through the registered provider and sequential `occurrence.place-shared` → `doc.patch` path.
- AST confirms only `shot_item_map`, `_item_ids`, and `project_shot_items` changed.
- D91 remains byte-identical with all 29 assertions.
- New controls: 8 test functions, 22 parameter-expanded cases.

Static verification:

- AST parse/compile: PASS
- Ruff baseline and candidate: PASS
- Mypy baseline shadow, candidate product, and new test: PASS
- `git diff --check`: PASS
- No pytest, imports, collection, services, or behavioral qualification performed.

Historical RED is only the author’s D91 request 2966: 5 failures / 5 errors. It is not claimed as a current RED for the new tests. New GREEN remains unverified pending MAIN.

Required combined MAIN recipe, after reviewed `404044d6aa` and normal host `010d0b27ddc406b168345b80757c078e0e8f3989`:

```bash
ASTRID_RUNTIME_CHECKOUT=<reviewed-runtime-tree> \
PYTHONPATH=<combined-agent-tree>:<reviewed-runtime-tree> \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/sdk/test_sequential_shared_item_provenance.py \
tests/editing_conformance/test_commit_runtime_shared_inverse.py \
tests/editing_conformance/test_doc_patch_v2.py::test_shot_item_replacement_records_physical_before_and_after_values \
tests/editing_conformance/test_occurrence_shared_historical.py \
tests/sdk/test_capture_move_exact_time.py
```

Require all original 10 shared-inverse cases, all 22 new cases, exact-time cases, and existing provenance controls to pass with zero skips/xfails.

Created the required commit message and empty `DONE` marker. No product files were modified.