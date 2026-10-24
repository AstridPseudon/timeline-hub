Implemented the G5 test-only fixture repair in [test_authoring_media.py](/home/user/work/wt/agt-F-document-publish-fixture-0014/tests/timeline/test_authoring_media.py:229).

- Replaced stale `fetch_bundle` monkeypatch with actual `TimelineSession.open`/`_bundle`/`commit` transport seam.
- Added full v2 request assertions and typed stale-conflict handling.
- Preserved revision/publication forwarding, refusal, and no-write assertions.
- No production files changed.

Tests:

- Targeted test: `1 passed`
- Whole file: `74 passed, 2 failed` — unrelated existing Runtime integration failures.
- Ruff: passed
- Mypy: passed
- `git diff --check`: passed
- Only assigned test file modified.

Commit message and `DONE` marker created.