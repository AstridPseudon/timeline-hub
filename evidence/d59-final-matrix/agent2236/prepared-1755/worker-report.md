Prepared the final-core harness only.

- Added parametric D73 candidate rows for P4 and final-core with exact four-SHA receipt manifests.
- Refreshed collection: 8,817 nodes / 392 files.
  - Core-blocking: 8,814
  - D13 env: 1
  - D23 deferred known-gap selectors: 2
- Included newly merged orphan-cleanup coverage.
- Hardened launcher checks for Runtime lock (15 files), client/schema identity, optional parent guards, clean trees, and exact source hashes.
- Added scoped CAS installer helper; temp-registry verification preserved outside rows byte-identically with 0600 backup.
- Positive dry probe: exactly one stub call, exit 17 preserved.
- Poisoned SHA probe: rejected, zero stub calls.
- No core/P4/full/browser bodies or service requests executed.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-final-core-prep-1755/evidence/final-core-prepared/`

Validation included collection-only, `bash -n`, AST syntax checks, `git diff --check`, dry/poison probes, and CAS install verification.

Note: the current integration base lacked the helper described as already merged, so I added the scoped equivalent. Final tuple rebind and body execution remain gated by D72/D59.

Commit message and `DONE` marker created.