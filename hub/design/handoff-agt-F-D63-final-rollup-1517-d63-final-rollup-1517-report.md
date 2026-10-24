# F/D63 final evidence rollup

Read-only final evidence rollup for the exact D60 set of 276 Agent rows, applying the corrected rename1508 overlay and completed paired-cause A/B1458 evidence. Original evidence is preserved; this publication adds no product source, test, generated-file, pin, or test-body change.

## Result

The exact 276 rows have one disjoint baseline partition:

| Baseline route | Rows |
| --- | ---: |
| Remaining NEW-OURS after the one bounded rename/name-body check | 199 |
| Authenticated renamed counterparts | 2 |
| Exact upstream counterparts | 75 |
| **Total** | **276** |

The 199 NEW-OURS rows retain the settled precedence: 147 current qualified PASS, 45 existing environment, 1 existing D23 deferred, 5 current core-open, and 1 visible non-core known gap (order 55). Missing exact selectors are not called `UNKNOWN` for the regression guard.

The 2 authenticated renamed counterparts are order 129 (current PASS; final-cut review) and order 181 (current OPEN; REVIEW only). Order 181 maps by identical function name/body, has source fix `2a8f` under unique security `1513`, and has no home PASS receipt; its exclusive current-proof owner remains `agt-F-D63-env-catalogue-current-1508`.

The 75 exact counterparts are 66 upstream FAIL plus 9 upstream PASS. Of the 66 fail-both rows, only 7 (orders 146–150, 217, 218) qualify as pre-existing, using matching retained exception/assertion/input setup from A/B1458. The other 59 remain cause-open: four precise different cause boundaries (orders 5, 49, 50, 51), 41 explicitly summary-only/missing-old-traceback limits, and 14 retained-but-unqualified causes. No current failure is invented from a baseline status match. The 9 upstream-PASS contrasts are the prior 8 (orders 1, 169, 173, 220, 221, 222, 223, 228) plus renamed order 129; all require final-cut confirmation.

## Current qualification and blockers

| Current qualification | Rows |
| --- | ---: |
| PASS | 162 |
| OPEN | 112 |
| DEFERRED | 2 |
| **Total** | **276** |

The core split remains 152 PASS / 5 OPEN / 2 DEFERRED; non-core remains 10 PASS / 107 OPEN. The five blocking core rows inside exact276 are:

| Order | Exact ID | Current status | Current category | Baseline route | Evidence |
| ---: | --- | --- | --- | --- | --- |
| 11 | `tests/editing_conformance/test_provider_occurrence_fork.py::test_v2_registered_fork_reply_physical_effects_step_reads_and_undo[True]` | `FAIL` | `UNPROVEN` | `new_ours_current_core_open` | `actual-home1330-core159-ordinary.xml; d60-comparison-rows-1452/order-11; d63-new-ours-rename-201` |
| 13 | `tests/editing_conformance/test_provider_occurrence_fork.py::test_disjoint_head_merge_and_preview_keep_other_edit` | `FAIL` | `UNPROVEN` | `new_ours_current_core_open` | `actual-home1330-core159-ordinary.xml; d60-comparison-rows-1452/order-13; d63-new-ours-rename-201` |
| 98 | `tests/editing_conformance/test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[1]` | `FAIL` | `UNPROVEN` | `new_ours_current_core_open` | `d54-d57-final-classification-rollup-1242; actual-home1330-core159-ordinary.xml; d60-comparison-rows-1452/order-98; d63-new-ours-rename-201` |
| 99 | `tests/editing_conformance/test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[2]` | `FAIL` | `UNPROVEN` | `new_ours_current_core_open` | `d54-d57-final-classification-rollup-1242; actual-home1330-core159-ordinary.xml; d60-comparison-rows-1452/order-99; d63-new-ours-rename-201` |
| 162 | `tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight` | `UNKNOWN` | `UNPROVEN` | `new_ours_current_core_open` | `d54-current-rollup-1338.current_status_exceptions; d60-comparison-rows-1452/order-162; d63-new-ours-rename-201` |

Orders 11, 13, 98, and 99 are current FAIL and remain blocking NEW-OURS core rows. Order 162 is the held D13 missing carrier/admission row with current UNKNOWN status; it is retained as held evidence, not promoted or treated as a baseline UNKNOWN. Two additional blockers are tracked outside exact276: the forward `track.create` omitted-created cases for `stable-track` and `historical-track`, a Runtime authentication/source seam owned through the unique security route. Thus the current blocking-core count is 7 (5 inside / 2 outside exact276). The two D23 deferred rows are orders 170 and 213 and remain excluded from PASS.

## Contract and evidence limits

The v2 contract sections 1–5 were read. The preserved request scope includes `api_version`, `project_id`, `timeline_id`, the exact `base_revision_id`/`base_publication_id`, `commands`, `label`, full step fields (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields|atomic`), request `reads`, `dry_run`, `source`, `rationale`, `group_id`, and HTTP `Idempotency-Key`. The preserved reply scope includes accepted/merged canonical closure, IDs/digests/commands/id_map/records/steps/dependencies/effects/bindings/history/durable receipt; dry-run `would_status` with `receipt: null`; conflict reason/head; and invalid code/path/hint/suggested_command. The existing evidence says the production caller uses this route; this rollup makes no new implementation claim.

No tests, original/full runs, source execution, live-daemon search, installs, package acquisition, children, or source/test edits were performed. The JSON/TSV contain the exact order/ID/current status/core/category/baseline-route/evidence table. Validation was limited to read-only structural/count/hash checks.
