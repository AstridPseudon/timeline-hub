# Report — F-authoring-ABA whole-path ownership

Source-cause verdict: PASS. Product qualification: FAIL/unqualified.

- Native shared-occurrence refusal is Agent-owned at [`inverse.py:31-112`](/home/user/work/wt/vw-F-authoring-ABA-whole-path-review-0638/astrid/sdk/timeline/inverse.py:31) and [`_command_state.py:290-367`](/home/user/work/wt/vw-F-authoring-ABA-whole-path-review-0638/astrid/sdk/timeline/_command_state.py:290). The inverse rewrites historical `item_id:item-1` to the placement-local `item_id:shot-item-placement-…`. Runtime correctly rejects this at `timeline_commit_auth.py:1160-1161`: the site matches neither authenticated native sites nor effect sites. Retaining the historical spelling would fail Runtime’s sequential observation check because that path is absent from the current published image. Current Agent records cannot satisfy both guards with the unchanged carrier.

- Ordinary shared-media refusal is Runtime-owned. Agent preserves the shared source and authenticated `owners: [occ-a, occ-b]`. Runtime’s [`timeline_commit_auth.py:1332-1334`](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1332) requires the inverse successor to be absent before and the retained source to be absent before; the retained sibling keeps the source root reachable, violating that turnover assumption. This conflicts with C0c’s retained-shared-root rule. Do not weaken the strict guard.

Trace confirmed through `capture_occurrence_swap_media` (`native_occurrence_media_commands.py:287-293`), Agent commit capture (`commit.py:1192-1217`), inverse/coalescing/materialization, private sequential capture, and Runtime validation (`timeline_commit_auth.py:2140-2150`, `2460`).

Tests:

- Mandated diagnostic:
  `...pytest ... tests/editing_conformance/test_authoring_item_observation_boundary.py`
  → **4 failed, 85 passed**. The four visible failures are the intended positive shared-occurrence controls.
- Single-occurrence native and ordinary-media Runtime validation controls → **PASS**.
- Source-copy production inverse:
  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ... test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo`
  → **1 passed**.
- Ruff → failed only on diagnostic-test import ordering (`I001`, line 129); no source edits made.
- Mypy → **pass**.
- `git diff --check` → **pass**.

Agent SHA: `71e8231debe39f1be574a9ed4a40537409e889ef`  
Runtime SHA: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`  
Frozen R4 refs inspected by SHA; no checkout or edits. Sol0631 final report was not published. Original11466 remains FAIL; product merge remains FAIL/unqualified.

No repository source changes were made. Commit message and empty `DONE` marker were written.