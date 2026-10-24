# Runtime full census report

Terminal artifact: `runtime-full-1024005856-29085`

- Result: exit 1
- Command: `env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3`
- Counts: 6479 passed, 36 failed, 26 skipped, 15 xfailed, 0 errors, 0 XPASS, 0 deselected, 12 warnings
- Duration: 416.59s
- Runtime snapshot: tree `703b1aac…`, key `95461764…`; exactly matches HEAD `458595850c…`
- External tuple: Agent `b61cebe8…`, App `7135ac72…`, Composition `635f4de0…`
- No baseline was run. No pre-existing labels are assigned under D32.

## Exact failure inventory

Manifest/conformance:

- `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current`
- `tests/test_recorded_responses.py::test_rerecording_is_byte_identical_to_committed_responses`
- `tests/test_recorded_responses.py::test_unnormalized_bodies_satisfy_their_contract_schema[publish_conflict_409]`

Retired-route fixture failures:

- `tests/test_spec_reference.py::test_parent_receipt_compaction_preserves_publication_integrity`
- `tests/test_stage1_runtime_contract_completion.py::test_http_target_mutations_require_idempotency_key`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_over_authored_headless_shell_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_over_empty_headless_shell_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_on_a_fresh_timeline_is_accepted_and_replays`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_genuinely_empty_headless_timeline_still_accepts_expected_head_null`
- `tests/test_timeline_headless_overwrite_refused.py::test_cas_correct_republish_after_reading_the_head_is_accepted`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_references]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_shots]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[snapshot]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[dependency]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[None-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[None-parent]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[speed1-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[speed1-parent]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[3/2-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[3/2-parent]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[False-False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[False-True]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[True-False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[True-True]`
- `tests/test_timeline_legacy_occupancy.py::test_exact_f1_over_http`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_occupied_destination_without_shot_head_is_not_adopted[False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_occupied_destination_without_shot_head_is_not_adopted[True]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_closure_update_and_exact_retry_precede_live_checks`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[receipt]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[occurrence]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[digest]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[projection]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[removed]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_historical_reuse_keeps_newer_global_shot_head[False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_historical_reuse_keeps_newer_global_shot_head[True]`

## Classification and repairs

- Manifest: `ours`, source-profile/generated-artifact setup. R0 changed `packages/python/astrid_runtime_client/__init__.py`; `contract/artifacts.json` still has the prior digest. Owner: Runtime R0. Smallest repair: regenerate `contract/artifacts.json`. Target: `python -m pytest -q tests/test_artifact_manifest.py`.

- Recorded responses: `ours`, stale conformance fixture/contract after R5. Runtime now emits `410 retired_route`; committed `publish_conflict_409.json` expects `409 conflict`, and `common.json` excludes `retired_route`. Owner: Runtime R5/contract. Update the error schema, OpenAPI response, and recorder fixture. Target: `python -m pytest -q tests/test_recorded_responses.py`.

- Remaining 33 failures: `ours`, retired fixtures invoking old writers. Every captured traceback reaches `RuntimeService._require_timeline_command()` at `service.py:1652`; `publish_parent_composition()` calls it at `service.py:2796`. HTTP composition/legacy routes likewise directly reject with `410 retired_route`, reason `timeline_commit_required`.

  This is consistent with the R5 product-authority decision, not a provider regression. Owner: Runtime R5/test migration. Port the meaningful assertions to the v2 commit caller or retain dedicated 410/no-write authority tests; do not restore the retired writers.

  Targeted commands for future repair:

  - `python -m pytest -q tests/test_spec_reference.py::test_parent_receipt_compaction_preserves_publication_integrity`
  - `python -m pytest -q tests/test_stage1_runtime_contract_completion.py::test_http_target_mutations_require_idempotency_key`
  - `python -m pytest -q tests/test_timeline_headless_overwrite_refused.py`
  - `python -m pytest -q tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes`
  - `python -m pytest -q tests/test_timeline_legacy_occupancy.py`

No source-profile/setup mismatch, provider-regression, or proven pre-existing finding was identified. Normal repository checks are `python generators/generate.py --check`, the TypeScript conformance generator check from `README.md`, and `python scripts/artifact_manifest.py --check`; no separate lint/typecheck target is configured.

No tracked edits were made. No tests were invoked by this worker. `commit-msg` and `DONE` were created as required.