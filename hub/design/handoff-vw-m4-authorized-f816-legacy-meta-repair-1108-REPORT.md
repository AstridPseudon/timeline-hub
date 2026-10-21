# Authorized f816 legacy metadata repair — 2026-10-21

The exact target `/home/user/work/wt/vw-m1-ssr-snapshot` passed fresh eligibility checks: clean HEAD `f8164bef73215272562c4d6974acadbd82c2898a`, tree `4946dfa80999f3f9d828840c701544a67c8fe2b`, and ancestor of Agent integration HEAD `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`. No active worker, process/cwd/fd, lease, queued/running target test, or current active brief claimed the graph.

The original 631-byte legacy metadata was backed up at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m1-ssr-snapshot/meta.before-worktree-repair-20261021T1108Z.bak`

Only this field was appended:

`worktree=/home/user/work/wt/vw-m1-ssr-snapshot`

Only our obsolete `vw-m1-ssr-snapshot` line was removed from `lead/keep-worktrees`. No fa25 lease or protected scene-host/current pin/graph/dist/snapshot/report/media path was touched.

Exact approved command:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/recycle vw-m1-ssr-snapshot`

Result: `recycled vw-m1-ssr-snapshot`, exit 0. Post-check: target absent, recycler marker present, branch `tl/vw-m1-ssr-snapshot` preserved. Estimated allocated bytes freed: **505909248**.

No product tests, central suite, browser, render, install, socket, or bulk scratch operation was run.
