# Agent free-multi ABA / rational-FPS code repair

Implemented against `922317bd58aa4db8f7cced85b37dd96038ae17df` in the assigned worker worktree. Product code changed; no schema, fixture, repository process document, integration worktree, shared dependency, or git ref was changed. Commit is left to the harness.

## Source changes

- `astrid/sdk/timeline/rebase.py`: forward plans use the existing identity-only history check. For move-set records, an additional strict history view retains original selections, bindings, and source/structure/activity reads, while ordinary clip values are checked against the final head by the existing executor. The original plan, commands, claims, and records are never refreshed or mutated. Inverse/restore plans retain the full strict check; `inverse.py` is unchanged.
- `astrid/sdk/timeline/units.py`: extracted Main's existing mapping/list rational FPS parser into `_rational_fps`, with its original positive-integer policy.
- `astrid/sdk/timeline/_timing_evaluators.py`: calls that shared parser at the same two nested canvas locations, retaining its scalar fallback and existing default.
- `astrid/sdk/timeline/capture.py`: existing `rate()` uses the shared rational parser, retaining its scalar finite-number validation and existing default. `_move_set.py`, the common-delta computation, quantizer, and half-open overlap predicate are unchanged.
- `tests/editing_conformance/test_recipe_free_move_set.py`: forward success, genuine membership refusal, source/identity history refusal, list-rate parity, canonical quantization pin, and exact inverse coverage; all old correct assertions retained.
- `tests/sdk/test_timing_compiler.py`: shared rational validation and supported `base_parent_payload.config.theme_overrides.visual.canvas.fps` coverage. Existing nested parent mapping/list half-frame tests remain intact.

## Assertion ledger

Names below are in `tests/editing_conformance/test_recipe_free_move_set.py` unless prefixed otherwise.

| Original assertion/site | Final assertion/site |
| --- | --- |
| `test_membership_predicates_sources_and_aba_refuse_atomically[read-aba]`: single later `hold=2`, forward refusal | One-to-one correction: `test_forward_equal_value_aba_accepts_original_guards[same-value-False]` uses the same basis, other row, move, and single later `hold=2`; forward succeeds with exact original bundle, records, commands, unchanged claims and head. Its inverse still refuses with `intervening_write`. |
| Review's two later `hold=3`, `hold=2` writes | Same success test `[aba-False]` and `[aba-True]`; `[same-value-True]` also verifies same-batch V3 creation. All four retain the separate strict inverse refusal. |
| New independent negative replacing the incorrect negative's intended safety role | `test_forward_changed_membership_refuses_atomically`: a new destination blocker remains in the final head; `selection_changed`, unchanged head and plan records, no partial writes. |
| Existing membership/source/order negatives | Original `[lane-entry-aba]`, `[lane-root-aba]`, `[source]`, `[member]`, `[order]` assertions unchanged. |
| Existing activity-history negative | `test_inactive_lane_members_do_not_block_but_their_activity_is_guarded` unchanged; still `intervening_write`. |
| Additional source/identity history protection | `test_forward_source_and_identity_aba_remain_guarded[clip-root/track-root/asset/registry-source/rate]`: equal final heads still refuse root republication or source/dependency ABA atomically. |
| Existing mapping-rate assertions, all three codecs | Original `test_shared_rational_quantized_delta_preserves_windows_holds_and_opaque[at/at_ms/both]` calls a shared assertion helper containing every previous assertion, plus exact rational-derived starts and canonical dependency pin. |
| New list-rate regression | `test_shared_rational_quantized_delta_accepts_main_list_rate_spelling[at/at_ms/both]` runs those same assertions and compares exact rows, writes, dependencies, bindings, selections, and created IDs with mapping input. Starts are `1.003`, `3.003`, a common two-second translation separation. |
| Existing half-open and source/inverse tests | All four IDs of `test_half_open_destination_contacts_and_real_blockers`, plus `test_source_registry_reads_and_same_value_assignments_remain_guarded`, unchanged. |
| Existing golden, created-ID and dependent safety | Golden same-batch V3/order/opaque assertions, occupied-ID refusal, surviving-dependent refusal, two-own-stage inverse/redo, and JSON reload assertions unchanged. |
| `tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties` | Both original mapping/list IDs and every assertion unchanged. Added invalid positive-integer cases in both supported nested canvas owners and valid base-parent mapping/list cases. |

No passing behavior test was converted to refusal, skipped, deleted, or weakened. The sole incorrect refusal expectation was converted to success as explicitly requested.

## Exact test commands and results

All commands ran directly from the assigned worktree with shared dependencies used read-only. No full, 462, 173, Runtime, App, browser, live-socket, generation, pin/freeze, render, or integration suite was requested or run.

