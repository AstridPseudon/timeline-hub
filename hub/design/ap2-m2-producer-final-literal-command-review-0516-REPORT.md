# AP2 M2 producer final literal command review — 0516

## Decision

**APPROVE** the two new literal suite registrations from
`ap2-m2-producer-literal-hash-first-cause-repair-0516`, for one source-only
preflight followed by the one authorized actual only after that preflight
passes. This approval is for the commands as written; it is not authority to
execute either command.

## Exact binding reviewed

- Frozen keeper root: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Frozen keeper HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- Frozen keeper tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- External gate:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
- External gate SHA-256: `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`
- Committed wrapper: `scripts/testing/run-producer-public13-list.sh`
- Wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

Both digests are exactly 64 lowercase hexadecimal characters. The external
gate hash is checked first, then the wrapper hash, before either `preflight`
or `run` is passed to the unchanged external gate. The gate retains the
original keeper root argument and its frozen HEAD/tree, clean-state, KEEP,
body/helper/config, cohort, graph, short-environment, argv, and child-return
code checks.

The exact registered commands are:

```
app ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh | cut -d' ' -f1)" = 460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh preflight
app ap2-m2-producer-literal-hash-first-cause-repair-0516-actual test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh | cut -d' ' -f1)" = 460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh run
```

## Cause and controls

The prior preflight `14393` failed before invoking its gate because it used a
63-character wrapper digest (`...dca4f`) and did not hash the external gate.
The repaired registrations correct both defects. The repair report is
`ap2-m2-producer-literal-hash-first-cause-repair-0516-REPORT.md`.

Independent offline shell-form controls, run with the same `bash -c` shell
form as the central service, passed:

- exact gate + wrapper hashes: GREEN;
- independently wrong gate hash: refused before sentinel;
- independently wrong wrapper hash: refused before sentinel;
- wrong path: refused before sentinel;
- old truncated wrapper digest: refused before sentinel.

The registrations contain exactly two new lines, and both have literal
gate-before-wrapper 64-hex predicates. No prior registration was changed by
this review.

## Source and existing preflight evidence

The source was checked at the exact frozen HEAD/tree above. It is clean, has
the required KEEP marker at the approved worker path, and retains the normal
`node_modules -> /home/user/work/app/node_modules` link. The approved source
delta remains wrapper-only. Current hashes match the standing 0501 review:

```
tests/e2e/local/producer-ownership-current-pin.spec.ts       d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
tests/e2e/local/support/producer-ownership-current-pin.ts    50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
playwright.producer-ownership-current-pin.config.ts         5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
```

The one central complete source preflight already read for this exact frozen
source is result
`ap2-m2-producer-final-frozen-keeper-review-0501-ap2-m2-producer-final-frozen-keeper-review-0501-preflight-1021050416-31261`,
exit 0, with `public13 preflight PASS checks=10`, Agent
`8130a401...`, Runtime `2c4ac180...`, graph `public13`, and private
isolation. The newly repaired literal registration has **not** been executed
by this reviewer; its post-approval central preflight remains pending and must
be run once by the orchestrator. No actual, build, browser, full suite,
install, or live-socket command was run here.

## Changed callers and handoff

- Changed live callers: none.
- Changed suite registrations: exactly the two new lines named above.
- Product source, producer body/helper/config, pins, gate, wrapper, short
  environment, child-RC handling, and shared dependency graph: unchanged.
- Commit message path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-literal-command-review-0516/commit-msg`
- DONE marker:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-literal-command-review-0516/DONE`

Recommended next step: execute only the new `...-preflight` registration
once, inspect its result, and submit the new `...-actual` registration only
if that exact preflight is green and the orchestrator’s existing lock/one-run
conditions hold.

