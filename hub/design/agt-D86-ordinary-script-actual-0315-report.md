## Report

Completed the source-only F-D86 actual9211 correction on base `7e23790248f17b8a4492fc9aee88d2c4e1df328d` (`tl/integration`).

Changed only the three allowed files:

- S3 parent/media caller now uses `capture_clip_add`, preserving the original row and opaque identity while supplying authoritative `created` claims.
- Ordinary union caller now commits occurrence creation separately from text bindings, preserving both parameterized cases and retry/grouped-inverse assertions.
- Timeline script caller now performs a genuine timeline text-binding rebind and reads the prior accepted revision, preserving the historical-script proof and 96db canonical digest correction.

Original selectors, parameters, decorators, assertions, raises, branches, identities, and guards remain conserved.

Candidate blobs:

- S3: `b6c0224200543ed30af96361c0d6bddf3caeca9f`
- Ordinary union: `52d62549652d089268bcf6b59d96ff43e68a62ca`
- Timeline script: `729445cd499dd2f975b7374cce95ed8a44b97e5d`

Baseline blobs were `de9f02e...`, `e9351f0...`, and `91c85a2...`.

Validation completed:

- Candidate and baseline Ruff: passed.
- Candidate and baseline mypy: passed with no issues.
- `git diff --check`: passed.
- AST parse/compile and selector/assertion/control-flow conservation: passed.

No pytest, collection, helper/fixture execution, service, browser, build, or timing run was performed. Functional behavior remains pending protected review and the central behavior batch.

Proposed existing D72 log entry: `F-D86 actual9211 / ordinaryscript4 source correction`. No ledger or product files were written.

All 161 actual outcomes remain retained; outside this reservation, existing family findings are unchanged. Actual11789 remains under its separate classifier.

Commit message written:

```text
test(timeline): F-D86 correct ordinary script callers

Align the reserved ordinary-script scenarios with current allocation, capture,
and timeline text-binding APIs while preserving their original proofs.
```

`DONE` was created.