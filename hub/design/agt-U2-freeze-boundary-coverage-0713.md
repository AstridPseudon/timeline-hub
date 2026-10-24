## Report

Restored U2 boundary assertions in the three permitted test files:

- D18 bounded waits/admission deadline and materialization-budget refusal.
- Activation claim denial, lost reply, readiness, custody, cleanup, provider fail-closed, and lifecycle predicates.
- Media timeline/registry identity, digest/origin, and exact frame equality checks.

Validation:

- Exact collection: **632 tests collected**
- Compile: passed
- Scoped mypy: passed, no issues
- Ruff: no new diagnostics versus baseline
- Worker diff check: passed
- Origin-main ancestry: passed

No test bodies, real-host, render, browser, full-suite, or provider journeys were run per instructions. Pre-existing unrelated diff-check findings remain in `position-keys.ts` and `test_duck.py`.

Commit message and `DONE` marker created.