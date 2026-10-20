# Agent area: size, deletion-ledger audit, dead code, second writers (0905)

Read-only audit. Source: `git -C /home/user/work/agent`, HEAD `931d7ec5` (Merge tl/agt-m2-occurrence-delete-sync; the ledger quotes integration 4a75f68f, which is an ancestor). No repo changes, no commit message.

Method: `git grep -c ''` over `astrid/sdk`, `astrid/packs/timeline/`, `astrid/core/timeline/`, `tests/editing_conformance` at HEAD; non-product = `tests/`, `test_*`, `fixtures/`, `docs`, `*.md`, `*.json/yaml/txt`, `*.ts` generated. Line counts are physical lines (blank and comment lines included), not the PLAN's "authored" definition.

## 1. Size

Strict glob (`astrid/sdk/timeline*`, `astrid/packs/timeline/`, `astrid/core/timeline/`), product `.py` only:

| group | product lines | files |
|---|---|---|
| astrid/sdk/timeline* (incl. `timeline/` dir) | 19,865 | 59 |
| astrid/packs/timeline/ | 6,995 | 16 |
| astrid/core/timeline/ | 14,839 | 57 |
| **total product** | **41,699** | **132** |

Tests and fixtures:
- `tests/editing_conformance`: 47,873 lines in 71 files. Python tests and runner: 11,262 lines in 44 files. JSON fixtures: 36,548 lines in 26 files. Other: 63 lines.
- Largest fixtures: `recipe_m2_placement_create_unplace.json` 6,752; `recipe_m2_app_clip_scalar_fields.json` 6,317; `recipe_m2_occurrence_delete.json` 4,491.

Against target: the PLAN boundary (timeline core, all four repos, ~20–26k) is exceeded by the Agent area alone. The 41.7k figure is an upper bound because it includes modules that are not timeline core in the PLAN sense (see the outside-glob note below). Even so, Agent-only is roughly 1.6–2x the whole-product target. Largest contributors are in section 3 of the top-15 list below.

Outside the requested glob but Agent-owned timeline writer code (not counted above): `astrid/sdk/remote.py` 2,773 (timeline methods incl. `replace_parent_media` 1278–1503, `update_parent_element`, `set_text_binding`), `astrid/sdk/authoring_remote.py` 326, `astrid/sdk/authoring_bundle.py` 46, `astrid/packs/rendering/docs/scripts/timeline_document.py`, `astrid/packs/shots/cli.py`, `astrid/packs/rendering/actions/render/managed_timeline.py`, `astrid/core/execution/generic_host.py` (`_publish_assembled_timeline` at 8401). `astrid/sdk/workspace_client.py` has a `publish_parent_composition` client method (434).

Top 15 product files in the area (lines, what it is):

| # | lines | file | what |
|---|---|---|---|
| 1 | 4,067 | astrid/packs/timeline/cli.py | the `timelines` CLI parser and verbs |
| 2 | 1,676 | astrid/core/timeline/authoring_bundle.py | authoring candidate publish/promote (WC1, WC2) |
| 3 | 1,278 | astrid/sdk/timeline_filmstrip.py | filmstrip views |
| 4 | 1,221 | astrid/sdk/timeline/reflow.py | Checkout voice/re-flow, moments, retime |
| 5 | 1,159 | astrid/sdk/timeline/model.py | Checkout/Clip/Voice model |
| 6 | 1,095 | astrid/core/timeline/shot_composition_migration.py | legacy shot→composition migration (calls publish_parent_composition, line 1030) |
| 7 | 1,052 | astrid/sdk/timeline_sheet.py | cut-sheet parse/save (AG03; history reads at 621–638) |
| 8 | 1,020 | astrid/sdk/timeline_address.py | address resolution |
| 9 | 1,015 | astrid/sdk/timeline_cuts.py | cut helpers |
| 10 | 1,011 | astrid/packs/timeline/cli_visualize.py | visualize verb |
| 11 | 939 | astrid/sdk/timeline/commit.py | commit provider (accepted-history checks, `history_unavailable` paths) |
| 12 | 890 | astrid/core/timeline/projection.py | event projection |
| 13 | 887 | astrid/sdk/timeline/check.py | checks (advisory policy) |
| 14 | 883 | astrid/sdk/timeline_editing.py | deprecated retime helpers still present (D07) |
| 15 | 686 | astrid/core/timeline/shot_composition_projection.py | shot composition projection |

