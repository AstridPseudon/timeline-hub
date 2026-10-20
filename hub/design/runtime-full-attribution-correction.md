# Runtime full-suite attribution correction — 2026-10-20T12:38:53Z

## Correction dated 2026-10-20

The raw artifacts for `rt-m2-promotion-integrated-gates-full-restore-integration-1020150647-16434` correct the attribution of the later Runtime full. Its authoritative START source was the promotion-only integration state: merge `81f8c7e0b22c34804015c054762af3d737e4698a`, tree `0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`. The raw result is **5523 passed, 14 failed, 18 skipped, 22 xfailed** (exit 1).

The 14 failures are seven known baseline nodes plus seven new visual-seam nodes. The seven visual-seam nodes are **unclassified** here; this record does not turn them into promotion regressions or storage-preflight findings. The full covers the `0e3a5b9`/`81f8` promotion state only. It does **not** cover the later `a51` CAS merge or `c45` text resolution, and it makes no current-green, current-full, delivery, or pin-mutation claim.

Prior full `16608` remains raw **5533 passed / 8 failed / 18 skipped / 24 xfailed** on its exact `7f6` source; it includes seven known baseline failures plus the inherited audit race fixed by `16ac`. Its raw count remains eight. The current public producer `0.2.13`/`2c4` is immutable and the compatible server is a distinct source. Any future full is manager-direct `integration:runtime` work only.

This correction changes document attribution only; the request, snapshot, summary, and log under the test-service artifact directory remain unchanged.

Audit1213 correctly found that the queued request had been described as an immutable2c4 snapshot. That was false. The process error was reading a provisional queued snap as final.

| Request | Actual source | Actual state/result |
|---|---|---|
| runtime-full-restore-integration-1020095412-22308 | Runtime tree2ae8508a1d3dac62e99c27056585eedc62bf5ff6, matching8609333 | FINAL:5194passed,7known failures,18skipped,25xfailed,316.42s; historical ONLY |
| runtime-full-restore-integration-1020112501-27435 | Runtime tree330ea3969cb9cce77271404f31793c21abd5993f, matching129493b2aff614560d9b7ac2577957e799cf30ec | FINAL:5491passed,7same known failures,18skipped,24xfailed,621.80s; statusFAIL/exit1,0new failure nodes |

Cause: test-run recomputes integration HEAD/tree on each queued attempt before slot checks. It freezes source only when RUNNING and creates the test snapshot. No test-service code change is required. Runtime now records a queued tree only as provisional, records actual running/final snap, and verifies every claimed result against raw summary/snap/cached_from before publishing. Future worker briefs explicitly state START-time attribution. This request was never a completed2c4 full and no second full was submitted.

The source publication remains immutable clientproducer2c4/013 with its exact800/61/9/1/5 passing gates. Compatible server patches and tests are recorded separately. The completed full covers the current batch at129493b. All seven failure node IDs exactly match historical22308; this is baseline-only, not an all-green suite. Artifact bytes still equal2c4. Existing registered-completion strict positives remain OPEN; no refusal was loosened.
