# Runtime R2r full-seed review — 1728

Independent Luna review of `a00e009df4f568b2496291d3357b65dcfee8ca7c` against integration `d9e2a71e8`.

**Disposition: bounded Runtime acceptance PASS; complete cohort remains FAIL 437 passed / 1 failed.**

- Focused exact Agent-bac command: **67 passed in 65.55s**.
- Exact nine-file author cohort with exact Agent-bac tuple: **437 passed, 1 failed in 190.18s**. Sole failure: `test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]`, refusing before the new matcher because the authenticated original/landing input parent pin differs from the immutable source parent pin. This is the known Agent capture defect, not grounds to relax Runtime pin comparison.
- Original-nine strict regression with the required observer and permanent evidence: **9 passed in 16.89s**; 23 captures and 27 per-node reports retained.
- Ruff auth/test, Pyright auth, and `git diff --check`: all pass with zero diagnostics for the scoped files.
- Changed paths are exactly `runtime_protocol/timeline_commit_auth.py`, `tests/fixtures/timeline_three_products_seed.json`, and `tests/test_timeline_commit_sequential_verifier.py`. No product/provider/wire/schema/root-report/deletion changes.
- Red/green-complete/transcript-head packet SHA-256 declarations all verify. Green seed preserves 13,073-byte App body, SHA-256 `90f926fe...3721dd`, 21 commands, 21 steps, 21 assertions, atomic merge, receipt/history/restart/idempotency, and honest in-process transport.
- Separate central HTTP proof remains **1 passed in 1.74s** on snapshot tree `f79a2355cfb39d9ada7721978bd20d5702105778`; no duplicate HTTP credit claimed.

Evidence and full commands are in the worker report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-fullseed-review-1728/report.md`

Next owner: Agent capture correction for the transcript pin mismatch, then rerun the exact cohort. Do not declare 438 passed or full green.
