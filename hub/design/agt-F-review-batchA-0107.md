## Review report

No source changes; worktree is clean. Separate verdicts:

- **Scalar: PASS** — genuine `value_at(root, physical, path)` fix; compile, Ruff, diff-check, and Python 3.13 mypy passed. Default mypy had the identical NumPy stub environment error for baseline/candidate.
- Scalar merge receipt verified: `tl/integration` → `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`; SHA-256 matched author candidate.

- **Owned move: FAIL** — `_commit_parent_variant` always uses `emit_document_commands`, but `delete_film` removes `parent['occurrences']`; the emitter explicitly rejects managed-membership changes. No merge requested.

Exact verdicts:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-review-batchA-0107/evidence/verdictscalar.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-review-batchA-0107/evidence/verdictownedmove.md`

Checks run: in-memory compile, Ruff baseline/candidate, `git diff --check`, default mypy baseline/candidate, and `mypy --python-version 3.13`. No pytest, fixture/service execution, browser, build, or full suite.

Next step: repair the owned membership baseline through the registered semantic path, then obtain a fresh protected review.