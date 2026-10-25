## Completed

- Scoped `_request_id` per HTTP request while keeping repeated reads stable within one request.
- Fixed unavailable-route diagnostics to use a private ID plus SHA-256 public-ID hash.
- Corrected the new Ruff import-order issue.
- Added keep-alive, redaction, nested/thread isolation tests.
- Preserved public envelopes, strict contexts, tags, and persistence behavior.

## Tests

- Targeted diagnostics: `12 passed, 1 deselected`
- Adjacent runtime tests: `95 passed, 2 deselected`
- Compile: passed
- `git diff --check`: passed
- Ruff changed-file baseline comparison: zero new diagnostics

The deselected door test is blocked by sandbox socket permissions. Native/full provider replay was not run per task constraints.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-SWAP-3250-return-1444/evidence/verification.md`

Commit message and `DONE` marker are written. No design handoff was written because worker rules prohibit direct writes to `design/`; manager can publish from the evidence/final report.