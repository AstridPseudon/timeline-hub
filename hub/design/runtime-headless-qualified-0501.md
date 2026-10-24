## Result: FAIL

- Qualification: 12 passed, 1 failed, 13 total.
- Failure: `test_cas_correct_republish_after_reading_the_head_is_accepted`
- Actual `created` order begins with `track`; retained expectation requires `asset, clip, track`.
- Source owner: Agent `astrid/sdk/timeline/_doc_patch.py` allocation ordering. No production/test changes or rerun made.

All other 12 nodes passed, including the four scoped-row parameters: `timeline_references`, `timeline_shots`, `snapshot`, and `dependency`.

Provenance:

- Runtime: `66657fda…`, tree `51aa4532…`
- Agent archive: `9cd3dbe…`, tree `57f0231d…`
- Module origins verified from the archive and current Runtime worktree.

Checks passed:

- `ruff check tests/test_timeline_headless_overwrite_refused.py`
- `git diff --check`
- Worktree clean.

The brief’s Agent hash includes an extra `3`; the valid object matching the requested tree was used. Complete boundary capture was unavailable because the retained test has no pre-assertion capture seam; this is documented in [qualification-evidence.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R5-headless-qualified-0501/qualification-evidence.md). DONE marker and commit message were written.