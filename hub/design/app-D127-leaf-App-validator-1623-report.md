# D127 report

Implemented strict reviewed-new App validator adoption in [p2-runtime-phase-bootstrap.test.ts](/home/user/work/wt/app-D127-leaf-App-validator-1623/tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts).

- Added exact helper hash arm for `4ee0424b…`.
- Validates lifecycle, leaf frames, loss/share/denominator relationships, buffer completeness, durations, privacy, and phase contradictions.
- Preserved normal and legacy `6c9…` arms.
- Added focused mutation coverage.
- Only assigned file changed.

Tests:

- Mutation selector: PASS.
- D105 bootstrap control: PASS.
- Scoped ESLint: PASS.
- `git diff --check`: PASS.
- D78 bootstrap: blocked; selected Runtime checkout lacks the helper.
- Strict typecheck: fails on existing missing generated/virtual modules and unrelated errors.

Candidate helper hash verified exactly. No activation, actual P2, browser, full suite, or service replay run.

Evidence: `facts.json`, `source-custody.json`, `predicate-map.json`, `commands-results.md`.