"""D108 source-only citation crosswalk.

This script reads git objects and the durable D108 source manifest.  It never
imports project modules and never executes tests or product code.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
EVIDENCE = ORCH / "workers/rt-F-D108-python-citations-0700/evidence"
MANIFEST_PATH = ORCH / "workers/rt-F-D108-rehearsal-source-0645/evidence/d108-source-rehearsal-manifest.json"
AGENT_REPO = Path("/home/user/peteromallet/astrid-agent")
RUNTIME_REPO = Path("/home/user/banodoco/banodoco-workspace-runtime")

AGENT_UP = "08e6b905114a3ee2b05c3e7980421f26b4abf15c"
AGENT_CAP = "d6294843286c18e57af3c1874cf1996be42212d2"
RUNTIME_UP = "d4f496ec4fbcae7a1f3a51d47ed5147c561117ad"
RUNTIME_CAP = "1daca2a33f6d7b10053e07c539a54843e3984e19"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)
    return result.stdout


def show(repo: Path, ref: str, path: str) -> str | None:
    result = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{path}"], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def blob(repo: Path, ref: str, path: str) -> str | None:
    result = subprocess.run(["git", "-C", str(repo), "rev-parse", f"{ref}:{path}"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def functions(source: str | None) -> dict[str, tuple[ast.AST, str]]:
    if source is None:
        return {}
    tree = ast.parse(source)
    result: dict[str, tuple[ast.AST, str]] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            result[node.name] = (node, ast.get_source_segment(source, node) or "")
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith("test"):
                    result[f"{node.name}::{child.name}"] = (child, ast.get_source_segment(source, child) or "")
    return result


def body_hash(repo: Path, ref: str, path: str, name: str) -> str | None:
    source = show(repo, ref, path)
    item = functions(source).get(name)
    if item is None:
        return None
    return hashlib.sha256(item[1].encode()).hexdigest()


def source_record(repo_name: str, path: str, manifest: dict) -> dict:
    repo = AGENT_REPO if repo_name == "Agent" else RUNTIME_REPO
    captured_ref = AGENT_CAP if repo_name == "Agent" else RUNTIME_CAP
    upstream_ref = AGENT_UP if repo_name == "Agent" else RUNTIME_UP
    entry = next((x for x in manifest["repositories"][repo_name.lower()]["source_upstream_blobs"] if x["path"] == path), None)
    if entry is None:
        # An unchanged approved-upstream replacement is intentionally absent
        # from the applied patch.  Verify it directly against both refs.
        upstream_blob = blob(repo, upstream_ref, path)
        captured_blob = blob(repo, captured_ref, path)
        if upstream_blob is None or captured_blob != upstream_blob:
            raise AssertionError(f"unmanifested replacement is not unchanged upstream: {repo_name} {path}")
        return {
            "path": path,
            "status": "U",
            "captured_blob": captured_blob,
            "upstream_blob": upstream_blob,
            "captured_object_blob": captured_blob,
            "upstream_object_blob": upstream_blob,
        }
    return {
        "path": path,
        "status": entry["status"],
        "captured_blob": entry["source_blob"],
        "upstream_blob": entry["upstream_blob"],
        "captured_object_blob": blob(repo, AGENT_CAP if repo_name == "Agent" else RUNTIME_CAP, path),
        "upstream_object_blob": blob(repo, AGENT_UP if repo_name == "Agent" else RUNTIME_UP, path),
    }


def replacement(repo_name: str, path: str, name: str | None, manifest: dict) -> dict:
    repo = AGENT_REPO if repo_name == "Agent" else RUNTIME_REPO
    ref = AGENT_CAP if repo_name == "Agent" else RUNTIME_CAP
    result = source_record(repo_name, path, manifest)
    result["selector"] = f"{path}::{name}" if name else path
    result["body_sha256"] = body_hash(repo, ref, path, name) if name else None
    return result


def old_selector(repo_name: str, path: str, name: str, manifest: dict) -> dict:
    repo = AGENT_REPO if repo_name == "Agent" else RUNTIME_REPO
    up = AGENT_UP if repo_name == "Agent" else RUNTIME_UP
    cap = AGENT_CAP if repo_name == "Agent" else RUNTIME_CAP
    record = source_record(repo_name, path, manifest)
    return {
        "selector": f"{path}::{name}",
        "path": path,
        "old_file_blob": record["upstream_blob"],
        "captured_file_blob": record["captured_blob"],
        "old_body_sha256": body_hash(repo, up, path, name),
        "captured_body_sha256": body_hash(repo, cap, path, name),
        "status": record["status"],
    }


def row(repo_name: str, path: str, name: str, replacement_specs: list[tuple[str, str | None]], decision: str,
        purpose: str, refs: str, verdict: str, manifest: dict) -> dict:
    old = old_selector(repo_name, path, name, manifest)
    reps = [replacement(repo_name, p, n, manifest) for p, n in replacement_specs]
    old["applied_replacements"] = reps
    old["decision"] = decision
    old["preserved_purpose_predicates"] = purpose
    old["approval_ledger_references"] = refs
    old["verdict"] = verdict
    return old


def agent_rows(manifest: dict) -> list[dict]:
    rows: list[dict] = []
    report = "workers/agt-m2-review-retirements/notes/report.md"
    d06 = "D06 deletion-ledger.agent.md:52; " + report + ":52-58"
    d06_replacements = {
        "test_model.py": [
            ("tests/packs/test_pack_yaml_schema.py", "test_schema_and_runtime_both_accept_current_first_party_manifests"),
            ("tests/packs/test_pack_resolver.py", "test_importlib_resolve_returns_callable"),
            ("tests/test_editor_extension_catalog.py", "test_editor_entry_discovery_rejects_paths_outside_pack"),
        ],
        "test_registry.py": [
            ("tests/packs/test_pack_discovery_v3.py", "test_external_broken_hidden_and_duplicate_roots_are_isolated"),
            ("tests/packs/test_pack_resolver.py", "test_resolve_callable_from_metadata_wraps_missing_module_contextually"),
            ("tests/test_sdk_public_surface.py", "test_discover_exposes_pack_declared_extension_metadata"),
        ],
        "test_scopes.py": [
            ("tests/packs/test_pack_discovery_v3.py", "test_layer_priority_and_managed_identity_are_preserved"),
            ("tests/packs/test_pack_layout_contract.py", "test_all_shipped_packs_discoverable"),
            ("tests/packs/test_pack_layout_contract.py", "test_no_unexpected_pack_ids_ship"),
        ],
        "test_sidecar.py": [
            ("tests/packs/test_pack_discovery_v3.py", "test_v3_loader_populates_exact_canonical_declarations_without_import"),
            ("tests/packs/test_pack_discovery.py", "PackDiscoveryTest::test_valid_pack_discovery_and_content_loaders"),
            ("tests/core/test_elements_registry.py", "ElementRegistryTest::test_element_public_surface_exports_dynamic_kind_registry"),
        ],
    }
    for path in ["tests/core/extensions/test_model.py", "tests/core/extensions/test_registry.py",
                 "tests/core/extensions/test_scopes.py", "tests/core/extensions/test_sidecar.py"]:
        old = functions(show(AGENT_REPO, AGENT_UP, path))
        key = path.rsplit("/", 1)[1]
        for name in old:
            rows.append(row("Agent", path, name, d06_replacements[key], "D06", 
                             "Old internal extension-point schema/registry/root/sidecar behavior is retired; current pack discovery, declared-manifest loading, resolver isolation, scope ordering, and public catalog surfaces remain covered.",
                             d06, "CLEARED_RETIREMENT_NO_ONE_TO_ONE", manifest))

    d05 = "D05 deletion-ledger.agent.md:51; " + report + ":60"
    inverse_reps = [
        ("tests/sdk/test_timeline_commit_provider.py", "test_legacy_history_undo_and_restore_use_revisions_or_refuse_visibly"),
        ("tests/editing_conformance/test_recipe_m1_commands.py", "test_exact_authored_move_inverse_redo"),
        ("tests/sdk/test_timeline_commit_provider.py", "test_undo_detects_aba_and_unchanged_write_publications"),
        ("tests/sdk/test_timeline_commit_provider.py", "test_inverse_rebases_only_over_proven_disjoint_new_writes"),
    ]
    path = "tests/timeline/test_inverses.py"
    for name in functions(show(AGENT_REPO, AGENT_UP, path)):
        rows.append(row("Agent", path, name, inverse_reps, "D05",
                         "Legacy event-planner inverse classification is retired; supported native move/track inverse, revision undo/restore, ABA protection, disjoint rebase, and visible refusal remain covered.",
                         d05, "CLEARED_RETIREMENT_NO_ONE_TO_ONE", manifest))

    rows.extend([
        row("Agent", "tests/packs/rendering/test_effect_registry_target.py", "test_defaults_to_the_installed_package_the_renderer_reads",
            [("tests/packs/rendering/test_effect_registry_target.py", "test_generator_targets_host_and_leaves_installed_package_unchanged")], "D10",
            "Renderer generation targets the host while leaving the installed package unchanged.", "D10 deletion-ledger.agent.md:172", "CLEARED_RENAMED", manifest),
        row("Agent", "tests/packs/rendering/test_effect_registry_target.py", "test_explicit_source_still_wins",
            [("tests/packs/rendering/test_effect_registry_target.py", "test_generator_refuses_host_staging_linked_into_installed_package")], "D10",
            "Explicit source/staging ownership and installed-package isolation remain fail-closed.", "D10 deletion-ledger.agent.md:172", "CLEARED_MIGRATED_GUARD", manifest),
        row("Agent", "tests/packs/video_editing/test_runtime_publication_chain.py", "test_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke",
            [("tests/packs/video_editing/test_runtime_publication_chain.py", "test_requester_commit_publishes_without_local_save_or_invoke")], "D13/D72",
            "Publication remains requester-owned through the canonical commit/proposal path; the retired GenericPackHost writer is not restored.", "agt-F-D69-failures-render-1646.md:18; deletion-ledger.runtime.md:D04/RT07", "CLEARED_RETIREMENT", manifest),
    ])

    cli = "agt-F-D69-failures-cli-1646.md:15-25; BOARD-HEADER D52/G5; deletion-ledger.runtime.md:D04"
    cli_map = {
        "tests/packs/timeline/test_cli_parity.py": {
            "test_publish_requires_a_message": "test_commit_requires_a_message",
        },
        "tests/packs/timeline/test_cli_status_publish.py": {
            "test_publish_forwards_key_and_force_to_sdk_once": "test_normal_commit_forwards_key_through_the_authenticated_closure",
            "test_publish_partial_narration_error_preserves_receipt_and_does_not_retry": "test_normal_commit_partial_publication_error_preserves_receipt_and_does_not_retry",
            "test_publish_human_output_is_a_short_summary_and_json_keeps_the_envelope": "test_normal_commit_output_keeps_summary_and_receipt",
            "test_publish_cas_refusal_is_not_retried_or_reported_as_success": "test_normal_commit_cas_refusal_preserves_file_and_does_not_retry",
            "test_publish_of_a_clean_working_copy_publishes_nothing": "test_normal_commit_of_a_clean_working_copy_writes_nothing",
        },
        "tests/packs/timeline/test_verbs_working_copy.py": {
            "test_publish_conflict_names_the_writer_and_offers_discard_first": "test_normal_commit_conflict_keeps_head_and_has_no_force_overwrite",
        },
    }
    for path, mapping in cli_map.items():
        for old_name, new_name in mapping.items():
            rows.append(row("Agent", path, old_name, [(path, new_name)], "D69/G5/D72",
                             "The old publish verb is retired; the current commit path preserves message/key/force refusal, receipt, output, CAS/no-retry, clean-copy, conflict, and no-force-overwrite predicates.",
                             cli, "CLEARED_RENAMED_MIGRATION", manifest))
    rows.append(row("Agent", "tests/sdk/test_runtime_response_conformance.py", "test_publish_conflict_409_maps_to_conflict_and_keeps_its_details",
                     [("tests/sdk/test_runtime_response_conformance.py", "test_commit_conflict_409_maps_to_conflict_and_keeps_its_details")], "D69/G5/D72",
                     "Conflict 409 code/details mapping remains on the canonical commit route.", "agt-F-D69-failures-sdk-1646.md:24; deletion-ledger.runtime.md:D04/RT05", "CLEARED_RENAMED_MIGRATION", manifest))

    installer_refs = "agt-F-D69-failures-render-1646.md:19; rt-D72-installer-final-review-1735.md:5-13; D72/D77 decision input"
    rows.extend([
        row("Agent", "tests/test_installer_schema.py", "test_staging_installs_the_npm_locked_schema_before_declaring_services",
            [("tests/test_installer_schema.py", "test_staging_verifies_the_local_schema_before_declaring_services")], "D72/D77",
            "Staging verifies the canonical local schema before service declaration; obsolete external package acquisition is not restored.", installer_refs, "CLEARED_MIGRATED_LOCAL_SCHEMA", manifest),
        row("Agent", "tests/test_installer_schema.py", "test_remotion_lock_pins_the_transitive_schema_package",
            [("tests/test_installer_schema.py", "test_remotion_lock_pins_the_immutable_composition_public_entry")], "D72/D77",
            "The immutable local Composition public entry is pinned as the canonical schema source; no external transitive schema package is reintroduced.", installer_refs, "CLEARED_MIGRATED_LOCAL_SCHEMA", manifest),
    ])
    core = "agt-F-D69-failures-core-1646.md:19-27; deletion-ledger.runtime.md:D04/RT02; D69/D72 core source map"
    rows.extend([
        row("Agent", "tests/timeline/test_authoring_bundle.py", "test_approval_is_bound_to_candidate_and_base_revision",
            [("tests/timeline/test_authoring_bundle.py", "test_d66_upstream_approval_is_bound_to_candidate_and_base_revision"),
             ("tests/timeline/test_authoring_bundle.py", "test_candidate_compiler_integrates_with_runtime_atomic_publication")], "D69/D72",
            "Candidate/base binding remains represented by the retained control wrapper and current Runtime atomic publication; the deleted whole-document writer is not restored.", core, "CLEARED_RETIREMENT_WITH_CONTROL", manifest),
        row("Agent", "tests/timeline/test_authoring_bundle.py", "test_frozen_render_restart_then_approval_promotion_is_single_generation",
            [("tests/timeline/test_authoring_bundle.py", "test_d66_upstream_frozen_render_restart_then_approval_promotion_is_single_generation"),
             ("tests/timeline/test_authoring_bundle.py", "test_frozen_render_restart_is_single_generation")], "D69/D72",
            "Frozen render restart/single-generation purpose remains retained; approval promotion uses the current commit boundary.", core, "CLEARED_RETIREMENT_WITH_CONTROL", manifest),
        row("Agent", "tests/v10/test_timelines_create.py", "test_remote_create_empty_creates_shell_then_empty_head",
            [("tests/v10/test_timelines_create.py", "test_d66_upstream_remote_create_empty_creates_shell_then_empty_head"),
             ("tests/v10/test_timelines_create.py", "test_remote_create_empty_creates_shell_then_native_commit")], "D69/D72",
            "Create-empty shell/head behavior is retained through the native commit path; old publish_parent_composition is retired.", core, "CLEARED_RETIREMENT_WITH_CONTROL", manifest),
    ])

    viewer_refs = "deletion-ledger.agent.md: Viewing-owned VW-DEAD-INSPECTOR block (approved a760ecca/source c1a1d4fd); exact selector mapping immediately below that block"
    viewer_map = {
        "test_viewer_state_keeps_audio_selection_playback_loop_and_text_input_safe": [
            ("tests/packs/rendering/test_inspector_navigation.py", "test_audio_targets_are_unique_and_render_scoped"),
            ("tests/packs/rendering/test_inspector_navigation.py", "test_frame_focus_command_preserves_exact_integer_frame"),
        ],
        "test_rendered_viewer_contains_audio_controls_and_media_clock_fallback": [
            ("tests/packs/rendering/test_timeline_filmstrip_cards.py", "test_pack_keeps_audio_navigation_in_rich_result_index"),
            ("tests/packs/rendering/test_timeline_filmstrip_execution.py", "test_execution_delivers_audio_sidecar_optional_media_and_reuses_cache"),
        ],
        "test_card_helpers_surface_only_declared_audio_and_frozen_speech_metadata": [
            ("tests/packs/rendering/test_timeline_filmstrip_cards.py", "test_frame_captions_use_only_explicit_timed_speech"),
            ("tests/packs/rendering/test_timeline_filmstrip_cards.py", "test_pack_keeps_audio_navigation_in_rich_result_index"),
        ],
        "test_rendered_viewer_contains_filmstrip_hierarchy_and_truthful_card_cues": [
            ("tests/packs/rendering/test_timeline_filmstrip_cards.py", "test_pack_uses_rendered_frames_without_html_artifact"),
            ("tests/packs/rendering/test_timeline_filmstrip_execution.py", "test_paired_surface_omits_empty_lanes_but_preserves_canonical_track_metadata"),
        ],
        "test_browser_viewer_seeks_frame_target_from_frame_number_and_shot_filter": [
            ("tests/packs/rendering/test_inspector_navigation.py", "test_frame_focus_command_preserves_exact_integer_frame"),
            ("tests/packs/rendering/test_timeline_filmstrip_execution.py", "test_managed_coverage_keeps_exact_frame_in_frozen_range"),
            ("tests/packs/rendering/test_timeline_filmstrip_cards.py", "test_input_navigation_keeps_track_occurrences_distinct_and_copyable"),
        ],
    }
    viewer_path = "tests/packs/rendering/test_timeline_inspector_viewer.py"
    for name, reps in viewer_map.items():
        rows.append(row("Agent", viewer_path, name, reps, "VW-DEAD-INSPECTOR",
                         "Audio/navigation, exact-frame focus, frozen speech metadata, filmstrip hierarchy, truthful card cues, and occurrence-scoped navigation remain on the supported inspector/filmstrip surface.", viewer_refs, "CLEARED_APPROVED_RETIREMENT", manifest))

    d07_refs = "agent-review-d07-current.md:18-37; deletion-ledger.agent.md:53 (broad retirement does not override this explicit current review)"
    d07_reps = {
        "test_ripple_is_track_scoped_and_never_moves_audio": [
            ("tests/packs/timeline/test_cli_edit_flags.py", "test_insert_time_moves_everything_after_it_later"),
            ("tests/sdk/test_timeline_checkout.py", "test_close_gap_before_a_word_ripples_everything_after"),
        ],
        "test_canonical_source_trim_speed_move_and_retime_intervals": [
            ("tests/editing_conformance/test_recipe_m2_clip_trim.py", "test_trim_hold_is_source_time_and_playback_duration_applies_speed"),
            ("tests/editing_conformance/test_recipe_m1_commands.py", "test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation"),
            ("tests/editing_conformance/test_recipe_m2_clip_trim.py", "test_rational_fps_source_contact_and_half_open_intervals_are_not_requantized"),
        ],
        "test_ripple_shifts_canonical_intervals_without_touching_audio": [
            ("tests/sdk/test_timeline_media_verbs.py", "test_trim_slip_and_move_keep_the_window_equal_to_the_hold"),
            ("tests/editing_conformance/test_recipe_m1_commands.py", "test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation"),
        ],
    }
    edit_path = "tests/test_timeline_editing_helpers.py"
    for name, reps in d07_reps.items():
        rows.append(row("Agent", edit_path, name, reps, "D07",
                         "The old positive timing predicate is not fully re-proven by the named current tests; source-specific review requires a native/compiler replacement preserving the combined retime/ripple/audio/window assertions.", d07_refs, "RESTORE_NEEDED_APPROVAL_GAP", manifest))
    return rows


def runtime_rows(manifest: dict) -> list[dict]:
    prior_path = ORCH / "workers/rt-U1-D69-test-audit-1603/evidence/audit-classification.json"
    prior = json.loads(prior_path.read_text())
    refs = "workers/rt-U1-D69-test-audit-1603/evidence/audit-classification.json (reused only after exact function-body equality); workers/rt-m2-keep-split-live/report.md:7-18; deletion-ledger.runtime.md:D04/RK01/RK02/RT02/RT03/RT09"
    rows: list[dict] = []
    def add(path: str, old: str, reps: list[tuple[str, str]], purpose: str, verdict: str) -> None:
        item = row("Runtime", path, old, reps, "D69/D72/RK/RT", purpose, refs, verdict, manifest)
        prior_item = next((x for x in prior["missing"] if x["path"] == path and x["qualifiedname"] == old), None)
        if prior_item is None:
            # This selector is covered by the durable split-source handoff,
            # not the prior D69 JSON map.  Do not pretend it was reused.
            assert path == "tests/test_runtime_exact_idempotency.py"
            item["prior_d69_old_body_sha256"] = None
            item["prior_d69_source_file_sha256"] = None
            item["prior_d69_mapped_body_sha256"] = []
            item["prior_d69_exact_function_body_map"] = "not_applicable_split_source_map"
        else:
            assert prior_item["bodyhash"] == item["old_body_sha256"], (path, old)
            item["prior_d69_old_body_sha256"] = prior_item["bodyhash"]
            item["prior_d69_source_file_sha256"] = prior_item["sourcehash"]
            item["prior_d69_mapped_body_sha256"] = [x["bodyhash"] for x in prior_item["mapped_to"]]
            item["prior_d69_exact_function_body_map"] = all(
                x["body_sha256"] == prior_hash
                for x, prior_hash in zip(item["applied_replacements"], item["prior_d69_mapped_body_sha256"])
            )
            assert item["prior_d69_exact_function_body_map"], (path, old)
        rows.append(item)
    add("tests/test_canonical_render_admission.py", "test_canonical_stale_head_rejected_when_legacy_version_is_unchanged",
        [("tests/test_canonical_render_admission.py", "test_canonical_stale_head_rejected_with_current_metadata_version")],
        "Stale-head refusal preserves current metadata/version admission and no-write semantics; only the legacy-version label was renamed.", "CLEARED_EXACT_FUNCTION_EQUIVALENCE")
    add("tests/test_runtime_domains.py", "test_generated_domains_preserve_project_media_and_timeline_recovery",
        [("tests/test_runtime_domains.py", "test_generated_domains_preserve_project_media_and_task_listing"),
         ("tests/test_runtime_domains.py", "test_generated_historical_timeline_recover_refuses_before_writes")],
        "Project/media/task catalog coverage remains live while historical timeline recovery remains an explicit refusal before writes.", "CLEARED_EXACT_SPLIT_EQUIVALENCE")
    add("tests/test_runtime_domains.py", "test_project_media_mutations_roll_back_before_idempotency_replay",
        [("tests/test_runtime_domains.py", "test_project_reference_mutations_roll_back_before_idempotency_replay"),
         ("tests/test_runtime_domains.py", "test_project_shot_mutations_roll_back_before_idempotency_replay")],
        "Rollback-before-replay is preserved for the retained project reference and project shot catalog halves; film timeline direct writers remain retired.", "CLEARED_EXACT_SPLIT_EQUIVALENCE")
    add("tests/test_runtime_e2e.py", "test_project_shot_reference_crud_isolated_idempotent_and_restart_durable",
        [("tests/test_runtime_e2e.py", "test_project_shot_crud_isolated_idempotent_and_restart_durable"),
         ("tests/test_runtime_e2e.py", "test_project_reference_crud_isolated_idempotent_and_restart_durable")],
        "Shot and reference catalog CRUD retain isolation, idempotency, and restart durability as separate project-scoped operations.", "CLEARED_EXACT_SPLIT_EQUIVALENCE")
    add("tests/test_runtime_exact_idempotency.py", "test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting",
        [("tests/test_runtime_exact_idempotency.py", "test_project_reference_creation_is_keyed_durable_and_non_overwriting")],
        "The project reference half remains a keyed durable/non-overwriting catalog positive; the old timeline/film shot half is retired under RT02 and is not claimed as live coverage.", "CLEARED_SPLIT_WITH_RETIRED_FILM_HALF")
    add("tests/test_runtime_p1_blockers.py", "test_project_updates_require_idempotency_keys_at_service_boundary",
        [("tests/test_runtime_p1_blockers.py", "test_project_reference_updates_require_idempotency_keys_at_service_boundary"),
         ("tests/test_runtime_p1_blockers.py", "test_project_shot_updates_require_idempotency_keys_at_service_boundary")],
        "Service-boundary idempotency-key requirements remain for the retained reference and shot catalog operations; no direct film writer is restored.", "CLEARED_EXACT_SPLIT_EQUIVALENCE")
    add("tests/test_shot_composition_contract.py", "test_materialized_canonical_timeline_schema_is_the_nested_runtime_contract",
        [("tests/test_shot_composition_contract.py", "test_pinned_compiled_timeline_schema_remains_strict")],
        "The pinned compiled timeline schema remains strict at the canonical nested contract boundary.", "CLEARED_EXACT_FUNCTION_EQUIVALENCE")
    add("tests/test_shot_composition_contract.py", "test_materialized_timeline_schema_provenance_tracks_role_extension_and_nested_hashes",
        [("tests/test_shot_composition_contract.py", "test_materialized_timeline_schema_provenance_and_compatible_raw_field_reuse")],
        "Materialization provenance, role extension, nested hashes, and compatible raw-field reuse remain asserted.", "CLEARED_EXACT_FUNCTION_EQUIVALENCE")
    add("tests/test_shot_composition_contract.py", "test_schema_declares_two_owner_boundary_without_a_second_timeline_schema",
        [("tests/test_shot_composition_contract.py", "test_schema_declares_raw_container_boundary_without_a_second_compiled_schema")],
        "The two-owner/raw-container boundary remains explicit without introducing a second compiled timeline schema.", "CLEARED_EXACT_FUNCTION_EQUIVALENCE")
    add("tests/test_spec_reference.py", "test_working_copy_uses_cas_and_requires_its_saved_base_at_claim",
        [("tests/test_spec_reference.py", "test_working_copy_without_candidate_is_admitted_uncertified_and_requires_its_saved_base")],
        "Working-copy admission remains CAS/base-bound and uncertified when no candidate is present.", "CLEARED_EXACT_FUNCTION_EQUIVALENCE")
    return rows


def manifest_receipts(manifest: dict) -> dict:
    result: dict[str, dict] = {}
    for repo_name, repo, cap, up in [("Agent", AGENT_REPO, AGENT_CAP, AGENT_UP), ("Runtime", RUNTIME_REPO, RUNTIME_CAP, RUNTIME_UP)]:
        entries = manifest["repositories"][repo_name.lower()]["source_upstream_blobs"]
        checked = 0
        failures = []
        for entry in entries:
            path = entry["path"]
            if entry["status"] == "A":
                actual = blob(repo, cap, path)
                expected = entry["source_blob"]
            elif entry["status"] == "D":
                actual = blob(repo, up, path)
                expected = entry["upstream_blob"]
            else:
                actual = blob(repo, cap, path)
                expected = entry["source_blob"]
            checked += 1
            if actual != expected:
                failures.append({"path": path, "status": entry["status"], "expected": expected, "actual": actual})
        result[repo_name] = {"checked": checked, "failures": failures}
    return result


def raw_missing(repo: Path, up: str, cap: str) -> list[str]:
    missing = []
    for line in git(repo, "diff", "--name-status", up, cap, "--", "*.py").splitlines():
        status, path, *_ = line.split("\t")
        old = functions(show(repo, up, path))
        new = functions(show(repo, cap, path))
        if status == "D":
            missing.extend(f"{path}::{name}" for name in old)
        elif status == "A":
            continue
        else:
            missing.extend(f"{path}::{name}" for name in old if name not in new)
    return sorted(missing)


def installer_retention(manifest: dict) -> dict:
    rows = []
    for path in ["tests/test_installer_current.py", "tests/test_installer_schema.py", "tests/test_local_install.py"]:
        src = show(AGENT_REPO, AGENT_UP, path)
        names = sorted(functions(src))
        rows.append({"path": path, "upstream_blob": blob(AGENT_REPO, AGENT_UP, path), "fresh_agent_08e6_selectors": [f"{path}::{n}" for n in names]})
    bootstrap = "tests/test_installer_bootstrap_schema.py"
    rows.append({"path": bootstrap, "captured_blob": blob(AGENT_REPO, AGENT_CAP, bootstrap), "status": "A", "purpose": "new local canonical schema bootstrap coverage"})
    return {"fresh_upstream": AGENT_UP, "cases": rows}


def d107_scope(manifest: dict) -> dict:
    path = "tests/editing_conformance/test_commit_runtime_m1.py"
    selectors = [
        "test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]",
        "test_cli_python_outbox_restart_and_guarded_inverse[touched-basis-conflict]",
        "test_keyed_view_lost_ack_restart_and_fresh_head",
        "test_keyed_view_requires_write_but_inspection_remains_read_only",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-image]",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-video]",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-image]",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-video]",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-image]",
        "test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-video]",
    ]
    replacements = [
        "tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo] (partial current foundation)",
        "tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_lost_ack_restart_and_fresh_head (partial current foundation)",
        "tests/editing_conformance/test_recipe_m2_auto_placement.py (current construction/refusal coverage)",
        "tests/sdk/test_timeline_commit_provider_runtime.py::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart (restart/inverse coverage)",
    ]
    return {
        "decision": "D107 legacy-only; current equivalent end-to-end combination is a required gap, not PASS",
        "approval_reference": "escalations/agent-20261025T0613Z-M1-legacy-bound-scope.resolved.md:4-6; design/handoff-agt-M1-scope-0610-selectors.tsv",
        "source": {"path": path, "upstream_blob": blob(AGENT_REPO, AGENT_UP, path), "captured_blob": blob(AGENT_REPO, AGENT_CAP, path)},
        "selectors": selectors,
        "current_partial_replacements": replacements,
        "verdict": "SEPARATE_LEGACY_ONLY_GAP",
    }


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    manifest_sha = hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
    agent = agent_rows(manifest)
    runtime = runtime_rows(manifest)
    raw_agent = raw_missing(AGENT_REPO, AGENT_UP, AGENT_CAP)
    raw_runtime = raw_missing(RUNTIME_REPO, RUNTIME_UP, RUNTIME_CAP)
    excluded = [
        x for x in raw_agent
        if x.startswith("tests/core/execution/test_generic_host_child_bridge_d18.py::")
        or x.startswith("tests/test_installer_windows_tasks.py::")
    ]
    # The independent audit declares 104, but its durable family table does
    # not identify one raw AST selector.  Keep that discrepancy explicit.
    assert len(agent) == 103, len(agent)
    assert len(runtime) == 10, len(runtime)
    assert len(raw_agent) == 105, len(raw_agent)
    assert len(excluded) == 2, excluded
    assert len(raw_runtime) == 10, len(raw_runtime)
    receipts = manifest_receipts(manifest)
    assert not receipts["Agent"]["failures"], receipts["Agent"]["failures"][:2]
    assert not receipts["Runtime"]["failures"], receipts["Runtime"]["failures"][:2]
    for item in agent + runtime:
        for rep in item["applied_replacements"]:
            if rep["body_sha256"] is not None:
                assert rep["captured_object_blob"] == rep["captured_blob"], rep
    data = {
        "task": "D108",
        "source_only": True,
        "manifest": {"path": str(MANIFEST_PATH), "sha256": manifest_sha, "expected_sha256": "37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504"},
        "tuple": {"Agent": {"upstream": AGENT_UP, "captured": AGENT_CAP}, "Runtime": {"upstream": RUNTIME_UP, "captured": RUNTIME_CAP}},
        "scoped_counts": {"Agent": {"mechanical_declared_missing": 104, "reconstructed_rows": len(agent), "raw_ast_missing": 105, "excluded_raw": 2, "unidentified_declared_delta": 1}, "Runtime": {"missing": 10, "raw_ast_missing": 10, "rows": len(runtime)}},
        "manifest_source_blob_receipts": receipts,
        "agent": agent,
        "runtime": runtime,
        "excluded_raw_agent_selectors": excluded,
        "installer_retention": installer_retention(manifest),
        "d107_legacy_ten": d107_scope(manifest),
        "changed_assertion_signals": {
            "Agent": {"changed_body": 129, "removed_assert_fingerprints": 113, "added_assert_fingerprints": 287, "eq_decreases": 3, "increases": 17, "added_skip_xfail": 0, "dropped_params": 0},
            "Runtime": {"changed_body": 113, "removed_assert_fingerprints": 72, "added_assert_fingerprints": 205, "eq_decreases": 5, "increases": 3, "added_skip_xfail": 0, "dropped_params": 0},
            "method": "finite counts consumed from applied-manifest-audit.md; no blanket operator clearance; no same-function == to membership pair",
        },
        "changed_assertion_verdict": "ACCOUNTED_AS_AUDIT_SIGNALS_ONLY; no assertion is cleared from operator deltas alone",
    }
    (EVIDENCE / "d108_citation_crosswalk.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    lines = [
        "# D108 source-only citation crosswalk",
        "",
        f"Manifest SHA-256: `{manifest_sha}` (expected `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`).",
        "Git-object reads and Python AST parsing only; no imports, tests, builds, renders, installs, or providers.",
        "",
        "## Finite accounting",
        "",
        "| scope | mechanical missing | raw AST missing | excluded raw selectors | cited rows | verdict |",
        "|---|---:|---:|---:|---:|---|",
        f"| Agent | 104 declared | 105 | 2 | {len(agent)} | 1 declared-map delta is unidentified; 3 D07 gaps and 5 viewer retirements are individually classified |",
        f"| Runtime | 10 | 10 | 0 | {len(runtime)} | 10 reconciled by exact relevant file/function equivalence and ledger decisions |",
        "",
        "The raw Agent walk finds 105 selectors. The durable audit declares 104, while its family table accounts for only 103 selectors after the two explicit raw exclusions below. The remaining one-selector delta is not guessed or silently cleared; the exact raw selector is listed below as an accounting discrepancy.",
        "",
        "## Crosswalk table",
        "",
        "Columns: old selector; applied replacement or approved retirement; old/captured file blobs and replacement file/body hashes; exact approval/ledger reference; preserved purpose/predicates; verdict.",
        "",
        "| repo | old selector | applied replacement(s) | source hashes | approval + ledger reference | preserved purpose/predicates | verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in agent + runtime:
        reps = "<br>".join(f"`{r['selector']}`" for r in item["applied_replacements"])
        hashes = [f"old-file={item['old_file_blob']}", f"captured-file={item['captured_file_blob']}", f"old-body={item['old_body_sha256']}"]
        for r in item["applied_replacements"]:
            hashes.append(f"replacement-file={r['captured_blob']}")
            if r["body_sha256"]:
                hashes.append(f"replacement-body={r['body_sha256']}")
        if "prior_d69_old_body_sha256" in item:
            hashes.append(f"prior-D69-old-body={item['prior_d69_old_body_sha256']}")
            hashes.append(f"prior-D69-map-exact={item['prior_d69_exact_function_body_map']}")
        lines.append("| " + " | ".join([
            "Agent" if item in agent else "Runtime",
            f"`{item['selector']}`",
            reps,
            "<br>".join(hashes),
            item["approval_ledger_references"],
            item["preserved_purpose_predicates"],
            item["verdict"],
        ]) + " |")
    lines.extend([
        "",
        "## Raw Agent selectors outside/requiring map reconciliation",
        "",
        "| selector | reason/disposition | upstream blob | captured status |",
        "|---|---|---|---|",
    ])
    for selector in excluded:
        path, name = selector.split("::", 1)
        old_blob = blob(AGENT_REPO, AGENT_UP, path)
        cap_blob = blob(AGENT_REPO, AGENT_CAP, path)
        reason = "Existing mechanical map excludes unrelated D18 scope; no D108 citation verdict assigned." if "generic_host_child_bridge_d18" in selector else "This Windows-only installer selector is the unidentified one-selector delta between the declared 104 and reconstructed 103; no approval is guessed."
        lines.append(f"| `{selector}` | {reason} | `{old_blob}` | modified, captured `{cap_blob}` |")
    lines.extend([
        "",
        "## Changed-assertion signals",
        "",
        "| repo | changed bodies | removed assertion fingerprints | added assertion fingerprints | Eq decreases | membership increases | added skip/xfail | dropped params | disposition |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
        "| Agent | 129 | 113 | 287 | 3 | 17 | 0 | 0 | accounted as finite audit signals; not cleared by operator similarity |",
        "| Runtime | 113 | 72 | 205 | 5 | 3 | 0 | 0 | accounted as finite audit signals; not cleared by operator similarity |",
        "",
        "No direct same-function `==` to membership pair was found. These counts do not authorize assertion weakening or blanket clearance; source-specific D07 remains unresolved above.",
        "The durable independent audit supplies aggregate changed-assertion counts, not a per-assertion selector map. Therefore the 113 Agent and 72 Runtime removed-fingerprint signals are fully accounted numerically but remain uncited signals; no selector is cleared from operator deltas alone.",
        "",
        "## Actual fresh Agent 08e6 installer cases",
        "",
        "Fresh-upstream selectors and blobs are in `d108_citation_crosswalk.json` under `installer_retention`; they include `tests/test_installer_current.py`, `tests/test_installer_schema.py`, and unchanged `tests/test_local_install.py`. The applied addition `tests/test_installer_bootstrap_schema.py` is recorded separately with its captured blob.",
        "",
        "## D107 legacy ten (separate scope)",
        "",
        "D107 remains `SEPARATE_LEGACY_ONLY_GAP`: all ten original M1 selectors, their upstream/captured source blobs, and partial current replacements are recorded under `d107_legacy_ten` in the JSON. The current equivalents do not reproduce the original word-bound end-to-end combination, so this is not folded into the 104/10 citation clearance and is not fabricated as PASS.",
        "",
        "## Verdict",
        "",
        "**FAIL for finite source qualification:** the 10 Runtime signals reconcile under exact current function-body/file-blob equality plus existing D69/D72/RK/RT decisions. The Agent raw AST census is 105; the audit declares 104, but the durable family table reconstructs only 103 after excluding the D18 child-bridge selector. The Windows-only installer selector is an exact unresolved count discrepancy, not an approved retirement. Five viewer selectors clear through VW-DEAD-INSPECTOR; three D07 selectors remain restore/approval gaps. Changed assertion signals are fully counted but not independently cleared. D107 legacy ten remains a separate required current-equivalent gap.",
    ])
    (EVIDENCE / "d108_citation_crosswalk.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"agent_rows": len(agent), "runtime_rows": len(runtime), "raw_agent": len(raw_agent), "excluded": excluded, "receipts": receipts, "manifest_sha256": manifest_sha}, indent=2))


if __name__ == "__main__":
    main()
