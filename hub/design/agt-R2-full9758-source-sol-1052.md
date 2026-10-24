**Source-only classification complete; no fix.** Worktree remains clean at `c2b1f7e5a3`. Created `commit-msg` and `DONE`.

Full9758 remains **FAIL at observed tree `c13d368666e710bb911ff448b86251b516867c03`**, matching commit `ba55ac1e9e`: **231 failed, 45 errors, 17,673 passed, 4 skipped**. The six assigned files contain **60 failed nodes**. No current PASS is inferred from matching source.

**Source facts and attribution**

| Assigned file | Failed nodes | First cause in full9758 | Current source / exact later proof |
|---|---:|---|---|
| `test_provider_occurrence_fork.py` | 4 | Historical scratch payload reads use the live publication’s item codec; `shot item source changed` | d83 changes this seam. All four exact nodes passed in d83’s integrated 67-test receipt. |
| `test_captured_nested_redo.py` | 3 | Captured case: same historical codec seam. Two native-only cases: synthetic accepted boundaries lack `_runtime_document` | Codec changed; boundary requirement unchanged. Neither 67 nor 244 covers these nodes. |
| `test_inverse_owner_occurrence_order.py` | 10 | Restored occurrence is looked up in the live document where it was deleted; `missing or ambiguous identity` | d83 changes the historical read-codec seam. No exact-node proof in 67/244. Six forgery cases fail during preparatory undo, before their mutations. |
| `test_step_undo_v2.py` | 14 | Thirteen synthetic accepted-boundary cases lack `_runtime_document`; partial-deletion case lacks authenticated shot source during initial command execution | Relevant source and fixtures unchanged. No exact-node proof in 67/244. |
| `test_recipe_m1_commands.py` | 25 | Redo wraps native authoring bundles as accepted boundaries; closure compilation requires absent `_runtime_document` | Relevant requirement and fixtures unchanged. No exact-node proof in 67/244. |
| `test_recipe_m2_auto_placement.py` | 4 | Redo’s synthetic accepted-boundary wrapper lacks authenticated fork materialization evidence | Materialization validation unchanged. No exact-node proof in 67/244. |

These are **15 historical product-seam failures and 45 fixture/evidence-path failures**, with no import/setup exception among these 60. Fixture attribution does not waive the original behavior requirements or qualify those tests.

The 45 fixture failures comprise **40 `_runtime_document` KeyErrors**, **one unavailable shot source**, and **four missing materialization proofs**.

| Source | Full9758 → current | Current versus qualified d83 |
|---|---|---|
| `inverse.py` | Changed: `_input_read_state` added; both staged and direct input-read checks use it | Byte-identical, 69,027 bytes |
| `_command_state.py` | Identical | Identical, 32,620 bytes |
| `_commit_patch.py` | Changed by f91’s intermediate-root rebase correction | Identical, 69,321 bytes |
| `commit.py`, `commands.py`, `_step_undo.py`, `_doc_patch.py`, `native_occurrence_delete.py` | Identical | Identical |
| All six assigned original test files | Identical | Identical |

`inverse.py` SHA-256:

- Full9758/f91: `c1fea7c985b686e08cbe30cb90b958734d3c2aafce9f448e9952bd621b15b843`
- Reviewed source/d83/current: `41faadf389e7d42c6d43bf0013cfec7d27b87c936e5c3e6e11e6881da9d7031c`

`_validate_materializations` and `apply_inverse` retain identical function text between full9758 and current. No guard was relaxed.

**Exact failed-node inventory**

Each suffix below appends to `tests/editing_conformance/<named file>::`.

`test_provider_occurrence_fork.py` — historical codec; later exact d83 PASS:

```text
test_v2_registered_fork_reply_physical_effects_step_reads_and_undo[False]
test_v2_registered_fork_reply_physical_effects_step_reads_and_undo[True]
test_fork_and_edit_sequential_step_read_and_guarded_fork_step_undo
test_disjoint_head_merge_and_preview_keep_other_edit
```

`test_captured_nested_redo.py` — no exact-node proof in 67/244:

```text
test_captured_nested_redo_compiles_and_partitions_without_rewriting_source
test_native_only_accepted_inverse_redoes_without_effect_facts[one-of-ten-notes]
test_native_only_accepted_inverse_redoes_without_effect_facts[semantic-creation]
```

The first is historical codec; the remaining two lack `_runtime_document`.

`test_inverse_owner_occurrence_order.py` — historical codec; no exact-node proof in 67/244:

