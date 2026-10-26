# F D141l freeze2 proof independent review

## Verdict

**FAIL.** The integrated Agent/Runtime/Composition tuple, 22/17 selectors, flags, approved stub hash, poison-only manifest delta, and D89d arithmetic pass static review. The source packet cannot pass because the pristine comparator omits the required custody controls and the future admission validator is not actually authenticated or tuple-bound.

## Concrete findings

- **F-001 — blocking:** `command-pristine.sh:36-61` is only a pre-disk check plus direct pytest. It has no exact SHA/tree/path or clean guard, before/after source records, interpreter witness, raw/XML/log custody, after-disk check, continuous monitor, one-heavy lock, or body/monitor/evidence status propagation.
- **F-002 — blocking:** the pristine route enforces only the 4 GB stop floor, not the D89d full-pair floor `4714564096` with a dispatch witness.
- **F-003 — blocking:** the pristine JUnit parent `evidence/private/pristine` is not created by the script, and raw output files are not owned or retained by it.
- **F-004 — blocking:** `admitted_dispatch` accepts a JSON file and brief based on weak shape checks and a substring. It does not bind the existing authenticated request-test/test-run receipt, exact service/request ID, source tuple/tree, manifest, command, or brief hash; stale/self-authored material can pass.
- **F-005 — blocking-receiving:** App is represented by a nonexistent sentinel path and placeholder SHA/tree/parents. A genuine future App receipt cannot be consumed by this command as authored. This remains a receiving prerequisite, not source approval.
- **F-006 — provenance:** the source packet says the task text contained `303e`, but the genuine source-worker manager brief contains `303a`; Git confirms `303a` exists and `303e` does not. Do not report the unsupported discrepancy as input history.
- **F-007 — custody:** the cut’s writable `KEEP` marker is not protection, and neither route verifies modes, inode/path identity, complete dependent-directory custody, or post-run raw/XML dataflow. The pristine route has no KEEP marker.
- **F-008 — parity:** cut and pristine environments differ: cut has the toolchain Node path and `ASTRID_RUNTIME_SOURCE_ROOT`; pristine omits both and does not verify interpreter realpath/version.
- **F-009 — trace gap:** the genuine source-work trace is continuous only from `05:00:57Z` to `05:04:32Z` (44 five-second samples, minimum `4693712896`). It does not cover the earlier `04:57:57.501Z` source dispatch; the older 254-sample trace is retained 26496 evidence, not a backfill.

## Genuine later receiving requirements

1. Verify the App owner’s genuine freeze-2 receiving receipt and bind its exact head/tree/parents through the existing normal route.
2. Issue one controller admission at or above `4714564096` bytes and validate its exact route receipt, service/request identity, source tuple, command, and brief.
3. Run the required Agent 8585/pristine 64197 full pair with corrected custody, then run the explicitly authorized selected CLI P4 reproof. No new scope decision is owed.

No product tests, collection, provider import, service request, body, pin, source, or historical receipt mutation was performed.
