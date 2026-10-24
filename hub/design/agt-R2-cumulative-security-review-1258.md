## Review report

Scope qualified on joined Agent `e5fa8aac0eea52d7e5cedae49cafe81e5c03b810` (tree `aeeeecd4bb8997f9ecc418f4dd52cff3936d1860`), with no source edits.

Passed:

- Author cohort: `336 passed`
- M1 structural-removal lane: `10 passed`
- Redo/fixture neighbors: `203 passed`
- Authenticated inverse restoration: `9 passed`
- Strict custody/ABA controls: `17 passed`
- Absent/null/opaque controls: `3 passed`
- Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`
- All 46 original M1 test-function ASTs unchanged
- Production caller confirmed through `inverse.py` → `_materialization_sites` and `_step_undo.py`

Direct XML evidence:

- [author336.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-security-review-1258/evidence/author336.xml)
- [m1ten.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-security-review-1258/evidence/m1ten.xml)
- [neighbors203.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-security-review-1258/evidence/neighbors203.xml)
- [inverse9.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-security-review-1258/evidence/inverse9.xml)
- [strict17.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-security-review-1258/evidence/strict17.xml)
- [opaque3.xml](/tmp/claude-0/-home/user/work/wt/agt-R2-cumulative-security-review-1258/evidence/opaque3.xml)

Open finding: M1’s `null-payload` and `null-config` positives still fail before accepted history because `_commit_patch.py:194` rejects contradictory list/null parent mirrors. The separate read-only classification identifies this as a genuine source bug; no workaround or weakened expectation was applied. Therefore this is scoped PASS only, not a green full/core claim.

Exact joined blobs include `_commit_patch.py` `620ced06…`, `_step_undo.py` `57c24639…`, `inverse.py` `b5ac471e…`, and `_doc_patch.py` `1cba1169…`.

Worktree is clean; commit message and `DONE` marker written.