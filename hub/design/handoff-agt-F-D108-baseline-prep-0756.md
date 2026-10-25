# F-D108 source-only baseline preparation

Prepared the exact upstream924 comparison inputs for MAIN's pending `agent-core-full` terminal. This handoff is source-only; no body, collection, service, browser, install, probe, registry, suite, product, or test action was performed.

Evidence index:

- `workers/agt-F-D108-baseline-prep-0756/evidence/d108-upstream924-node-index.tsv`
- SHA-256: `72534d6e122d282310f9275952f9711abd73c4a3ff8194e6eb5d56b6867cf917`
- 276 unique D54a rows, ordered 1..276.
- Each row retains the raw current node ID, current-selector identity, source-inventory membership, upstream raw node ID/outcome, XML ordinal and testcase blob identity; failure kind/type/location and failure-text identity are retained where present.

The 201 upstream-absent rows carry exactly one existing bounded D63 function-name/body rename check: 2 authenticated counterparts, 199 no-match results, 0 ambiguous results. Known D13 ENV and D23 deferred identities are pre-indexed; D52 records zero approved dead-scope assignments in this exact set.

Summary JSON: `workers/agt-F-D108-baseline-prep-0756/evidence/d108-upstream924-node-index-summary.json` (SHA-256 `61d309853e1e68f20de4238c7cde258bc485462a7c17251c06b56e58e05e3736`). Handoff JSON contains the source custody paths and hashes.

The retained service `agt-F-D60-baseline-amend-1336-full-upstream-final-9244377-1024135120-1621` is FAIL, not PASS: 12,396 passed, 91 failed, 14 errors, 16 skipped, 566 subtests; XML SHA-256 `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`. Per the D54 custody correction, full-run Runtime isolation remains uncertain. No current failure classification or numeric core-open count is published before the D108 terminal.

Validation: XML parsed to its closing `</testsuites>`, exact-set uniqueness/order arithmetic passed, and source hashes were captured. MAIN must bind the existing D73 manifest/checkouts and run the unchanged published command from `agent-core-full-command.md`.
