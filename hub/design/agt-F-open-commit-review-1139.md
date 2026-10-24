PASS — independent no-weakening review.

- Reviewed commit `50dd32d5cef2bef9dd10e4e7b824a39558c91fb4`, tree `bef976a8d49480a47891023673123bacd5ca0116`.
- Blobs:
  - `test_timeline_open_commit.py`: `5f853095...`
  - `test_timeline_open_commit_v2.py`: `ad1d1193...`
- Only the two assigned files changed. Publication mappings use provider/peer-head pairs and preserve exact-pair validation; production `timeline.open()` exercises `TimelineSession`.
- All 23 test ASTs, parameters, decorators, and assertions preserved. Only two intended setup assignments were added.

Evidence:

- Pytest: `42 passed in 5.69s`
- Ruff: scoped diagnostics `22 → 22`, identical; repository baseline `2143 → 2143`
- Mypy: `1902 → 1902`
- `git diff --check`: PASS
- Worktree clean; no product, runtime, schema, pin, or shared-helper changes.
- No full/HTTP/browser suite run.