## Result

Created safe retained-evidence pack:

- `evidence/swap29224-facts.json`
- `evidence/swap29224-facts.tsv`
- `evidence/swap29224-facts.md`

Key finding: the original popup SWAP observed HTTP 503 `not_ready` / `runtime_unavailable`; this was not the intended accepted commit reply (expected 200 with receipt).

Runtime ledger correlation:

- Ordinals 1–2 completed provider, accept, receipt, and HTTP 200 response phases.
- Ordinal 3 retained only `provider/start`; accept, receipt, provider-end, and response phases are unavailable.
- No backend failure was inferred.

Tests/typecheck/lint were not run per the evidence-only brief. Prior retained checks: popup oracle 4/4 passed, D66 plain-stack checks 22/22 passed, and the central original run failed only at popup SWAP with readiness passing.

Commit message written to the requested path; `DONE` marker created. No product or test files changed.