## 2. Deletion ledger, Agent rows

Checked against HEAD with `cat-file`/`grep`. "Consistent" means status matches the repo.

| row | status (ledger) | repo check | verdict |
|---|---|---|---|
| D05 | DELETED | `astrid/core/timeline/inverses.py` and `tests/timeline/test_inverses.py` GONE. Replacement tests present: `test_legacy_history_undo_and_restore_use_revisions_or_refuse_visibly` (tests/sdk/test_timeline_commit_provider.py:808), `test_undo_detects_aba_and_unchanged_write_publications` (:403), `test_inverse_rebases_only_over_proven_disjoint_new_writes` (:626), `test_exact_authored_move_inverse_redo` (tests/editing_conformance/test_recipe_m1_commands.py:70). `fc33e0e7` is an ancestor. | consistent |
| D06 | DELETED | `astrid/core/extensions/` GONE. `6c5b616a` is an ancestor of HEAD. Replacing tests present: `test_external_broken_hidden_and_duplicate_roots_are_isolated` (tests/packs/test_pack_discovery_v3.py:141), `test_editor_entry_discovery_rejects_paths_outside_pack` (tests/test_editor_extension_catalog.py:44). | consistent; the ledger note "not physically merged onto 4a75f68f" is stale |
| D07 | in-progress | `astrid/sdk/timeline_editing.py` still has `retime`/`retime_with_ripple` (351, 367). `57a1e595` is NOT an ancestor. | consistent. No replacing test named |
| D13 | in-progress (agent+runtime) | `_publish_assembled_timeline` at `astrid/core/execution/generic_host.py:8401` (ledger path `astrid/sdk/generic_host.py` is wrong); calls `publish_timeline_render` (8412). No `publishTimelineRender` in Agent. | consistent; ledger path wrong; no replacing test named |
| D01a / D01b | in-progress (agent+app) | Agent side not checked in depth; `native_occurrence_media_commands.py` and `native_placement_commands.py` present. | no replacing test named (D01a/b evidence is App/Runtime only) |
| AG01 | in-progress | `astrid/sdk/timeline/journal.py` (335) and `outbox.py` (56) present | consistent; no replacing test named |
| AG02 | in-progress | `store.publish_bundle` (store.py:257) present | consistent; no replacing test named |
| AG03 | held | `astrid/sdk/timeline_sheet.py` present, but it has no `three_way`/`fetch_bundle` call. Its history reads (`_history_dir`, 621–638) are a local undo path, see section 4. | consistent; **no replacing test named**; the merge path the ledger names should be checked (it may be in `packs/timeline/cli.py`) |
| AG-M2-TB01 | held (design only) | `remote.py:2446` set_text_binding and `:2456` rebind ✓; `publish.py:173` pin_narration ✓; `timeline_document.py:179` ✓; `packs/shots/cli.py:135` ✓. Spike test `tests/editing_conformance/test_recipe_text_binding_spike.py` present. | consistent |
| AG-M3-CAP-01..04 | held | `tests/sdk/test_capture_source_runtime.py` and `test_capture_closure_source.py` present and the named positives exist (`test_missing_candidate_working_copy_is_admitted_uncertified` :217, `test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies` in closure_source :130). | consistent |
| AG05 | HELD | `managed_timeline.py:893` `_project_exact_parent_head` ✓; `test_real_saved_entire_expansion_golden` (test_timeline_capture_projection.py:253) and `test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows` (:266) present. | consistent |
| WC1 | held | `authoring_bundle.py:1620` `publish_authoring_candidate` (ledger says :1587 — drift) | line drift; no replacing test named |
| WC2 | held | `authoring_bundle.py:1571` `promote_approved_authoring_candidate` (ledger :1538 — drift). Only re-exports in `astrid/sdk/authoring_bundle.py`, `sdk/__init__.py:80`; test callers `tests/timeline/test_authoring_bundle.py:471, 476, 623` (ledger cites `tests/test_authoring_bundle.py:458,483` — wrong path and lines) | path and line drift |
| WC3 | held | `remote.py:1278`–`1503` `replace_parent_media` ✓ | consistent; replacement `tests/test_timeline_clip_replacement.py` present |
| WC4 | held | `timeline_elements.py:16` `update_parent_element` ✓ (the method is also at `remote.py:1259`); `tests/core/test_timeline_element_publication.py` present | consistent |
| WC5 | held | `draft_voiceover.py:475` `bound.publish(...)` ✓ (file is `astrid/packs/video_editing/shared/draft_voiceover.py`); `TargetBoundAuthoringBundle.publish` at `authoring_remote.py:230` ✓ | consistent. Replacement test named as `test_draft_voiceover.py`; real path is `tests/packs/video_editing/test_draft_voiceover.py` |
| WC6 | held | `timeline_document.py` publish at 215 ✓. Ledger test refs `test_authoring_feedback.py:210`, `test_authoring_media.py:227` are drifted; actual publish calls are at `tests/timeline/test_authoring_feedback.py:54,148,269` and `tests/timeline/test_authoring_media.py:370,766`. | line/path drift |
| WC7 | held | `store.py:257` `publish_bundle` ✓, `publish.py:44` ✓. Ledger test `tests/test_timeline_publish_connection.py` does NOT exist; the real file is `tests/sdk/test_timeline_publish_connection.py`. | path drift |
| WC8 | held | `store.py:169` `three_way`, `:139` `_merge`, `:574` `fetch_bundle` ✓; `checkout.py:203` (`whole=True`) ✓; `packs/timeline/cli.py:2808` ✓ | consistent |
| WC9 | held | `docs/timeline-editing-guide.md` (263, 294) ✓, `docs/timeline-authoring-capabilities.md` (12, 28) ✓, `astrid/packs/rendering/docs/SKILL.md` (349, 643) ✓. **`document-checkout.md` does not exist** in Agent docs. | row names a missing doc; check whether it lives elsewhere |
| WC10 (runtime) | held | Agent-side callers present: `astrid/core/dev/reference_realm.py:99`, `shot_composition_migration.py:1030` (gated), `remote.py:534` (create_empty path via `:480`). **Additional Agent-side callers not in the WC10 row**: `sdk/workspace_client.py:434`, `remote.py:409, 1454`, `authoring_remote.py:302`, `timeline_elements.py:59`, `timeline/store.py:300`, `packs/rendering/docs/scripts/timeline_document.py:92`, `authoring_bundle.py:1605, 1640` | row incomplete |
| CT1 | done | `test_missing_candidate_working_copy_is_admitted_uncertified` (:217) and `test_missing_candidate_certificate_without_authority_refuses_before_admission_writes` (:227) present; the retired refusal name is absent | consistent |

