# P2 bulk21061 finite existing-evidence return

This is a bounded handback from the retained original run. It does not add a verdict, retry the profile, reconstruct a request body, or attribute a cause.

## Result

- Fixed tuple: App `fd2f843a` / tree `9fd43cb9`, Agent `0d142f79` / tree `f490451a`, Runtime `a3cd1a32` / tree `64bb0caf`, Composition `635f4de0` / tree `5ab5191a`.
- Preflight `19129`: PASS, exit 0.
- Original `21061`: FAIL, exit 1. Readiness passed; the bulk test errored after the caller-side 90-second `page.waitForResponse` timeout.
- The intended gesture POST was absent from the retained browser trace. The trace contains no POST to the commit route; it contains one successful history read and read-only inspection POSTs. Consequently there is no intended Runtime request ordinal, no Runtime-pending claim, and no commit receipt/result to report.

## Safe phase classification

The old schema-1 phase file contains Runtime commit phase records for only request ordinals 1 and 2. Both have observed handler, authorization, coordinator admission/lock, provider, accept, receipt, and HTTP response phases; both ended with HTTP status 200. Their timing precedes the browser gesture window and is classified as pre-gesture seed/setup. The phase file does not preserve the exact seed operation label or caller actor identity.

The old helper does not emit queue duration, handler duration, exact execution-lock wait, or caller receipt. These remain UNKNOWN. The 170 retained app-runtime terminal records are not mapped to route/body identity; two are failed (ordinals 42 and 45). No watchdog dump is attributed to the gesture or to phase request 1/2.

The profile lineage discrepancy is preserved: the lineage claims `7c1663…` / `1c2ac0…`, while the actual recorded source files are `e082c9…` / `fe3aac…`. This is an environment-provenance discrepancy only.

## Original records

The exact retained files remain at the paths listed in [finite-facts-21061.json](finite-facts-21061.json). The key records are the original manifest, readiness/original JUnit XML, log, phase JSONL, trace ZIP, and terminal-stack directory. The packet intentionally stores metadata and hashes only; it does not copy the 137 MB run.

Allowlisted source anchors are `tests/e2e/local/three-products.p2-tour.spec.ts:125` (commit response wait), `:664` (bulk gesture), and `:791` (test).
