# D127 report

Verdict: **FAIL**.

Found an App-owned strictness gap in `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts:257-280`: reviewed-new `lifecycle` is not cross-validated against phases, durations, or `retention.final_request.outcome`. Contradictory completed/returned/pending states can pass.

Proof passed:

- D105 + D127 validator mutations: **2 passed**
- Qualified Runtime D78 bootstrap: **1 passed**
- Qualified Runtime reviewed-new normal harness/bootstrap with exact helper `4ee0424b…`: **1 passed**
- ESLint, App/node TypeScript checks, Ruff, mypy, Python 3.11 compile, diff check: **passed**
- Runtime focused observer test: **1 passed**
- Reused central receipt: **23 passed in 3.46s**, not duplicated

`npm run typecheck:strict-islands` remains baseline-failing on missing generated/virtual modules and unrelated implicit-any errors.

No source edits, installs, generated files, activation, full/browser/native/SWAP suites, or unrelated profiles were performed. Evidence is under `evidence/`; prior 1613 FAIL remains retained.