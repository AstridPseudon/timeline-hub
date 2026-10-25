# P2 D105a placement original handoff

- Readiness: `1 PASS / 0 FAIL / 0 SKIPPED`, duration `23.696006s`.
- Original: `0 PASS / 0 FAIL / 0 SKIPPED / 1 ERROR` in the XML; service exit `1`, body duration `144s`.
- Body: `app-pin-51239c79-p2-d105a-placement-0644-1025064349-31962`.
- Preflight: `app-pin-51239c79-p2-d105a-placement-0644-preflight-1025064319-2816` PASS.
- Host: `app-pin-51239c79`; tuple and trees are in the handoff JSON and actual manifest.

First predicate and source/caller:

`P2 Runtime phase sink already exists` at `tests/e2e/local/support/harness.ts:122`, from `prepareP2CommitPhaseCapture()` called by `DirectHarness.start()` at `tests/e2e/local/support/harness.ts:631`; original test entry is `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1199`. This is a setup error before the placement gesture.

Intended POST/status: NOT REACHED; HTTP/status UNKNOWN. No placement request, receipt, canonical/history/reload/native Undo result, or ring outcome was observed. Correlation is UNKNOWN.

Existing bounded D102 packet: prior ADD had intended Undo POST, HTTP 503, public `not_ready/runtime_unavailable`; internal reason, exception class chain, sanitized file:line:function, and ring correlation were UNKNOWN because no bounded diagnostic line was retained. The separate old D102 context regression was the strict `CommitContext` rejection of `request_id`, fixed by Runtime `1daca2a33`; this placement setup failure does not establish that cause.

Safe artifact paths:

- Actual manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-D105a-placement-original-0644/submission/p2-placement/actual-manifest.json`.
- Source preflight manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-D105a-placement-original-0644/submission/p2-placement/source-preflight-manifest.json`.
- Original XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-51239c79-p2-d105a-placement-0644-1025064349-31962/d66/p2-automatic-child-placement.xml`.
- Actual manifest SHA-256: `868f0bf1ef0f76b894fdaadf2d22f5eaa211ba8a348a8669f1ce6d3fc67248ae`.
- Source preflight manifest SHA-256: `2ec53255ac3de1dee82a774cb2eb8be0ab6c359c13ab9f466de4b94d3fc937a9`.

No raw logs, stacks, messages, locals, payloads, credentials, private URLs, or opaque identifier values are exported. No retry, alternate route, source fix, waiver, or gate GO was performed.
