# Producer retention recovery review — 0838

Decision: **APPROVE**, limited to Sol’s 0822 owned retention correction. This is an independent first review of that correction, not a review of a prior review. No App source, test/spec, helper, pin, assertion, selector, timeout, or central registration was changed by this review. Live callers changed: **NONE**.

## Exact cause and lifetime

The first failing value in the real nested path was the non-physical `RUN_ROOT` string. The 0753 wrapper creates `SHORT_ENV_ROOT=/tmp/tla-XXXXXX`, sets `SHORT_APP_ROOT=$SHORT_ENV_ROOT/a`, symlinks `a` to the real App root, and calls the public runner with `SHORT_APP_ROOT`. The public runner therefore creates and retains:

```text
APP_ROOT=/tmp/tla-CbE2Zp/a
RUN_ROOT=/tmp/tla-CbE2Zp/a/.public13-effective-ordinary
```

The central 17481 log records the same short-path family for the hosted package and both Playwright attachments: `/tmp/tla-CbE2Zp/a/.public13-effective-ordinary/.../error-context.md` and `trace.zip`. The helper’s first relevant guard is `test "$(realpath "$RUN_ROOT")" = "$RUN_ROOT"`; the short-symlink `RUN_ROOT` fails that equality before `mkdir "$DURABLE_ROOT"`, before either copy, before identity, and before `SHA256SUMS`. This is the exact cause of the lost packet, not a producer or DOM inference. Earlier 0753/0801 controls invoked the inner public runner with a physical App path and could not exercise this value.

The run root exists from public13’s `mkdir -p "$RUN_ROOT/..."` until its EXIT cleanup `find "$RUN_ROOT" -depth -delete`. On the failure path, retention is attempted first but exits at the realpath guard; the normal cleanup then removes the run root, explaining the missing DOM/trace/log/manifest. Separately, the wrapper creates `LIST_ROOT` and installs one trap, then installs a later `cleanup_short_environment` trap that replaces it. The original 0753 path therefore left the child-log temp directory alive; the preserved before control measured exactly one leaked temp.

## Owned correction and exact artifacts

The correction is minimal and owned:

1. `producer-public13-runner-0717-owned.sh` passes `$(realpath "$RUN_ROOT")` to the unchanged helper, preserving the helper’s physical-root guard. Its added failure handler prints `producer failure retention FAILED ...` and forces the outer status nonzero when retention itself fails.
2. `producer-runner-0717-owned.sh` adds `find -P "$LIST_ROOT" -depth -delete` to the final cleanup trap, preserving the child status while closing the previously observed temp lifetime.

Corrected artifact paths and full SHA256 values:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-physical-keeper-gate-0717-owned.sh  0f193b6c54bcb9f2333acfe7bd39c67c56b58ee60bce498212577b3e115cc499
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-public13-runner-0717-owned.sh  d1a6616d477f6529de8c949286278fca906df44a1f5e9fe24b78e3ccb4cc4f10
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-retain-failure-artifacts-0753.sh  dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-runner-0717-owned.sh  0f57d4885999f265ee43a14acb14a9abe58014dc773edc9edb3423687f8add39
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-custody-gate-0717-owned.sh  b7c6f4806c02d8315b3eb69c4b4c469e7b908375603a5a0c967df5bbae60efb9
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-module-format-probe-0717-owned.mts  d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-only-gate-0717-owned.sh  10abb0571dc927aa1945ec8f1ae4008bcf995b594225fecb68f5a86584d0555040336032ced515d6ac50de9481d8f
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-only-probe-0717-owned.mts  a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
```

The verified manifest line for `producer-startup-only-gate-0717-owned.sh` is the exact 64-hex value shown above; no artifact was rewritten during this review.

## Minimality, guards, and preserved controls

`rebindings.json` and `minimal-reversed.diff` prove that path/hash rebinding reverses exactly and leaves only the two intended hunks above. The unchanged chain preserves source HEAD/tree, keeper cleanliness and `KEEP`, original wrapper hash, Agent/Runtime heads and trees, locked graph and Composition pins, argv, list-one/zero-test/child-RC checks, cleanup, refusal guards, and shared-install isolation. The public runner still calls the unchanged helper, which still copies only `browser-output` and exact `child.log`, requires `error-context.md` and `trace.zip`, records identity, and writes `SHA256SUMS`.

The preserved real outer-chain launch-only result is five controls, each dispatched through exactly four shell bodies in this order:

```text
producer-startup-custody-gate-0717-owned.sh
producer-physical-keeper-gate-0717-owned.sh
producer-runner-0717-owned.sh
producer-public13-runner-0717-owned.sh
```

Each had exactly one child dispatch, no browser/build/daemon/socket, and the outer cleanup assertions `run_root_removed=true`, `dist_removed=true`, `node_modules_restored=true`.

| Control | Outer RC | Manifest | Temp created/leaked | Result |
|---|---:|---:|---:|---|
| before 0753 copies | 1 | no | 2 / 1 | reproduces loss |
| after 0822 copies | 1 | yes | 2 / 0 | retained error-context, trace, exact child log, identity, and verified SHA manifest |
| absent-output | 1 | no | 2 / 0 | visibly refused; no manifest |
| copy-failure | 1 | no | 2 / 0 | visibly refused with retention failure; no manifest |
| success | 0 | no | 2 / 0 | normal success cleanup |

Preserved control result: `outer controls PASS count=5 browser=0 build=0 daemon=0 socket=0 shared_writes=0`.

## Evidence commands and results

Preserved 0822 command/result: `python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/outer-controls.py` — PASS, five real outer-chain controls as counted above.

Independent offline witness run in this review:

```text
sha256sum -c /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts.sha256
PASS — 8/8 artifacts.

reverse substitution from rebindings.json plus minimal-reversed.diff
PASS — 6/6 unchanged/rebound proofs and the exact 2-file minimal delta.

sh -n <each of the 6 corrected .sh artifacts>
PASS — 6/6.
```

Earlier preserved evidence, not rerun here: source-only public13 preflight `PASS checks=11`; central 0805 module-format probe `PASS: DirectHarness loaded as ESM; no daemon invoked`. No unchanged broad guard, browser, build, daemon, socket, install, or full suite was rerun.

Original central outcomes remain unchanged: 23671 and 17481 are **FAIL/UNKNOWN**. Central 17481 failed at the unchanged initial assertion (`transcript-lane-chip` expected 2, received 0) before producer actions; its temporary output was removed, and it did not prove a producer cause.

## Literal central proposal (syntax checked, not submitted)

Both bodies below were generated from the stored registration with only the final 0822 artifact root, final startup-gate hash, and mode changed. Each passed `bash -n`. The preflight must run first; the run is a later separately authorized single actual execution. Neither was registered or submitted by this review.

