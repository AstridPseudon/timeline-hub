## F-D86 source review

- **PASS_SOURCE:** Candidate commit `9e88f5ba09` matches required SHA:
  `3e225883044678e0af68867e2873faf988bf10090d7d17898d6d1092d3a635db`.
- Candidate AST compiles in memory; diff is limited to `native_word_anchor_fixture.py`.
- Verified bootstrap FPS `30`, exact authored rational FPS patch, guarded `doc.patch`, half-open/exact timing flow, source/pin conservation, and current Agent/Runtime validation paths.
- Original semantic failures remain separate; no blanket closure or source changes applied.
- Worktree remains clean; exact candidate boundaries are unapplied.

Checks:

- `git diff --check`: passed.
- Ruff baseline: passed, `current=2143 baseline=2143`.
- Mypy: blocked by environment (`types-PyYAML` missing; NumPy stubs require Python 3.12).
- No pytest, collection, fixture execution, service, browser, or full-suite runs performed per task constraints.

**FAIL_SOURCE:** None found within the bounded static review. Runtime functional acceptance remains unverified by this worker.

Created the required commit message and empty `DONE` marker.