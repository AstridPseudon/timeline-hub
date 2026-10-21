# AP2 M2 producer approved final command and one case — 0512

## Result

The approved final producer command was registered as two new owned literal
central-service entries: a source-only `preflight` and the one permitted
`actual`. Both verify the recomputed wrapper SHA-256 before invoking the
unchanged keeper gate. The actual was **not submitted** because the shared
browser lock is occupied by `full24749`.

The source-only central preflight was submitted once and failed before the
keeper gate. No retry was made.

## Exact source and cohort

- Source keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Source HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- Source tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Approved gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
- Final wrapper: `scripts/testing/run-producer-public13-list.sh`
- Recomputed wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`
- Agent cohort: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime cohort: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Composition graph: public13, archive SHA-256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`; package version `0.0.13`
- Producer artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`

The registered final commands are:

```text
test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh preflight

test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh run
```

The first submitted preflight used the same gate and an absolute keeper-path
hash predicate. Its exact central command was:

```text
test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh preflight
```

## Test result and first cause

Central command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-approved-final-command-and-one-case-0512 ap2-m2-producer-approved-final-command-and-one-case-0512-preflight --no-cache
```

Result ID:
`ap2-m2-producer-approved-final-command-and-one-case-0512-ap2-m2-producer-approved-final-command-and-one-case-0512-preflight-1021051127-14393`

Result: exit 1 in 1 second. The command failed at the external
`sha256sum`/`test` predicate; the keeper gate was not entered (`log.txt` and
`runner.log` were empty). The protected keeper was independently rechecked
afterward and still had the approved HEAD, tree, clean state, dependency link,
and wrapper hash. This is a command-environment preflight failure, not a
producer assertion result.

Static source-only checks after the result passed: `sh -n` for wrapper and
gate; exact HEAD/tree/wrapper hash; clean keeper; body/helper/config hashes;
`node_modules -> /home/user/work/app/node_modules`; public13 graph version;
two central registrations; and disk availability of 14,054,136 KiB (>10 GiB).
The previously approved independent keeper preflight remains
`ap2-m2-producer-final-frozen-keeper-review-0501-ap2-m2-producer-final-frozen-keeper-review-0501-preflight-1021050416-31261`, exit 0.

## Browser-lock disposition

`/home/user/work/.app-m1-browser.lock` exists. App manager status records
`app-m4-canonical-full-current-execute-r21` as the sole `full24749` run on the
App, with the lock owned by that run. No producer actual was queued, and no
polling worker was started.

## Body/assertion scope

Producer body count executed: **0**. The approved spec contains one Playwright
test body and the wrapper's list mode requires exactly `Total: 1 test in 1
file`; neither list mode nor run mode reached that check in this attempt.
Therefore ownership preservation, foreign/user/raw-order, reload, retry/lost
acknowledgement, undo, and zero-legacy assertions remain unverified here.
The keeper's source, test body, helper, Playwright config, live callers,
cohort pins, graph, and shared dependencies were unchanged.

## Next step

After `full24749` releases the browser lock, the orchestrator should validate
the new relative service-root hash predicate with one source preflight and,
only if green, submit the registered actual once from the exact keeper. Do not
reuse the failed preflight result as actual evidence.

