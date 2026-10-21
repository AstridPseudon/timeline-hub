# ap2-m2-selected-clean-keeper-main-port-1120 report

## Result

Corrected the selected1110 MAIN packet's custody and portability data. The
packet is **HOLD for MAIN execution**, not an actual result.

- Rebound the source identity to App commit
  `0cc2583aaf07e89190b9344b5ac82849d6279586` / tree
  `320e74a93676c781e83885b86ec237b4a1465d80`.
- Replaced dirty/wrong `/home/user/work/app` custody with the real clean
  detached keeper `/home/user/work/wt/app-pin-0cc2583a`.
- Added the empty, non-symlink protected lease in `design/`.
- Exported the runner, source helper, parent helper, selected P1 driver, and
  lease to absolute `design/` paths; the packet contains their computed hashes.
- Made only path/data rebinding changes: exported helpers accept explicit
  graph/archive paths, and the runner uses the exact keeper and exported
  helper/driver paths. Existing runner966/currentdcd4 controls remain intact.
- Did not export the 287 MB graph archive, any install, or any large artifact.

## Exact tests and results

All commands were run read-only against the assigned App worktree or the
explicit shared artifact paths. The assigned worktree remains clean.

```text
sh -n design/ap2-m2-selected-clean-keeper-main-port-1120-runner.sh                         PASS
sh -n design/ap2-m2-selected-clean-keeper-main-port-1120-source-common.sh                  PASS
sh -n design/ap2-m2-selected-clean-keeper-main-port-1120-parent-media-central.sh           PASS
sh -n design/ap2-m2-selected-clean-keeper-main-port-1120-selected-p1-driver.sh             PASS
keeper HEAD/tree/clean checks                                                               PASS
exported artifact hash inventory and packet consistency                                     PASS
```

One existing cheap preflight/control was run after all binding edges were
audited, against an exact clean detached source clone at the selected commit,
with the existing local Node22/public13 graph. Exact command shape:

```sh
env -i HOME=/root LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin \
  NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 \
  NORMAL014_LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph \
  NORMAL014_LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar \
  APP_KEEPER_ROOT=/home/user/work/wt/app-pin-0cc2583a SELECTED_FINAL95_MODE=preflight \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-runner.sh "$EXACT_CLEAN_SOURCE"
```

Observed result: **PASS**, including all 12 aggregate checks and exact
Playwright `1 test in 1 file` list1. No browser, Vite, Runtime, socket,
service, build, install, full suite, or actual was run. The temporary source
clone was removed after the control.

## Decisions

- Kept the runner's Node `v22.22.0` guard and public13 graph/archive guards.
  The task explicitly forbids weakening version, effective77, source,
  credential, receipt, zero-test, or retention controls.
- Kept the graph/archive external because the graph is an install artifact and
  the archive is 287 MB; the exported helper now takes verified MAIN path data
  without transferring the graph.
- Used `/home/user/work/wt/app-pin-0cc2583a` as the protected keeper because it
  is the verified clean detached exact checkout. `/home/user/work/app` was
  observed dirty and at `92c30b...`, so it is excluded.

## Blocked / remaining prerequisites

MAIN is blocked from the actual. Recorded MAIN has Node `20.19.4`; local
`/opt/node22/bin/node` is `22.22.0` but is not MAIN proof. The manager must
provide and independently verify:

1. a MAIN-qualified Node `22.22.0` executable, or a reviewed runner/graph pair
   proven against the honest MAIN toolchain; and
2. a physical, symlink-free public13 graph with the exact archive SHA,
   Composition 0.0.13, Vite 5.4.21, Vitest 4.1.5, Playwright 1.60.0, and 77
   regular archive members, without resolving through `/home/user/work/app/node_modules`.

The packet now requires an env-i Node20.19.4 honesty check before any runner
body, then a separate Node22.22.0/graph proof. The Node20 check cannot satisfy
the retained runner's Node22 guard and therefore leaves the packet HOLD.

Then run the env-i MAIN preflight in
`run-on-main-app2-selected-seed.md` from the central service's captured clean
source root, with the exact keeper and exported runner. Only after it passes
may the manager independently authorize the one guarded actual. No actual was
submitted here.

## Live callers and next steps

Changed live callers: **NONE**. No product source, test, spec, `.gitignore`, or
repo `design/` file was modified. Next step is manager review and MAIN-only
preflight; do not use this local Node22 control as MAIN evidence.
