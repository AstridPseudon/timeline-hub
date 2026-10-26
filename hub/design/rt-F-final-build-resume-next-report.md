## Report

- Preflight passed: corrected route/source/gate hashes matched; 5,112,872,960 bytes available.
- Submitted exactly one request: `integration:runtime delivery-v2-final --no-cache`.
- Request ID: `runtime-delivery-v2-final-1026174858-3359`
- `wait-test`: exit 2 in 0s.
- Refusal: `service TMPDIR is writable by another user: /tmp`
- Builder, staging, ZIP, and artifact validation: not run.
- No retry, alternate route, cleanup, or source changes. Worktree remains clean.
- Commit message written; `DONE` created.

Evidence: [result.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-build-resume-next/evidence/result.json)

The first-tool sampler captured 5,113,397,248 available bytes, but exited before request startup; sampler exit/reap is unknown. No builder lifecycle trace exists.

Recommended next step: repair the central service TMPDIR ownership/classifier configuration, then schedule a new authorized attempt.