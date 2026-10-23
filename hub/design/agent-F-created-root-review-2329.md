## Scoped PASS — created-root stage redo

- Reviewed candidate `4387ff0c` vs `d7db17a60`; only `_root_inverse.py` and the new test differ.
- Six-line guard relaxation is safe: authenticated stage identity/range, sequential intermediate guards, closure, owner, and baseline checks remain enforced.
- No product/test edits made. Worktree clean.

Tests:

- Exact collection: 17 collected, 0 deselected, 0 strict xfails.
- Exact targeted run: **17 passed in 6.55s**.
- Ruff: passed.
- Mypy: no issues in 2 files.
- `vendor_lock.py check`: passed.
- `artifact_manifest.py --check`: passed.
- Exact path and `git diff --check`: passed.

Limits:

- Did not rerun the known four alias-reason mismatches or broader suites.
- Author capture `420390B` was unavailable/lost as stated; own durable capture is retained [here](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-created-root-review-2329/evidence/observed-capture.txt>).
- This qualifies only the candidate root redo fix, not inherited `d7db17a60` inverse behavior or whole ancestry.

No blockers. Recommended next step: queue this scoped candidate for merge; handle the separate known alias mismatches independently.