Before the product fix, the newly added focused regressions reproduced **7 failures, 1 pass**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py::test_forward_equal_value_aba_accepts_original_guards tests/editing_conformance/test_recipe_free_move_set.py::test_shared_rational_quantized_delta_accepts_main_list_rate_spelling tests/editing_conformance/test_recipe_free_move_set.py::test_forward_changed_membership_refuses_atomically
```

After the initial product fix, the then-current move-set file passed **74 tests**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py
```

Final source: **138 passed in 12.97s**. This includes every move-set test and all direct timing-compiler neighbors. An earlier run of this same command during test development was 8 failed / 130 passed: the new exact test oracle incorrectly subtracted binary floats, and the new base-parent fixture retained an unresolved word anchor. Those new test-only errors were corrected with a Fraction oracle and fixed-start fixture; no old expectation or product arithmetic was changed to resolve them.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py tests/sdk/test_timing_compiler.py
```

Schema/floor/source-bound subset: **13 passed in 3.69s**.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py::test_full_move_set_schema_is_a_new_source_descendant_of_the_84fc_floor tests/sdk/test_timeline_materialization_schema_union.py::test_private_extent_proposal_is_one_addition_on_voiceover_floor tests/sdk/test_timeline_materialization_schema_union.py::test_removing_group_and_project_data_additions_reconstructs_private_carrier_bytes tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden tests/editing_conformance/test_pristine_initialize.py::test_complete_s2_schema_is_retained_additively tests/editing_conformance/test_materialization_map.py::test_product_capture_json_recovery_and_exact_source_pin_across_stale_heads tests/editing_conformance/test_materialization_map.py::test_source_bound_batch_preserves_earlier_stages_and_strict_inverse_guards tests/editing_conformance/test_materialization_version_boundary.py::test_source_bound_v2_cannot_use_an_unverified_legacy_bundle tests/editing_conformance/test_materialization_version_boundary.py::test_complete_public_s2_v1_keeps_original_capture_records_output_and_map
```

Replay/inverse neighbors: **14 passed in 2.04s**.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec tests/editing_conformance/test_recipe_m1_commands.py::test_replay_permits_disjoint_and_equal_state_while_inverse_guards_aba tests/editing_conformance/test_recipe_m1_commands.py::test_disjoint_same_child_rebase_and_original_guards_after_materialization tests/editing_conformance/test_recipe_m1_commands.py::test_semantic_owner_refuses_actual_source_change_and_inverse_source_aba tests/editing_conformance/test_recipe_m1_commands.py::test_collection_selection_detects_structural_publications_even_when_json_returns tests/editing_conformance/test_recipe_m1_commands.py::test_member_and_container_aliases_share_overlap_for_replay_and_inverse tests/editing_conformance/test_recipe_m1_commands.py::test_staged_inverse_keeps_opaque_strings_and_refuses_all_unchanged_overlap tests/editing_conformance/test_recipe_m1_commands.py::test_overlapping_read_is_verified_at_input_and_bad_late_stage_is_atomic
```

Targeted lint: **All checks passed**. Whitespace: **exit 0**.

```sh
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/rebase.py astrid/sdk/timeline/capture.py astrid/sdk/timeline/units.py astrid/sdk/timeline/_timing_evaluators.py
git diff --check
```

Final qualification totals **165 passing tests** across those three disjoint targeted invocations. `make check` was not run because its renderer/typecheck scope exceeds this source-only brief.

## Schema and probe results

Read-only Python checks compared schema bytes directly with `git show 922317bd58aa4db8f7cced85b37dd96038ae17df:astrid/core/timeline/schema/edit-command.schema.json`: identical. Raw-file SHA-256 is `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`; the existing floor tests use `(json.dumps(schema, indent=2) + '\n').encode()`, whose SHA-256 remains `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`. Counts remain **60 definitions / 34 clauses / 12 v2 clauses**. Removing only move-set reconstructs exact `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`; other floor tests above pass. No schema file changed.

Direct probes using the review's fixture/imports/history returned:

```text
literal-review-post-edit-head REFUSED identity_collision created identity is occupied
equal-original-value-and-identity-head ACCEPTED; original records and output exact
{'numerator': 30000, 'denominator': 1001} ACCEPTED [1.003, 3.003]
[30000, 1001] ACCEPTED [1.003, 3.003]
```

**Evidence of a problem in the literal review probe:** it assigns `head = deepcopy(plan.bundle)`, which already contains the moved clips and newly created V3. That is not the captured input with an equal-value ABA; it is the result of applying the entire batch. Making that literal probe succeed would violate original guards and occupied-created-ID protection. The implementation follows the settled repair specification: use `head = deepcopy(original)` for the forward equal-input ABA; retain refusal on the already-applied result. The two review `hold` records are unchanged. This discrepancy is reported rather than bypassed in product code.

## Handoff

No implementation blocker. Recommended next step: independent source review and harness commit; correct the review probe's head fixture. Runtime/App qualification remains outside this task and is not claimed here. Commit message and DONE marker are in the assigned worker directory.
