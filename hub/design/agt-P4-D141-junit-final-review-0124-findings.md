# P4 D141c final JUnit source review

Verdict: `PASS_OPERATIONAL_SOURCE`.

The 0119 candidate source packet fixes the finite 0114 custody defect. The new immutable manifest (`95f5ce…a4ab3`), launcher-materialized control manifest, generated control runmanifest, and candidate shell argv all resolve to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-junit-binding-return-0119/evidence/body-evidence/p4-d141c.xml`

The input and intended body destination are distinct, the intended new destination is absent before controller/body work, and the stale 0047 JUnit destination is absent. Field-by-field comparison with the preserved old manifest found exactly one change: `junit_paths`. The frozen four-way tuple, origins, guards, versions, profile values, timeout, selector manifest, test hash, and service fields are unchanged.

The unchanged launcher has SHA-256 `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`; `bash -n` passes. The candidate command retains `run -- -m pytest`, cleared `addopts`, `-p no:cacheprovider`, `--timeout=45`, later `-m integration`, and exactly the three original selectors. Selector copies at 0047, 0055, and 0119 are byte-identical with SHA-256 `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`.

The unchanged launcher controls are source evidence only: positive control preflight `0`, body stub exit `17`, one counter line; Agent-SHA-only poison exits `1` with `D73 launcher: agent SHA mismatch`, no body exit receipt, and zero counter lines. No pytest, product import, collection, original body, suite install, registry mutation, socket, or controller dispatch was performed in this review.

Whole-path bounds:

- W001 is closed by the 0119 source correction. The original 0114 `FAIL` and its stale path are retained as historical evidence.
- W002 is qualified at the observed retention bound: actual `KEEP` markers exist for workers 0047, 0055, 0105, and 0119, and raw test records 1347 and 10086; durable ORCH record directories remain. The unchanged selector manifest path remains the 0047 path and is authentic/protected; its copy hash is `59a416…668ac4`. App cumulative verdict and final delivery receipt still own closure.
- W003 remains a bounded missing fact: no direct body-process module telemetry exists. Source identity is established by the unchanged strict launcher guards, same-process command environment, and exact source comparisons. No telemetry gate or collector is invented.
- W004 is an App receiver dependency after an actual final result. No App receiver-owned body receipt exists yet; this is not a candidate source defect.

The preserved 10086 service is authentic 3/3 PASS, exit `0`, with JUnit SHA-256 `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`. The preserved 1347 service remains exit `1`, zero selectors, and no JUnit. Neither result is rewritten or reclassified.

This is source qualification only. It is not body/P4 behavior credit, CAS installation credit, REG credit, ship credit, MAIN GO, or cumulative qualification.
