# E3 source-only checks

No imports, test bodies, lint or typechecks executed. Source bytes are from `git show <recorded-sha>:<path>`. App advanced during this review; source citations remain pinned to the audited tuple.

| Repo | Audited SHA | HEAD at verification |
|---|---|---|
| Runtime | `44917baf5976d6a655d582fafc63fde7b6cb242d` | `44917baf5976d6a655d582fafc63fde7b6cb242d` |
| Agent | `22d00393f7d944f1d01505637ca00b1995c3e158` | `22d00393f7d944f1d01505637ca00b1995c3e158` |
| App | `f6a21c285267d6475816adbda74233907ac93911` | `860e9755c876ce510aabc5af0511ffe1886626f6` |

| Repo/path | SHA-256 |
|---|---|
| Runtime `contract/commit-v2.md` | `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7` |
| Runtime `runtime_protocol/daemon.py` | `3dd152c1c3b2744287cedc5fc6b51e39676b3870bae3577cbc555b8d21d8e9fb` |
| Runtime `runtime_protocol/local_worker_composition.py` | `cd77dab93dff8aafc8d9e2db1a8b5739e63f09da9ffe2b888252bc30b769a253` |
| Runtime `runtime_protocol/server.py` | `aa82d81b772edd8edbf76895e8198383a6a34412ab437630024b39aa43b55c52` |
| Runtime `runtime_protocol/service.py` | `94591ec2924b940eccb8deb87ec8c8d3913d803399b1a9737108eee78d0f542c` |
| Runtime `runtime_protocol/services.py` | `4870220d15e38331aca65283f67923f2e39597b6f5900336ce4f32d8433758a5` |
| Runtime `runtime_protocol/timeline_commit_auth.py` | `75f5141cadebafc9f887f5968f39f0ff030d1b2e6c724c24de0bd10b94cde2f0` |
| Runtime `runtime_protocol/timeline_commit_execution.py` | `2b0c256757f1bf0b3ab3124840250d2d8ef5dbec31a259c4b1e924e295619dd6` |
| Runtime `runtime_protocol/timeline_commit_port.py` | `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859` |
| Runtime `runtime_protocol/timeline_commit_provider.py` | `2dff389a11475420395a812d036888ad91c01e16df1170bb77917cc3cf128faf` |
| Runtime `runtime_protocol/timeline_commit_reference_projection.py` | `8143e69bc50775ab045d77977a3824923b37affc44eb8dd35930ab9927449370` |
| Runtime `runtime_protocol/timeline_commit_store.py` | `a2db29e4dbb5ef781d818690647e888b4eb02550c93a3e3d962df161d610d4cd` |
| Runtime `runtime_protocol/timeline_materialization.py` | `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` |
| Runtime `tests/test_native_custody.py` | `8d39fcb6bf09ef7cd2c9c8b9f60fe42ec611001f5fbc15b3c76ec9a152917a5f` |
| Runtime `tests/test_role_custody_authority.py` | `8d4d5ab0f006acce23bd5bb5f5c3cabb0be29582af245a2b11b3d04ab95ce094` |
| Runtime `tests/test_timeline_absent_head_repair_integration.py` | `8242d221ac6dfb740feaec0cc36a32ddb0304e8a4cc886a961e67aab57cca068` |
| Runtime `tests/test_timeline_commit_acceptance.py` | `a70ef657daf9f0599c66291e2a25616414e52934770466a4f503f4f57ffad07f` |
| Runtime `tests/test_timeline_commit_authentication.py` | `10f4f9b53e9a39afa735e26543c29cdb620c776a364b61e0009591212059ad6e` |
| Runtime `tests/test_timeline_commit_sequential_verifier.py` | `fe0cab7cc3a4edf806cbda718cfcdd4b80ca6534d8bad23805029e06c867d129` |
| Runtime `tests/test_timeline_forward_created_authority.py` | `90bfb24667bb7b0faff78ce0cb73d8b91c940fb5e05c1835495d305ff79467bf` |
| Runtime `tests/test_timeline_history_authenticated_read.py` | `a2f27a0e712022e72276470d19d109a83ace8039797ccfe7183dfaf2f585c0c4` |
| Runtime `tests/test_timeline_history_boundaries.py` | `98fb25698bcd5944cd3688ad6b017454682b1eae4e9e22c59ecf30a4b52cfda6` |
| Runtime `tests/test_timeline_inverse_stage_authentication.py` | `c5b44e6d11209385cbf85af4cfa7114802d2ab5e8e7b8712f9ec0a8d14fc155b` |
| Runtime `tests/test_timeline_recorder_abi_authority.py` | `676226476f2389aa673a66392a01f26229d5dbd0fb24d386047394d42bcb19c8` |
| Runtime `tests/test_zero_shim_boundary.py` | `8ecb6241a397e932c99a1a040f1d1fc92b460dace6f8272ad1739ac3256c499d` |
| Agent `astrid/core/execution/custody_broker.py` | `83b7a8124e3f42f6ceffa966e22be8c5695a5434066be08c554b60fd69e57e94` |
| Agent `astrid/sdk/timeline/_recording.py` | `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43` |
| Agent `astrid/sdk/timeline/commands.py` | `b89798a439daace286e6702647c670c532a21575719e4df1bda87607b855ee96` |
| Agent `astrid/sdk/timeline/inverse.py` | `0702cda4d096589e34485295cb40ffe00b0f11692bbb01fbfa5228daa1da69d4` |
| Agent `tests/core/execution/test_custody_broker.py` | `b743e1edc49574dacd6a750d07fa6f9201519693309512b3b8b6184307a74610` |
| Agent `tests/editing_conformance/test_doc_patch_v2.py` | `32e2fd46443106221e424fda9aa432efab6bccd55773a59664d86a400ba15629` |
| Agent `tests/editing_conformance/test_occurrence_shared_historical.py` | `5785329214ba0a5a4c1ee948d55f0378ff6d805ba4dd571519e386a88d67e669` |
| App `src/integrations/runtime/client.ts` | `8e3fdb4919ad993ba7e038f5eeab6a4d79e12d8dffb05e4003443e44d58e1d61` |
| App `src/integrations/runtime/dataProvider.ts` | `9213ed6694cef931fe84fa3c83fda0b06ed02532c1b9b6271ef48c32d38f8988` |
| App `src/integrations/runtime/generated.ts` | `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4` |
| App `src/integrations/runtime/operationHost.ts` | `c11f86dde0131e4c09fea568d340415e0f58c8f08bf8d4d9674b282568ce2284` |
| App `src/tools/video-editor/commands/commitSession.ts` | `7bddb9c4adc28ff7d7079c4011ae965e65952570abe248f3d0247789a3532648` |
| App `src/tools/video-editor/commands/localSaveSession.contract.test.ts` | `df2928aea8372c393b0979f6f495f691ed752d07857a4a13dab96eaa625886e1` |
| App `src/tools/video-editor/commands/localSaveSession.ts` | `def2c8c040daea9cff212c40f4f01062d2a6e7bfe6f76a4928cd53eabbf59230` |
| App `src/tools/video-editor/hooks/useTimelineSave.ts` | `33e0ff6b26689e8af62b099557e8455f6ba87ad2b9bbbcbc69e42ac84918638a` |
| App `supabase/functions/_shared/canonicalWriterRetirement.test.ts` | `e5441b41113a63190b4defa2706e7d64326423479117e6bd0878b9290efde974` |
| App `tests/e2e/local/auto-real-proxy.spec.ts` | `9e282a8265870fb8a6daf1e6a9f76543af39271308c1148ea82a679f869bc1c3` |

## Verified Python symbol and test locations

Existence is not a passing behavioral result. All Python selectors in the Luna audit are resolved below.