Summary of status problems:
- No row is "DELETED but code present" or "held but gone" for D05/D06.
- Rows with **no replacing test named**: D07, D13, D01a, D01b, AG01, AG02, AG03, WC1, WC2 (only test-only callers), WC9 (docs).
- Stale paths (fix in the ledger): D13 (`astrid/sdk/generic_host.py` → `astrid/core/execution/generic_host.py`); WC2, WC6, WC7, WC1, and WC5 (test paths and line numbers); WC10 (missing Agent callers); WC9 (`document-checkout.md` missing).
- Stale note: D06 "not physically merged" is wrong; its commit is an ancestor.

## 3. Dead-code candidates (no importer)

Corrected rerun (`scratchpad/deadcode.py`, output `scratchpad/deadcode.txt`) matches dotted paths, relative imports, and `from <pkg> import <module>`, across `astrid/`, `tests/`, `docs/`. Its zero-importer list is the same as the first pass: only package `__init__` files, plus the events payload modules that are reached through `events/schema/__init__.py`. Manual checks of the first-pass hits showed they are live through indirect imports:
- `packs/timeline/cli_working.py` (558): imported by `cli.py:3831, 4025` (`from astrid.packs.timeline import cli_working`).
- `core/timeline/moments.py` (281): `sdk/timeline/check.py:12`, `cli_working.py:325`.
- `core/timeline/text_fit.py` (116): `sdk/timeline/check.py:62`, `motion/model.py:704`.
- `core/timeline/arrangement_rules.py` (206): `core/timeline/__init__.py:5`.
- `core/timeline/events/schema/payloads/*.py` (21–198 each): imported through `events/schema/__init__.py`, which `projection.py:54` and `snapshot.py:16` import.
- Package `__init__.py` files (`sdk/timeline/__init__.py` 10, `core/timeline/validators/__init__.py` 7, `core/timeline/events/__init__.py` 1, `events/schema/__init__.py` 108, `payloads/__init__.py` 111): package markers, not dead.

