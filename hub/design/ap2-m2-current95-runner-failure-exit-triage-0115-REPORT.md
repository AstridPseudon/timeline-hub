# App2 current95 normal014 failure-exit triage

## Outcome

No App2 runner change is justified. The existing normal014 wrapper and the
central service command both preserve a failing child exit in offline probes.
The historical result 4657 remains a failure by its retained Playwright log,
despite its existing `status=pass` and `exit=0` files. I did not rewrite those
historical files and did not run a browser, socket, full, or re-gate suite.

The remaining defect is a central test-service result-integrity issue (or an
unavailable child-exit observation), not a demonstrated App2 wrapper swallow.
The service owner should investigate result 4657 and add child-exit/finalizer
instrumentation before any permitted rerun.

## Historical evidence

The result directory was inspected before any change:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-current95-existing-driver-gate-0104-normal014-integration-e2e-gate5-1021011023-4657`

- `status` is `pass` and `exit` is `0`.
- `summary` says `counts: 1 failed 1 passed (2.0m)` while claiming `pass exit=0`.
- `log.txt` retains the Playwright failure: `Timeout 90000ms exceeded` in
  `waitForCreatedProjectResponse`, with `1 failed` and `1 passed`.
- `runner.log` is empty, so there is no retained wrapper trace or child exit
  observation that can distinguish a node exit, `flock` exit, EXIT-trap exit,
  or service overwrite.
- The snapshot was App tree
  `43b6c9a9fbe1fa56dacdfaf934883f40f91b3905`, with key
  `817f9a762a4c67247c28f98ac24ac454`.
- The concurrent external hashes recorded by the service were Agent
  `57d6635616f2982b814cfcc059b670ea1a7c9f2c`, Runtime
  `9d1c43c647301da48a6e86ad82e466b501bd241a`, and Composition
  `4788e107f183e0523a740b691a20eb8261d7183c`.

The current 0108 profile author/history was checked before deciding whether
to edit. Its author worker was
`ap2-m2-main95-existing-runner-profile-repair-0108`; the existing profile
repair report records these exact before/after
hashes:

| App2-owned orchestration file | Before | After |
| --- | --- | --- |
| `normal014-source-common.sh` | `c48d03d9c07e10216f5da2474ba10b608430975039bb6eec84ac3f2d0d6e7d5a` | `1e3708e5dff0b0acc251e9c97d802aa39383fe52435d229448e3517ebbe9a101` |
| `normal014-app-central.sh` | `1c784bec132f50ccfb29ea825bd32de28448eafaede1dbeb7f937cb3df252c08` | `766e0b6a38a5d450a92aee8424d181041c54d523a8ea1427316cf02f3809d68c` |
| `normal014-parent-media-central.sh` | `383ace5a4ff5d197f24b2e92f31f829f78b9263513df70b5e457843b66229461` | `69507020c13b7351fd8350e39e481a186f21d4d4c4a98300102a4625f1142ffb` |

Those current hashes were also verified directly. The temp-hygiene changes
were already present before 4657 was requested at 01:10:23Z, so this triage
does not attribute the historical mismatch to an untested pre-fix wrapper.
There were no active normal014 or test processes when the probes began.

## Exact path classification

The historical command was:

`bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"`

The path is:

`Playwright node process -> flock -> normal014-app-central.sh conditional -> normal014-source-common.sh EXIT trap -> test-run subshell/timeout/nice/bash -c -> test-run RC -> status/exit files`

The existing App2 runner explicitly captures the `flock`/node status and exits
with it. The common helper captures `$?` in its EXIT trap, removes only its
owned run root, and returns the captured status; signal traps re-raise the
signal. This preserves failure-before-cleanup evidence.

The forbidden central service finalizer instead derives `ST=pass` whenever
its observed `RC` is zero and writes that result after cleanup. It does not
validate the captured log counts. An offline reproduction of this result
contract produced:

`synthetic_log=1 failed 1 passed rc=0 derived_status=pass`

This reproduces the status-integrity class, but not the unavailable historical
child RC. Therefore the exact 4657 swallow point cannot be proven from retained
artifacts; the central service owner owns the next investigation.

## Tests and probes

All were offline and targeted; no repository test suite was requested.

- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh` — passed.
- Existing common helper plus `flock` synthetic child probe — failing child returned 23, success child returned 0, and both owned run roots were absent after cleanup — passed.
- Exact service command shape, `timeout -k 60 90m nice -n 5 bash -c`, with synthetic child exits 23 and 0 — preserved 23 and 0 — passed.
- Synthetic finalizer contract probe with log text `1 failed 1 passed` and child exit 0 — derived `pass`, reproducing the service result-integrity defect class.
- No App worktree files were changed; `git status --short --branch` remained clean.

## Owner request and next steps

Central test-service ownership should inspect the 4657 process record and
dispatcher/finalizer logs, preserve the child RC and failure evidence before
cleanup, and make the result non-pass whenever a completed test reports a
failure. The owner should also add a regression probe for a failing-count log
and a nonzero child, plus a guard against writing `pass` when retained test
output says `failed`.

Do not rerun 4657, rewrite its historical status, edit `bin/test-run`, or
start a browser/socket gate as part of this triage.
