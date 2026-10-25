# Report

Verdict: **FAIL**.

Reviewed the plan and prep artifacts read-only. Passing checks:

- JSON parsing and `bash -n` for normal/preflight fragments.
- Exact 22-root selector/order crosswalk.
- Named upstream and captured integration commit/tree provenance.
- 100 Python source hashes against Runtime 7070.
- `git diff --check`.

Blocking findings:

- C0 example uses `optionalreads`; contract requires step `reads`.
- `Idempotency-Key` is incorrectly shown inside JSON instead of as an HTTP header.
- Five missing roots and the D73 launcher lack explicit `UNKNOWN_MISSING_UPSTREAM_SELECTOR`.
- Frozen-ref labels resolve to different objects than recorded commits.
- Reported 41-file matrix has only 34 manifest entries and a generated-cache hash mismatch.

No tests, runners, bodies, installs, heavy suites, or writes to product/shared sources were performed. D59/census remain pending; no executable pristine-upstream gate is claimed.

Outputs:

- [review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-tail-pristine-review-1851/evidence/review.json)
- [source-manifest.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-tail-pristine-review-1851/evidence/source-manifest.json)
- [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-tail-pristine-review-1851/evidence/validation.md)

Commit message and `DONE` marker were created.