**Result: no product module in the area is provably unimported at HEAD.** Deletion candidates for M4 are therefore *not* whole modules. They are legacy surfaces inside live modules:
- `astrid/sdk/timeline_checkout.py:133–153`: `# noqa: F401` re-exports of store internals (`_write_step`, `_read_step`, `_redo_dir`, `_history_dir`, `three_way`, `fetch_bundle`). Remove once their callers (`timeline_sheet.py:621`, tests that monkeypatch `tc.fetch_bundle`) move.
- `astrid/sdk/timeline_editing.py:351–401` (`retime`, `retime_with_ripple`): D07.
- `astrid/core/timeline/shot_composition_migration.py` (1,095): live only through the migration path that calls `publish_parent_composition` (line 1030 gates it); a deletion candidate after its migration callers move (WC10).

## 4. Duplicate edit/history paths still present

Second writers (publish a whole document or a whole closure):
- `publish_parent_composition` callers, Agent: `astrid/core/dev/reference_realm.py:99`; `astrid/core/timeline/authoring_bundle.py:46, 1605, 1640`; `astrid/core/timeline/shot_composition_migration.py:151, 1030`; `astrid/sdk/remote.py:409, 534, 1454, 2318`; `astrid/sdk/workspace_client.py:434`; `astrid/sdk/authoring_remote.py:302–310`; `astrid/sdk/timeline_elements.py:59–64`; `astrid/sdk/timeline/store.py:300–314`; `astrid/packs/rendering/docs/scripts/timeline_document.py:92–94, 215`.
- Whole-candidate publish (`publish_authoring_candidate`): `authoring_bundle.py:1620`, `remote.py:1395, 1468`, `timeline_elements.py:64`, `store.py:261, 304`, `packs/timeline/cli.py` (via checkout publish 2973), `packs/timeline/cli_working.py:493` (`tl.publish`), `packs/rendering/docs/SKILL.md:643`, `video_editing/shared/draft_voiceover.py:475`.
- Checkout publish (whole document + three-way): `sdk/timeline/publish.py:44, 89, 111–115` (incl. the narration second publish), `sdk/timeline/store.py:257–282`.
- Direct shot text writers (AG-M2-TB01): `sdk/remote.py:2446, 2456`; `sdk/timeline/publish.py:173–189`; `packs/rendering/docs/scripts/timeline_document.py:179`; `packs/shots/cli.py:135`.
- Whole-closure media/effect swaps (WC3, WC4): `sdk/remote.py:1278–1503`; `sdk/timeline_elements.py:16`.

Legacy history and revert paths (second history, not the Runtime's accepted history):
- Whole-file local undo/redo: `astrid/sdk/timeline/checkout.py:160, 175, 180` (save writes history steps), `checkout.py:224–258` (`undo`/`redo` over `_history_dir`/`_redo_dir`), `astrid/packs/timeline/cli.py:3578–3583` (`_cmd_undo` falls through to it unless `--publication`). Keep only if the owner wants local drafts undoable; otherwise it is a second history.
- Sheet restore from local history: `astrid/sdk/timeline_sheet.py:621–638`.
- Whole-unit three-way (WC8): `astrid/sdk/timeline/checkout.py:203` (`whole=True`), `astrid/packs/timeline/cli.py:2808–2809` (`store._units(..., whole=True)`).
- Publication-undo (`astrid/sdk/timeline/sync.py:261`) is the command-path undo and is NOT a duplicate.

## Next steps (recommended)
1. Fix the ledger paths and line numbers listed in section 2 (the orchestrator owns that file).
2. Name replacing tests for D07, D13, D01a/b, AG01–03, WC1–2, WC9.
3. Decide `checkout.undo`/`sheet` local-history fate (second history) before M4.
4. (Done) Corrected dead-code rerun confirms section 3.

## Unverified
- The importer scan is text-based. It can miss dynamic loading that is not spelled as a module path (for example `importlib` with a computed name), though pack.yaml `runtime_module` entries are dotted and were covered.
- Did not verify App/Runtime halves of D01/D13.
- Line counts are physical lines, not PLAN "authored" lines.
