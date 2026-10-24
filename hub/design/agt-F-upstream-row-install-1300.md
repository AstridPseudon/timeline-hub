## D54a report

Installed only `agent full-upstream-25359` via guarded atomic replacement.

- Exact row: [candidate bytes](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-upstream-baseline-1254/evidence/suites.conf.candidate:1>)
- Row size/hash: `4204` bytes / `5b31f373…b20bc3c7`
- Registry pre/post: `18deaf1e…e2c9e07c` → `5b297d31…7f41520`
- Outside-row hash: `f14b6ef0…46a8efc7` unchanged
- Backup: [UTC predecessor backup](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-upstream-row-install-1300/evidence/suites.conf.pre-20261024T130218Z.bak>), hash `18deaf1e…e2c9e07c`
- Actual receipt: `atomic-single-row-replacement`

Verification passed: candidate `bash -n`, registry mode `0600`, non-symlink, exact clean Agent source `25359ed…`, Runtime `becfe6d…`, and clean assigned worktree.

No tests, full suite, or service request was run. Manager should queue exactly one `full-upstream-25359` service run. DONE marker and commit message were created.