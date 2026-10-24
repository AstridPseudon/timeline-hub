# D69 restored-47 plus two-audit service request

The existing `d69-restored47-nodes` row is ready for the manager's first actual
49-body request after the real-service diagnostic below passed. The source manifest remains the
identity manifest: 47 rows, 34 functions, 20 parameterized rows, and 27
non-parameterized rows. Its XML/class selectors are not transport selectors.

The installed tuple is:

- Agent `ef0363985e645481952448619f2cbb25e9d51a66`,
  tree `1be86f3bb070ec0712afa334c7d7fa4c1d4e0a6d`;
- Runtime `bc227de07262accb702eae8a44c4a666b568c08e`,
  tree `1d410a674d827979caf10d2da2ce3767b68c75da`;
- lock `runtime.lock.json` source commit `bc227de07262accb702eae8a44c4a666b568c08e`;
- authenticated profile `agent-remotion-v3-819acf-1110`, with its existing
  package-lock, registry-state, composition archive, node, schema, import,
  and 15-file lock guards.

Transport is derived for every manifest row as
`row.path::row.current_function + row.parameter`. The two conflict
parameters contain spaces, so their shared function is passed once; actual
collection proves that it expands to both manifest rows. The two final
selectors are the reviewed path-form audit predicates. Thus the request has
48 transport arguments and collects exactly 49 rows, with no missing, extra, or
duplicate membership.

Exact manager request:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent d69-restored47-nodes --files "tests/packs/timeline/test_cli_parity.py::test_publish_requires_a_message tests/packs/timeline/test_cli_status_publish.py::test_publish_forwards_key_and_force_to_sdk_once tests/packs/timeline/test_cli_status_publish.py::test_publish_partial_narration_error_preserves_receipt_and_does_not_retry[False] tests/packs/timeline/test_cli_status_publish.py::test_publish_partial_narration_error_preserves_receipt_and_does_not_retry[True] tests/packs/timeline/test_cli_status_publish.py::test_publish_human_output_is_a_short_summary_and_json_keeps_the_envelope tests/packs/timeline/test_cli_status_publish.py::test_publish_still_requires_a_revision_message tests/packs/timeline/test_cli_status_publish.py::test_publish_cas_refusal_is_not_retried_or_reported_as_success[False] tests/packs/timeline/test_cli_status_publish.py::test_publish_cas_refusal_is_not_retried_or_reported_as_success[True] tests/packs/timeline/test_cli_status_publish.py::test_publish_of_a_clean_working_copy_publishes_nothing tests/packs/timeline/test_verbs_working_copy.py::test_a_refusal_from_the_head_lookup_is_one_plain_line_upstream_publish[argv0] tests/packs/timeline/test_verbs_working_copy.py::test_a_refusal_from_the_head_lookup_is_one_plain_line_upstream_publish[argv1] tests/packs/timeline/test_verbs_working_copy.py::test_a_refusal_from_the_head_lookup_is_one_plain_line_upstream_publish[argv2] tests/packs/timeline/test_verbs_working_copy.py::test_publish_conflict_names_the_writer_and_offers_discard_first tests/sdk/test_authoring_revision_diff.py::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[missing_child] tests/sdk/test_authoring_revision_diff.py::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[foreign_project] tests/sdk/test_authoring_revision_diff.py::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[foreign_timeline] tests/sdk/test_authoring_revision_diff.py::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[wrong_revision] tests/sdk/test_authoring_revision_diff.py::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[corrupt_bytes] tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones_r4_original tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head_r4_original tests/sdk/test_timeline_publish_connection.py::test_a_publish_with_no_client_writes_through_the_connection_it_opens_r4_original tests/sdk/test_timeline_publish_connection.py::test_a_publish_with_a_client_writes_through_that_client_r4_original tests/sdk/test_intent_app_astrid.py::test_three_way_legacy_head_is_not_a_conflict_and_keeps_intent_r4_original tests/sdk/test_intent_app_astrid.py::test_merge_keeps_a_film_namespace_key_outside_the_known_list_in_the_namespace_r4_original tests/sdk/test_runtime_response_conformance.py::test_publish_conflict_409_maps_to_conflict_and_keeps_its_details_r4_route tests/sdk/test_timeline_restructure.py::test_three_way_merge_works_on_the_stored_form_r4_original tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original tests/sdk/test_timeline_store_fixes.py::test_publish_merge_keeps_candidate_parent_config_changes_next_to_head_changes_r4_original tests/sdk/test_timeline_store_fixes.py::test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins_r4_original tests/core/test_timeline_element_publication.py::test_d69_upstream_sameclip_exacthead_publication_preserves_closure_and_user_params tests/core/test_timeline_element_publication.py::test_d69_upstream_stale_head_and_concurrent_cas_reject_without_rebase tests/core/test_timeline_element_publication.py::test_d69_upstream_bad_duration_never_publishes[0] tests/core/test_timeline_element_publication.py::test_d69_upstream_bad_duration_never_publishes[-1] tests/core/test_timeline_element_publication.py::test_d69_upstream_bad_duration_never_publishes[inf] tests/core/test_timeline_element_publication.py::test_d69_upstream_bad_duration_never_publishes[nan] tests/core/test_timeline_element_publication.py::test_d69_upstream_unadmitted_owner_and_sourceclip_reject tests/packs/rendering/test_live_scene_composition.py::test_d69_upstream_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[0] tests/packs/rendering/test_live_scene_composition.py::test_d69_upstream_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[1] tests/packs/rendering/test_timeline_filmstrip_cards.py::test_d69_upstream_pack_uses_rendered_frames_without_html_artifact tests/packs/rendering/test_timeline_filmstrip_execution.py::test_d69_upstream_input_only_is_a_materializable_compact_filmstrip_bundle tests/packs/video_editing/test_runtime_publication_chain.py::test_d66_upstream_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke tests/test_installer_schema.py::test_d66_upstream_remotion_lock_pins_the_transitive_schema_package tests/timeline/test_authoring_bundle.py::test_d66_upstream_approval_is_bound_to_candidate_and_base_revision tests/timeline/test_authoring_bundle.py::test_d66_upstream_frozen_render_restart_then_approval_promotion_is_single_generation tests/v10/test_timelines_create.py::test_d66_upstream_remote_create_empty_creates_shell_then_empty_head tests/v10/test_timelines_create.py::test_d69_upstream_remote_create_empty_generates_ulid_when_no_id_given tests/packs/timeline/test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap tests/packs/timeline/test_cli_edit_flags.py::test_voice_line_swap_reflows_and_reports") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The registered command supplies deliberate argv0 `d69-restored47-nodes` to
the inner `bash -c`, so the service's appended selector arguments all reach
pytest through `"$@"`. It retains the existing source AST, import/schema,
Runtime, lock, profile, and node guards. No pytest body was requested by this worker. The harmless diagnostic is
requested on integration:agent through the real test service.

