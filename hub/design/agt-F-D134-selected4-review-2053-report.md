## Report

Verdict: `FAIL_SOURCE`

- Sol2041’s two `rebased` → `merged` assertions are source-supported for fresh omitted-control ABI-1 requests; historical exact-key receipts retain `rebased`.
- Found one blocking HTTP setup defect: the root patch installs `parent.clips: []`, then the next sequential patch asserts `clips` is absent, causing `previous_value_mismatch` before HTTP/lost-ACK/restart behavior.
- Seven UNKNOWN cases and authored request controls remain conserved. No product/test changes made.

Validation:

- Python 3.11 AST/compile: PASS
- Ruff: PASS
- Mypy: known baseline only (`types-PyYAML` missing)
- `git diff --check`: PASS
- Runtime pin: clean immutable `ab1e4f614198…`
- Exact own3 selectors: setup prerequisite refusal, 3 errors; no behavior credit
- HTTP selector: NOTRUN per prerequisite-stop rule

Evidence: `evidence/` in the worker directory. `DONE` and D134 commit message were created.