Created [m2-group-ownership.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-group-ownership.md).

Findings: raw groups survive the authoring codec, but canonical graph/projection behavior differs; App serialization drops unknown group fields. Exact row-order restoration and created-track batch undo need shared inverse work.

Recommends explicit Agent/App approval before reusing the existing parent group array. The three `it.fails` fixtures remain unchanged.

Both offline probes passed, exit 0. Exact commands, results, limitations and next steps are in [REPORT.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-audit/REPORT.md). Repository suites and browser/live publication were not run.

No product/test changes; Agent worktree clean. Commit message written.