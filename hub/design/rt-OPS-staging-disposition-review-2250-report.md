# D139 OPS staging disposition review

**Assessment: `PASS_ASSESSMENT`**  
**Disposition: `UNAPPLIED_HOLD` / `FAIL_SOURCE`**

- Verified candidate `25f311f8` is exactly `9524356` plus a README-only qualification delta.
- `drop_staging.py`, executable launcher, and all 14 tests are byte-identical; launcher remains `0755`.
- Confirmed all five residual findings remain unresolved:
  archive replacement, worker detachment, late lease, partial fallback deletion, and evidence replacement.
- Reused authentic evidence: 14 baseline tests PASS; five private subprocess controls remain RED (5 failures). No tests were rerun.
- Static checks passed: AST parsing, hash/mode custody, `git diff --check`, and clean worktree.
- No installation, real cleanup, acquisition, full suite, or source/test modification performed.

The hold is correct. The current worker `flock` is advisory and is not shared by lifecycle, lease, evidence, archive, and cleanup writers. Safe implementation requires either a cross-writer exclusion protocol held through final deletion or a retained recovery copy for fallback. This is outside the current source-only scope and requires an orchestrator contract decision regarding same-UID concurrency guarantees.

Evidence written to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-staging-disposition-review-2250/evidence/`

Commit message and `DONE` marker were prepared.