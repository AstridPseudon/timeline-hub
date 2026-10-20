# Runtime full-suite attribution correction — 2026-10-20T12:38:53Z

Audit1213 correctly found that the queued request had been described as an immutable2c4 snapshot. That was false. The process error was reading a provisional queued snap as final.

| Request | Actual source | Actual state/result |
|---|---|---|
| runtime-full-restore-integration-1020095412-22308 | Runtime tree2ae8508a1d3dac62e99c27056585eedc62bf5ff6, matching8609333 | FINAL:5194passed,7known failures,18skipped,25xfailed,316.42s; historical ONLY |
| runtime-full-restore-integration-1020112501-27435 | Runtime tree330ea3969cb9cce77271404f31793c21abd5993f, matching129493b2aff614560d9b7ac2577957e799cf30ec | RUNNING; no final result/count yet |

Cause: test-run recomputes integration HEAD/tree on each queued attempt before slot checks. It freezes source only when RUNNING and creates the test snapshot. No test-service code change is required. Runtime now records a queued tree only as provisional, records actual running/final snap, and verifies every claimed result against raw summary/snap/cached_from before publishing. Future worker briefs explicitly state START-time attribution. This request was never a completed2c4 full and no second full was submitted.

The source publication remains immutable clientproducer2c4/013 with its exact800/61/9/1/5 passing gates. Compatible server patches and tests are recorded separately. This running full covers their current batch at129493b; it is not an all-green result yet. Artifact bytes still equal2c4. Existing registered-completion strict positives remain OPEN; no refusal was loosened.
