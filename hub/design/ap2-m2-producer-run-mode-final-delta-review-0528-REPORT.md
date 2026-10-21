# App M2 producer run-mode final delta review — 0528

## Result: APPROVE

The final0524 gate repair is valid and is the smallest permitted delta. The
prior0524 HOLD was caused by the artifact being absent at review time; it is
historical missing-artifact status, not a current code rejection.

## Immutable tuple

- Frozen keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Keeper HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` /
  `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Final gate:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh`
- Final gate SHA-256: `cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97`
- Original0501 gate SHA-256: `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`
- Frozen wrapper: `scripts/testing/run-producer-public13-list.sh`
- Wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

`diff -u` between the original0501 gate and final0524 gate shows only the
closed `preflight|list` → `preflight|list|run` usage/allowlist extension.
The keeper HEAD/tree/clean/KEEP, captured service tree, wrapper hash, body,
helper/config, graph/cohort, short-path, argv, and child-return-code guards
are unchanged. The wrapper already supports `run`; no underlying source or
executable change was needed. Live callers remain unchanged.

## Controls and evidence

The final gate captures `SERVICE_ROOT=$PWD`, checks the service tree before
dispatch, and invokes the frozen wrapper with the frozen keeper root and the
selected mode. Both central registrations bind the final gate and wrapper by
their full SHA-256 values before invocation.

The offline proof exercised the committed wrapper's real forwarder branch with
an isolated child stub: list and run reached the exact root and Playwright
argv; unknown, wrong, and missing modes refused before child dispatch; and
child exit status 7 propagated. The stub is harness evidence only and makes no
product acceptance claim. Existing custody negatives also passed: wrong base,
extra tracked file, body/helper/config drift, and wrong HEAD/tree/wrapper hash.

The retained collection is
`test --config playwright.producer-ownership-current-pin.config.ts
tests/e2e/local/producer-ownership-current-pin.spec.ts`; list adds
`--list`. List requires exactly `Total: 1 test in 1 file`; run accepts
exactly one passed or one failed result and propagates the child status.

Central source-only evidence is result
`ap2-m2-producer-run-mode-closed-repair-0524-ap2-m2-producer-run-mode-closed-repair-0524-preflight-1021052700-1778`:

```text
pass, exit 0, 5s; App tree d63fe4f1e1f32a01acfc9d11cda6c29066fce162
public13 preflight PASS checks=10
Agent 8130a401bf44a518d5a40ae274d398b8c560be55
Runtime 2c4ac180c2220bdad966bc01e95ad230e99ce26a
graph=public13 isolation=private
```

The exact registered actual suite approved for one orchestrator-run is
`app ap2-m2-producer-run-mode-closed-repair-0524-actual`, whose immutable
command is:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh | cut -d' ' -f1)" = cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh run
```

This reviewer did not run the actual, browser, hosted build, full suite, or
install. The actual result is therefore unverified and must not be inferred
from the stub or preflight.

## Commands run by this review

- `sha256sum` on final gate, original gate, and wrapper — expected hashes.
- `diff -u` final gate vs original gate — only the run whitelist/usage delta.
- `sh -n <final gate>` — PASS.
- `sh guard-probes.sh` — PASS.
- Final gate missing/unknown mode and wrong-service-root probes — PASS refusal.
- Final gate `preflight` on the exact frozen tree — PASS, source-only.

Recommended next step: run the exact registered actual suite once under the
central service and report its real one-test result; do not alter this tuple.
