# WC6 current-source composition note

## Scope

Composed the reviewed WC6 slice onto `ee896821` only. The change carries the
bounded native document-script adapter, same-alias occurrence media rebind,
Runtime-authenticated selection/verified-media reads, the accepted-boundary
whole-payload inverse proof, the address-aware scalar media manifest check, and
the corrected dropped-HTTP-acknowledgement proof.

## Conflicts and resolutions

- Current P1 authority, scene/source hydration, and selected-parameter helpers
  were retained. The current `commands.py` F1 `prior_records` and
  `staged_records` behavior was not replaced by the older WC6 file.
- Current parent-registry authority and native parent media behavior were
  retained. The same-alias branch was added only inside the existing occurrence
  media swap path; it validates every alias consumer, updates only bounded
  payload mirrors, and preserves opaque registry fields and alias order.
- Current ordinary media planning was retained. Existing same-alias bindings
  keep authored/opaque fields, and imported entries receive only Runtime's
  exact generation/variant pin needed for authenticated capture.
- `document_diff.py` had no current successor, so the reviewed bounded adapter
  was added as a new file. The script publishes supported timing/track/declared
  parameter edits and same-alias rebinds through `TimelineSession`; unsupported
  structure, narration/text, and unqualified media changes still refuse.
- The reviewed inverse payload guard was composed around current root/cache and
  authority machinery. It requires `AcceptedRecords`, remaps only the verified
  known item identities, permits only the verified internal-timeline link to
  change, and compares all other opaque payload data exactly. The absent-
  ancestor child-write exemption was not retained.
- The current stale-head local test was adapted to the native session seam, and
  the feedback test now exercises a bounded parent timing command. The reviewed
  native HTTP lifecycle test includes the corrected deferred-response fault,
  exact retry body, restart, disjoint rebase, payload tamper refusal, and ABA
  refusal.

## Protected paths and held behavior

- No integration worktree, Runtime/App/Composition repository, branch/ref,
  shared virtualenv, shared `node_modules`, runtime checkout, or other worker
  worktree was modified.
- No old whole-document writer, parent-CAS publication, narration/text binding
  lifecycle, WC3/WC5/D13/carrier/audio source, Composition pin, schema, seed,
  matrix, marker, or full-suite change was imported.
- Existing current P1/F1/Scene/Root/service/ordinary-media/docs behavior and
  the legacy positive requirements remain protected; no old positive was
  rewritten as a refusal.

## Commands and evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_clear_batches.py::test_matching_child_write_cannot_prove_absent_ancestor_read tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_rebind_updates_known_consumers_and_preserves_opaque_registry_fields tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_payload_still_guards_all_other_input tests/timeline/test_authoring_feedback.py::test_document_view_adapter_emits_native_command_for_explicit_parent_timing tests/timeline/test_authoring_feedback.py::test_document_view_adapter_holds_narration_and_same_alias_media_changes tests/timeline/test_authoring_feedback.py::test_document_view_adapter_requires_the_exact_pinned_base tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback`
  — **12 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/rendering/docs/scripts/timeline_document.py astrid/sdk/authoring_media.py astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/document_diff.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/native_occurrence_media_commands.py astrid/sdk/timeline/sync.py astrid/sdk/workspace_client.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_scalar_commands.py tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py`
  — **All checks passed**.
- `git diff --check` — **passed**.
- Central test service: `targeted --files "tests/timeline/test_authoring_media.py"`
  — **71 passed, 1 deselected in 9.93s**. The deselected case is the
  pre-existing `@pytest.mark.integration` legacy whole-publication positive;
  no full suite was run.

The required full suite was not run. The central target is the evidence for the
real HTTP lifecycle; no local live-socket test was run.
