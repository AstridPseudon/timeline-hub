# D108/D69 original metric custody

Status: `EXACTMISSING` for the complete per-function/assertion membership.
This is a custody record, not a recomputation or semantic review.

## Authentic origin

The parser below is the exact Python command body that produced the requested
`changed=129 / removed_assert_fp=113 / added_assert_fp=287` Agent record,
recovered from the original reverse-audit worker log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-reverse-audit-0645/log.txt`

The command appears at log lines 6725–6741 (the `exec` record beginning with
`python - <<'PY'`); the output appears immediately after it. The original
parser file was not retained separately. `original-parser-source.py` is the
source-only recovery of that command body; its SHA-256 is recorded in
`input-hashes.sha256` as the recovered-source hash, not as a claim that an
original standalone file existed.

The parser's source identity is exact D108 tuple versus approved upstream:

| repo | current ref | approved upstream ref |
|---|---|---|
| Agent | `d6294843286c18e57af3c1874cf1996be42212d2` | `08e6b9051` |
| Runtime | `1daca2a33f6d7b10053e07c539a54843e3984e19` | `d4f496ec4` |

It reads the retained manifest's Python `source_upstream_blobs`, loads fresh
upstream and captured tuple source with `git show`, parses with Python `ast`,
hashes complete test-function source, fingerprints assertion expressions via
`ast.dump(..., include_attributes=False)`, and compares `Eq`/`In` operators
plus decorator-name counts. No modules, providers, tests, or live requests
were run by the original audit.

## Precisely surviving metric output

The original command output retained these exact aggregate records:

```text
agent up 2536 applied 4893 missing 104 added 2461 changed 129 removed_assert_fp 113 added_assert_fp 287 Eq_dec 3 In_inc 17 skip_add 0 xfail_add 0 param_drop 0
runtime up 525 applied 1494 missing 10 added 979 changed 113 removed_assert_fp 72 added_assert_fp 205 Eq_dec 5 In_inc 3 skip_add 0 xfail_add 0 param_drop 0
```

The worker also retained a separate, earlier direct-tuple parser output with
`113 removed / 289 added` for Agent and `72 removed / 205 added` for Runtime;
that distinct record is not substituted for the manifest-backed totals above.
These authored historical records are not recomputed or reconciled here.

The only surviving per-function membership-like data is the first 20 removed
assertion examples printed by that separate direct-tuple pass. They are
preserved below as provenance, not as the complete membership for the
129/113/287 result:

### Agent

```text
tests/sdk/test_coverage_empty_cut.py:test_a_declared_fade_in_is_a_dip_not_a_gap(-1/+1)
tests/sdk/test_host_bootstrap_source_identity.py:test_bootstrap_passes_inventory_identity_and_restarts_on_change(-3/+6)
tests/test_capability_ledger.py:test_shipped_ledger_reconciles_historical_capability_sets(-2/+2)
tests/core/test_timeline_element_publication.py:test_sameclip_exacthead_publication_preserves_closure_and_user_params(-11/+18)
tests/v10/test_domain_cli_projects_timelines.py:test_timelines_list_and_recover_are_one_sdk_call(-1/+4)
tests/packs/timeline/test_verbs_working_copy.py:test_draft_flow_checkout_edit_status_discard(-2/+4)
tests/test_installer_platforms.py:test_windows_task_settings_and_no_console_executable(-3/+1)
tests/core/timeline/test_clip_fields.py:test_render_status_defaults_to_pinned_union_composition(-1/+1)
tests/stage1/test_capability_parity_gate_luna.py:test_stage1_capability_parity_is_explicit_and_family_proven(-1/+1)
tests/stage1/test_vendored_workspace_client_parity_luna.py:test_vendored_client_is_the_locked_runtime_artifact(-1/+1)
tests/stage1/test_runtime_client_cutover.py:test_documented_project_cli_mutations_return_committed_receipts(-1/+4)
tests/timeline/test_authoring_feedback.py:test_document_publish_stdout_and_durable_receipt_contain_shared_feedback(-2/+4)
tests/v10/test_domain_cli_projects_timelines.py:test_timelines_parser_has_visualize_and_no_aliases(-2/+2)
tests/core/test_timeline_element_publication.py:test_stale_head_and_concurrent_cas_reject_without_rebase(-2/+2)
tests/sdk/test_timeline_script.py:test_runtime_pin_flow_returns_old_script_after_binding_rebind(-1/+4)
tests/packs/rendering/test_timeline_visualize_motion_views.py:test_visualize_prints_page_counts_timing_and_next_commands(-1/+2)
tests/packs/rendering/test_live_scene_composition.py:test_layer_materialization_retains_null_window_support_rejection(-1/+1)
tests/packs/rendering/test_live_scene_composition.py:test_service_layered_plan_native_renderer_isolates_and_adjusts_once(-2/+7)
tests/sdk/test_coverage_empty_cut.py:test_a_deliberate_hold_waives_an_empty_cut(-2/+1)
tests/stage1/test_cold_launch_autobootstrap.py:test_source_profile_provisions_explicit_render_runtime(-1/+1)
```

### Runtime

```text
tests/test_visual_seam_admission.py:test_publication_and_render_preserve_uncovered_child_with_advisory_report(-1/+1)
tests/test_shot_composition_runtime.py:test_stale_publication_rolls_back_and_retry_conflicts(-2/+9)
tests/test_shot_composition_runtime.py:test_parent_composition_history_paginates_and_restores_exact_closure_over_http(-2/+11)
tests/test_timeline_render_publication.py:test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart(-3/+22)
tests/test_canonical_render_admission.py:test_unsafe_occurrence_seam_is_advisory_and_materialized_for_render(-2/+2)
tests/test_spec_reference.py:test_parent_receipt_compaction_preserves_publication_integrity(-1/+17)
tests/test_shot_composition_runtime.py:test_stale_head_conflict_carries_machine_readable_reason_over_http(-4/+7)
tests/test_runtime_domains.py:test_generated_python_client_exercises_versioned_domains_on_real_daemon(-3/+0)
tests/test_shot_composition_runtime.py:test_failure_injection_rolls_back_every_publication_write(-3/+12)
tests/test_timeline_render_publication.py:test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence(-4/+5)
tests/test_canonical_render_admission.py:test_canonical_conflicting_populated_clip_lists_fail_closed(-1/+2)
tests/test_spec_dedup.py:test_offline_migration_and_compaction_of_duplicate_render_specs(-2/+2)
tests/test_platform.py:test_linux_proc_identity_parser_uses_stat_and_brackets_start_tick(-2/+2)
tests/test_timeline_native_inspection.py:test_markdown_png_custody_and_dedup(-2/+8)
tests/test_shot_composition_runtime.py:test_parent_composition_restore_preserves_payload_and_declared_media_dependency_closure(-2/+2)
tests/test_visual_seam_admission.py:test_publication_rejects_unsafe_resolved_child_without_partial_rows(-2/+2)
tests/test_timeline_render_publication.py:test_publication_is_fenced_atomic_and_exactly_replayable(-11/+22)
tests/test_shot_composition_runtime.py:test_lost_response_replay_returns_original_head_after_a_newer_publish(-4/+13)
tests/test_shot_composition_runtime.py:test_same_head_concurrent_publishers_have_one_winner(-2/+14)
tests/test_shot_composition_runtime.py:test_parent_composition_restore_uses_selected_admission_integrity_budget(-3/+3)
```

The complete set of assertion-expression fingerprints, all function keys, and
the exact parser stdout membership were not emitted into a durable artifact.
They cannot be reconstructed authoritatively without a new audit/recomputation,
which this task forbids. No equivalence is inferred from the current source.

## Retained tool sizes

The original reverse-audit log is 1,980,538 bytes. The retained published
manifest is 461,196 bytes; the initial-mechanical and applied-manifest reports
are 7,138 and 10,314 bytes respectively. Their SHA-256 values, plus the
recovered parser-source hash, are in `input-hashes.sha256`.
