## Report

Implemented the bounded `79b33f8a..77945bb6` port onto `3f770a45`:

- Removed publish’s duplicate accepted-history journal append.
- Routed sheet retained-basis lookup through verified Runtime cursor pagination.
- Preserved local draft journal, outbox, undo/redo, and recovery behavior.
- Added page-two pagination coverage.

Files changed: [publish.py](/home/user/work/wt/agt-m2-ag01-current-cut-gate/astrid/sdk/timeline/publish.py), [revisions.py](/home/user/work/wt/agt-m2-ag01-current-cut-gate/astrid/sdk/timeline/revisions.py), [timeline_sheet.py](/home/user/work/wt/agt-m2-ag01-current-cut-gate/astrid/sdk/timeline_sheet.py), and focused tests.

Tests:

- Focused journal/history/sheet/recovery suite: `107 passed`
- Revision/history suite: `32 passed`
- Central Runtime lane: `35 passed, 5 failed`; the requested retained-history test passed. Failures were unrelated retired direct shot-write tests in `tests/stage1/test_runtime_client_cutover.py`.
- `git diff --check`: passed.
- No full suite requested.

Remaining consumers found by `rg`:

- Runtime accepted-history readers: `astrid/sdk/timeline/sync.py:156`, `astrid/sdk/timeline_elements.py:52-60,149-185`, and core inverse/history paths.
- Local journal writers remain intentionally in `transaction.py` and `checkout.py` for unsent draft/recovery behavior.

Next step: qualify or migrate those remaining accepted-history readers before any further deletion sweep.

Commit message and `DONE` marker written.