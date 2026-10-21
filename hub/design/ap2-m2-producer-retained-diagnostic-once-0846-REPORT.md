# Producer retained diagnostic — 0846

## Result

The approved single retained diagnostic was executed once and **failed before producer execution**. No App source, spec, assertion, selector, timeout, pin, or helper changed. Live callers changed: **NONE**. Historical runs 23671 and 17481 remain FAIL/UNKNOWN.

## Central runs

- Preflight suite: ap2-m2-producer-retention-recover-review-0838-preflight-b7c6f480
- Preflight run ID: ap2-m2-producer-retained-diagnostic-once-0846-ap2-m2-producer-retention-recover-review-0838-preflight-b7c6f480-1021084449-25899
- Preflight: PASS, exit 0, 7 seconds, checks=11; service App tree c1ac3383624322ae8d67b10dee36965670d91cd7.
- Actual suite: ap2-m2-producer-retention-recover-review-0838-run-b7c6f480
- Actual run ID: ap2-m2-producer-retained-diagnostic-once-0846-ap2-m2-producer-retention-recover-review-0838-run-b7c6f480-1021084525-19080
- Actual: FAIL, exit 1, 92 seconds, exactly 1 test collected and 1 executed (1 failed).
- Actual log: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-retained-diagnostic-once-0846-ap2-m2-producer-retention-recover-review-0838-run-b7c6f480-1021084525-19080/log.txt

The two named suites were generated from the full syntax-checked literal body in the approved 0838 report. The actual suite command ended with:

    ... && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-custody-gate-0717-owned.sh | cut -d' ' -f1)" = b7c6f4806c02d8315b3eb69c4b4c469e7b908375603a5a0c967df5bbae60efb9 && flock -n /home/user/work/.app-m1-browser.lock true && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/artifacts/producer-startup-custody-gate-0717-owned.sh run

Central submission commands:

    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-retained-diagnostic-once-0846 ap2-m2-producer-retention-recover-review-0838-preflight-b7c6f480 --no-cache)
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-retained-diagnostic-once-0846-ap2-m2-producer-retention-recover-review-0838-preflight-b7c6f480-1021084449-25899
    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-retained-diagnostic-once-0846 ap2-m2-producer-retention-recover-review-0838-run-b7c6f480 --no-cache)
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-retained-diagnostic-once-0846-ap2-m2-producer-retention-recover-review-0838-run-b7c6f480-1021084525-19080

## Source and artifact identity

- Keeper: /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717, HEAD 6b0267c62aa8773132f1496d5014279e6c1edf61, tree c1ac3383624322ae8d67b10dee36965670d91cd7, clean, KEEP present.
- Service snapshot: App tree c1ac3383624322ae8d67b10dee36965670d91cd7, clean.
- Agent pin: 8130a401bf44a518d5a40ae274d398b8c560be55.
- Runtime pin: 2c4ac180c2220bdad966bc01e95ad230e99ce26a.
- Final0822 custody gate: b7c6f4806c02d8315b3eb69c4b4c469e7b908375603a5a0c967df5bbae60efb9.

Final0822 sha256sum -c artifacts.sha256: PASS, 8/8. The retained packet is /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-real-retention-path-cause-0822/evidence/failure-1792572330-28858/.

Packet SHA256SUMS verification: PASS:

    e76c6936742c7325c445c2a4e1f5a2ef8fac3cf946695025f7b71fb658199594  ./browser-output/.last-run.json
    465fcd7c9b075104c2ba8784b156374bbe664f8f9473cd9d93aebe301feb61ef  ./browser-output/producer-ownership-current-8d488-ves-only-owned-scene-output/error-context.md
    83da20c50cfc949ea1690f410a04e92c306238f64948846e11f6cbab68d1a972  ./browser-output/producer-ownership-current-8d488-ves-only-owned-scene-output/trace.zip
    cff312e8d7dcc17b3382e799c3c359cbbb7866d2f6ac56347dc48cfeb7c693f3  ./child.log
    e6c687ceb56f8e9e72e548ab036213c9fb4517247f9ae65204a5a1e9e053b6b0  ./identity.txt

unzip -t trace.zip: PASS, no compressed-data errors.

## First causal boundary

The unchanged test failed at tests/e2e/local/producer-ownership-current-pin.spec.ts:92:

    getByTestId('transcript-lane-chip'): expected 2, received 0 after 5 seconds

The retained DOM shows the seeded route reached the mounted timeline: the dedicated project/timeline were selected, the Transcript data lane was visible, and exactly two protected transcript occurrence buttons rendered with the expected labels and source IDs. Playwright found no data-testid="transcript-lane-chip" elements. The first causal boundary is therefore the App mounted transcript-lane rendering/test contract (rendered occurrence buttons versus the expected chip test ID), not the producer and not missing seed publication. No deeper source cause is claimed.

The trace also records ACP 503 acp_unavailable responses and one Runtime commits-history 409 history_unavailable. These are observed secondary conditions, not proven causes of the missing chip selector; the timeline/revision reads used by the fixture returned 200.

## Reached versus unreached

Reached: hosted build, one browser worker, fixture setup, route navigation, Runtime health/timeline/revision reads, Transcript lane visibility, initial chip-count assertion, and durable packet retention.

Unreached: transcriptRegenerate, sceneMoveShots, any producer mutation request, accepted commit, refusal branch, lost-ACK retry, inverse/undo, zero-legacy assertion, and later protected-row checks. No retry or second actual was submitted.

## Minimal next action

The App owner should diagnose why the current mounted route renders the two transcript occurrences without the existing transcript-lane-chip test ID (including whether the route uses the registered renderer or host fallback), using this retained DOM/trace packet. Do not repair, alter assertions/selectors/timeouts/auth, rerun, cut a writer, or claim producer qualification from this run.
