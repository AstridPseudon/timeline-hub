# Handoff: ap2-P4-ten-reader-port-review-0604

## Verdict

**FAIL — out-of-scope tracked report.** The candidate source commit
`dd465f9e986a0bd690a4babe40199f86007c861a` is based directly on
`47aa77266f2287ad14519b07ce0bba7d4bba2170` and changes exactly the requested
test plus an added root `report.md`. The brief's one-path scope therefore
fails. The source tree was not modified by this review.

## Evidence

The requested test is byte-for-byte donor exact:

- donor `b8163c059a633af4b15836ab974188f6ed2fd398`
- donor blob `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`
- candidate test blob `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`
- direct donor→candidate test diff: exit 0

Base→candidate paths are:

```text
A report.md
M tests/editing_conformance/test_p4_ten_note_v2_runtime.py
```

The extra report blob is `b3cdb895dda475b025ffe0ef652dacfc15fa254c`.
`git diff --check` passed. The one-path outside-scope proof exits 1 solely for
that report. The candidate worktree was clean after inspection.

## Checks

- Integration collection with Runtime pin `34eac004`: **PASS**, exactly 1 test
  collected.
- Scoped Ruff on the test: **PASS**.
- Private-cache mypy on the test: **PASS**, no issues.
- No test body was executed.

## Boundaries

This was a bounded SOURCEPREP packet-fidelity review, not the independent
Agent product review and not acceptance-readiness. No HTTP, socket,
service/body, full suite, browser, build, or original-node run was performed.
No product or source changes were made. The owner should remove the extra
tracked `report.md`, then obtain a fresh current test-only port and repeat the
independent review before any acceptance-readiness or HTTP work.
