# D141/F pristine App receiver handoff

This packet prepares one exact source receiver. It is not a test receipt and carries no proof credit.

## Receiver

The existing worker metadata route is:

```text
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D141-pristine-receiver-0007 full --no-cache
```

Then use the returned id:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test <returned-result-id>
```

The receiving worktree is `/home/user/work/wt/app-D141-pristine-receiver-0007`, pinned at commit `7ca61bb3280beca21d98a854af266a382f7ce5df`, tree `974de7cd08900872eeb0bd6f6004d44323e01fab`, and clean. Its package, package-lock, and runtime-lock hashes match the published frozen source manifest.

The existing App full suite is `npm test -- --maxWorkers=3`. Its complete scope is the package's `test:app` Vitest command (the four existing checks followed by `vitest run --config config/testing/vitest.config.ts`) and its `test:node` command (the pinned serial `node --import tsx --test` file list and skip-guard reporter). No new suite or wrapper is involved.

The supported local toolchain observed read-only is `/opt/node20/bin/node` `v20.20.0` and `/opt/node20/bin/npm` `10.8.2`; the package requires Node `>=20.19.0` and declares `npm@10.8.2`. `node_modules` resolves to the shared `/home/user/work/app/node_modules`, which must remain read-only. Presence is not dependency-readiness proof.

The service owns durable result paths under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/<result-id>/` (`request`, `status`, `exit`, `summary`, `log.txt`, `d66`) and the test snapshot `/home/user/work/wt/.test-<result-id>`. Actual dispatch must bind private temp/cache/output paths; no shared cache, install, browser, or node_modules mutation is permitted.

## Comparator and gates

The pristine comparator must separately guard `/home/user/banodoco/reigh-app` for the same commit, tree, clean status, package/lock hashes, Node20 path, and `npm test -- --maxWorkers=3`, with `ASTRID_PUBLIC_CHECKOUT`, `ASTRID_APP_DIRECT_DIST`, and `NODE_PATH` unset. The live checkout is currently clean but fails those source pins, so it is a finite missing input. Do not check it out or adapt source in response.

Do not dispatch either body until the final U3 App head, all cut heads, and MAIN GO are recorded. Reconcile Vitest and Node results separately by result id and retain the production C0 v2 request/reply contract unchanged, including accepted/merged/conflict/invalid/preview fields and canonical receipt/history/undo data.
