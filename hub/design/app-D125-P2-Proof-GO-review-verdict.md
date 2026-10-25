# D125 independent Proof P2 verdict

Overall **NO-GO**. Qualified **partialGO** for five verified complete original tails only. The exact terminal request had 5 PASS, 2 FAIL, and 1 serially NOTRUN; GO requires all eight original tails to pass on the exact tuple with truthful custody.

The authentic preflight was `app-pin-fe3309db-d73-p2-fe3309db-submit-preflight-1025140913-15235` (PASS, exit 0). The sole terminal request was `app-pin-fe3309db-d73-p2-fe3309db-submit-1025140943-3250` (exit 1 after 554s, one body, no duplicate). Its durable submitted plan is present and hashes to `36fc0caa325e5a262a587c6342e329bca0929d49fe21e0a9f0c3bde3b9ad9a81`; it binds the exact IDs and recipes. Four pinned heads/trees and clean checkout state were independently verified.

Qualified PASS tails: popup ADD (`p2-popup.spec.ts:941`), parent move (`p2-tour.spec.ts:746`), transition None single (`p2-tour.spec.ts:778`), transition None bulk (`p2-tour.spec.ts:798`), and automatic child placement (`p2-elements-assets.spec.ts:1214`). Frozen helpers verify canonical closure/digests, history/records, reload, guarded native inverse, and zero legacy traffic. Popup ADD uses `assertOnlyCommits` (`p2-popup.spec.ts:338-349`); tour tails use `wire.legacy === []` (`p2-tour.spec.ts:688-744`); element tails use `assertNoLegacy` (`p2-elements-assets.spec.ts:773-775`).

Unmet cases:

- SWAP (`p2-popup.spec.ts:949`): first unmet predicate at line 495, expected accepted HTTP 200 but received 409. Public static tag `history_unavailable` matches Runtime/C0 source `runtime_protocol/timeline_commit_baseline.py:24-27`, `runtime_protocol/service.py:2572-2577`, and `contract/commit-v2.md:597-602`. Exact lower private phase-to-test attribution is **UNKNOWN**.
- Element edit (`p2-elements-assets.spec.ts:1038`): first unmet predicate at line 1052, dialog status did not contain `applied`. Pending element HTTP outcome is **UNKNOWN** without an authentic response; no backend cost is inferred.
- registerAsset (`p2-elements-assets.spec.ts:1133`): serially NOTRUN after the element-edit failure.

Readiness was 1/1 PASS. Reported profile: Node 20.19.4, Runtime AstridRuntime/0.1 with Python 3.13.16, workspace.v1, provider astrid-v1, compiler authoring-bundle-1. No historical result, native 1.75 result, source-only handoff, or Proof venue result was borrowed. No body, preflight, browser, suite, probe, replay, or source change was performed by this review. Raw payloads, credentials, private URLs, stacks, and opaque private identities remain unpublished. Source/typecheck/lint are N/A for this read-only review.
