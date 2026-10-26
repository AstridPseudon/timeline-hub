# D141 full/pristine handoff

This is a ready-but-gated handoff, not an execution receipt. The App working-tree content was restored to base 5696769dfca056676cde1ab46d8bc94354b3a44a, tree 0748df404125114a0f68b701fa76f43abd3fc79a, with zero base-relative repository diff paths. The branch HEAD remains the prior evidence-only prep commit until the harness records cleanup.

## Gate

Use /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/D141-cut-tuple.md as the cut source. Its frozen App comparator is commit 7ca61bb3280beca21d98a854af266a382f7ce5df, tree 974de7cd08900872eeb0bd6f6004d44323e01fab. The final U3 App integration head and recorded MAIN GO are pending. Do not dispatch either body until both are recorded and all cut heads are frozen.

The retained U3 record reports a linked-worktree metadata permission failure with six unresolved paths. That is a manager/controller prerequisite, not a D141 execution result.

## Normal App full

The existing registration at tests/suites.conf:69 is exactly:

npm test -- --maxWorkers=3

Use the ordinary receiving checkout through the existing service:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app full

The alternative existing worker-receipt route is:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <final-u3-worker-name> full

The worker metadata must identify repo=app, its ordinary worker checkout, and the clean final qualified source head/tree. Follow the returned result ID with the existing wait-test command. Do not create a new request row, wrapper, or receiving framework. The integration:app route is /home/user/work/app; it is not the frozen pristine checkout.

The supported toolchain is Node from /opt/node20/bin with PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin, npm 10.8.2, and package engine >=20.19.0. Bind private per-run TMPDIR, npm cache, XDG/Vite/Vitest cache, and durable result/D66 paths as listed in recipe.json; browser output is private per-run if the actual receiver invokes browser tooling, while /opt/pw-browsers is the read-only browser install. The service wrapper itself owns the snapshot, result, log, summary, status, exit, and D66 paths; no shared cache or node_modules may be mutated.

## Frozen pristine comparator

The comparator must run in the existing /home/user/banodoco/reigh-app checkout only after guards pass:

- HEAD exactly 7ca61bb3280beca21d98a854af266a382f7ce5df;
- HEAD^{tree} exactly 974de7cd08900872eeb0bd6f6004d44323e01fab;
- git status --porcelain empty;
- unset ASTRID_PUBLIC_CHECKOUT, ASTRID_APP_DIRECT_DIST, and NODE_PATH;
- use Node20 PATH and the same npm test -- --maxWorkers=3 suite family;
- use the private comparator temp/cache/output paths in recipe.json.

The comparator is Farm/Main-owned direct execution from that existing checkout, or an already-registered worker metadata route pinned to exactly that commit/tree. request-test integration:app is not a valid pristine receiver. No previous pristine receipt exists in this packet; no comparator result or outcome is claimed.

## Reconciliation and production boundary

Parse the normal and pristine logs separately. Keep Vitest Test Files and Tests counts separate from test:node reporter counts. Reconcile by result ID: report files, tests, authorized expected failures, unexpected failures, exit code, and source/graph postflight guards. Historical normal receipt app-m4-agentchat-fixed-current-one-full-r36-app-full-published014-agentchat-fixed-r36-07d86990c-1021075701-20810 records 1520 Vitest files, 19454 passed, and 3 authorized expected failures; it is context only, not D141 evidence. Do not invent a pristine receipt or add the historical counts to the Node counts.

The production caller and C0 request/reply contract are unchanged: preserve the full request scope (base, commands, label, steps, reads, merge, idempotency, dry-run, source, rationale, group id) and accepted/merged/conflict/invalid/preview shapes, including canonical closure, receipts, records, bindings, history, undo, conflict/head, invalid code/path/hint, and preview null-receipt semantics.
