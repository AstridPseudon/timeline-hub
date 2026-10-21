# AP2 M2 ordinary producer result action — 0514

## Decision

**HOLD — prerequisite not satisfied.** No ordinary-batch writer deletion or
patch artifact is justified. The approved producer actual never ran, so there
is no product outcome from which to trace a dead fallback or remove a writer.

## Consumed 0512 result

- Source keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Source HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` /
  `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Agent cohort: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime cohort: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Composition cohort: public13, package `0.0.13`, archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Producer artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Wrapper: `scripts/testing/run-producer-public13-list.sh`
- Wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f`

The central preflight result was:

```text
ap2-m2-producer-approved-final-command-and-one-case-0512-ap2-m2-producer-approved-final-command-and-one-case-0512-preflight-1021051127-14393
exit 1 in 1 second
```

Exact command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-approved-final-command-and-one-case-0512 ap2-m2-producer-approved-final-command-and-one-case-0512-preflight --no-cache
```

Its first cause was the external `sha256sum`/`test` predicate. The keeper gate
was not entered; no build, browser, producer body, or producer assertion ran.
The approved 0501 independent preflight remains a separate PASS, but is not an
actual result.

The shared browser prerequisite also remains held: `/home/user/work/.app-m1-browser.lock`
is owned by App `full24749`. 0512 correctly submitted no actual and did not
retry the failed preflight.

## Producer body scope

The frozen body has one test:
`removes only stale owned transcript output and moves only owned scene output`.
Its retained assertions cover the dedicated current head, stale-row removal,
exact native commands, preservation of foreign/user rows and raw order,
visible refusal with no commit, reload, lost-ack retry with the same request
body and idempotency key, and guarded undo. Body count executed: **0**; all
remain unverified by this result.

## Ordinary writer/caller delta

No App product files were changed. `useTimelineOps` remains HOME-owned and was
not edited. The ordinary fallback writer `saveTimelineInOrder` remains live;
the central fallback and all other families remain live. No legacy-caller
delta, before/after hash pair, or row-local patch artifact is claimed.

## Tests and next prerequisite

- No App targeted tests were run: this task was blocked before a justified
  product change existed.
- Required next step is exactly: after `full24749` releases the browser lock,
  run the registered relative service-root source preflight once; only if it
  passes, submit the registered producer actual once from the exact keeper.
  Do not treat the failed preflight as producer evidence.

