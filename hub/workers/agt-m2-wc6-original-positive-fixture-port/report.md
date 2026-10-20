Implemented the bounded test-only fixture/import port in `tests/timeline/test_authoring_media.py`.

- Uses Runtime locator at exact `a0dca169…`.
- Uses `trusted_seed` for the parent fixture.
- Preserves all original positive assertions and strict narration/structural holds.
- Central lane: parent-label neighbor passed; original test reaches import/reuse, then exposes the exact remaining gap: `timeline_commit_required`.
- Local neighbors: `70 passed, 2 deselected`; preserved positives `4 passed`.
- Ruff and `git diff --check` passed.
- No full suite, product/provider/Runtime/shared-dependency changes.

Reports, handoff, commit messages, and `DONE` are written under the worker directory.