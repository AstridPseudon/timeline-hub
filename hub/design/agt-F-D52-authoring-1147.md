# D52/G4 bounded authoring assessment

## Result

Verified the exact 16-node membership from `agent-F-D52-classification-1132.csv` rows 223–231. All remain live; no no-caller or exclusive-code proof supports deletion. No confirmed current production defect was established from source-only evidence.

Current accepted-write authority is intact:

- Document publishing uses `TimelineSession._bundle()` and `commit_many()` (`timeline_document.py:252-332`, `sync.py:193-209,518-585`).
- Authoring publication builds the v2 request and calls `writer.commit_timeline()` (`authoring_commit.py:84-186`, `authoring_bundle.py:1833-1873`).
- Undo derives from accepted history records, command ordinals, steps, bindings, and recorded writes (`commit.py:1011-1108`, `_step_undo.py:10-114`, `inverse.py:312-470`).
- No caller-supplied snapshot or synthetic authority was found.

## Finite 16-node mapping

| # | Node | Current caller/source span | Assessment |
|---:|---|---|---|
| 1 | `test_document_publish_forwards_new_stale_head_to_runtime` (`test_authoring_media.py:229-350`) | `timeline_document.py:252-332`; `sync.py:518-585` | **Faithful stale caller fixture.** Test still fakes `open_bundle()`/direct transport `commit`; production now opens `TimelineSession`, reads `_bundle()`, and flushes through `commit_many()`. |
| 2 | `test_document_publish_captures_verified_media_before_document_patches` (`test_authoring_media.py:353-397`) | `timeline_document.py:80-115` | **Unavailable cause.** Current source explicitly captures verified media before residual document emission; no current failure traceback proves a source defect. |
| 3 | `test_public_document_swap_and_residual_patch_use_original_sequential_closure[True]` (`test_authoring_media.py:399-533`) | `timeline_document.py:80-115`; `emitter.py:169-205,239-293` | **Faithful stale/input-boundary case.** The emitter intentionally rejects contradictory physical-root aliases; retained evidence does not prove the fixture supplied the required occurrence/source identity. |
| 4 | Same test, `[False]` | Same spans | **Faithful stale/input-boundary case**, same cause as #3. |
| 5 | `test_public_document_compound_inverse_restores_exact_original` (`test_authoring_media.py:536-549`) | `authoring_bundle.py:1833-1873`; `commit.py:1011-1108`; `_step_undo.py:10-114` | **Unavailable cause.** Accepted-record inverse path is live; no current failure detail remains. |
| 6 | `test_catalog_import_remains_reusable_after_later_parent_cas_conflict` (`test_authoring_media.py:1532-1554`) | `authoring_media.py:332-657`; document caller `timeline_document.py:244-279` | **Unavailable cause.** Catalog planning/import remains a public live helper; summary-only evidence does not identify a defect. |
| 7 | `test_semantic_removal_undo_restores_exact_closure` (`test_authoring_publication_migrations.py:180-187`) | `authoring_commit.py:100-113`; `commit.py:1011-1108` | **Unavailable cause.** Current removal uses registered `occurrence.delete`; inverse uses accepted history. Missing input/environment evidence prevents a defect assignment. |
| 8 | `test_selected_alias_forks_and_retains_exact_sibling[first]` (`test_authoring_shared_alias_commit.py:50-110`) | `authoring_commit.py:84-186,189-248`; `authoring_bundle.py:1833-1873` | **Unavailable cause.** Production fork caller is live and current source creates deterministic native forks while preserving the sibling. No current traceback establishes a source defect. |
| 9 | Same test, `[second]` | Same spans | **Unavailable cause**, same boundary as #8. |
| 10 | `test_edits_to_new_duplicate_are_not_hidden_by_added_occurrence_summary` (`test_authoring_feedback_residual.py:139-156`) | `authoring_feedback_residual.py:17-194`; feedback summary `authoring_feedback.py:137-175` | **Unavailable cause.** New-duplicate baseline comparison is present; no current source failure is established. |
| 11 | `test_remote_parent_media_replacement_publishes_exact_closure_once` (`test_timeline_clip_replacement.py:168-223`) | `remote.py:1338-1597`; `timeline_media_replacement.py:156-266` | **Faithful stale retired-writer fixture.** Production routes through native `replace_selected_media()`/session commit; test still requires retired `publish_parent_composition()`. |
| 12 | `test_absent_collection_is_restored_exactly` (`test_recipe_text_binding_native.py:80-83`) | `native_text_binding.py:36-68`; `inverse.py:200-270,312-470` | **Unavailable cause.** Presence-aware text-binding and inverse restoration are live; not deferred word binding. |
| 13 | `test_multiple_births_in_absent_collection_have_exact_batch_inverse` (`test_recipe_text_binding_native.py:193-198`) | Same spans | **Unavailable cause**, same native text-binding boundary as #12. |
| 14 | `test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases` (`test_timeline_sheet_native.py:589-620`) | `timeline_sheet.py:730-881`; `sync.py:306-362,518-585` | **Unavailable cause.** Native sheet uses normal session commit/retry/undo paths; no source defect proven. |
| 15 | `test_joined_music_updates_source_and_literal_duration_for_publication` (`test_timeline_structure.py:82-125`) | `timeline_structure.py:143-168`; `authoring_bundle.py:1833-1873` | **Unavailable cause.** `join_music()` remains the production mutation path; summary-only evidence gives no defect. |
| 16 | `test_p4_note_conflict_reruns_public_function_from_verified_peer_document` (`test_p4_note_rerun.py:67-128`) | `commit_session.py:163-254,263-280` | **Unavailable cause.** Public `Timeline.commit(fn)` performs bounded conflict reruns from the verified peer document; no current failure evidence proves otherwise. |

There are zero confirmed “deferred word binding” nodes in this exact 16-node set.

## Repairs considered

Compared current source after the relevant post-full9758 repairs, including:

- `c2584a0143`: migrated document publication to the opened `TimelineSession` seam.
- `5da353c641`: materialized shared-alias authoring edits.
- `4e7121fef4`, `4b79850b51`, `fd7769e56a`: authoring publication identity/source repairs.
- `dba4468649`, `977e28ef44`, `dfe105e13e`, `0eab665187`, `668b183783`, `1c9171b855`, `ca8915f23d`: accepted-history, inverse, source, and redo repairs.

## At most three repair scopes

1. **Port stale writer fixtures:**  
   `tests/timeline/test_authoring_media.py`, `tests/test_timeline_clip_replacement.py`  
   Update fakes/assertions to `TimelineSession`/native media replacement while preserving v2 request, no-write, closure, and conflict assertions.

2. **Authoring closure evidence:**  
   `tests/timeline/test_authoring_shared_alias_commit.py`, `test_authoring_feedback_residual.py`, `test_authoring_publication_migrations.py` with current `authoring_commit.py`, `emitter.py`, and inverse authority.  
   First obtain a current traceback before changing production source.

3. **Native binding/sheet/rerun evidence:**  
   `test_recipe_text_binding_native.py`, `test_timeline_sheet_native.py`, `test_timeline_structure.py`, `test_p4_note_rerun.py` with `native_text_binding.py`, `inverse.py`, `timeline_sheet.py`, and `commit_session.py`.  
   Re-run only the named selectors after confirming fixtures/environment.

No tests, registry calls, production execution, package changes, or source edits were performed. Worktree is clean.