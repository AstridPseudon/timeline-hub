# AP2-M2 parent newborn approved one actual 0806

## Result

Submitted exactly one central actual with `--no-cache`. It failed at the first real product boundary; no rerun was made.

- Registration: `app ap2-m2-parent-newborn-approved-one-actual-0806-integration`
- Test ID: `ap2-m2-parent-newborn-approved-one-actual-0806-ap2-m2-parent-newborn-approved-one-actual-0806-integration-1021080656-31285`
- Count: 1 collected, 1 executed, 1 failed; no zero-test pass
- Service target/tree: worker `ap2-m2-parent-newborn-approved-one-actual-0806`, App tree `b0cb1f973c0e1b465241ebef38bd267fd39f0434`
- Source target: `/home/user/work/wt/ap2-m2-parent-newborn-current-proof-source-0748`
- Source HEAD/tree: `af1605a28f31a53b5a3472251493d44941b618fe` / `b0cb1f973c0e1b465241ebef38bd267fd39f0434`
- Gate/helper/driver hashes: `cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270`, `a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3`, `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`

Exact registered command:

```sh
test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' | cut -d' ' -f1)" = 'cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' run
```

## First failing boundary

The sole test was `three-products.spec.ts:1440`, and the first real failure was the lost-ack recovery assertion at line 1557: after the 90-second predicate ceiling, recovery showed `attempts: 0` instead of the required `attempts: 1`. The central result exit was 1 after 175 seconds. Later body/key, reload, restart, undo, and zero-legacy outcomes are unverified because execution stopped at this boundary.

The run reached the hosted build/browser phase. Gate guards passed separately for the service tree, protected keeper HEAD/tree/clean/KEEP, helper, and driver. The source manifest recorded the approved source identity and the exact Agent/Runtime pins.

## Durable failure packet

Retained before disposable run-root cleanup at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/`

Verified present: `playwright-trace.zip`, `error-context.md`, `runner-tail.log`, `bounded-browser-evidence.json`, `source-identity.txt`, `evidence-presence.json`, `retention.log`, and `result.txt`. The packet records `runner_status=1`, `trace=true`, and source HEAD/tree `af1605a28f31a53b5a3472251493d44941b618fe` / `b0cb1f973c0e1b465241ebef38bd267fd39f0434`.

## Cleanup and decisions

The central disposable run root was cleaned after evidence copy; the durable failure packet was retained. The assigned worktree remains clean. No source, spec, helper, driver, option, pin, selector, timeout, or assertion change was made. Per the task instruction, the failed actual was not retried.

