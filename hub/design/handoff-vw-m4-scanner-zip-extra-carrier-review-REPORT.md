Decision: **REQUEST CHANGES**.

Found two carrier gaps:

- Symlinked source parents are followed.
- Destinations are unbounded; `SHA256SUMS` is accepted before checksum generation and then overwritten.

Created the minimal UNAPPLIED replacement amendment:

[delivery-build-owner-scanner-extra-review.unapplied.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-zip-extra-carrier-review/delivery-build-owner-scanner-extra-review.unapplied.patch)

Report and commands:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-zip-extra-carrier-review/report.md)
- [COMMAND](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-zip-extra-carrier-review/COMMAND)

`bash COMMAND`: passed private checks and reproduced the original gaps. Approved scanner/instructions were byte-identical. Worktree remains clean; no full build or suite run. `DONE` and commit message were written.