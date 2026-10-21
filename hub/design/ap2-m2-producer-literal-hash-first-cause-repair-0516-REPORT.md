# AP2 M2 producer literal hash-first cause repair — 0516

## Scope and diagnosis

This repair changes only the two new producer registrations in the shared
central suite allow-list. The App source, committed wrapper, external gate,
producer body/helper/config, cohort pins, graph, and live callers are
unchanged.

The exact first cause of preflight `14393` was the shell predicate itself:
the registered command compared the wrapper SHA-256 against the 63-hex
literal ending `...dca4f`, while the committed wrapper digest is the distinct
64-hex value ending `...dca4f0`. In `bash -c` form, `test` returned 1 and the
`&& sh ... final-keeper-gate.sh preflight` child was not evaluated; the
central `log.txt` and `runner.log` were empty. The old command also did not
hash the external gate before invoking it.

## Exact source and hashes

- Source HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- Source tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- External gate:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
- External gate SHA-256: `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`
- Committed wrapper: `scripts/testing/run-producer-public13-list.sh`
- Wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

Both digests were recomputed as exactly 64 lowercase hexadecimal characters.

## New literal registrations

The preflight registration is:

```text
app ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh | cut -d' ' -f1)" = 460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh preflight
```

The actual registration has the same gate-first and wrapper-first guards,
ending in `...final-keeper-gate.sh run`; it is registered for the orchestrator
but is not submitted by this task.

The unchanged external gate retains the approved keeper root argument and
checks clean service tree, `KEEP`, keeper HEAD/tree, keeper cleanliness,
wrapper bytes, body/helper/config hashes, Agent/Runtime cohort, normal graph,
short paths, argv/test paths, and dependency isolation before delegation.

## Offline controls

Using the same `bash -c` shell form as the central service:

- GREEN: exact gate and wrapper digests permitted the post-`&&` sentinel.
- RED: wrong gate, wrong wrapper, wrong path, and the old truncated wrapper
  digest each returned 1 and did not invoke the sentinel child.
- Registration inspection found exactly two new lines, each with literal
  gate-before-wrapper 64-hex predicates.

The independent literal-command review report
`ap2-m2-producer-final-literal-command-review-0516-REPORT.md` APPROVED these
exact registrations before central execution.

## Central result

The one requested source-only central preflight passed:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-literal-hash-first-cause-repair-0516 ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-literal-hash-first-cause-repair-0516-ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight-1021051918-19123
```

Result: exit 0 in 5 seconds, App tree
`d63fe4f1e1f32a01acfc9d11cda6c29066fce162`. The unchanged gate reported
`public13 preflight PASS checks=10`, Agent `8130a401bf44a518d5a40ae274d398b8c560be55`,
Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, graph `public13`, and
private isolation. The existing preflight resolver also reported its expected
hosted-build resolver PASS; no separate build command was submitted.

No actual, browser, full suite, install, source edit, or live caller change
was made. The registered actual remains unsubmitted pending the orchestrator's
separate authorization and runtime-lock decision.
