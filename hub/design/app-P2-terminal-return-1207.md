## D30 report — P2 same-ID return

No code, config, source, or test changes. Worktree remains clean. Commit message written and `DONE` created.

Retained run only:

`wait-test app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933`

Result: exit 1, 469s; 0 passed, 3 failed, 5 not run. Preflight, native seed/history, selector collection, and mounted readiness passed.

Failures:

1. `tests/e2e/local/three-products.p2-elements-assets.spec.ts:377:1`; assertion `:391` expected dialog status substring `applied`, but the status element was absent after 5s. H36 recorded `apply-click → request-start → retained`; request was a scoped commit with an idempotency key, terminal remained `pending`. No response, request-failed, request-finished, abort, receipt, or server outcome was observed.

2. `tests/e2e/local/three-products.p2-popup.spec.ts:815:1`; deep equality at `:464` expected the added child row track `V2`, received `plate`. The failure occurred before `accepted(...)` at `:807`; popup receipt/history correlation is therefore unverified.

3. `tests/e2e/local/three-products.p2-tour.spec.ts:690:1`; receipt correlation at `:299` expected `receipt.receipt_id === post.key`. Safe classes: expected UUID-like id, SHA-256 `a498bfcfedceca40f633865067adb023668946b0cf9dedfb9bb386c1f11bc1ff`; received `txn-` plus 32 hex, SHA-256 `a8b67fbb0d387da2799168471c7cbebbccfb4b90953fccc54dbd430772276c43`. HTTP 200 and accepted/merged-shaped data were reached; durable history was not checked afterward.

H36 retention is qualified against d6ed’s producer:

- Trigger: collector has an Apply boundary; fixture retention runs in `tests/e2e/local/support/app.ts:89-96`.
- Writer: `tests/e2e/local/support/p2-element-diagnostic.ts:320-363`.
- Bounds: 24 events, 8 pending requests, 24 KiB serialized output, 500 ms retention deadline, 150 ms UI read, elapsed values capped at 600,000 ms.
- Allowlisted enums and nested keys are enforced by the selected projector; URLs, bodies, authorization, payloads, and private identifiers are not serialized.
- Actual H36 state: `observed`, failed test, `beforePageClose=true`, `pageClosed=false`, connection `connected`, dialog `present`, UI status `unknown`, response status `UNKNOWN`, response `none`, failure `none`, terminal `pending`, losses all false.
- The producer has no `requestfinished` stage; absent response/failure/abort facts remain unknown.

Evidence inventory:

- Summary: 50,361 bytes, SHA-256 `624248a835d9611364063959810a2c7fc136df03e7a659ac10db40719599b510`.
- Log: 13,303 bytes, SHA-256 `909b20b7ebb753f55186a5e21df0eb7df2fc16b6a03e2cd929fe88c6b3899b8f`.
- Primary error contexts: element 14,295 bytes (`1a382b…`), popup 16,057 bytes (`093e68…`), tour 12,244 bytes (`06cb70…`).
- H36 source and attachment are both 1,260 bytes, SHA-256 `08509524d5fd04f181b3fac8d0cdd211a32e2f4a107c4e78807ae4713e8533a4`; attachment identity is `p2-element-apply-diagnostic-json-e10a7d579404ff3c3025f251ecd178c60be77a1c.json`.
- Mounted bootstrap, D21 environment, and mounted-readiness diagnostics were inventoried from the retained result; traces were not extracted or used.

Selected App source: `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e6deed676b917f857708445b7d37a5aa8`, parents `cad736828b4890a4df5fff42a22bfa4851a0ecfc` and `01ea81395a9bb8f091262a9d8275407675188fe6`. Same-ID snapshot commit/parents were not separately retained. Daemon/provider identity is unavailable.

`git diff --check`: PASS. No repeat, live GO, probe, browser, build, HTTP, or backend run performed.