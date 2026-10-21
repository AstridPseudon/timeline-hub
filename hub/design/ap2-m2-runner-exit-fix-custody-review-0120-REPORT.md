# App2 current95 runner exit custody review

## Disposition

**HOLD.** There is no new App2 helper patch to approve. The three mutable
`normal014` helper artifacts are byte-identical to the already reviewed profile
repair, while the 4657 false pass remains a central test-service result
integrity defect. The owner is the central test-service and dispatcher
maintainer, not the App2 helper author.

I did not edit `bin/test-run`, rewrite 4657, start a browser, socket,
localhost, full, or additional real-gate run, or change any product source.

## Frozen inputs and discrepancy

The current95 triage report and `DONE` marker were present before review. I
waited the required 30 seconds after confirming the report was frozen, then
inspected the helper artifacts.

Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-current95-existing-driver-gate-0104-normal014-integration-e2e-gate5-1021011023-4657`

The retained files say:

- `status` is `pass` and `exit` is `0`.
- `summary` says `pass exit=0` and also says `1 failed 1 passed`.
- `log.txt` contains a Playwright `Timeout 90000ms exceeded`, then `1 failed`
  and `1 passed`.
- `runner.log` is empty.

This is a real result contradiction. The historical result remains a failure
for review purposes; no historical file was changed.

## Changed artifact custody

No new changed artifact was found after the author freeze. The current hashes
are the same hashes recorded for the existing profile repair:

| Path | SHA-256 | Review |
| --- | --- | --- |
| `design/normal014-source-common.sh` | `1e3708e5dff0b0acc251e9c97d802aa39383fe52435d229448e3517ebbe9a101` | unchanged existing profile |
| `design/normal014-app-central.sh` | `766e0b6a38a5d450a92aee8424d181041c54d523a8ea1427316cf02f3809d68c` | unchanged existing profile |
| `design/normal014-parent-media-central.sh` | `69507020c13b7351fd8350e39e481a186f21d4d4c4a98300102a4625f1142ffb` | unchanged existing profile |

The App2 worktree is clean. I did not rereview the unchanged source, lock,
authority, or profile identity beyond the custody checks below.

## Offline custody checks

All checks were local and offline:

- `sh -n` on all three helpers: **PASS**.
- Synthetic child through `flock` and the existing EXIT trap: child exit `23`
  returned `23`; child exit `0` returned `0`; generated owned run roots were
  absent after both exits: **PASS**.
- The service command shape `flock -> timeout -k 1 5s -> nice -n 5 -> bash -c`
  with failure evidence (`1 failed 1 passed`) and child exit `23` returned
  `23`; its owned run root was absent: **PASS**.
- Existing source, lock, checkout authority, cleanup, signal, and short-child
  guards were present: **PASS**. In particular, the old202 default remains
  explicit, the locked graph archive digest remains checked, checkout commit
  identity remains checked, cleanup preserves the saved status, signal traps
  re-raise, and the Python base remains executable-checked.
- The helper's conditional captures the `flock`/child status and exits with
  that status in both App and parent wrappers: **PASS**.

The exact central finalizer rule was also reproduced offline against the two
required synthetic outcomes:

```text
failure evidence + child 23 -> derived=fail rc=23
failure evidence + child 0  -> derived=pass rc=0
```

The second line is the unresolved false-pass class. The App2 helper cannot fix
it because the helper correctly returns the child status and the central
service writes the final result after the child has completed.

## Required owner action

The central test-service owner must preserve the actual child RC through the
dispatcher/finalizer and make any completed result non-pass when retained test
output contains a failure. Add a central regression for both synthetic child
outcomes and for failure-count evidence with RC 0. Only after that fix is
frozen and independently reviewed should 4657-equivalent qualification be
requested. Do not relabel 4657 or treat the existing App2 helper hashes as a
new false-pass fix.

No App2 code change is recommended.