- Runtime `runtime_protocol/server.py:294` — `_timeline_commit`
- Runtime `runtime_protocol/service.py:2435` — `commit_timeline`
- Runtime `runtime_protocol/service.py:2450` — `_execute_timeline_commit`
- Runtime `runtime_protocol/timeline_commit_auth.py:100` — `site`
- Runtime `runtime_protocol/timeline_commit_auth.py:451` — `validate_bindings`
- Runtime `runtime_protocol/timeline_commit_auth.py:604` — `_physical_owner`
- Runtime `runtime_protocol/timeline_commit_auth.py:2111` — `command_output`
- Runtime `runtime_protocol/timeline_commit_auth.py:2243` — `_capture_document_images`
- Runtime `runtime_protocol/timeline_commit_auth.py:2449` — `_capture_owners`
- Runtime `runtime_protocol/timeline_commit_auth.py:2469` — `validate_sequential_capture`
- Runtime `runtime_protocol/timeline_commit_auth.py:2779` — `validate`
- Runtime `runtime_protocol/timeline_commit_execution.py:69` — `execute`
- Runtime `runtime_protocol/timeline_commit_port.py:493` — `validate`
- Runtime `runtime_protocol/timeline_commit_port.py:639` — `preview`
- Runtime `runtime_protocol/timeline_commit_port.py:650` — `accept`
- Runtime `runtime_protocol/timeline_commit_port.py:664` — `_validate_sequential_execution`
- Runtime `runtime_protocol/timeline_commit_store.py:202` — `_verify_accepted`
- Runtime `runtime_protocol/timeline_commit_store.py:875` — `_validate`
- Runtime `runtime_protocol/timeline_commit_store.py:1173` — `preview`
- Runtime `runtime_protocol/timeline_commit_store.py:1214` — `accept`
- Runtime `runtime_protocol/timeline_commit_store.py:1424` — `_publish`
- Runtime `runtime_protocol/timeline_materialization.py:39` — `materialization_join`
- Runtime `tests/test_native_custody.py:28` — `test_native_custody_publish_release_and_adopted_signal_use_guard`
- Runtime `tests/test_native_custody.py:62` — `test_native_custody_rejects_wrong_target_or_version`
- Runtime `tests/test_native_custody.py:76` — `test_native_custody_rejects_another_live_controller_while_owned`
- Runtime `tests/test_native_custody.py:98` — `test_native_custody_recovers_when_prior_controller_is_proven_absent`
- Runtime `tests/test_native_custody.py:127` — `test_native_custody_rejects_unsafe_owner_file`
- Runtime `tests/test_native_custody.py:136` — `test_native_custody_wraps_platform_identity_drift_without_signaling`
- Runtime `tests/test_native_custody.py:152` — `test_native_custody_preserves_controller_after_metadata_changes`
- Runtime `tests/test_native_custody.py:171` — `test_native_custody_rejects_each_different_live_controller_incarnation`
- Runtime `tests/test_native_custody.py:198` — `test_native_custody_rejects_unavailable_or_malformed_actor`
- Runtime `tests/test_native_custody.py:212` — `test_native_custody_rejects_missing_or_malformed_persisted_controller`
- Runtime `tests/test_native_custody.py:227` — `test_native_custody_unknown_prior_controller_observation_does_not_adopt`
- Runtime `tests/test_native_custody.py:243` — `test_native_custody_real_reparented_controller_signals_and_releases`
- Runtime `tests/test_role_custody_authority.py:40` — `test_pending_cleanup_owner_is_durable_but_cannot_signal`
- Runtime `tests/test_role_custody_authority.py:49` — `test_pre_spawn_obligation_binds_only_exact_admission_before_exec`
- Runtime `tests/test_role_custody_authority.py:62` — `test_signal_holds_shared_guard_until_kernel_call_completes`
- Runtime `tests/test_role_custody_authority.py:93` — `test_old_actor_or_generation_cannot_signal_after_transfer`
- Runtime `tests/test_role_custody_authority.py:100` — `test_transfer_before_durable_commit_leaves_old_owner`
- Runtime `tests/test_role_custody_authority.py:112` — `test_commit_then_lost_ack_recovers_exact_durable_replay`
- Runtime `tests/test_role_custody_authority.py:140` — `test_positive_owned_child_exit_allows_recovery_but_unknown_does_not`
- Runtime `tests/test_role_custody_authority.py:150` — `test_pid_reuse_or_absence_never_creates_actor_death_proof`
- Runtime `tests/test_role_custody_authority.py:164` — `test_unknown_or_reused_target_never_signals`
- Runtime `tests/test_role_custody_authority.py:169` — `test_runtime_epoch_transition_does_not_seize_delegated_roles`
- Runtime `tests/test_role_custody_authority.py:180` — `test_bounded_exclusive_lock_timeout_leaves_authority_unchanged`
- Runtime `tests/test_role_custody_authority.py:188` — `test_inherited_creator_credentials_do_not_bind_retained_child`
- Runtime `tests/test_role_custody_authority.py:201` — `test_retained_binding_serializes_waiter_and_refuses_changed_capture`
- Runtime `tests/test_role_custody_authority.py:215` — `test_reference_verification_is_read_only_and_requires_exact_designated_actor`
- Runtime `tests/test_role_custody_authority.py:243` — `test_runtime_owner_two_handoff_cycles_fence_historical_claim`
- Runtime `tests/test_role_custody_authority.py:258` — `test_runtime_relinquish_rejects_wrong_actor_or_generation_unchanged`
- Runtime `tests/test_role_custody_authority.py:265` — `test_legacy_detached_runtime_never_acquires_new_claim_authority`
- Runtime `tests/test_role_custody_authority.py:275` — `test_runtime_lineage_breaks_refuse_without_write`
- Runtime `tests/test_role_custody_authority.py:295` — `test_runtime_claim_rechecks_incarnation_and_same_uid`
- Runtime `tests/test_role_custody_authority.py:309` — `test_runtime_claim_exclusive_guard_commits_only_one_successor`
- Runtime `tests/test_role_custody_authority.py:326` — `test_runtime_commit_lost_ack_replays_exact_intent`
- Runtime `tests/test_role_custody_authority.py:343` — `test_runtime_release_precommit_failure_preserves_original_signal_authority`
- Runtime `tests/test_role_custody_authority.py:353` — `test_other_roles_cannot_enter_runtime_relinquish_contract`
- Runtime `tests/test_role_custody_authority.py:360` — `test_actual_darwin_self_identity_and_boundary_use_native_shared_marker`
- Runtime `tests/test_timeline_absent_head_repair_integration.py:40` — `test_repair_exact_bootstrap_retry_restart_and_edit_undo`
- Runtime `tests/test_timeline_absent_head_repair_integration.py:86` — `test_repair_rollback_before_receipt_and_exact_retry`
- Runtime `tests/test_timeline_commit_acceptance.py:160` — `test_atomic_acceptance_exact_recorder_projection_and_same_content_edge`
- Runtime `tests/test_timeline_commit_acceptance.py:188` — `test_identical_retry_after_restart_and_head_advance`
- Runtime `tests/test_timeline_commit_acceptance.py:207` — `test_modern_labels_steps_effects_reads_and_actor_roundtrip_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:287` — `test_legacy_rebased_receipt_and_history_keep_v2_metadata_absent_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:321` — `test_recorder_digest_preserves_main_event_ids_and_stream_sequence`
- Runtime `tests/test_timeline_commit_acceptance.py:344` — `test_changed_payload_and_publication_only_cas_refuse_without_writes`
- Runtime `tests/test_timeline_commit_acceptance.py:370` — `test_invalid_prepared_values_are_atomic`
- Runtime `tests/test_timeline_commit_acceptance.py:400` — `test_failure_after_receipt_rolls_back_every_row`
- Runtime `tests/test_timeline_commit_acceptance.py:417` — `test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once`
- Runtime `tests/test_timeline_commit_acceptance.py:465` — `test_preview_is_validated_and_reserves_nothing`
- Runtime `tests/test_timeline_commit_acceptance.py:486` — `test_parent_clip_aliases_preserve_opaque_values_and_exact_retry`
- Runtime `tests/test_timeline_commit_acceptance.py:524` — `test_history_pages_keep_fixed_bounds_and_reject_foreign_cursor`
- Runtime `tests/test_timeline_commit_acceptance.py:543` — `test_nested_acceptance_is_refused`
- Runtime `tests/test_timeline_commit_acceptance.py:551` — `test_timeline_commit_retention_survives_online_and_offline_compaction`
- Runtime `tests/test_timeline_commit_acceptance.py:583` — `test_verified_baseline_keeps_main_receipt_event_and_unknown_intent`
- Runtime `tests/test_timeline_commit_acceptance.py:612` — `test_unproven_baseline_and_same_content_legacy_write_fail_closed`
- Runtime `tests/test_timeline_commit_acceptance.py:625` — `test_commit_integrity_detects_missing_history_and_corrupt_record`
- Runtime `tests/test_timeline_commit_acceptance.py:672` — `test_complete_recorder_roundtrip_and_replay_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:691` — `test_valid_json_recorder_corruption_fails_every_durable_read_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:701` — `test_corrupt_acceptance_event_and_receipt_facts_fail_closed_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:739` — `test_retry_checks_accepted_event_prefix_without_repair`
- Runtime `tests/test_timeline_commit_acceptance.py:754` — `test_original_retry_ignores_corrupt_later_acceptance`
- Runtime `tests/test_timeline_commit_acceptance.py:804` — `test_upstream_v31_schema_migration_installs_empty_history_without_invented_baselines`
- Runtime `tests/test_timeline_commit_acceptance.py:857` — `test_legacy_timeline_v31_fixture_remains_a_distinct_migration_source`
- Runtime `tests/test_timeline_commit_acceptance.py:882` — `test_real_acceptance_links_consumed_inputs_and_keeps_old_bytes_after_restart`
- Runtime `tests/test_timeline_commit_acceptance.py:938` — `test_live_capture_accept_race_rolls_back_history_receipt_and_input_links`
- Runtime `tests/test_timeline_commit_acceptance.py:964` — `test_complete_detached_child_closure_projects_and_reuses_exact_rows`
- Runtime `tests/test_timeline_commit_acceptance.py:999` — `test_nonmanaged_project_media_relation_cannot_authorize_commit`
- Runtime `tests/test_timeline_commit_acceptance.py:1023` — `test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated`
- Runtime `tests/test_timeline_commit_authentication.py:47` — `test_inverse_omitted_created_claim_is_distinguished_from_explicit_empty_and_ordinary`
- Runtime `tests/test_timeline_commit_authentication.py:62` — `test_inverse_omitted_created_claim_requires_exact_restoration_identity`
- Runtime `tests/test_timeline_commit_authentication.py:130` — `test_valid_record_accepts_and_retry_or_preview_preserves_authoritative_steps`
- Runtime `tests/test_timeline_commit_authentication.py:144` — `test_provider_command_normalizes_empty_allocation_claims_only`
- Runtime `tests/test_timeline_commit_authentication.py:162` — `test_final_parent_reuse_keeps_the_exact_projected_effect_boundary`
- Runtime `tests/test_timeline_commit_authentication.py:196` — `test_forged_provider_records_are_rejected_without_writes`
- Runtime `tests/test_timeline_commit_authentication.py:245` — `test_native_text_alias_refusals_are_atomic`
- Runtime `tests/test_timeline_commit_authentication.py:258` — `test_native_text_alias_duplicate_slot_is_ambiguous`
- Runtime `tests/test_timeline_commit_authentication.py:277` — `test_native_assembly_aliases_project_to_their_agent_physical_sites`
- Runtime `tests/test_timeline_commit_authentication.py:290` — `test_native_assembly_aliases_reject_malformed_or_foreign_sites`
- Runtime `tests/test_timeline_commit_authentication.py:306` — `test_native_assembly_aliases_authenticate_at_the_sealed_boundary`
- Runtime `tests/test_timeline_commit_authentication.py:316` — `test_materialization_turnover_requires_the_captured_physical_owner`
- Runtime `tests/test_timeline_commit_authentication.py:335` — `test_read_claims_are_checked_at_input_and_in_dependency_union`
- Runtime `tests/test_timeline_commit_authentication.py:353` — `test_valid_read_union_can_keep_extra_captures_or_conservative_scope`
- Runtime `tests/test_timeline_commit_authentication.py:366` — `test_atomic_mode_requires_authoritative_scope_dependencies`
- Runtime `tests/test_timeline_commit_authentication.py:384` — `test_sequential_step_reads_use_the_prior_step_output_and_keep_batch_reads`
- Runtime `tests/test_timeline_commit_authentication.py:444` — `test_sequential_created_child_boundary_uses_the_native_birth_not_future_output`
- Runtime `tests/test_timeline_commit_authentication.py:515` — `test_native_record_assertions_and_additional_effects_on_a_real_film`
- Runtime `tests/test_timeline_commit_authentication.py:575` — `test_created_child_is_a_valid_later_step_read_boundary`
- Runtime `tests/test_timeline_commit_authentication.py:659` — `test_rebased_child_bindings_follow_only_authenticated_owner_edges`
- Runtime `tests/test_timeline_commit_authentication.py:875` — `test_created_child_public_acceptance_and_strict_refusals`
- Runtime `tests/test_timeline_commit_authentication.py:968` — `test_created_child_public_sequential_birth_aliases_accept_fields_and_atomic`
- Runtime `tests/test_timeline_commit_authentication.py:995` — `test_created_child_public_atomic_keeps_birth_tamper_refusals`
- Runtime `tests/test_timeline_commit_authentication.py:1053` — `test_created_child_promotion_keeps_prior_parent_media_and_mirror_writes`
- Runtime `tests/test_timeline_commit_authentication.py:1069` — `test_created_child_public_refuses_uncaptured_foreign_source_dependency`
- Runtime `tests/test_timeline_commit_authentication.py:1100` — `test_created_child_public_captured_transcript_advances_sequential_manifest`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:69` — `test_private_sequential_carrier_accepts_authenticated_candidate`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:75` — `test_private_sequential_history_survives_restart_and_exact_retry`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:106` — `test_private_sequential_history_revalidates_retained_facts`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:150` — `test_private_sequential_carrier_rejects_context_tampering_without_write`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:163` — `test_private_sequential_carrier_rejects_prepared_digest_and_boundary_tampering`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:183` — `test_private_sequential_carrier_rejects_boolean_command_ordinal`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:196` — `test_private_sequential_carrier_is_one_attempt_and_does_not_extend_history`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:213` — `test_moved_head_staged_alias_without_private_proof_fails_closed`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:254` — `test_retained_real_capture_runs_both_verification_stages`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:260` — `test_moved_history_replays_authenticated_original_and_landing`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:338` — `test_retained_real_capture_rejects_replay_forgery`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:361` — `test_coordinated_capture_record_map_and_digest_forgery`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:402` — `test_private_capture_malformed_json_has_a_structured_refusal`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:427` — `test_real_capture_rejects_all_replay_ordinal_ranges`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:436` — `test_real_capture_requires_complete_ordered_correspondence`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:452` — `test_private_capture_detaches_and_consumes_on_validation_failure`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:474` — `test_private_capture_is_discarded_before_a_later_accept_attempt`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:573` — `test_public_three_products_seed_preserves_full_raw_assertions_and_history`
- Runtime `tests/test_timeline_commit_sequential_verifier.py:604` — `test_public_three_products_scope_forgery_refuses_without_write`
- Runtime `tests/test_timeline_forward_created_authority.py:74` — `test_real_forward_omission_keeps_exact_allocations`
- Runtime `tests/test_timeline_forward_created_authority.py:108` — `test_explicit_inexact_claims_refuse_without_writes`
- Runtime `tests/test_timeline_forward_created_authority.py:117` — `test_declared_allocation_and_retired_reservation_remain_exact`
- Runtime `tests/test_timeline_forward_created_authority.py:148` — `test_omitted_claim_is_authenticated_from_the_exact_track_creation`
- Runtime `tests/test_timeline_forward_created_authority.py:158` — `test_omission_does_not_authorize_changed_commands_or_allocation_facts`
- Runtime `tests/test_timeline_forward_created_authority.py:198` — `test_mutated_provider_allocations_refuse_without_writes`
- Runtime `tests/test_timeline_history_authenticated_read.py:24` — `test_production_history_authenticates_bound_once_and_preserves_exact_reply`
- Runtime `tests/test_timeline_history_authenticated_read.py:56` — `test_pagination_and_later_mutation_keep_fixed_head_and_reverify`
- Runtime `tests/test_timeline_history_authenticated_read.py:85` — `test_equal_revision_publications_are_each_authenticated`
- Runtime `tests/test_timeline_history_authenticated_read.py:109` — `test_later_request_rechecks_all_authority_and_never_writes`
- Runtime `tests/test_timeline_history_authenticated_read.py:158` — `test_cursor_scope_and_head_are_checked_again_without_writes`
- Runtime `tests/test_timeline_history_authenticated_read.py:174` — `test_authorization_still_precedes_authenticated_history`
- Runtime `tests/test_timeline_history_boundaries.py:99` — `test_http_history_keeps_fixed_head_and_distinct_same_revision_edges`
- Runtime `tests/test_timeline_history_boundaries.py:139` — `test_http_history_scope_auth_and_limits_refuse_without_leaking_data`
- Runtime `tests/test_timeline_history_boundaries.py:184` — `test_http_dry_run_needs_write_scope_and_reserves_nothing`
- Runtime `tests/test_timeline_history_boundaries.py:201` — `test_http_revision_reads_keep_manifest_pinned_children_after_new_head`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:228` — `test_grouped_inverse_effects_use_authenticated_stage_images`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:268` — `test_current_agent_inverse_stage_round_trip`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:334` — `test_current_agent_inverse_rejects_forged_stage`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:372` — `test_current_agent_inverse_native_membership_is_authenticated`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:423` — `test_reviewer_replaced_native_write_is_refused_before_persistence`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:460` — `test_grouped_canonical_stage_observations_retry_exactly`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:516` — `test_store_authenticated_split_and_note_inverse_restores_both_native_mirrors`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:569` — `test_store_split_and_note_native_mirror_forgery_refuses_without_writes`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:596` — `test_store_split_and_note_requires_exact_forward_history`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:686` — `test_source_copy_native_roots_authenticate_and_round_trip`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:704` — `test_source_copy_native_root_forgeries_refuse_without_durable_writes`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:772` — `test_actual_leaf_and_fork_inverse_stages_authenticate_losslessly`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:806` — `test_actual_leaf_inverse_forgery_is_refused`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:888` — `test_retained_occurrence_order_inverse_preserves_authenticated_physical_pins`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:907` — `test_retained_occurrence_order_forgeries_refuse_losslessly`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:983` — `test_retained_native_order_packet_authenticates_against_physical_closure`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:996` — `test_retained_native_order_packet_rejects_coordinated_forgery`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:1081` — `test_retained_nested_ranges_bind_immediate_identity_and_exact_captures`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:1098` — `test_nested_inverse_authenticates_boundaries_without_durable_forgery`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:1181` — `test_actual_nested_inverse_authenticates_complete_retained_boundaries`
- Runtime `tests/test_timeline_inverse_stage_authentication.py:1195` — `test_actual_nested_inverse_forgeries_refuse_losslessly`
- Runtime `tests/test_timeline_recorder_abi_authority.py:74` — `test_genuine_fork_recorder_authority_history_and_exact_retry`
- Runtime `tests/test_timeline_recorder_abi_authority.py:85` — `test_caller_cannot_supply_recorder_authority`
- Runtime `tests/test_timeline_recorder_abi_authority.py:96` — `test_history_authority_requires_accepted_event_commitment`
- Runtime `tests/test_timeline_recorder_abi_authority.py:112` — `test_through_and_through_legacy_submission_is_classified_as_abi_one`
- Runtime `tests/test_timeline_recorder_abi_authority.py:145` — `test_native_coverage_omissions_at_submit_keep_abi_two`
- Runtime `tests/test_timeline_recorder_abi_authority.py:208` — `test_supported_genuine_legacy_acceptance_remains_replayable_after_restart`
- Runtime `tests/test_timeline_recorder_abi_authority.py:227` — `test_legacy_history_cannot_acquire_injected_mode_two`
- Runtime `tests/test_timeline_recorder_abi_authority.py:267` — `test_accept_and_merge_freeze_mode_and_bind_exact_records_request_and_metadata`
- Runtime `tests/test_timeline_recorder_abi_authority.py:302` — `test_genuine_v2_preview_does_not_persist_recorder_authority`
- Runtime `tests/test_timeline_recorder_abi_authority.py:316` — `test_provider_cannot_supply_recorder_authority`
- Runtime `tests/test_timeline_recorder_abi_authority.py:328` — `test_prechange_both_absent_is_legacy_without_reclassifying_records`
- Runtime `tests/test_timeline_recorder_abi_authority.py:357` — `test_mode_commitment_rejects_unilateral_removal_and_metadata_records_or_chain_tamper`
- Runtime `tests/test_timeline_recorder_abi_authority.py:403` — `test_event_mode_requires_integer_enum_even_with_rehashed_event`
- Runtime `tests/test_timeline_recorder_abi_authority.py:421` — `test_postaccept_stripping_and_fullrewrite_cannot_downgrade_frozen_mode`
- Runtime `tests/test_zero_shim_boundary.py:17` — `test_cli_accepts_only_canonical_spellings`
- Runtime `tests/test_zero_shim_boundary.py:35` — `test_backup_verifier_has_no_live_legacy_switch`
- Runtime `tests/test_zero_shim_boundary.py:39` — `test_http_surface_has_no_removed_route_aliases`
- Runtime `tests/test_zero_shim_boundary.py:52` — `test_connect_uses_installed_client_without_mutating_import_path`
- Runtime `tests/test_zero_shim_boundary.py:79` — `test_start_does_not_inject_checkout_into_child`
- Runtime `tests/test_zero_shim_boundary.py:158` — `test_wait_endpoint_does_not_adopt_incumbent_discovery`
- Agent `tests/core/execution/test_custody_broker.py:112` — `test_isolated_wrapper_reaches_fake_peer_without_workload_startup_hook`
- Agent `tests/core/execution/test_custody_broker.py:138` — `test_isolated_wrapper_invalid_peer_never_executes_target`
- Agent `tests/core/execution/test_custody_broker.py:153` — `test_isolated_wrapper_target_restores_network_hook_and_original_environment`
- Agent `tests/core/execution/test_custody_broker.py:229` — `test_pending_cleanup_owner_is_durable_but_cannot_signal`
- Agent `tests/core/execution/test_custody_broker.py:238` — `test_suspended_launch_resume_is_durable_exact_and_one_shot`
- Agent `tests/core/execution/test_custody_broker.py:263` — `test_failed_suspended_resume_consumes_intent_without_retry`
- Agent `tests/core/execution/test_custody_broker.py:288` — `test_pre_spawn_obligation_binds_only_exact_admission_before_exec`
- Agent `tests/core/execution/test_custody_broker.py:301` — `test_signal_holds_shared_guard_until_kernel_call_completes`
- Agent `tests/core/execution/test_custody_broker.py:332` — `test_old_actor_or_generation_cannot_signal_after_transfer`
- Agent `tests/core/execution/test_custody_broker.py:339` — `test_transfer_before_durable_commit_leaves_old_owner`
- Agent `tests/core/execution/test_custody_broker.py:351` — `test_commit_then_lost_ack_recovers_exact_durable_replay`
- Agent `tests/core/execution/test_custody_broker.py:379` — `test_positive_owned_child_exit_allows_recovery_but_unknown_does_not`
- Agent `tests/core/execution/test_custody_broker.py:389` — `test_pid_reuse_or_absence_never_creates_actor_death_proof`
- Agent `tests/core/execution/test_custody_broker.py:403` — `test_unknown_or_reused_target_never_signals`
- Agent `tests/core/execution/test_custody_broker.py:408` — `test_runtime_epoch_transition_does_not_seize_delegated_roles`
- Agent `tests/core/execution/test_custody_broker.py:419` — `test_bounded_exclusive_lock_timeout_leaves_authority_unchanged`
- Agent `tests/core/execution/test_custody_broker.py:457` — `test_strict_birth_fence_precedes_exact_authenticated_recapture`
- Agent `tests/core/execution/test_custody_broker.py:469` — `test_anchor_cannot_upgrade_unproven_or_changed_admission`
- Agent `tests/core/execution/test_custody_broker.py:493` — `test_multiple_exec_refresh_persists_exact_token_and_rejects_old_reference`
- Agent `tests/core/execution/test_custody_broker.py:515` — `test_refresh_failure_never_signals_or_adopts_replacement`
- Agent `tests/core/execution/test_custody_broker.py:543` — `test_only_definitely_unsuccessful_exec_signal_is_retried`
- Agent `tests/core/execution/test_custody_broker.py:569` — `test_exec_retry_is_bounded_and_transfer_still_fences_actor_generation`
- Agent `tests/core/execution/test_custody_broker.py:587` — `test_disk_recovery_cannot_resurrect_live_refresh_anchor`
- Agent `tests/core/execution/test_custody_broker.py:602` — `test_only_positive_retained_direct_child_exit_settles_absent_signal`
- Agent `tests/core/execution/test_custody_broker.py:627` — `test_real_authority_absence_reconciles_only_positive_retained_root`
- Agent `tests/core/execution/test_custody_broker.py:679` — `test_anchor_persistence_failure_never_creates_live_refresh_authority`
- Agent `tests/core/execution/test_custody_broker.py:687` — `test_live_anchor_owner_loss_is_fenced_even_after_authority_transfer`
- Agent `tests/core/execution/test_custody_broker.py:697` — `test_failed_admission_cannot_gain_signal_authority_from_refresh`
- Agent `tests/core/execution/test_custody_broker.py:731` — `test_listener_signal_v1_exact_echo_bytes_remain_unchanged`
- Agent `tests/core/execution/test_custody_broker.py:740` — `test_listener_signal_v2_returns_exact_successful_authority_reference`
- Agent `tests/core/execution/test_custody_broker.py:750` — `test_listener_signal_v2_foreign_authenticated_engine_never_signals`
- Agent `tests/core/execution/test_custody_broker.py:768` — `test_listener_signal_v2_invalid_binding_never_reaches_authority`
- Agent `tests/core/execution/test_custody_broker.py:777` — `test_listener_signal_v2_rejects_exact_shape_and_scalar_type_changes`
- Agent `tests/core/execution/test_custody_broker.py:798` — `test_listener_signal_v2_authority_failure_has_no_success_ack`
- Agent `tests/core/execution/test_custody_broker.py:810` — `test_listener_signal_v2_conflicting_return_is_uncertain_after_kernel_call`
- Agent `tests/core/execution/test_custody_broker.py:821` — `test_listener_signal_v2_exact_refresh_term_then_stale_kill_then_current_kill`
- Agent `tests/core/execution/test_custody_broker.py:866` — `test_cr1a_chain_preserves_admission_resume_ready_baseline_and_revisions`
- Agent `tests/core/execution/test_custody_broker.py:885` — `test_cr1a_pre_ready_refresh_is_admission_and_staged_interleave_does_not_reset_base`
- Agent `tests/core/execution/test_custody_broker.py:909` — `test_cr1a_disk_history_tampering_is_permanently_fenced`
- Agent `tests/core/execution/test_custody_broker.py:931` — `test_cr1a_chain_rejects_substitution_and_fresh_disk_bootstrap`
- Agent `tests/core/execution/test_custody_broker.py:946` — `test_cr1a_signal_checkpoint_failure_disables_proof_and_never_appends_uncommitted_ledger`
- Agent `tests/core/execution/test_custody_broker.py:959` — `test_cr1a_ambiguous_signal_keeps_committed_refresh_without_replay`
- Agent `tests/core/execution/test_custody_broker.py:969` — `test_cr1a_every_failed_checkpoint_permanently_disables_proof`
- Agent `tests/core/execution/test_custody_broker.py:1011` — `test_cr1a_broker_ready_checkpoint_interleave_publishes_exact_staged_base`
- Agent `tests/core/execution/test_custody_broker.py:1041` — `test_cr1a_failed_broker_ready_persistence_never_publishes_baseline`
- Agent `tests/core/execution/test_custody_broker.py:1059` — `test_cr1a_admission_checkpoint_failures_cannot_bootstrap_proof`
- Agent `tests/core/execution/test_custody_broker.py:1077` — `test_cr1a_suspended_admission_cannot_publish_ready_before_consumed_resume`
- Agent `tests/core/execution/test_custody_broker.py:1087` — `test_admission_chain_keeps_authenticated_pre_ready_suffix`
- Agent `tests/core/execution/test_custody_broker.py:1113` — `test_admission_chain_rejects_unretained_or_foreign_history`
- Agent `tests/core/execution/test_custody_broker.py:1131` — `test_pending_admission_chain_only_proves_exact_never_spawned_obligation`
- Agent `tests/core/execution/test_custody_broker.py:1171` — `test_ordinary_observed_descendant_retains_fixed_token_without_exit_race_anchor`
- Agent `tests/core/execution/test_custody_broker.py:1192` — `test_observed_descendant_registration_failures_latch_uncertainty`
- Agent `tests/core/execution/test_custody_broker.py:1217` — `test_observed_fixed_token_signal_preserves_all_existing_fences`
- Agent `tests/core/execution/test_custody_broker.py:1238` — `test_observed_postcapture_exec_keeps_original_token_and_rejects_uncertain_cleanup`
- Agent `tests/core/execution/test_custody_broker.py:1299` — `test_native_census_retains_protected_uid_zombie_and_kernel_topology`
- Agent `tests/core/execution/test_custody_broker.py:1311` — `test_native_identity_preserves_public_shape_birth_and_microsecond_compatibility`
- Agent `tests/core/execution/test_custody_broker.py:1323` — `test_native_selected_absence_is_observation_and_zombie_is_not_live_authority`
- Agent `tests/core/execution/test_custody_broker.py:1332` — `test_native_census_failures_never_become_empty_success`
- Agent `tests/core/execution/test_custody_broker.py:1350` — `test_native_census_rejects_non_user_selectors`
- Agent `tests/core/execution/test_custody_broker.py:1356` — `test_native_census_rejects_platform_and_pointer_abi`
- Agent `tests/core/execution/test_custody_broker.py:1368` — `test_birth_formatter_retains_fixed_english_day_padding_and_local_time`
- Agent `tests/core/execution/test_custody_broker.py:1375` — `test_descendant_diagnostic_preserves_pid_phase_and_cause`
- Agent `tests/core/execution/test_custody_broker.py:1392` — `test_initial_descendant_identity_outcomes_are_distinct_and_sticky`
- Agent `tests/core/execution/test_custody_broker.py:1411` — `test_registration_timeout_diagnostic_retains_launch_pid_and_phase`
- Agent `tests/core/execution/test_custody_broker.py:1433` — `test_unadmitted_absence_retains_durable_non_authority_and_continues_other_admission`
- Agent `tests/core/execution/test_custody_broker.py:1455` — `test_unadmitted_absence_reconciliation_failures_are_sticky`
- Agent `tests/core/execution/test_custody_broker.py:1487` — `test_unadmitted_tombstone_survives_future_census_and_cannot_be_upgraded`
- Agent `tests/core/execution/test_custody_broker.py:1502` — `test_anchored_roles_do_not_gain_unadmitted_absence_disposition`
- Agent `tests/core/execution/test_custody_broker.py:1510` — `test_unadmitted_disposition_never_settles_existing_uncertainty_or_unseen_fork_history`
- Agent `tests/core/execution/test_custody_broker.py:1522` — `test_initial_census_child_cannot_use_unadmitted_absent_parent`
- Agent `tests/core/execution/test_custody_broker.py:1532` — `test_observed_census_does_not_change_linux_pidfd_admission`
- Agent `tests/core/execution/test_custody_broker.py:1546` — `test_postcapture_absence_without_native_precondition_remains_fail_closed`
- Agent `tests/core/execution/test_custody_broker.py:1558` — `test_legacy_entry_cannot_upgrade_unadmitted_tombstone`
- Agent `tests/core/execution/test_custody_broker.py:1573` — `test_fresh_reconciliation_child_is_admitted_and_retained_through_reparenting`
- Agent `tests/core/execution/test_custody_broker.py:1592` — `test_unadmitted_candidate_never_captures_token`
- Agent `tests/core/execution/test_custody_broker.py:1614` — `test_birth_bound_zombie_is_observation_until_absence_not_reap`
- Agent `tests/core/execution/test_custody_broker.py:1633` — `test_terminal_candidate_contradictions_remain_sticky`
- Agent `tests/core/execution/test_custody_broker.py:1651` — `test_initial_terminal_birth_microseconds_must_match_census`
- Agent `tests/core/execution/test_custody_broker.py:1659` — `test_inner_terminal_observation_never_settles_outer_admission`
- Agent `tests/core/execution/test_custody_broker.py:1680` — `test_terminal_candidate_presence_blocks_final_census`
- Agent `tests/core/execution/test_custody_broker.py:1691` — `test_native_candidate_observation_has_explicit_non_authority_outcome`
- Agent `tests/core/execution/test_custody_broker.py:1705` — `test_mach_capture_diagnostics_preserve_primary_and_release_without_secrets`
- Agent `tests/core/execution/test_custody_broker.py:1748` — `test_ordinary_live_candidate_never_reconciles_token_or_partial_binding_failure`
- Agent `tests/core/execution/test_custody_broker.py:1769` — `test_anchored_zombie_uses_strict_identity_api_not_candidate_observation`
- Agent `tests/core/execution/test_custody_broker.py:1779` — `test_new_candidate_cannot_use_zombie_admitted_parent_ancestry`
- Agent `tests/core/execution/test_custody_broker.py:1821` — `test_initial_capture_zombie_uses_original_production_native_census`
- Agent `tests/core/execution/test_custody_broker.py:1852` — `test_initial_native_capture_failure_same_precise_zombie_retains_zero_authority`
- Agent `tests/core/execution/test_custody_broker.py:1878` — `test_postcapture_nonqualifying_observations_stay_sticky`
- Agent `tests/core/execution/test_custody_broker.py:1890` — `test_capture_failure_post_observation_precedes_persistence_and_persistence_cannot_clear_failure`
- Agent `tests/core/execution/test_custody_broker.py:1903` — `test_capture_terminal_candidate_cannot_hide_new_descendant`
- Agent `tests/core/execution/test_custody_broker.py:1912` — `test_capture_terminal_observation_leaves_other_admitted_obligation_unchanged`
- Agent `tests/core/execution/test_custody_broker.py:1925` — `test_capture_terminal_observation_rechecks_authenticated_actor`
- Agent `tests/core/execution/test_custody_broker.py:1938` — `test_capture_terminal_rule_never_clears_prior_uncertainty`
- Agent `tests/core/execution/test_custody_broker.py:1947` — `test_capture_terminal_candidate_serializes_concurrent_observers`
- Agent `tests/core/execution/test_custody_broker.py:1977` — `test_command_diagnostic_decodes_argc_excludes_environment_and_redacts_secret_flags`
- Agent `tests/core/execution/test_custody_broker.py:1989` — `test_command_diagnostic_malformed_or_overlimit_args_are_explicit`
- Agent `tests/core/execution/test_custody_broker.py:1995` — `test_command_diagnostic_brackets_actual_parent_and_image_without_authority`
- Agent `tests/core/execution/test_custody_broker.py:2018` — `test_opted_in_command_diagnostic_keeps_live_capture_failure_and_zero_authority`
- Agent `tests/core/execution/test_custody_broker.py:2036` — `test_command_diagnostic_is_disabled_for_existing_owners`
- Agent `tests/core/execution/test_custody_broker.py:2045` — `test_command_diagnostic_rejects_ambiguous_leading_argument_or_environment_boundary`
- Agent `tests/core/execution/test_custody_broker.py:2050` — `test_command_diagnostic_inflated_argc_cannot_persist_environment`
- Agent `tests/core/execution/test_custody_broker.py:2058` — `test_command_diagnostic_opaque_payload_is_digest_only`
- Agent `tests/core/execution/test_custody_broker.py:2069` — `test_shell_combined_options_cannot_expose_path_shaped_command`
- Agent `tests/core/execution/test_custody_broker.py:2076` — `test_ambiguous_environment_entries_are_rejected_before_hashing`
- Agent `tests/core/execution/test_custody_broker.py:2088` — `test_command_diagnostics_requires_exact_per_run_opt_in`
- Agent `tests/core/execution/test_custody_broker.py:2099` — `test_opted_in_success_records_metadata_without_granting_extra_authority`
- Agent `tests/core/execution/test_custody_broker.py:2114` — `test_optional_diagnostic_write_failure_preserves_acquired_custody`
- Agent `tests/core/execution/test_custody_broker.py:2137` — `test_no_authority_post_absence_uses_production_census_and_retains_pending_evidence`
- Agent `tests/core/execution/test_custody_broker.py:2167` — `test_post_absence_revalidates_fresh_actor_root_and_ancestry`
- Agent `tests/core/execution/test_custody_broker.py:2206` — `test_post_absence_rejects_precise_precondition_and_acquisition_errors`
- Agent `tests/core/execution/test_custody_broker.py:2232` — `test_post_absence_preserves_reparented_admitted_child_and_outer_obligation`
- Agent `tests/core/execution/test_custody_broker.py:2258` — `test_reference_verification_uses_real_independent_authority_without_writes`
- Agent `tests/core/execution/test_custody_broker.py:2273` — `test_reference_verification_rejects_changed_binding_and_kernel_identity`
- Agent `tests/core/execution/test_custody_broker.py:2299` — `test_reference_verification_rejects_pending_corrupt_and_lost_retained_history`
- Agent `tests/core/execution/test_custody_broker.py:2318` — `test_reference_verification_does_not_ignore_retained_designation_drift`
- Agent `tests/core/execution/test_custody_broker.py:2353` — `test_post_token_terminal_candidate_keeps_zero_authority_and_original_ancestry`
- Agent `tests/core/execution/test_custody_broker.py:2374` — `test_post_token_terminal_candidate_rejects_identity_or_authority_drift`
- Agent `tests/core/execution/test_custody_broker.py:2397` — `test_post_token_absence_preserves_fail_closed_reconciliation`
- Agent `tests/core/execution/test_custody_broker.py:2444` — `test_failed_candidate_diagnostics_bypass_saturated_history_and_preserve_redaction`
- Agent `tests/core/execution/test_custody_broker.py:2463` — `test_failed_candidate_command_metadata_identity_mismatch_remains_unproved`
- Agent `tests/core/execution/test_custody_broker.py:2478` — `test_failed_candidate_unavailable_or_vanished_command_metadata_never_changes_failure`
- Agent `tests/core/execution/test_custody_broker.py:2486` — `test_failed_candidate_metadata_io_occurs_only_after_immediate_native_post`
- Agent `tests/core/execution/test_custody_broker.py:2511` — `test_failed_candidate_optional_observer_exception_cannot_mask_original_capture`
- Agent `tests/core/execution/test_custody_broker.py:2526` — `test_optional_failure_metadata_attachment_preserves_original_capture_and_journal`
- Agent `tests/core/execution/test_custody_broker.py:2540` — `test_mandatory_failure_journal_error_retains_original_capture_chain_and_uncertainty`
- Agent `tests/core/execution/test_custody_broker.py:2575` — `test_historical_tombstone_does_not_chase_continuous_new_live_children`
- Agent `tests/core/execution/test_custody_broker.py:2595` — `test_new_absence_is_finalized_before_fresh_live_child_without_fixed_point_chase`
- Agent `tests/core/execution/test_custody_broker.py:2619` — `test_genuinely_new_absence_every_round_still_exhausts_same_bound_and_stays_sticky`
- Agent `tests/core/execution/test_custody_broker.py:2639` — `test_command_inventory_stream_consumes_exact_frames_without_coalescing`
- Agent `tests/core/execution/test_custody_broker.py:2658` — `test_command_inventory_rejects_bound_operation_before_helper_spawn`
- Agent `tests/core/execution/test_custody_broker.py:2693` — `test_command_inventory_canonical_peer_predicate_rejects_foreign_root`
- Agent `tests/core/execution/test_custody_broker.py:2706` — `test_command_inventory_final_close_never_clears_unresolved_operations`
- Agent `tests/core/execution/test_custody_broker.py:2718` — `test_command_inventory_client_rejects_stale_reply_and_latches_transport`
- Agent `tests/core/execution/test_custody_broker.py:2738` — `test_command_inventory_execute_retains_original_helper_on_each_failure`
- Agent `tests/core/execution/test_custody_broker.py:2802` — `test_command_inventory_owner_channel_end_never_erases_non_eof_failure`
- Agent `tests/core/execution/test_custody_broker.py:2829` — `test_command_inventory_rejects_every_unsupported_environment_delta`
- Agent `tests/core/execution/test_custody_broker.py:2841` — `test_command_inventory_binds_multiple_pack_subpaths_operation_specifically`
- Agent `tests/core/execution/test_custody_broker.py:2861` — `test_command_inventory_client_endpoint_is_noninheritable_and_root_bound`
- Agent `tests/core/execution/test_custody_broker.py:2884` — `test_command_inventory_first_failure_retains_primary_chain_without_secret_values`
- Agent `tests/core/execution/test_custody_broker.py:2912` — `test_command_inventory_actual_request_validation_journals_first_failure_before_spawn`
- Agent `tests/core/execution/test_custody_broker.py:2962` — `test_command_inventory_reply_failure_is_bound_to_completed_original_operation`
- Agent `tests/core/execution/test_custody_broker.py:2980` — `test_capture_substage_terminal_with_clean_release_retains_zero_authority`
- Agent `tests/core/execution/test_custody_broker.py:3011` — `test_capture_substage_release_or_identity_failure_stays_sticky`
- Agent `tests/core/execution/test_custody_broker.py:3029` — `test_real_owned_terminal_capture_substage_releases_mach_port`
- Agent `tests/core/execution/test_custody_broker.py:3172` — `test_one_same_transaction_live_capture_retry_never_defers_history`
- Agent `tests/core/execution/test_custody_broker.py:3233` — `test_real_owned_live_capture_retry_uses_actual_native_token`
- Agent `tests/core/execution/test_custody_broker.py:3383` — `test_live_capture_retry_rejects_every_unqualified_boundary`
- Agent `tests/core/execution/test_custody_broker.py:3476` — `test_prospective_command_descendant_anchors_before_initial_capture_and_refreshes_at_signal`
- Agent `tests/core/execution/test_custody_broker.py:3497` — `test_prospective_original_capture_rejects_same_wall_birth_different_monotonic_start`
- Agent `tests/core/execution/test_custody_broker.py:3507` — `test_prospective_optional_target_gone_keeps_original_fixed_capability`
- Agent `tests/core/execution/test_custody_broker.py:3527` — `test_prospective_authority_failures_are_not_target_declines`
- Agent `tests/core/execution/test_custody_broker.py:3547` — `test_real_owned_ordinary_descendant_exec_refreshes_retained_anchor`
- Agent `tests/core/execution/test_custody_broker.py:3652` — `test_ordinary_signal_consumes_only_pre_mutation_target_gone_without_settling_custody`
- Agent `tests/core/execution/test_custody_broker.py:3679` — `test_target_gone_marker_does_not_settle_nonordinary_consumers`
- Agent `tests/core/execution/test_custody_broker.py:3695` — `test_ordinary_signal_never_consumes_exited_from_authority_or_later_phases`
- Agent `tests/core/execution/test_custody_broker.py:3738` — `test_consumed_target_gone_still_rejects_present_or_reused_final_census`
- Agent `tests/core/execution/test_custody_broker.py:3752` — `test_consumed_target_gone_accepts_only_fresh_absent_census_without_dropping_handle`
- Agent `tests/core/execution/test_custody_broker.py:3765` — `test_real_owned_admitted_zombie_signal_observation_requires_original_reap_and_final_census`
- Agent `tests/core/execution/test_custody_broker.py:3852` — `test_first_anchored_target_capture_exit_is_precise_sibling_without_commit_or_kernel`
- Agent `tests/core/execution/test_custody_broker.py:3874` — `test_original_root_capture_exit_uses_only_bounded_original_wait`
- Agent `tests/core/execution/test_custody_broker.py:3903` — `test_capture_exit_after_definitely_unsuccessful_kernel_is_typed_retry_gone`
- Agent `tests/core/execution/test_custody_broker.py:3921` — `test_ordinary_descendant_pre_signal_exit_preserves_handle_and_final_census_obligation`
- Agent `tests/core/execution/test_custody_broker.py:3965` — `test_initial_descendant_capture_exit_requires_fresh_terminal_target`
- Agent `tests/core/execution/test_custody_broker.py:4009` — `test_command_inventory_actual_client_owner_accepts_only_macos_cf_addition`
- Agent `tests/core/execution/test_custody_broker.py:4063` — `test_command_inventory_cf_exception_never_allows_other_environment_drift`
- Agent `tests/core/execution/test_custody_broker.py:4086` — `test_name_no_port_retry_rejects_nearby_capture_errors`
- Agent `tests/core/execution/test_custody_broker.py:4112` — `test_retained_reference_deadline_bounds_a_held_cleanup_guard`
- Agent `tests/core/execution/test_custody_broker.py:4129` — `test_role_bound_signal_passes_deadline_to_first_reference`
- Agent `tests/core/execution/test_custody_broker.py:4146` — `test_reconciliation_finite_burst_settles_without_round_count_limit`
- Agent `tests/core/execution/test_custody_broker.py:4169` — `test_reconciliation_churn_cannot_reset_absolute_deadline`
- Agent `tests/core/execution/test_custody_broker.py:4193` — `test_reconciliation_expiration_at_final_boundary_cannot_succeed`
- Agent `tests/core/execution/test_custody_broker.py:4217` — `test_reconciliation_lock_wait_uses_parent_deadline_and_is_not_sticky`
- Agent `tests/core/execution/test_custody_broker.py:4230` — `test_busy_lock_is_retryable_but_an_error_inside_the_guard_still_poisons`
- Agent `tests/core/execution/test_custody_broker.py:4254` — `test_real_reconciliation_burst_and_deadline_keep_exact_custody`
- Agent `tests/core/execution/test_custody_broker.py:4400` — `test_retry_decision_records_first_refusal_without_replacing_capture_failure`
- Agent `tests/core/execution/test_custody_broker.py:4450` — `test_real_later_absence_reconciles_without_rewriting_capture_history`
- Agent `tests/core/execution/test_custody_broker.py:4585` — `test_later_native_absence_reuses_existing_reconciliation_with_all_guards`
- Agent `tests/core/execution/test_custody_broker.py:4647` — `test_later_absence_refuses_departed_parent_with_detached_grandchild`
- Agent `tests/core/execution/test_custody_broker.py:4716` — `test_retry_internal_census_keeps_every_pending_sibling`
- Agent `tests/core/execution/test_custody_broker.py:4784` — `test_internal_census_cannot_lose_child_of_missing_pending_parent`
- Agent `tests/core/execution/test_custody_broker.py:4827` — `test_handled_first_census_identity_stays_exact_without_freezing_ancestry`
- Agent `tests/core/execution/test_custody_broker.py:4856` — `test_linux_descendant_gone_before_registration_is_absent_not_a_violation`
- Agent `tests/core/execution/test_custody_broker.py:4867` — `test_linux_descendant_pid_reused_before_registration_is_absent`
- Agent `tests/core/execution/test_custody_broker.py:4877` — `test_linux_descendant_exiting_during_pidfd_bind_is_absent`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:69` — `test_tagged_null_explicit_clear_and_intermediate_equal_writes`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:81` — `test_literal_object_keys_and_json_values`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:95` — `test_bad_operands_refuse_atomically`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:102` — `test_idless_lists_are_atomic_even_when_rows_contain_an_id`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:112` — `test_ordered_insert_move_remove_and_created_claim`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:130` — `test_list_guards_and_anchors`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:144` — `test_mirrored_clips_have_one_authored_identity`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:152` — `test_shared_physical_child_edit_updates_every_owner`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:165` — `test_shot_alias_and_revision_edit_one_shared_image`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:172` — `test_ambiguous_entity_alias_refuses_and_qualified_revision_selects_one`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:203` — `test_managed_writes_refuse_before_looking_up_absent_refs`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:209` — `test_ancestor_replacement_cannot_hide_managed_edges_or_conflicting_mirrors`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:221` — `test_provider_merges_disjoint_fields_and_inverse_uses_actual_landing_head`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:234` — `test_atomic_fallback_and_explicit_atomic_refuse_disjoint_same_scope`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:244` — `test_history_aba_is_a_conflict_even_with_equal_final_value`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:254` — `test_sequential_step_reads_are_checked_and_persisted`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:273` — `test_mixed_native_capture_keeps_inherited_reads_at_original_boundaries`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:316` — `test_inherited_reads_do_not_authorize_forged_native_capture`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:333` — `test_mixed_native_inherited_reads_replay_at_landing_head`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:361` — `test_inherited_native_read_conflicts_with_later_dependency_writes`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:384` — `test_invalid_wire_shapes_are_deterministic`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:401` — `test_real_word_compiler_effects_belong_to_anchor_step_before_unrelated_note`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:416` — `test_config_ancestor_updates_required_clip_mirror`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:425` — `test_ordered_read_detects_shape_aba_and_membership_read_ignores_reorder`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:439` — `test_list_move_merges_unread_sibling_item_field`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:458` — `test_list_move_conflict_precedence`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:489` — `test_field_edit_merges_intervening_sibling_order_change`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:499` — `test_patch_after_semantic_created_root_uses_sequential_materialized_boundary`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:517` — `test_two_semantic_children_with_same_timeline_alias_refuse_atomically`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:530` — `test_rebase_follows_shared_physical_successor_for_disjoint_child_fields`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:545` — `test_rebase_requires_source_bound_materialization_and_exact_managed_edges`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:600` — `test_authenticated_successor_chain_lands_on_exact_physical_image`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:622` — `test_native_parent_mirrors_capture_one_logical_effect_and_undo_exactly`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:637` — `test_still_reachable_original_image_does_not_follow_other_owners_branch`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:652` — `test_created_ids_remain_reserved_after_patch_removal`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:665` — `test_list_inverse_restores_exact_order_and_landing_head_sibling_value`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:678` — `test_occurrence_item_replacement_preserves_managed_links`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:685` — `test_authoritative_effect_inverse_roundtrips_lists_null_and_clear`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:700` — `test_effects_store_actual_previous_value_at_landing_boundary`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:709` — `test_schema_generator_is_idempotent`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:716` — `test_object_keys_that_look_like_identity_tokens_are_literal`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:723` — `test_alias_previous_value_uses_present_logical_clips_when_one_mirror_is_absent`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:736` — `test_registry_registration_uses_only_verified_media_inputs`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:748` — `test_patch_and_native_entity_aliases_detect_equal_value_history_overlap`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:759` — `test_shot_item_replacement_records_physical_before_and_after_values`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:774` — `test_declared_qualified_scope_read_follows_authenticated_shared_successor`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:785` — `test_semantic_step_cannot_submit_provider_only_edge_effects`
- Agent `tests/editing_conformance/test_doc_patch_v2.py:795` — `test_semantic_creation_then_patch_rebases_over_unrelated_parent_field`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:27` — `test_historical_shared_exact_physical_retry_preview`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:85` — `test_historical_shared_undo_redo_retains_physical_source`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:99` — `test_historical_shared_refuses_without_writes`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:158` — `test_historical_shared_media_and_opaque_fidelity`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:180` — `test_historical_shared_destination_membership_guards`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:198` — `test_historical_shared_rejects_inconsistent_port_images`
- Agent `tests/editing_conformance/test_occurrence_shared_historical.py:231` — `test_production_session_freezes_foreign_intent_and_retries_lost_ack`

## Measured reduction inputs

- Parent comparison blocks, auth.py 2216–2224 + 2231–2239: 18 physical/nonblank lines; identical except indentation and refusal message.
- Owner enumeration blocks, auth.py 521–526 + 2451–2458: 14 physical/nonblank lines; caller-specific occurrence lookup must remain at the caller.
- App f6a21c2..860e975 changes five harness files only; none of the App paths hashed here changed.

Control `PLAN.md` SHA-256: `bdff6fbea3f6021af1f739eaff0c91650f90a17c34dccb62fb76d120eceb5075`.

Control `design/E-PLAN.md` SHA-256: `420e7c1975cae70610ec2e827c204aab14af0b326528f6e9b24c7d75a6fae8aa`.

Control `design/BOARD-HEADER.md` SHA-256: `790cf239dbe917ee5264c9aa9defc093c655733664c5126c6a2b8307f82c57bf`.

Control `design/runtime-E3-custody-audit-1956.md` SHA-256: `3d71eb38e2d4b44deb9c802c08692eda779f29efe4b4950c7763b6e4f9c2d60b`.
