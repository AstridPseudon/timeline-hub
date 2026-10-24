# D52/G4 source/evidence review

Verdict: **PASS for source classification; target test-only diff is safe.** No behavior PASS is claimed.

The target merge `8c223d77fef71e52b1bdc42f205c82af5cfc5d25` changes only:

- `tests/sdk/test_timeline_open_commit.py`
- `tests/sdk/test_timeline_open_commit_v2.py`

The added publication-pair fixtures align tests with the authenticated current `TimelineSession` reader. Existing strict request, retry, merge, undo, dry-run, and error assertions remain intact. `git diff --check`: **PASS**. Worktree remains clean.

## Exact 16-node membership

JSON terminal orders `{117,118,166,172,173,221–231}` and matching CSV rows produce exactly these 16 nodes:

| Nodes | Current source evidence | Classification |
|---|---|---|
| `test_document_publish_forwards_new_stale_head_to_runtime` | `timeline_document.py:252-333`; `sync.py:193-209,313-362` | Faithful stale writer fixture; production uses `TimelineSession.commit_many`. |
| `test_document_publish_captures_verified_media_before_document_patches` | `timeline_document.py:80-115` | Cause unavailable; verified media capture remains live. |
| `test_public_document_swap_and_residual_patch_use_original_sequential_closure[True/False]` | Test fixture `test_authoring_media.py:451-457`; `_command_state.py:290-302` | Faithful fixture/input-boundary case. Retained traceback is specifically `shot item source is unavailable`, not contradictory alias selection. |
| `test_public_document_compound_inverse_restores_exact_original` | `authoring_bundle.py:1833-1873`; `inverse.py:312-470`; `_step_undo.py:312+` | Cause unavailable; accepted-history inverse remains live. |
| `test_catalog_import_remains_reusable_after_later_parent_cas_conflict` | `authoring_media.py:332-657`; `timeline_document.py:276-279` | Cause unavailable. |
| `test_semantic_removal_undo_restores_exact_closure` | `authoring_commit.py:84-186`; `sync.py:415-455` | Cause unavailable; registered delete and history inverse remain live. |
| `test_selected_alias_forks_and_retains_exact_sibling[first/second]` | `authoring_commit.py:189-248`; `authoring_bundle.py:1833-1873` | Cause unavailable; native fork caller remains live. |
| `test_edits_to_new_duplicate_are_not_hidden_by_added_occurrence_summary` | `authoring_feedback_residual.py:17-194`; `authoring_feedback.py:56-175` | Cause unavailable; residual summary path remains live. |
| `test_remote_parent_media_replacement_publishes_exact_closure_once` | `remote.py:1338-1597`; `timeline_media_replacement.py:156-266` | Faithful retired-writer expectation; production now commits through the v2 session path. |
| `test_absent_collection_is_restored_exactly` / `test_multiple_births_in_absent_collection_have_exact_batch_inverse` | `native_text_binding.py:36-80`; `inverse.py:312-470` | Cause unavailable; not deferred word binding. |
| `test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases` | `timeline_sheet.py:849-881`; `sync.py:306-362,415-455` | Cause unavailable; normal session commit/undo path remains live. |
| `test_joined_music_updates_source_and_literal_duration_for_publication` | `timeline_structure.py:143-168`; `authoring_bundle.py:1833-1873` | Cause unavailable; helper and publication caller remain live. |
| `test_p4_note_conflict_reruns_public_function_from_verified_peer_document` | `commit_session.py:163-254` | Cause unavailable; bounded verified-head rerun remains live. |

No node is proven dead-scope, pre-existing, or deferred.

## Corrections to the design report

- The `[True]/[False]` media nodes should not be described as an ambiguous-alias rejection. The retained full9758 traceback shows the exact current fixture omits `_runtime_document` before calling `capture_occurrence_swap_media`; the observed cause is `history_unavailable: shot item source is unavailable`.
- “Post-full9758 repairs” is chronologically overstated. The full run was requested at `2026-10-24T09:50Z` on tree `c13d368...`. Most listed repairs precede that run. Only `1c9171b855`, `0eab665187`, and `668b183783` are post-run repairs. Historic full results must remain separate from current-source qualification.

## Ready PR-sized scopes

1. **Port stale writer fixtures**

   Files:

   - `tests/timeline/test_authoring_media.py`
   - `tests/test_timeline_clip_replacement.py`

   Preserve all v2 request fields, exact closure assertions, CAS/no-write guards, and inverse behavior while matching `TimelineSession.commit_many` / native replacement.

   Command:

   ```text
   pytest -q tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime tests/test_timeline_clip_replacement.py::test_remote_parent_media_replacement_publishes_exact_closure_once
   ```

2. **Qualify authoring closure fixtures**

   Files:

   - `tests/timeline/test_authoring_media.py`
   - `tests/timeline/test_authoring_shared_alias_commit.py`
   - `tests/timeline/test_authoring_feedback_residual.py`
   - `tests/timeline/test_authoring_publication_migrations.py`

   First repair exact source/input materialization where required; do not change production code without a new traceback.

3. **Qualify native binding/sheet/rerun evidence**

   Files:

   - `tests/editing_conformance/test_recipe_text_binding_native.py`
   - `tests/sdk/test_timeline_sheet_native.py`
   - `tests/sdk/test_timeline_structure.py`
   - `tests/sdk/test_p4_note_rerun.py`

   Preserve presence/null semantics, strict inverse guards, accepted-record authority, and bounded rerun behavior.

Tests were not run, per the read-only brief. No live calls, installs, source execution, full suite, gate, or environment execution was performed.