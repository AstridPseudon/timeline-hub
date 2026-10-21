# App M2 producer run-mode closed repair — 0524

## Result

The concrete `6793` defect is repaired once in one new owned external gate artifact. The immutable approved gate remains untouched. No App product source, live caller, wrapper, producer body, helper, config, pin, graph, or dependency was changed.

The old `6793` actual remains an invocation failure with zero collected/body tests: the approved gate accepted only `preflight|list`, while the registered actual passed `run`. The `0520` result is preserved as setup/invocation failure, not product evidence, and the unchanged actual was not rerun.

## Exact artifacts and identities

- Frozen source keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Frozen source HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` / `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Immutable approved gate (untouched): `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
- Approved gate SHA-256: `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`
- New owned gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh`
- New gate SHA-256: `cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97`
- Committed wrapper: `scripts/testing/run-producer-public13-list.sh`
- Committed wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

The new gate is an exact copy of the approved gate except for these two whitelist/usage pairs:

    -MODE=${1:?usage: $0 preflight|list}
    +MODE=${1:?usage: $0 preflight|list|run}
     case "$MODE" in
    -  preflight|list) ;;
    -  *) echo "usage: $0 preflight|list" >&2; exit 2 ;;
    +  preflight|list|run) ;;
    +  *) echo "usage: $0 preflight|list|run" >&2; exit 2 ;;
     esac

All keeper HEAD/tree/clean/KEEP/helper/body/config/graph/hash/short-path, cohort, isolation, argv, and child-return-code guards remain present and unchanged. The wrapper already accepted and implemented `preflight|list|run`, so no additional prerequisite was found.

## Mode and dispatch graph

The route is: central registration -> full 64-hex new-gate hash -> full 64-hex committed-wrapper hash -> new gate(snapshot root, mode) -> keeper/source/tree/clean/KEEP/body/helper/config/graph/custody checks -> `cd` frozen keeper -> existing wrapper(frozen keeper, mode) -> wrapper validates absolute root and mode -> existing public13 runner(short App alias, `ordinary`).

Mode branches are:

- `preflight`: `PUBLIC13_PREFLIGHT_ONLY=1`, private graph/run root and resolver, then exit before hosted build/browser.
- `list`: runner reaches the npm test command; the wrapper forwarder invokes Playwright with `--list`.
- `run`: runner reaches hosted build then the test command; the wrapper forwarder invokes Playwright without `--list`.

Exact collection seam retained: config `playwright.producer-ownership-current-pin.config.ts`; spec `tests/e2e/local/producer-ownership-current-pin.spec.ts`; list argv `test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list`; run argv is the same without `--list`. The existing one-test guard remains `Total: 1 test in 1 file`; run requires exactly one passed or one failed result and propagates the child status.

## New central registrations

Exactly two uniquely named external entries were added to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`: `app ap2-m2-producer-run-mode-closed-repair-0524-preflight` and `app ap2-m2-producer-run-mode-closed-repair-0524-actual`.

Each entry hashes the new gate as `cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97`, hashes the committed wrapper as `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`, then invokes the new gate. The actual entry passes `run`; it was registered but not submitted.

## Evidence and exact commands

All commands below were run without a browser, hosted build, full suite, install, live product socket, or actual dispatch.

- `sh -n <new gate>` — PASS.
- `diff -u <approved gate> <new gate>` — PASS; only the whitelist/usage pairs above differ.
- `sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-frozen-delta-luna-resume-0453/guard-probes.sh` — PASS: valid successor, wrong base, extra tracked file, body/helper/config drift, and final HEAD/tree/wrapper-hash negatives.
- Ephemeral stub against the committed wrapper's real forwarder branch — PASS: list and run reached the exact intended root and argv; unknown, wrong, and missing modes refused with no child; child exit 7 propagated. The stub used a short private `/tmp` directory and EXIT cleanup.
- New gate missing mode, unknown mode, and wrong service root — PASS refusal before child dispatch.
- Direct `sh -x <new gate> preflight` — PASS source-only resolver; private `0.0.13` package/evaluation paths were used and no hosted build/browser was entered.
- Central command: `R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-run-mode-closed-repair-0524 ap2-m2-producer-run-mode-closed-repair-0524-preflight --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"` — PASS.

Central result: `ap2-m2-producer-run-mode-closed-repair-0524-ap2-m2-producer-run-mode-closed-repair-0524-preflight-1021052700-1778`, exit 0, exact source tree `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`, 10 preflight checks. The log reports the expected resolver PASS and `public13 preflight PASS` with Agent `8130a401...`, Runtime `2c4ac180...`, graph `public13`, and private isolation.

## Independent delta review and scope

Independent final review: **APPROVE**. The new external gate is a byte-level copy with only the closed whitelist extension; the committed wrapper hash and all frozen source/graph identities are unchanged. No live callers changed (zero). The App worktree remains clean at the frozen HEAD/tree. No actual, browser, hosted-build, or product qualification is claimed.

Recommended next step: the orchestrator may consider the uniquely registered actual only under its existing one-actual authorization and lock conditions; the actual has not been run by this worker.