Expected durable JUnit output:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-snapshot-launch-sol-1642/evidence/d69-restored47.xml`


The Agent HEAD guard is the exact existing P4 predicate: the normal HEAD with
its exact parents, or a synthetic HEAD whose sole parent is that normal HEAD.
Both cases require the exact Agent tree. The shell uses pipefail so a failed
47-row AST/metadata source gate cannot be hidden by tee. The normal Runtime,
lock/all15, import/schema, profile819acf and Node20 guards remain in place.
The final pytest call has a 45-second test timeout.

The installed d69-preflight row has byte-identical guards and argument transport;
only the suite key and final pytest executable differ. Its harmless stub checks
all 48 transport arguments plus the original pytest options, records service
HEAD/tree/parents and exits 37. This expected diagnostic exit is not a behavior
verdict. The body row is ready only after the real-service result demonstrates
exactly one stub invocation and exit 37 propagation.

Diagnostic result: agent-d69-preflight-1024164256-28403 (integration:agent).
Durable diagnostic command and artifacts:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-snapshot-launch-sol-1642/evidence/diagnostic-request.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-snapshot-launch-sol-1642/evidence/d69-stub-result.json
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-snapshot-launch-sol-1642/evidence/d69-source-preflight.json

The selector string is byte-identical to worker1634's successful exact49
collection (transport SHA256 6f6e080c887a7976ee6bf132f7bdb90a49aaa7d25262b67ac40ee278d36a18ef).
No second collection is needed. The manager alone requests one body run.


READY: the real service completed the diagnostic in 2 seconds. It reports fail
exit=37 as deliberately requested by the stub; diagnostic acceptance is PASS.
The stub ran exactly once in the service-created snapshot
/home/user/work/wt/.test-agent-d69-preflight-1024164256-28403, HEAD
e6fb511912e7f6b0bca209c794f616e1262d52ea, sole parent ef0363985e645481952448619f2cbb25e9d51a66,
and tree 1be86f3bb070ec0712afa334c7d7fa4c1d4e0a6d. The 47-row/34-function
source gate passed there. Full guards completed before the stub; it verified
all 48 selector arguments. Wrong-source poison exited 1 before the stub.
The actual result is retained in evidence/service-{request,snap,log.txt,summary,exit,status}
and diagnostic-source-preflight.json under the durable worker directory above.
No behavior verdict or JUnit XML exists. The manager may now request ONE body.
