Implemented the reviewed dead-inspector deletion on `490c10ac`.

- Removed 5 files / 353 lines, including HTML viewer, assets, pack declarations, and private tests.
- Verified no remaining code callers; public `inspector_navigation` and filmstrip paths remain.
- Updated Agent ledger/STATUS evidence only.
- Created `commit-msg`, `commit-msg.txt`, and `DONE`.

Tests:

- `pytest ...test_inspector_navigation.py ...test_timeline_filmstrip_cards.py ...test_timeline_filmstrip_execution.py ...test_pack_yaml_schema.py ...test_pack_rendering_extensions.py ...test_pack_discovery.py` — **125 passed**
- `pytest ...test_pack_layout_contract.py ...test_timeline_visualize_pack.py ...test_timeline_inspection_contract.py` — **58 passed**

No full, pixel, geometry, crop/statistics, or timing-evaluator tests were run. Viewing can mark `VW-DEAD-INSPECTOR` deleted after the harness provides the merge SHA.