# App private392 cleanup-qualified launch source

## Result

Source delivery is ready for independent runner-repair review. The change is
limited to the approved private392 runner port on App source `85ae206b`:

- Added `scripts/testing/private392-http-runner.sh` from candidate
  `7a8762e05a97dbd3fdf2c188aa14292d066933c5`, retaining its exact Agent,
  Runtime, schema, 75-artifact, lock, driver, public-lock, clean-checkout,
  credential/project, outbox, and ambient-environment guards.
- Replaced the reviewed `exec` defect with a foreground Vitest child, explicit
  status preservation, an `EXIT` cleanup trap, and signal traps that preserve
  interrupt status while allowing `EXIT` cleanup.
- Added exact Python executable/import-root probes for `astrid`,
  `astrid_runtime_client`, and `runtime_protocol`. These probes use only the
  caller-supplied qualified interpreters and exact source checkouts.
- Added `scripts/testing/private392-http-runner.test.mjs`, one static/subprocess
  failure-cleanup witness. It exercises the same failure-status/trap shape and
  verifies the disposable root is removed. It performs no transport or socket
  work.

The existing private App source remains the source of truth. No generated
counterpart, `runtime.lock.json`, public HOME lock, driver, schema, Runtime,
Agent, dependency, pin, or shared install was changed.

## Exact custody

- App source: `85ae206b815381da31c229cc9107e322cb9c612f`.
- Agent: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`, parent
  `e010e6a3868e963471244491bb6672c3e4a5135e`, tree
  `2f2685d85c3f65b458795100a8045371eb19ee06`.
- Runtime: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`, tree
  `8be43e13acb436120f8a63b1a178d64c49422461`.
- Driver SHA-256: `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981`
  (unchanged).
- App lock SHA-256: `3ee0aa69fbff9faeff76a44aedc4e7fb70a69970ceec25c0fde788dbdb37d873`.
- Generated lock blobs remain the approved values:
  `44bad1f8e9df2e1e473fb6af7b10d9ed3e3cbd0e0e23e67c842328e548cb722b`,
  `54144eb6dbc27b595ca428122faea48348519958fd6aea25a47dbfd7199fd451`, and
  `8b2522dd630ea2b2b004c87acd527ad0d30f24e429ba7069b791bf3a94aa08f7`.

## Checks

All commands were run in the assigned App worktree, with no live runner:

```text
sh -n scripts/testing/private392-http-runner.sh                         PASS
node --check scripts/testing/private392-http-runner.test.mjs             PASS
node --test scripts/testing/private392-http-runner.test.mjs              PASS (1 test)
git diff --check                                                       PASS
node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0
                                                                         PASS
node_modules/.bin/tsc --noEmit --pretty false                              PASS
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
                                                                         PASS
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
                                                                         PASS (3 files, 30 tests)
```

No hosted build, browser, localhost/socket, request-test, live HTTP/Door
selector, or full suite was run, as required by the task.

## Qualified environment finding

The retained successful native/Door `10824` evidence used the exact Agent
source identity above and recorded `/home/user/work/venv-agent/bin/python` for
the Agent lane. The private392 App launch contract requires the paired
`/home/user/work/venv-runtime/bin/python` for Runtime. Both executable paths
are absent in this sandbox. `/home/user/work/venv-app2-native/bin/python`
exists, but it is not the qualified pair and was not substituted.

Therefore the live runner is intentionally **HOLD / unverified** pending one
bounded dispatcher prerequisite: provide read-only qualified Agent and Runtime
interpreters for the exact `1303ce6b` + `f8da4b6d` pair, then invoke the runner
with those explicit paths and the exact clean checkouts. Do not create or
modify a shared environment in this App worker. A child-venv request was not
made because the documented child helper provisions only an Agent child and
would not by itself preserve the required Runtime `f8da4b6d` pairing.

The existing public HOME `2c4ac180` lock remains untouched and remains a fatal
mismatch for this private runner.

