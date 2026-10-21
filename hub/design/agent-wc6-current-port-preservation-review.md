# WC6 current-port preservation review

## Decision

**APPROVE bounded merge.** Candidate `c8d69323c62115eb5fc37db31fc43c89ffef67b9`
(tree `204ee6aefc097c494aa2025151821e6ed9c05036`) is a safe port from
`5a625dd4c01149a085a9df85952b34cad70801f9` (tree `d305ffabf98dcdb615979d7d18a44daec60abb4c`).
This approves the WC6 native document-script/media/inverse slice only; it does
not close the remaining legacy whole-parent or other held WC6 behavior.

## Current-source and merge check

- The candidate changes only the 13 requested Agent paths: the document script,
  authoring-media custody, command state/commit/inverse/media/sync/client
  helpers, and their focused tests. It does not change generated Runtime or
  Composition pins/schema/client artifacts.
- The base already carries the current Main497/ordinary6ba55/29, Runtime95bd
  (published014), and Composition13 adoption floors. The current Scene, cache
  and facade source remains present. A read-only three-way `git merge-tree` of current
  `931ebb3da20eba1851b5bcd3a75ffdca4c10fefd` with `c8d69323c` produced tree
  `ee3d71f125b6c78edb3acfd178edb3cb818bdf2c` with no conflicts.
- That merge result retains the current `f6485dc4e` staged-inverse changes,
  including its deferred grouped-track selection guard, while adding the
  candidate's accepted materialized-payload proof. It also retains the current
  Scene extraction/cache files and `_recording.py` changes. Merge the candidate
  with current integration; do not replace current files wholesale from the
  stale common-base view.

## Data-preservation findings

The new `document_diff.py` is a 426-line closed adapter, not a generic writer.
It requires the exact pinned parent/placement/shot bases, stable membership and
order, and per-row baselines. It emits existing native commands for the bounded
clip timing/params, parent-track label, and same-alias media cases. Narration,
text payload edits, structure, placement changes, unknown fields and
unqualified selections remain explicit refusals. The script-local `Writer`,
`publish_parent_composition` call, and whole-candidate publication call are
gone from `timeline_document.py`.

The WC1-owned helper is intentionally still present: the generic
`publish_authoring_candidate` implementation and its `store.py` bridge remain
for the legacy/WC1 callers. The exact remaining legacy whole-parent positive is
still visible as
`tests/timeline/test_authoring_media.py::test_real_runtime_import_and_parent_publication_roundtrip`,
with its integration marker and `publish_parent_composition` setup. It was not
rewritten as a refusal, skipped, or deleted. The catalog-reuse/CAS-conflict
positive also remains. This is the required split: script whole-writer gone,
WC1-owned helper and legacy positive retained.

Media custody is bounded and lossless for the approved slice. Same-alias swaps
validate every consuming clip before writing, preserve alias membership/order,
clip identity/order, source-window/timing fields, registry labels and opaque
registry fields, and update only the enumerated payload media mirrors. Local
media planning retains existing authored/opaque alias fields; import receipts
carry Runtime-owned exact generation/variant pins; publication resolves exact
old/new Runtime selections and verified media before native capture. No generic
whole-payload rewrite is introduced.

Inverse safety remains strict. The candidate's materialized-payload allowance
is authenticated by `AcceptedRecords`, exact accepted command identity and
closure/source mapping; only the verified internal-timeline compiler link may
change, while opaque payload data remains exact. The absent-ancestor child-write
weakening is explicitly rejected. Existing opaque/order/membership, created-ID,
same-batch, disjoint, and A-to-B-to-A guards remain. The three-way merge keeps
the public `f648` grouped-track guard as well.

The approved f386 source chain is preserved: `tests/timeline/test_authoring_media.py`
at candidate `c8d69323c` is byte-identical to the reviewed
`f386a1205` file. Thus the native fixture still creates and checks the exact
Runtime `voiceover_script` binding with `slot: None`, UTF-8 `hello`, its
descriptor/CAS bytes, and the original transcript list across checkout,
publication and reload. The prior exact direct/HTTP qualification was not
repeated per task instruction.

## Evidence

Independent compact checks on the candidate:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_inverse_clear_batches.py::test_matching_child_write_cannot_prove_absent_ancestor_read \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_rebind_updates_known_consumers_and_preserves_opaque_registry_fields \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_payload_still_guards_all_other_input \
  tests/timeline/test_authoring_feedback.py::test_document_view_adapter_emits_native_command_for_explicit_parent_timing \
  tests/timeline/test_authoring_feedback.py::test_document_view_adapter_holds_narration_and_same_alias_media_changes \
  tests/timeline/test_authoring_feedback.py::test_document_view_adapter_requires_the_exact_pinned_base \
  tests/timeline/test_authoring_media.py::test_local_registry_replacement_is_readonly_and_strips_stale_authority \
  tests/timeline/test_authoring_media.py::test_import_reuses_catalog_across_retry_keys_and_preserves_distinct_names \
  tests/timeline/test_authoring_media.py::test_supplied_plan_is_rechecked_before_catalog_read_or_import
— 13 passed in 1.94s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/ruff check [all 13 changed Python paths]
— All checks passed

git diff --check 5a625dd4c c8d69323c
— passed

git merge-tree --write-tree 931ebb3da c8d69323c
— conflict-free; tree ee3d71f125b6c78edb3acfd178edb3cb818bdf2c
```

The first pytest attempt without the read-only Runtime checkout on `PYTHONPATH`
stopped during collection with `ModuleNotFoundError: runtime_protocol`; no test
body ran. The successful command above uses the existing shared Runtime source
read-only. No full suite, browser, renderer, live HTTP qualification, or the
existing 251-direct-plus-1-HTTP qualification was rerun.

## Follow-up

Merge `c8d69323c` into current integration with the conflict-free three-way
composition, retain the legacy whole-parent positive as an open migration item,
and keep the WC6 row bounded rather than marking all legacy writers deleted.
