# D127 report

Verdict: **FAIL (source)**. Focused proof: **NOTRUN due source gate**.

Found blocking gap `D127-LIFECYCLE-001`: the validator accepts:

- `pending_at_stop` with a raised or ended dispatch phase.
- `returned_without_response` with a raised dispatch phase.

These contradict frozen helper derivation. No repository files were changed.

Passed:

- Node20 source selector: 2 passed, 2 skipped.
- Scoped ESLint.
- App and node TypeScript checks.
- `git diff --check`.
- Scope: only `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`.
- Helper SHA: `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`.
- Review commit: `5a9e0eb523353a95af45563a4f3e80bd8772222e`.
- Diff SHA256: `d8d1f5846ae9c198cd41c0364cd887f2591d2308de3b9ac7e5195575576148b3`.

Focused D78/bootstrap proof was not run because the brief requires SOURCE PASS first. Existing unchanged Runtime evidence was not duplicated.

Evidence is under the assigned worker `evidence/` directory; commit message and `DONE` marker are present. Recommended next step: bind lifecycle to dispatch phase state, add the missing contradiction negatives, then rerun source and focused proof.