# D111 element29218 retained lifecycle facts

Result: the retained packet supplies a finite failing-request lifecycle record, but it does not record process start/restart, store creation, fallback, or cache-clear behavior. Those fields are `UNKNOWN`.

## Evidence

- Historical tuple matches the requested fixed tuple: App `0b6cee269f32079c5446036bbca8a484176799bc`, Agent `8c88ea8f06b65f9b79fb7810af04720845c5cc6f`, Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- `d66/runtime-private/p2-commit-phase.jsonl` is 17,589 bytes, SHA-256 `82f12c15de1747274dcbc8d2df536928caa7bec8fff9b87c79ed27d2e71b6733`; it parses as 128 JSON objects: 3 summaries and 125 phase events.
- Retention counters: rolling capacity 128; 135 events seen; 128 retained; 7 dropped. The final retained request has 22 events seen/retained and outcome `pending`.
- Runtime request ordinal 3 has phase events 104–125, from 33,900.778 ms through 35,005.407 ms: dispatch queue start/end, handler entry start, eight authorization start/end pairs, coordinator admission/lock starts, and provider start. No provider end, receipt, accept, or HTTP response was recorded for that ordinal. The summary's last phase is `authorization` and its response/receipt/provider durations are unresolved.
- Request ordinals 1 and 2 have retained HTTP response phase pairs with status 200 (four status events each). This is a phase fact only and is not attributed to the element request.
- `d66/p2-element/three-products.p2-elements-4b4f7-tch-reload-and-guarded-Undo/p2-element-apply-diagnostic.json` is 2,344 bytes, SHA-256 `8f7c1d0ee9aad49d0170a39e6f3be963624f39d6715df220c14db3b067d90ad1`. It records six App events: apply-click (25,206 ms), request-start (25,769 ms), test-outcome (30,438 ms), retained (30,474 ms), teardown-start (30,475 ms), page-close (30,489 ms). Response status is `UNKNOWN`; terminal state is `pending`; page close is observed; UI at retention was connected/present/pending/applying.
- `d66/runtime-private/runtime.stderr.log` is empty (0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Runtime stdout is 513 bytes but is not exported or interpreted because it contains private service material.

## Explicit unknowns and searched files

I searched the complete 418-member `d66.tgz` listing and the full parsed `d66/runtime-private/p2-commit-phase.jsonl`. No startup/spawn/process-boundary/store/fallback/cache-clear artifact or phase was present. The 12,753-byte `d66/runtime-private/p2-commit-phase.stacks.txt` is retained only by hash (`e81648260b440449572e2c9beb146d41bf2c2c7b5f7c225a8df19b6bae887fb5`); its raw content is not exported and does not prove cold/restart/error/fallback.

Accordingly, process boundary, process start, restart, store creation/reuse, fallback, cache clear, causal error, Runtime response/receipt for the incomplete request, and production non-flat-curve status are `UNKNOWN`. No source, instrumentation, browser/body/replay/provider/profile/HTTP/service capture, or test rerun was performed.

The complete machine-readable packet, including all artifact hashes and sanitized event ordinals/timings, is [element29218-lifecycle.json](./element29218-lifecycle.json).
