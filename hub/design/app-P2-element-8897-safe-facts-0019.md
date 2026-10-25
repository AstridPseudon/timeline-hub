# P2 element safe evidence handoff

Run `app-pin-fd2f843a-p2-provider-element-0014-1025001412-8897` is a finite same-ID handoff for the released Runtime `a3cd1a32…` tuple. It is not an independent NO-GO review or a whole-path diagnosis.

## Correlated facts

- Pins: App `fd2f843a…` / tree `9fd43cb9…`; Agent `0d142f79…` / tree `f490451a…`; Runtime `a3cd1a32…` / tree `64bb0caf…`; Composition `635f4de0…` / tree `5ab5191a…`.
- Readiness: 1 passed; XML suite time 26.681106 s, testcase 9.775 s.
- Original: 1 failed; XML suite/testcase time 26.388 s; line 412 timed out after 5 s waiting for dialog status `applied`. The retained body diagnostic records the response watcher seeing `page_closed` during teardown.
- The phase JSONL has 123 records: 120 phase events plus 3 summaries. All three summaries have `truncated: false`; the helper bounds are 8 requests, 128 events, 64 KiB, a 2 s watchdog, and one watchdog capture.
- Ordinals 1 and 2 complete through provider, accept, receipt, and HTTP response. Each has two observed HTTP response events, both status 200. Their handler spans are 2,208.971 ms and 18,129.731 ms.
- The element apply request correlates to ordinal 3. Its last recorded phase is `authorization`; provider has one start with no end; accept, receipt, and HTTP response are absent/UNKNOWN. Handler, coordinator admission, coordinator lock, and provider are started without a retained end.
- The single 2 s watchdog dump is owned by ordinal 3: it is the only ordinal with an incomplete dispatch. The private dump remains mode 0600 and was not copied or printed. Safe projection: 4 thread sections, 72 frames, with `validate_commit_value` in `runtime_protocol/timeline_commit_validation.py:173` categorized as provider validation.
- The actual pending window is 4,518 ms from diagnostic `request-start` to test outcome, and 4,563 ms to page close. Only 45 ms of post-test-outcome activity is retained. No post-close outcome is available; any later response is UNKNOWN.

## Safe comparison boundary

The authentic published 7131/Runtime 732 packet reports the same line-412 boundary and no observed accept/receipt/HTTP response, but does not provide this run’s three-ordinal phase capture. The authentic 11589/Runtime bc04 packet reports ordinal-3 provider validation with 4,558 ms to test outcome and 4,626 ms to page close. Current a3cd is 4,518 ms and 4,563 ms, with ordinal 3 provider-started but incomplete. These are boundary differences only; they do not establish a common cause, deadlock, or permanent failure.

## Retention and method

The source manifest, XML, phase JSONL, private stack dump, and safe diagnostic were checked by exact SHA-256, timestamp, size, and mode. Raw bodies, auth material, keys, URLs, request identifiers, and raw stack text remain private. The complete v2 request/reply shapes in `/home/user/work/runtime/contract/commit-v2.md` were read and left unchanged.

No production source, test, collector, browser run, endpoint, debugger, or full suite was added or changed. No source-dependent test rerun was made.
