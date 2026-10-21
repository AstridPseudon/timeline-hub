# AP2 M2 producer exact-hash actual report

## Result

The one authorized producer actual was submitted once and failed closed before
build at the wrapper's `isolation` preflight. I did not retry, edit the source,
run a browser locally, or run another suite.

## Approval and source custody

The required 0416 source and independent review both explicitly approved the
final external hash-guarded command and preflight.

- Source worker: `ap2-m2-producer-final-external-hash-binding-0416`
- Source commit: `97187ce3c1576559239f869067a9cef8ffb5f357`
- Source tree: `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`
- Frozen 0404 source: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`
- Wrapper SHA-256: `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`
- Existing runner SHA-256: `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Effective Composition/public source: public13, archive/tarball SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Preflight result: `1021041952-21577`, PASS, `public13 preflight PASS checks=10`
- Preflight command: `request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-preflight --no-cache`

The preflight also verified the immutable body/config hashes, all 75 Runtime
artifacts, all 77 Composition files, disk and private isolation. The 0416
one-byte wrapper-drift control rejected before invocation.

## Actual command and first result

Exact command submitted through the central service, once, with `--no-cache`:

```text
request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-actual-e2e-integration --no-cache
```

The registered command was:

```text
cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 run
```

Result: `ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-actual-e2e-integration-1021042209-28181`, exit 1 in 2 seconds.

First retained packet/trace:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-actual-e2e-integration-1021042209-28181`

The retained log is:

```text
producer preflight FAIL
- isolation
```

The exact source worktree was recreated from the approved branch for the
central run. Its wrapper hash and source commit/tree matched. The failure was
`check_isolation`: the exact source worktree did not have the required
`node_modules` symlink. No build, browser, producer body, or external runner
was reached (`runner.log` is empty).

## Assertion scope

No protected foreign/user raw/order, reload, lost-ACK, restart, exact
body/key, retry, undo, zero-legacy, accepted owned removal/move/hold, or
atomic-refusal assertion executed. They remain unverified. No live callers
changed, no product files changed, and this worker worktree is clean.

## Blocker and next step

The actual is not qualified. The blocker is the central-service isolation
state of the recycled exact source worker, not a product assertion result.
The orchestrator should decide whether to repair/re-provision that exact
worker's private dependency link under the same custody rules and authorize a
new run. This worker performed no retry.
