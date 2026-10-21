# App M2 producer final reviewed one-case report — 0532

## Result

The one explicitly authorized central actual was submitted exactly once. It
did not qualify: the sole collected test failed during Runtime startup before
producer traffic or ownership assertions.

Central result:

- Test ID: `ap2-m2-producer-final-reviewed-run-one-case-0532-ap2-m2-producer-run-mode-closed-repair-0524-actual-1021053231-23729`
- Status/exit: `fail`, exit `1`, elapsed `67s`
- Count: `1` test collected, `0` passed, `1` failed
- Test: `tests/e2e/local/producer-ownership-current-pin.spec.ts:87:3`
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-final-reviewed-run-one-case-0532-ap2-m2-producer-run-mode-closed-repair-0524-actual-1021053231-23729`
- Forwarded Playwright argv: `test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts`; the wrapper's exact-one-test guard reported one test.

Exact registered command executed:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh | cut -d' ' -f1)" = cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh run
```

## First failure and scope

The hosted build completed successfully. Playwright then launched the one
original test, whose worker-scoped harness failed at
`DirectHarness.startRuntime` / `startRuntime` while launching
`python -m runtime_protocol.cli start`. The first failure was:

```text
Runtime exited 1: {"error":{"code":"startup_error","message":"realm root must not traverse a symlink"},"ok":false}
```

The failure occurred at 2 ms in the test, before the producer action. No
producer request body was observed or accepted (`bodycount=0`); transcript
delete, scene move/hold, reload/retry, lost-acknowledgement, undo, protected
row/order, opaque/raw, and zero-legacy assertions were not reached. The
result log is the authoritative first-cause record.

## Immutable source and guards

- Source/worker HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- Source/worker tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Final gate SHA-256: `cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97`
- Committed wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`
- Body SHA/tree: `36dd91257fd13dcad0d58b48c790caa5063b4c8c` /
  `d908845dbc8e5ebf96698d08621557e904f20c52`
- Spec/helper/config hashes remained the reviewed values:
  `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`,
  `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`,
  `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
- Agent/Runtime cohort remained `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Private graph and official Composition identities remained the reviewed
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

No source, body, cohort, helper, config, selector, options, timeout, pin,
package, or live caller changed. The worker and frozen keeper were clean at
the same HEAD/tree after the run.

## Prerequisites and evidence

- Final0528 explicit review: `APPROVE`.
- Retained central source preflight: result suffix `1778`, exit 0,
  `public13 preflight PASS checks=10`; it was not repeated.
- Existing `/home/user/work/.app-m1-browser.lock`: nonblocking read-only
  `flock` inspection was `AVAILABLE` before submission. The lock file was not
  removed or bypassed.
- Free disk before submission: `15,273,080 KiB` (~14.6 GiB), above the 10 GiB
  floor.
- Short normal run root before submission: absent. No source copy, graph, or
  install was created by this worker.
- At most two relevant normal source copies were involved: this worker's
  central snapshot and the frozen keeper; pre-existing unrelated worktrees
  were not touched. The runner-owned short graph used its private temporary
  root and left no stale run root in this worker.
- The retained offline real-wrapper dispatch/refusal/child-status proof was
  not rerun or changed.
- Central request used the named suite once with `--no-cache`; no second run,
  local browser, full suite, install, or source change was made.

## Blocker and next step

Qualification is blocked by the central Runtime startup refusal that the realm
root must not traverse a symlink. The historical `6793` invocation failure was
not used as product evidence. Do not rerun from this worker; a future run
requires an explicitly authorized correction of the symlinked realm-root
launch environment and a fresh review of whether the exact frozen command may
be submitted again.
