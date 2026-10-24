## PASS — bounded census complete

No product/test files were changed. Exact D32 retained-route scope is 30 nodes:

- `test_native_sheet_current.py` (24):
  - `test_custom_pack_param_refuses_without_client_inputs`
  - `test_same_semantics_original_pins_exact_commands_reload_inverse` for `[False|True] × [cli|python|sheet-cli|sheet-python]`
  - `test_unchanged_text_cannot_hide_an_existing_inflight_sheet`
  - `test_unsupported_cells_refuse_whole_batch_before_queue` for:
    `asset-""`, `asset-null`, `hold-""`, `hold-"clear"`, `hold-None`, `hold-null`, `opaque-2`, `text-None`, `text-ƒ(mark)`, `text-null`, `text-{"a":1}`, `transition-""`, `transition-null`, `x-1 ~ignored`
- `tests/packs/timeline/test_cli_native.py` (4):
  - `test_cli_matches_full_app_portable_golden`
  - `test_cli_native_preview_and_lost_ack_retry`
  - `test_cli_native_track_selector_is_parent_scoped`
  - `test_help_exposes_native_entry_and_explicit_legacy_working_copy`
- `tests/sdk/test_scene_dispatch_contract.py` (2 setup rows):
  - `test_scene_request_and_sdk_admission_keep_certified_source[False]`
  - same `[True]`

The “about 33” wording is not supported by D32. The adjacent three FakeCheckout fixture nodes are a separate fixed/test-only family, and the seven CLI-surface nodes are already qualified; neither belongs here.

### Causes and existing proof

- 28 rows are direct retained `--native`/legacy-route callers. Current connected sheets already reach `TimelineSession.commit_many`, but detached `apply` still reaches `Checkout.save`; non-`--commit` undo/redo still uses local checkout state.
- Two Scene setup rows reach retired `publish_parent_composition`. Ordinary `timelines check` currently does `find_draft → Checkout.load → tl.check`; it does not carry a candidate through the managed Scene executor.
- D32 maps all 30 to `Luna2254/G5/R5`. Prior evidence is explicitly scoped only: `1794f0a2e` retained-caller test migration, with later `19646/2340` targeted evidence. No current reconciliation row has an independent proof reference.

### Current production paths

- Native sheet: `show --as sheet --native` → `cli_native.show_native`; connected `apply` → `cli._cmd_apply` → `cli_native.commit_edit` → `NativeSheet.apply` → `TimelineSession.commit_many`.
- Retired detached path: `cli._cmd_apply` → `apply_sheet` → `Checkout.save`.
- Retired local undo/redo path: `cli._cmd_undo/_cmd_redo` → `Checkout.undo/redo`; only `--commit` uses `TimelineSession.undo`.
- Scene check: `cli._cmd_check` loads a detached checkout and calls `tl.check`; no ordinary managed Scene result is returned to the checker.

### Smallest independent repairs

1. **G5 — retained CLI/sheet callers**  
   Owner: Agent/G5. Allowed seam: `astrid/packs/timeline/cli.py`, `cli_native.py`, `cli_parser.py`, `cli_common.py`, `astrid/sdk/timeline_sheet.py`, `astrid/sdk/timeline/checkout.py`, plus the two retained test files. Route every real mutation through `commitTimeline`; keep unsupported-cell and refusal predicates unchanged.

   Acceptance:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
   /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
   tests/editing_conformance/test_native_sheet_current.py

   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
   /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
   tests/packs/timeline/test_cli_native.py
   ```

2. **Scene carrier**  
   Owner: Viewing/Scene. Allowed seam: `_cmd_check`, `Checkout`, `check.py`, and the existing managed visualization executor/result path. Carry the admitted candidate and certified source through the existing executor; do not restore publication or create a new writer.

   Acceptance must use the central targeted service because this is a managed/live path:

   ```bash
   R=$(.../request-test vw-F-retired-callers-census-0358 targeted \
     --files "tests/sdk/test_scene_dispatch_contract.py") && .../wait-test "$R"
   ```

3. **R5 Runtime boundary**  
   Owner: Runtime/R5. Keep old routes as HTTP 410 `retired_route`; do not restore them. The replacement is canonical `commitTimeline`, with the existing Runtime acceptance transaction and full v2 envelope. Contract surfaces are `contract/schemas/common.json`, `contract/openapi/workspace-v1.yaml`, recorded responses, and authority tests.

   ```bash
   PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q \
   tests/test_timeline_legacy_authority.py \
   tests/test_timeline_authority_door.py \
   tests/test_timeline_shot_authority.py \
   tests/test_timeline_reference_authority.py
   ```

### Required v2 replacement shape

Each producer sends `Idempotency-Key` plus:

`api_version`, `project_id`, `timeline_id`, exact base revision/publication pair, ordered `commands`, nonempty `label`, partitioning `steps`, `merge`, `reads`, `dry_run`, and optional `source/rationale/group_id`.

Success remains `{data, receipt}` with `accepted` or `merged`, complete canonical closure/digest, normalized commands, provider-authored step patches/dependencies, `merge_mode`, head pairs, and receipt/result equality. Preview returns the same candidate data with `receipt: null`. Undo/redo use the same commit route with `timeline.inverse`, `args.publications`, optional per-publication `steps`, and fresh idempotency keys. Retired routes return 410 with no receipt/history.

### Checks performed

- Read D32 map, current reconciliation, review, PLAN, peer assignment, current source, and frozen R4 refs read-only.
- Extracted exactly 30 retained-route rows.
- `git diff --check`: PASS.
- Worktree status: clean.
- No tests, lint, typecheck, full suite, live service, browser, or original failure rerun performed, as instructed.

Blocked remains the missing ordinary Scene invocation/result carrier and unqualified retained-caller behavior.