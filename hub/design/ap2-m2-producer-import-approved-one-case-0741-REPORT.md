# App M2 corrected original producer case — 0741

## Result

**FAIL — one central attempt, stopped on the first behavioral failure.** The
approved custody packet was accepted and the wrapped original producer case
was built and launched. Exactly one unchanged test was collected and
executed, then failed before its producer mutation assertions:

```text
tests/e2e/local/producer-ownership-current-pin.spec.ts:87:3
producer ownership on the current mounted route › removes only stale owned transcript output and moves only owned scene output
expected getByTestId('transcript-lane-chip') count 2, received 0 at line 92
```

```text
result_dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-helper-expect-import-0717-ap2-m2-producer-import-approved-one-case-0741-actual-64e7befb48c89f33-integration-1021074320-23671
status=fail exit=1 duration=88s collected=1 executed=1 passed=0 failed=1
scope=original producer-ownership-current-pin.spec.ts, one selected test
```

No retry was submitted. No writer cut or behavioral PASS is claimed. The
failure blocks qualification pending an independently authorized diagnosis.

## Exact registration and invocation

The unique registration was added to
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`.
The stale 0721 registration was left untouched. The exact registered line was:

```text
app ap2-m2-producer-import-approved-one-case-0741-actual-64e7befb48c89f33-integration test "$(git -C "$PWD" show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 rev-parse HEAD)" = 6b0267c62aa8773132f1496d5014279e6c1edf61 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test -z "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 status --porcelain=v1 --untracked-files=all)" && test -f /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-helper-expect-import-0717/KEEP && test "$(readlink /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717/node_modules)" = /home/user/work/app/node_modules && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-startup-custody-gate-0717-owned.sh | cut -d' ' -f1)" = 64e7befb995b38fbf387b9ac2c0fb698dda59b514dfec54adb3be12c10f3ace4 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-runner-0717-owned.sh | cut -d' ' -f1)" = 48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce && flock -n /home/user/work/.app-m1-browser.lock true && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-startup-custody-gate-0717-owned.sh run
```

Submission was exactly once:

```text
request-test ap2-m2-producer-helper-expect-import-0717 ap2-m2-producer-import-approved-one-case-0741-actual-64e7befb48c89f33-integration --no-cache
wait-test ap2-m2-producer-helper-expect-import-0717-ap2-m2-producer-import-approved-one-case-0741-actual-64e7befb48c89f33-integration-1021074320-23671
```

The registration checks the central service's captured TREE separately from
the protected keeper HEAD/tree; it does not compare a synthetic service HEAD
to the keeper HEAD.

## Custody and preserved bytes

```text
sourceTARGET=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
keeper_HEAD=6b0267c62aa8773132f1496d5014279e6c1edf61
keeper_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
service_captured_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
helper_SHA256=d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b
spec_SHA256=d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
config_SHA256=5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
original_wrapper_SHA256=329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
owned_wrapper_SHA256=48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce
owned_custody_gate_SHA256=64e7befb995b38fbf387b9ac2c0fb698dda59b514dfec54adb3be12c10f3ace4
Agent_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55
Agent_TREE=236c3e57e0265c52b81ba8085de3193026176bff
Runtime_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a
Runtime_TREE=7ab412cc4bcbe517efcfa806e092336390312e18
Composition_package=0.0.13
```

The source remained clean with `KEEP` and `SOURCE_LEASE` present; its
`node_modules` link remained `/home/user/work/app/node_modules`. The locked
graph remained physical. The gate's source closure, graph, Agent/Runtime
pins, original selector/config/spec, list/argv, zero-test and child-status
guards were retained. No source, helper, config, spec, pin, assertion,
selector, timeout, or artifact behavior was changed here.

## Cleanup and prerequisites

Before submission: disk was 12 GiB free, the browser lock was nonblocking,
no local browser/test process or active test snapshot was present, and the
selected 8082 run was terminal `FAIL exit=1` (not an exit-0 false green).
The run's required 10 GiB floor passed; post-run disk was 15 GiB free.

After terminal cleanup:

```text
source_clean=yes
keeper_HEAD/tree=6b0267c62aa8773132f1496d5014279e6c1edf61/c1ac3383624322ae8d67b10dee36965670d91cd7
KEEP=present
SOURCE_LEASE=present
keeper_node_modules=/home/user/work/app/node_modules
keeper_.public13-effective-ordinary=absent
owned_artifact_hashes=unchanged
test_running_marker=absent
browser_lock=idle
local_browser_or_test_processes=none
```

The central wrapped build/browser run was the only actual attempt. No local
socket, browser, build, install, full suite, or retry was run by this worker.

## Next step

Keep the result packet and immutable source/artifacts. Investigate the
mounted-route transcript seed/render boundary that produced zero initial
chips, preserving the original test's ownership/foreign/user/raw/order,
recovery/retry, inverse, and zero-legacy assertions. Any source or assertion
change requires a new reviewed candidate and a separately authorized central
run.
