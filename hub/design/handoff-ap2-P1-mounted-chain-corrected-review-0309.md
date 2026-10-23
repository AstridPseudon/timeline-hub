# P1 mounted-chain corrected-source review

Result: **FAIL — second independent source review**.

Reviewed App `d054162c9` on base `tl/ap2-P1-mounted-chain-first-return-0303`
(`1372d5fe7` prior source; prior independent review `0259` was FAIL). Only the
new `tests/e2e/local/three-products.p1-chain.spec.ts` differs from App 4394.
The first-return and source handoffs exist at the flat ORCH paths.

Two source-readiness gaps remain in exercised replies:

1. The refusal branch checks status/reason/current head and nonempty conflicts,
   but not the required normalized conflict entry `path` (or `ref`/path shape)
   from C0c §4.
2. The merged canonical closure checks the new clip's opaque data, but does not
   explicitly check that its foreign `org.example` namespace/null `clear` value
   and absent `app.astrid` state survive the merged reply. Those states are
   checked for other replies, not for the merged closure itself.

The correction otherwise addresses the prior FAIL: authentic pending dependent
outbox; trim held before `route.fetch`; Agent before trim acceptance; `merged`
plus authentic `rebased_onto`; post-acceptance lost ACK; exact body/key and
receipt retry with one history entry; stable created ID/order guards; refusal
canonical state/message; v2 step/dependency nesting; and legacy-write observer.
The fixture descriptor limitation and unexecuted invalid/preview variants are
honest. No live browser/socket/full/H3 run was performed.

Checks: Playwright list PASS (2 tests), TypeScript PASS, scoped ESLint PASS,
`git diff --check` PASS, and baseline-to-HEAD diff contains only the new spec.

Per the task instructions this is a second source failure and routes to Sol;
no source repair is made here.
