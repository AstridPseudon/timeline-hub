# WC6 native same-alias final proof

Status: **blocked on the required Runtime pair; ledger held until merged**.

## Exact pair and source

- Agent source: branch `tl/agt-m2-wc6-native-fixture-proof`, base `17f8434e`, with
  the uncommitted changes in this worker tree. The latest central snapshot used
  for the HTTP proof was `489a6cc3269769bd2e30175a9e00b46f198ee89f`.
- Runtime: archived commit `7f6dd89`, selected through
  `tests.helpers.runtime.use_runtime(commit='7f6dd89')` from
  `/home/user/work/runtime`; the daemon ran with `authoring_profile='astrid'`.
- Mutable state was a fresh temporary realm. The source closure and source
  objects came from Runtime's archived film fixture. The mutable parent,
  shots, and internal revisions were accepted through
  `tests/helpers/trusted_seed.py`, whose request includes the approved native
  bootstrap shape (`created: []`). No borrowed Runtime tree was modified.

## What the proof reaches

`test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
uses the real `timeline_document.py` script with an actual `AstridClient` and
`WorkspaceClient` over the Runtime daemon. It reaches and verifies:

- checkout, local-path import, exact old/new Runtime selections, and native
  `occurrence.swap-media` acceptance;
- same-alias registry order, opaque registry data, two consuming clips, known
  `items`/`assets.source` mirrors, unknown namespaced payload data, source
  placement isolation, and exact old/new selection arguments;
- real reload from the accepted head;
- a stale session held across publication and later rebased disjoint parent
  edit; and
- the atomic bad case: changing an opaque payload namespace is held before
  history changes.

The proof currently does **not** finish the required undo/retry leg. Runtime
`7f6dd89` accepts the same-alias publication, but rejects the inverse at the
Runtime boundary with:

```text
original inverse read changed
ref: occurrence:occurrence-1/shot
path: payload
kind: inverse_dependency_changed
status: conflict
```

The local Agent inverse guard was narrowed to recognize an unchanged descendant
write as proof for an absent ancestor read, but the required archived Runtime
daemon owns this acceptance/inverse decision and is intentionally not modified.
This is an external pair compatibility blocker, not a test skip or denial
substitution.

## Commands and results

- `ruff check astrid/sdk/timeline/inverse.py astrid/sdk/timeline/sync.py astrid/packs/rendering/docs/scripts/timeline_document.py tests/helpers/trusted_seed.py tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py tests/timeline/test_authoring_media.py` — passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_occurrence_media.py tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py -k 'not real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba' -m 'not integration'` — `145 passed, 2 deselected`.
- `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py -m integration` — `2 passed`.
- Central targeted HTTP proof, exact command `pytest -q tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba` — fails only at the required Runtime inverse step with the conflict above. Earlier central attempts also proved the fixture/setup issues were corrected: stale registry identity, asset mirror metadata, child FPS, verified-media propagation, and script source enum.

## Remaining original positives to map/delete next

Do not claim whole WC6 completion. The following original whole-document or
legacy-writer positives remain:

- `tests/timeline/test_authoring_media.py::test_real_runtime_import_and_parent_publication_roundtrip` — direct `publish_parent_composition` fixture and whole-parent publication.
- `tests/timeline/test_authoring_media.py::test_catalog_import_remains_reusable_after_later_parent_cas_conflict` — `publish_authoring_candidate`/`StaleWriter` path.
- `tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping` — fake whole-candidate writer.
- `tests/timeline/test_authoring_bundle.py::test_group_move_compiles_and_uses_existing_publication_boundary` — structural group-move whole-candidate writer.
- `tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields` — broad structural compiler publication.

Narration/text mapping remains explicitly held by
`tests/timeline/test_authoring_feedback.py::test_document_view_adapter_holds_narration_and_same_alias_media_changes`;
that is a guard to preserve until the native text-binding lifecycle exists,
not a positive to rewrite as refusal. Selection/placement/structural mapping
must be handled before deleting the positives above.
