## Report — FAIL_SOURCE

Reviewed `tl/agt-D86-main-shared-inverse-2333` against base `5d4ae93c83`.

Finding: the fixture appends `repeated-third` at [test_commit_runtime_shared_inverse.py:74-90](/home/user/work/wt/agt-F-main-inverse-review-2348/tests/editing_conformance/test_commit_runtime_shared_inverse.py:74), then calls `emit_document_commands`. The emitter retains `placements` in `_outside()` and rejects closure-membership changes at [emitter.py:266-267](/home/user/work/wt/agt-F-main-inverse-review-2348/astrid/sdk/timeline/emitter.py:266). Thus setup would raise before `edit.commit`; all 10 selectors are affected. This requires a semantic occurrence-creation command, not a product fix in review.

Checks passed:

- AST conservation: 5 test bodies/assertions/raises/decorators/parameters unchanged; 10 selectors preserved.
- In-memory compile and `py_compile`: passed.
- Ruff candidate and baseline: passed.
- Mypy candidate and baseline: passed.
- `git diff --check`: passed.
- Only the assigned test file differs; worktree clean.
- No pytest, service, build, or function execution run, per D85/D86 rules.

No merge requested. Recommended next step: repair the fixture setup with the appropriate semantic occurrence command, then repeat protected review and later MAIN qualification.