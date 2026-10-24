## Report

Implemented only the exact `b4f8471a9` fixture leaf in `tests/sdk/test_timeline_restructure.py`.

- Public exact revision/publication reader wired with pagination, inspection, and revision endpoints.
- Original assertions and test bodies preserved.
- Function hash changes limited to `restructure_runtime` plus `list_timelines`; assertion hash unchanged.
- No product code or shared dependencies changed.

Tests:

- Collection: 48 tests collected.
- Fixture/public-reader controls: 7 passed.
- Public preflight, native pin controls, genuine anchor: 3 passed.
- Session-pair suite plus controls: 9 passed.
- Restructure/connection representatives: passed.
- Normal-publish representative: failed before any write because `RemoteTimelines._native_projection` imports renderer code under the unchanged `no_renderer` guard. Classified as separate product boundary failure.
- Ruff baseline: 2148 current / 2148 baseline.
- Mypy baseline: 1911 current / 1911 baseline.
- Vendor lock, artifact manifest, compile, and `git diff --check`: passed.

The prior broad 87-test run remains unqualified due to its timeout with partial `F` output; it was not repeated.

Commit message written and `DONE` marker created.