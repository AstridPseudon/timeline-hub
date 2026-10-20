# Report

Decision: **APPROVE** the bounded consumer seam only.

Candidate: `6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214`  
Tree: `32dc0de053ffb98d718077a111994181ae03ea15`

- Read-only review confirmed shared config/vector/extent/fact delivery across still, Player, and client-render paths.
- Per-clip invalid-cap fallback is preserved.
- 4000/4500 behavior and serialization stripping are covered.
- Public13 root probe passed at frames 105/119/120.
- `git diff --check`: passed.
- No package, lockfile, pin, dependency, product source, branch, or ref changes.

Known constraints: 10 pre-existing App2 TypeScript diagnostics and 8 MAIN574 label failures remain separately owned. No whole-project `tsc`-zero or full-suite claim.

An initial probe used an incorrect frame-119 opacity oracle; the corrected boundary probe passed.

Artifacts: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-complete-cap6b7-consumer-gate/report.md), [COMMAND.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-complete-cap6b7-consumer-gate/COMMAND.md). Worktree remains clean; `DONE` and commit message were written.