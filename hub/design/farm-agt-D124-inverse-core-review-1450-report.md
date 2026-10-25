## Report: tf-agt-D124-inverse-core-review-1450 (read-only source/core review)

**Verdict: PASS for the source/core diagnosis.** The reproducer was not re-run here, Ruff and the Python 3.11 compile were refused, and this is not product acceptance. The blocker is Runtime-owned, not Agent-owned.

### Stop event
Bash calls were refused with "This command requires approval" for:
1. `/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_d124_grouped_inverse_boundary.py`
2. `/usr/bin/python3.11 -I -c "py_compile …"` on the new test file, into TMPDIR
3. `/usr/bin/python3.11 -I /tmp/w-6805b6cd51/ast_check.py <test file>`

Per the brief's STOP rule I did not retry or work around these. Their results are NOTRUN.

### Checks run and results
- Base check: worktree HEAD = `a0d8398604780c01cb4213e91af1fedb49b17afd`.
- `git diff --name-status a4e016… a0d8398…` → only `A tests/sdk/test_d124_grouped_inverse_boundary.py` (135 insertions). Product, lock, native seed and contract are unchanged.
- `git diff --check` over the same range → exit 0.
- Product file SHA256s (10 Agent files and `runtime.lock.json`) match the source manifest.
- Regression file SHA256 `3edecac0…51ca` matches the manifest, the publication, and the base blob.
- Handoff SHA256s match `publication.json`: root-cause `15ba548d…`, validation `f8b25e93…`, source-manifest `c1c04674…`.
- Runtime pin `5e9ad1c6` (tree `de2954a0`), read via `git show` from `/home/user/work/runtime`: `timeline_commit_auth.py` `72d4611d…`, `service.py` `7277fc12…`, `timeline_commit_store.py` `7d307566…`. All match the manifest.
- Test-file helpers and Runtime methods all exist at the pin, and the file has no skip/xfail/weakening markers in source.
- **Not run:** the tiny 3-case pytest. The dependency path `/home/user/work/agent-runtime-projection-0856/site-packages` does not exist, and `/home/user/work/venv-agent-typecheck-v2` does not exist. Per the brief I did not acquire them. The author's recorded result (2 PASS / 1 RED) is not independently reproduced.

### Source trace (confirmed by reading)
- Agent `_step_undo.inverse_stages` 329–352 yields the whole grouped birth step as one group. Agent `inverse.apply_inverse` 1132–1187 records track → occurrence → shot in reversed order, with one `inverse.stage` binding whose native range covers the full group. Agent `_commit_patch` 474–492 and 564–593 project the stage boundaries.
- Runtime `_inverse_stage_boundaries` (5e9ad):
  - 1450–1472: the root removal for `occurrence:child` removes the occurrence from `native_image`.
  - 1473 and 1489: the sequential check for the earlier child-track write runs before that removal and passes.
  - 1755–1757: full payload equality passes.
  - 1764–1765: the final per-write lookup of that same track write runs on the post-removal image. `site` at 154–156 then raises "provider occurrence alias is outside its boundary". This is the only path that emits that message.
- The ungrouped comparators avoid it. The ungrouped birth stage has only root writes, so it hits the `continue` at 1759–1763. The ungrouped child-track inverse keeps the occurrence alive at stage end, so 1764 resolves.

### Findings
- **F1 (Runtime):** the blocker is `timeline_commit_auth.py` 1764–1765, the final lookup of earlier child-write aliases after owner/root removal. The Agent diff does not contribute.
- **F2 (reasoning only):** that 1764 is the sole failing guard is source-derived, not executed.
- **F3:** I did not re-open the plan's exclusion of Agent-side alternatives (split step, move boundaries, rewrite refs). The Runtime effect-site alternative is blocked by the row-preserving check at 1514–1534, as the handoff states.
- **F4 (minor):** the handoff cites "site155–156"; the actual lines are 154–156.
- **F5 (minor):** a case name changed between the first and final test runs (`inverse` → `inverses`). The final file is what the custody run used.

### Evidence files
- `…/orch/workers/tf-agt-D124-inverse-core-review-1450/evidence/review.md`
- `…/orch/workers/tf-agt-D124-inverse-core-review-1450/evidence/validation.json`
- `…/orch/workers/tf-agt-D124-inverse-core-review-1450/BLOCKED` (partial-block reason)

SHA256 of the two evidence files is not computed, because Bash stopped after the refusal.

### Recommended next steps
- Runtime owns the correction at 1764–1765 (evaluate each write's after-state at its sequential boundary, or resolve through the sequential image). It must keep the C0 §§2/5/7 provenance, membership and owner/digest checks.
- When approval is available, run in order: scoped Ruff, Python 3.11 compile, and the tiny 3-case test once the projection dependency is present. Expect 2 PASS / 1 FAIL, and report it honestly.
- No commit message was written, since the worktree has no changes from this review.
