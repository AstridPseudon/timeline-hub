# D141w independent custody whole-path review

Bounded verdict: **FAIL_CUSTODY**, not a product or popup-functional verdict.

- `p2-automatic-child-placement`: **PASS**. Preflight `...preflight-1026101609-6758` passed; normal `...submit-1026101639-9168` passed with exit 0 in 259 s. Native readiness and guarded Undo/placement both passed.
- `p2-popup-add`: **FAIL_CUSTODY**. Preflight `...preflight-1026102125-437` passed, but normal IDs `...submit-1026102149-13234` and `...submit-1026102155-20413` both ended `cancelled`. No popup body verdict is credited.
- `p2-parent-move`, `p2-transition-none-single`, `p2-transition-none-bulk`, `p2-register-asset`, `p1`, `p3`: **NOTRUN**.

The unchanged builder has one normal `request-test` call per `--submit` invocation. The first invocation was still able to create ID `...2149-13234` after the artifact contained only the passing preflight. The worker then launched a second `--submit` resume against that same artifact, creating `...2155-20413`; the daemon recorded it as an identical run in flight. This is overlapping worker/process custody misuse, not a native internal retry and not an independent caller. The first divergence was launching the resume at controller-log lines 2579–2641 while the initial invocation from lines 2460–2521 had not been proven dead; the trace shows the overlap at `10:21:49.224`/`10:21:49.227` and IDs at `10:21:54.262`/`10:21:59.291`.

The prior worker's initial progress/KEEP obligation failure remains an actual custody limitation; this review does not backfill it or convert missing evidence into a pass.

ID `13234` was running, cancellation was queued, and wait/reap reached terminal `cancelled` with exit 130. ID `20413` was queued, cancellation was queued, and wait reached terminal `cancelled` with no body exit/summary; its retained `why` says it was identical to `13234` in flight. Neither body is credited. The retained five-second traces contain 63 placement samples (minimum 5,622,292,480 bytes) and 36 popup samples (minimum 5,776,478,208 bytes); neither reached the 4,000,000,000-byte standing stop. A separate review-only two-sample five-second `df` trace is recorded; it did not run or backfill any service work.

One bounded next step: continue only with the original reviewed remaining-selector packet, beginning at `p2-parent-move`, with one live submit owner and same-artifact/same-ID inspection. Preserve both popup IDs as cancelled and do not reopen or rerun popup ADD. If any resumed artifact lacks the actual normal ID, stop and retain the first custody error; do not issue another request.

No source, product, test, registry, queue, generated file, pin, Git metadata, canonical install, body, browser, diagnostic, request-test, wait-test, request-stop-test, full suite, typecheck, or lint command was run by this review. The assigned Composition worktree remains clean.