```text
test_nested_delete_recreation_keeps_exact_stage_order[False-0]
test_nested_delete_recreation_keeps_exact_stage_order[False-1]
test_nested_delete_recreation_keeps_exact_stage_order[True-0]
test_nested_delete_recreation_keeps_exact_stage_order[True-1]
test_nested_occurrence_partition_forgery_refuses_without_writes[order]
test_nested_occurrence_partition_forgery_refuses_without_writes[native-range]
test_nested_occurrence_partition_forgery_refuses_without_writes[effect-range]
test_nested_occurrence_partition_forgery_refuses_without_writes[source]
test_nested_occurrence_partition_forgery_refuses_without_writes[step]
test_nested_occurrence_partition_forgery_refuses_without_writes[ordinal]
```

`test_step_undo_v2.py` — no exact-node proof in 67/244:

```text
test_aba_tail_refuses_even_when_the_current_guard_matches
test_disjoint_later_commit_survives_and_inverse_uses_actual_landing_head
test_gap_before_newer_target_is_its_input_but_not_earlier_targets_tail
test_step_patch_is_never_executed_as_inverse_instructions
test_semantic_creation_reversal_preserves_unselected_root_and_redoes
test_partial_semantic_deletion_restores_source_and_order_from_accepted_boundary
test_one_of_ten_notes_preserves_other_steps_and_redoes_exactly
test_whole_inverse_records_each_sequential_reversal_instead_of_coalescing
test_last_step_restores_its_own_input_not_commit_input
test_step_contains_contiguous_command_run_and_reverses_all_its_commands
test_later_step_dependency_refuses_subset_but_all_steps_reverse[dependency0]
test_later_step_dependency_refuses_subset_but_all_steps_reverse[dependency1]
test_later_step_dependency_refuses_subset_but_all_steps_reverse[dependency2]
test_inverse_execution_rechecks_surviving_steps_without_a_preflight_scan
```

Partial semantic deletion fails at initial source capture; the other thirteen lack `_runtime_document`.

`test_recipe_m1_commands.py` — missing `_runtime_document`; no exact-node proof in 67/244:

```text
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed0-track-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed0-track-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed0-clip-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed0-clip-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed1-track-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed1-track-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed1-clip-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed1-clip-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed2-track-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed2-track-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed2-clip-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed2-clip-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed3-track-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed3-track-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed3-clip-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed3-clip-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed4-track-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed4-track-occurrence:occ-1]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed4-clip-parent]
test_structural_removal_inverse_redo_preserves_full_rows_and_authored_order[removed4-clip-occurrence:occ-1]
test_remove_last_clip_keeps_exact_container_shape[payload]
test_remove_last_clip_keeps_exact_container_shape[config]
test_remove_last_clip_keeps_exact_container_shape[both]
test_remove_last_clip_keeps_exact_container_shape[null-payload]
test_remove_last_clip_keeps_exact_container_shape[null-config]
```

`test_recipe_m2_auto_placement.py` — missing authenticated materialization; no exact-node proof in 67/244:

```text
test_exact_capture_replay_inverse_and_redo[image-anchor]
test_exact_capture_replay_inverse_and_redo[image-absent]
test_exact_capture_replay_inverse_and_redo[video-anchor]
test_exact_capture_replay_inverse_and_redo[video-absent]
```

**Validation and proof limits**

Executed now:

```text
git diff --check
git status --short
```

Both exit 0; no diff or status output. No tests, full suite, original ABA, or static gates were rerun, as permitted for source-only classification.

Inspected actual XML and [prior exact commands/results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-historical-source-sol-0959/evidence/commands.txt):

- Author receipt: **67 passed**; integrated d83 receipt: **67 passed**. They cover four of these exact 60 failed nodes.
- Neighbor receipt: **244 passed**, covering item observation, undo projection, **`test_provider_step_undo_v2.py`**, duplicate occurrence, and media-manifest inverse. It covers none of these exact failed nodes; provider step-undo is a different file.
- Prior d83 `make ruff PY=/home/user/work/venv-agent/bin/python`: PASS, **2143/2143**.
- Prior d83 `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: PASS, **1902/1902**.

Production remains connected through `RuntimeCommitService.commit` → `commands.execute` → `apply_inverse` → `_validate_inputs` → `_input_read_state`, including landing replay. Request/reply handling and the full v2 fields remain untouched; this is source verification, not new end-to-end qualification.

**Decision and next steps**

No concrete additional current product defect was established, so no patch or regression was added. Investigation is complete; qualification remains open.

R2 should independently review this attribution, then qualify the **eleven uncovered historical-codec nodes** on current source. The **45 fixture cases** need an R2-owned fixture/compatibility decision at `accepted_boundaries`, `test_step_undo_v2.accepted`, and the native bundle builders, preserving every original assertion. Any proposed change to `Closure`/`document_from_bundle` crosses the allowed correction seam and needs the R1/commit owner.

No new code review is required for this unchanged tree. Full9758’s failures remain recorded at their observed scope.