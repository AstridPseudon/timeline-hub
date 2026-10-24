## D69 SDK triage report

Counts: **1 confirmed live regression / 10 exact decision conflicts / 0 env / 5 PASS**.

Evidence: retained XML `d69-restored47.xml` SHA256 `005ea787…`; service run had **49 cases: 39 failed, 10 passed, 0 skips/errors**. No rerun performed.

### Per-case evidence

All restored bodies match upstream-924 AST exactly; body hashes and upstream blobs come from `d69-restored47.json`.

| XML selector | Status / exact traceback | Current source cause | Upstream body |
|---|---|---|---|
| `tests.sdk.test_authoring_revision_diff::test_missing_or_mismatched_pin_fails_without_partial_or_current_fallback_r4_original[missing_child]` | PASS; actual pin-mismatch refusal | Current [test_authoring_revision_diff.py](/home/user/work/wt/agt-F-D69-failures-sdk-1646/tests/sdk/test_authoring_revision_diff.py:155) | `c7b14cd9…`, blob `5036838d…` |
| Same selector `[foreign_project]` | PASS | Same actual scope | Same |
| Same selector `[foreign_timeline]` | PASS | Same actual scope | Same |
| Same selector `[wrong_revision]` | PASS | Same actual scope | Same |
| Same selector `[corrupt_bytes]` | PASS | Same actual scope | Same |
| `test_timeline_checkout::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones_r4_original` | FAIL: `NameError: three_way is not defined` at test line 315 | `three_way` removed from [store.py](/home/user/work/wt/agt-F-D69-failures-sdk-1646/astrid/sdk/timeline/store.py); import removed from test | `7d8cf03e…`, blob `be93759f…` |
| `test_timeline_persistence::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head_r4_original` | FAIL: `AttributeError: SimpleNamespace has no attribute _remote` | Current `Checkout.publish` reaches [sync.py](/home/user/work/wt/agt-F-D69-failures-sdk-1646/astrid/sdk/timeline/sync.py:43), while this exact body supplies the legacy fake client used by the removed whole-writer path | `e1eb217a…`, blob `79cf8b24…` |
| `test_timeline_publish_connection::test_a_publish_with_no_client_writes_through_the_connection_it_opens_r4_original` | FAIL: `store.publish_bundle` missing | `publish_bundle` removed; current publish path is [publish.py](/home/user/work/wt/agt-F-D69-failures-sdk-1646/astrid/sdk/timeline/publish.py:119) → `TimelineSession` | `536763a2…`, blob `914ec3a1…` |
| Same file, `test_a_publish_with_a_client_writes_through_that_client_r4_original` | Same `AttributeError` | Same | `dacf984a…`, same blob |
| `test_intent_app_astrid::test_three_way_legacy_head_is_not_a_conflict_and_keeps_intent_r4_original` | FAIL: `NameError: three_way is not defined` | Removed `store.three_way`; no current production caller | `e4d84003…`, blob `e4ac60c5…` |
| `test_intent_app_astrid::test_merge_keeps_a_film_namespace_key_outside_the_known_list_in_the_namespace_r4_original` | Same `NameError` | Same | `a2421d6c…`, same blob |
| `test_runtime_response_conformance::test_publish_conflict_409_maps_to_conflict_and_keeps_its_details_r4_route` | FAIL: sent `/composition-revisions`, fixture requires `/timelines/main/commit` | [WorkspaceClient.publish_parent_composition](/home/user/work/wt/agt-F-D69-failures-sdk-1646/astrid/sdk/workspace_client.py:429) still dispatches the retired route; `remote.py:411` remains a caller | `dc18b26e…`, blob `6fc67831…` |
| `test_timeline_restructure::test_three_way_merge_works_on_the_stored_form_r4_original` | FAIL: `NameError: three_way is not defined` | Removed legacy merger | `cc43d341…`, blob `69fdf1ce…` |
| `test_timeline_restructure::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original` | FAIL: invalid registry asset `R` has no canonical selected media identity | [timeline_duplicate.py](/home/user/work/wt/agt-F-D69-failures-sdk-1646/astrid/sdk/timeline_duplicate.py:246) changed upstream behavior from `check()` to `_check_core()`, bypassing the test’s validity seam. Live caller: `cli_working.py:457` → `duplicate_timeline` | `90ce8bd9…`, blob `69fdf1ce…` |
| `test_timeline_store_fixes::test_publish_merge_keeps_candidate_parent_config_changes_next_to_head_changes_r4_original` | FAIL: `NameError: three_way is not defined` | Removed legacy merger | `8f0ae33a…`, blob `444b5084…` |
| `test_timeline_store_fixes::test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins_r4_original` | Same `NameError` | Same | `35206c7b…`, same blob |

### Decision disposition

The ten removed-surface failures are exact conflicts, not environment gaps:

- PLAN G5 deletes `store.three_way` and `publish_bundle`.
- BOARD D52 permits removal of retired save routes/fallback writers and tests exercising only them.
- The deletion ledger simultaneously records WC7/WC8 as held/live and WC10 as held pending caller migration.
- D54a/D69 otherwise require upstream-pass/current-fail cases to be fixed.

Manager escalation must resolve those contradictory requirements before any source/test action. Restoring the bodies would resurrect forbidden writers; deleting/retiring them requires confirming the WC7/WC8/WC10 decisions.

### Product repair suggestions

- **Confirmed regression:** owner a PR around `timeline_duplicate.py:246,283`. Reconcile the `check()` → `_check_core()` decision while preserving renderer-off safety and the current Runtime commit writer.
- **Old route:** migrate remaining `publish_parent_composition` callers to the canonical v2 commit envelope, then apply R5 retirement; affected areas include `workspace_client.py`, `remote.py`, `reference_realm.py`, and `shot_composition_migration.py`.
- **Legacy merge/publish cases:** no safe repair can be proposed until WC7/WC8/WC10 are resolved; do not add aliases or resurrect writers.
- **Persistence case:** preserving the exact body requires the removed whole-candidate writer; otherwise the current authenticated `TimelineSession` path must remain authoritative.

### Verification

- No tests, collection, HTTP, body, full suite, or service rerun performed per brief.
- Read-only checks: current HEAD `ef0363985e645481952448619f2cbb25e9d51a66`; worktree clean; no product/test changes.
- Commit message written and `DONE` marker created.