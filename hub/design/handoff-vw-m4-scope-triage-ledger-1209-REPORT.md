# vw-m4-scope-triage-ledger-1209

Applied the 2026-10-21 11:53 UTC scope-triage ruling to the two requested documentation surfaces only:

- `design/deletion-ledger.viewing.md`: closed the D08 umbrella as KEEP because the duration and host appendix rows are intentional adapters; retained the DELETED leaf evidence; kept D08a/b, D09, VW-D09a, VW-D09-LEGACY-FADE, and VW-AUDIO-STEP REQUIRED; set VW-D09b/c DEFERRED with the exact date and triage reference.
- Preserved the VW-D09b/c fallback behavior and the partial697 NON-EQUIVALENCE (697 vs 799, padding 16/697 vs 16/799, strict crossings 15 vs 16).
- Distinguished landed source deletion from the remaining VW-AUDIO-STEP/D08a/D08b Gate6 physical obligation and listed VW-D09b/c as the heavy-proof-only holds.
- `design/owner-film-differences.md`: added the bounded deferred-crop owner disclosure and exact triage reference.

Decision reference: `design/orchestrator-scope-triage-20261021T1147Z.md`.

## Verification

Commands run from `/home/user/work/wt/vw-m4-scope-triage-ledger-1209`:

```text
sed -n '1,240p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md
sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/orchestrator-scope-triage-20261021T1147Z.md
rg -n '11:53|D08 umbrella|D08a|D08b|D09|VW-D09a|VW-D09b|VW-D09c|VW-D09-LEGACY-FADE|VW-AUDIO-STEP|NON-EQUIVALENCE|heavy proof|Gate6|Broad D08 remains|D08 remains' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.viewing.md /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/owner-film-differences.md
git status --short
```

Results: required ruling/status text and preserved non-equivalence were found; the worktree status is clean. No code, build output, test suite, central test request, or physical run was used. There is no test log because this was documentation-only work.
