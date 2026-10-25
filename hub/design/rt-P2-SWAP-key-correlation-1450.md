# Report

Implemented P2 SWAP key correlation in the existing private diagnostic path.

- Added `idempotency_key_sha256`: exact accepted `Idempotency-Key`, UTF-8 SHA-256, lowercase hex.
- Added nested/thread-local request scope.
- Preserved raw-secret privacy, public responses, headers, persistence, schemas, and provider context.
- Absent, invalid, control-containing, or oversized keys omit the field.
- Preserved protected keepalive/private-ID/Ruff corrections.

Tests:

- 52 passed: diagnostic, history, unavailable-path, coordinator suites.
- 16 passed: commit routes.
- Ruff new test: passed.
- Production Ruff: 37 inherited baseline diagnostics, no new diagnostics.
- Compileall and `git diff --check`: passed.

Evidence: [source-handoff.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-SWAP-key-correlation-1450/evidence/source-handoff.md)

Live socket/keepalive, provider/native/browser/full suites remain unverified and require central test service. Commit message and `DONE` marker are present; harness should commit.