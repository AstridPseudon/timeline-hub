# private392 approved connector real gate

## Result

PASS. One authentic App HTTP/Door integration test ran after the independent
connector-custody approval at `4e0454f20085f0268b747ac1c572c0f3a05b40be`.
The App branch was clean at `4e0454f20` (`c500c0d53d9eba5c34922148089cfb28967ec5c3`)
and already contained the settled two-line source change: Door-bound primary
providers have no browser bearer token; the direct Runtime actor provider keeps
its token unchanged. No source/assertion changes were made for this gate.

## Preflight

Passed before the central run:

- producer lock: `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d`
- exact Agent pin/tree: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50` /
  `2f2685d85c3f65b458795100a8045371eb19ee06`, parent `e010e6a3868e963471244491bb6672c3e4a5135e`
- exact Runtime pin/tree: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414` /
  `8be43e13acb436120f8a63b1a178d64c49422461`
- clean Agent and Runtime checkouts; qualified `/home/user/work/venv-app2-native/bin/python`
- imports resolved under the exact Agent/Runtime checkout roots; ambient `PYTHONPATH`,
  `ASTRID_PUBLIC_CHECKOUT`, and `ASTRID_APP_DIRECT_DIST` were unset
- shell syntax: `sh -n scripts/testing/private392-http-runner.sh`
- driver digest: `sha256:54aa8bf25dee747499ccc3a3f15ebc1c61e95e6cb90c9ab72077d827ae67bd3a`
- Runtime artifact custody: 75 artifacts, manifest/version, bundle, component
  manifest, health schema, and Agent/Runtime schema equality all matched

The runner's exact Node custody probe could not be run locally because this
sandbox rejects Node-spawned `git` with `EPERM`; the equivalent shell
`git show`/hash custody checks passed. The central runner executed its own
authoritative custody probe successfully.

## Central test

Exact request:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-private392-approved-connector-real-gate ap2-m2-private392-approved-native-env-app-http-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The registered suite ran:

```text
env -u PYTHONPATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b \
ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python \
npm run test:integration:private392-http
```

The runner used Vitest `--no-cache --maxWorkers=1 --no-file-parallelism`.
Result: `Test Files 1 passed (1)`, `Tests 1 passed (1)`, exit `0`, duration
`6.49s` (central wrapper: `10s`). Evidence is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-private392-approved-connector-real-gate-ap2-m2-private392-approved-native-env-app-http-integration-1021000118-6846/log.txt`

## Assertions reached

All 29 `expect(...)` sites reached: 7 exact-identity assertions and 22 live
scenario assertions. The live case performed real capture/session and
`RuntimeDataProvider` Door traffic, fake IndexedDB outbox persistence, merge
and replace project-data writes, opaque/null/false/order preservation, lost
acknowledgement recovery, reload, exact request and idempotency-key retry,
direct Runtime-actor intervening edit, server rebase, undo, stale refusal with
unchanged head (zero write), and zero legacy POST traffic. The primary and
reloaded Door providers carry no browser bearer token; the direct Runtime
provider retains its actor token. This was a real capture/session pass, not an
environment-only pass.

## Scope and next steps

No hosted UI, hosted-build, local-browser, socket, full-suite, public adoption,
or hosted claim was made. No new suite, public pin, code, or assertion was
introduced. No failure cleanup was needed. Recommended next step: let the
orchestrator consume this PASS and merge the already-approved branch through
the normal integration queue.
