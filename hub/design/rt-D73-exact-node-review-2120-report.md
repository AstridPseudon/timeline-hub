## Result: FAIL_SOURCE_ONLY

Reviewed `ops-d73-exact-nodes` against the real launcher, `request-test`, `test-run`, parser semantics, immutable Runtime receipt, and Agent source origins.

Findings:

1. Rows omit `-m pytest -q`; launcher passes `-o` directly to Python, which exits 2.
2. Hard-coded request IDs/XML paths overwrite evidence across retries; not per central test ID.
3. Exact Agent origins contain launcher SHA `cec561…`, not reviewed launcher SHA `9f668e…`; the reviewed `PYTHONNOUSERSITE` fix is not consumed.
4. Five admission needs remain unapplied: two Agent receipts, rendered four-repo manifest, suite installation, and fresh per-ID results.

Passed source checks: exact 4+1 selectors, `--files` syntax, immutable Runtime commit/tree, source hashes, launcher syntax, no whole-file/fallback/filter/retarget, and retained positive17/poison-zero controls. Bodies and functional v2 behavior remain **NOTRUN**.

Evidence:

- [review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-review-2120/evidence/review.json)
- [source-manifest.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-review-2120/evidence/source-manifest.json)
- [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-review-2120/evidence/validation.md)
- [findings.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-review-2120/evidence/findings.md)

Checks: JSON validation, launcher `bash -n`, source/hash checks, selector/parser probes, and `git diff --check` all passed. No production files or suite configuration changed.