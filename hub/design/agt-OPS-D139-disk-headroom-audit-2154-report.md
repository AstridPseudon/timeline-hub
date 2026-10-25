# D139 audit report

- Result: `finite_no_eligible_normal_cleanup_candidate`
- Available: `5,310,427,136` bytes
- Required: `5,905,580,032` bytes
- Deficit: `595,152,896` bytes
- Source-worker estimate: `200,000,000` bytes, explicitly unverified; residual deficit `395,152,896` bytes.
- Eligible candidates: `0`

Excluded candidates included dirty merged worktree `agt-G2-open-commit`, protected KEEP source `agt-F-final-source-join-0816`, active suite bench `3b5cb...`, young registered bench `3e163...` (~22 minutes old), protected d22/f1012 environments, and previously refused runtime targets. No refusal was retried or bypassed.

Evidence recorded at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-OPS-D139-disk-headroom-audit-2154/evidence/`

Validation performed:

- `df -B1 /home/user/work`
- bounded top-directory `du -sx -B1`
- worktree, queue, bench-index, lease, and registration inspection
- limited `/proc` cwd/fd checks
- `jq empty` on JSON evidence
- worktree `git status --short`: clean

No tests run, per the audit-only brief. No operational mutation occurred. Commit message and `DONE` marker were written; manager review is required before any guarded cleanup route.