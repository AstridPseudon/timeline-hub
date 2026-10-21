# Handoff: Scene producer inventory audit

## Result

No code or inventory-document changes were needed. The current producer files remain within the fixed giant-file rationale tolerance, and the existing private helper/resource arrangement is sufficient.

Scoped counts (`wc -l`, threshold 1,200, allowed snapshot drift +/-50):

| File | Actual | Rationale | Delta | Result |
|---|---:|---:|---:|---|
| `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py` | 1,931 | 1,917 | +14 | within guard |
| `astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py` | 2,038 | 2,015 | +23 | within guard |
| `astrid/packs/rendering/rendering/renderers/remotion/run.py` | 1,800 | 1,796 | +4 | within guard |

The approved `ef7f39af3` commit changes `composed_frame.py`, `root_preparation.py`, Remotion `run.py`, and `test_scene_source_carry.py`; it does not change `filmstrip_cards.py` or `filmstrip_execution.py`. The latter two were checked because they are the relevant inherited Scene producer surfaces. The existing rationale entries accurately describe their seams. `pack.yaml` already declares `_audio_cache.py`, `filmstrip_cards.py`, and `filmstrip_execution.py` as implementation resources, so no new public API or pack declaration was added.

## Tests

- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale tests/packs/rendering/test_scene_source_carry.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py`
  - **1 failed, 106 passed, 20 errors**.
  - The one failure is inherited/unrelated: `astrid/sdk/timeline_sheet.py` is 1,466 lines while its existing rationale snapshot says 1,313 (+153, beyond the +/-50 guard). This task does not own that file.
  - The 20 errors are native source-carry fixture setup failures because the shared Remotion peers (starting with `react`) are absent. No install or shared dependency mutation was attempted.
- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_scene_source_carry.py -k transport tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py`
  - **21 passed, 105 deselected**.

No full, browser, live-socket, install, or bulk-copy suite was run. The worktree is clean; no producer behavior, sparse-frame list, dense query-only rows, or cache-minting semantics were changed.

## Decisions and next steps

- No extraction: the observed producer-file drift is within the unchanged 50-line guard, and extracting code solely to reduce a still-valid snapshot delta would add risk without a truthful boundary.
- The orchestrator should separately route the `timeline_sheet.py` inventory refresh/split decision to its owner. Native source-carry qualification needs the shared Remotion peers restored by the central environment owner; do not install them from this worker.
