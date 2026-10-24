## Report

Implemented renderer-free SDK timeline reads.

- Removed renderer timing enrichment from `RemoteTimelines._native_projection`.
- Added no-renderer public-read regression.
- Exact caller confirmed: `publish.py:116 → sync.py:152 → store.py:415 → remote.py:1287 → remote.py:1199`.
- The actual defect was in `astrid/sdk/remote.py`, so `_remote_timeline.py` required no change.

Tests:

- Facade/save-core: `46 passed`
- Exact shared fixture normal-publish selector: `1 passed`
- Authenticated pair/foreign/wrong-scope/parent/shared controls: `8 passed`
- Mypy: `1911/1911`
- Focused Ruff: passed
- Ruff baseline: `2147` current vs `2148` baseline; improvement only, baseline unchanged.
- Vendor lock, artifact manifest, and `git diff --check`: passed.

Known unrelated failure: stale helper fixture lacks `publication_id`; preserved and not modified.

Commit message and `DONE` marker created.