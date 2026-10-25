# D127 report

- Verified exact four-source tuple and clean pinned App checkout.
- Attached existing `/home/user/work/app/node_modules` via ignored symlink; `tsx` resolved from actual launch root.
- No source preflight or original P2 body was requested.
- Admission blocked: 5,144,580,096 bytes initially; final check 5,136,687,104 bytes, below the 5,200,000,000-byte floor.
- Durable plan, service IDs, and terminal receipt remain absent.
- Wrote bounded evidence to `evidence/`, `notes/`, `BLOCKED`, and commit message path.

Checks passed: JSON artifact parsing, exact Node/tsx resolution, pinned checkout integrity, clean worktree, `git diff --check`.

Next step: recheck storage; only run the exact existing `p2 --submit` command once the admission floor is met.