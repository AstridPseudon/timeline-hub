## Report

Audit-only follow-through completed. No product, test, guard, registry, profile, manifest, or benchmark files changed.

Terminal full evidence:

- Run `agent-full-post-g5-2225-1023222822-25691`
- `17,159 passed, 262 failed, 5 errors, 4 skipped`
- No retry or original-body rerun.
- Agent tree `50689a...`, parent `c36ca8...`; Runtime `8ea0766...`, tree `6047ac...`.
- Before/after source manifests byte-equal: Agent `a2859d...`, Runtime `a55c54...`.
- Origins and profile unchanged; profile manifest `ed4616...`, 23,108 entries.
- Worktree clean; `git diff --check` passed.

Targeted command, with pinned Runtime and normal pytest lanes, resulted in `189 passed, 1 deselected, 9 failed, 14 subtests passed`. The 23 guard and 2 lane tests pass when `PYTEST_PLUGINS` is unset.

## Bounded node map

All failures are `phase=call`.

- Cause: inherited full-runner plugin environment. Owner: central test harness. Smallest fix: nested pytest subprocesses must unset `PYTEST_PLUGINS` or preserve the harness directory in `PYTHONPATH`.

  `tests/test_skip_guard.py` nodes: `test_an_undeclared_skip_in_a_test_body_fails_the_run`, `test_an_undeclared_skipif_mark_fails_the_run`, `test_an_importorskip_in_a_test_body_fails_the_run`, `test_a_module_level_importorskip_fails_the_run`, `test_a_skip_that_pretends_to_be_declared_fails_the_run`, `test_a_copied_reason_on_an_unregistered_node_fails_the_run`, `test_a_declared_reason_must_match_the_registry_exactly`, `test_an_xfail_fails_the_run`, `test_a_declared_platform_skip_passes_and_is_listed_by_test_id`, `test_a_declared_dependency_skip_passes_where_no_job_provides_it_and_is_listed`, `test_a_missing_dependency_fails_in_the_job_that_is_meant_to_provide_it`, `test_a_missing_dependency_fails_in_a_lane_the_run_selected_by_name`, `test_a_test_in_several_lanes_is_one_declared_skip_where_one_of_them_does_not_hold`, `test_an_unregistered_marker_is_an_error_under_strict_markers`, `test_a_run_in_which_every_test_is_skipped_or_deselected_fails`, `test_a_module_of_a_deselected_lane_is_not_imported_unless_a_test_in_it_names_a_selected_lane`, `test_tests_deselected_by_a_lane_are_named_under_a_header_that_says_who_runs_the_lane`, `test_a_module_not_imported_because_of_its_lane_is_named_with_the_lane`, `test_a_run_with_nothing_left_out_prints_no_report`, `test_a_module_with_a_module_lane_and_one_per_test_lane_is_imported_when_its_other_tests_are_selected`, `test_a_test_removed_by_name_is_counted_and_not_attributed_to_its_lane`, `test_a_test_in_two_lanes_is_attributed_only_to_the_lane_that_makes_the_expression_false`, `test_a_module_the_run_never_asked_for_is_not_reported_as_not_imported`.

  `tests/test_lanes.py`: `test_a_module_of_a_lane_the_run_deselects_is_not_imported_and_fails_in_the_run_that_selects_it`, `test_a_missing_runtime_is_not_looked_for_in_the_default_lane_and_fails_in_the_integration_lane`.

- Cause: `python -I` ignores the supplied `PYTHONPATH`, causing `ModuleNotFoundError: astrid`. Owner: reshape/doctor smoke-test owner. Smallest fix: make the isolated smoke invocation use an importable installed package or equivalent isolated wheel path.

  `tests/reshape/test_doctor_contract_shapes.py`: `test_smoke_doctor_lane_accepts_both_payload_shapes[observed-with-ok]`, `[observed-without-ok]`.

- Cause: checked-in CLI surface still describes pre-G5 `publish`, `--native`, and legacy edit routes. Owner: later CLI manifest regeneration task. Smallest fix: regenerate through `python scripts/gen_cli_surface.py`; do not hand-edit now.

  `tests/test_artifact_manifest.py`: `test_cli_surface_is_current`, `test_planted_cli_surface_drift_is_named`.

  `tests/test_cli_surface_conformance.py`: `test_gateway_help_matches_every_exported_family_and_verb`.

- Cause: assertions still expect retired `publish`; current parser intentionally exposes `commit`. Owner: G5 CLI census/migration task. Smallest fix: update expected command tuples to the current supported workflow.

  `tests/test_canonical_aliases.py`: `test_product_timeline_parser_exposes_only_the_supported_verbs`, `test_product_timeline_parser_has_no_obsolete_aliases`.

  `tests/v10/test_domain_cli_projects_timelines.py`: `test_timelines_parser_has_visualize_and_no_aliases`.

- Cause: rationale documents 4,043 lines for `astrid/packs/timeline/cli.py`; current source has 3,978, exceeding the 50-line tolerance by 15. Owner: structure/docs inventory owner. Smallest fix: refresh that single rationale count.

  `tests/test_structure_contracts.py`: `test_giant_file_inventory_matches_rationale`.

## Exact checks

- `scripts/gen_cli_surface.py --check`: failed with the eight expected G5 drift paths.
- `git diff --check`: passed.
- No full suite requested.
- Commit message written to the assigned path; `DONE` marker created.