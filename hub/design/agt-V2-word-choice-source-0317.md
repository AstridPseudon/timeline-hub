Implemented F-D86 exact word-choice replay repair.

- Added namespaced `word_anchors` preservation through mirrored parent representations.
- Candidate/stale validation now uses authenticated `binding`; legacy fallback remains unchanged.
- Only allowed production files changed.

Checks:

- Ruff: passed (parent and candidate).
- Mypy: passed on both files.
- AST/in-memory compile: passed.
- `git diff --check`: passed.
- Tests/fixtures/services: not run per brief.

Independent protected review and MAIN originals remain for orchestrator follow-up. Commit message and `DONE` marker created.