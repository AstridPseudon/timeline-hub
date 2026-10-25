# D127 protected review report

Overall: **FAIL**.

- `PASS_PROOF`: exact existing central request `app-D127-leaf-retention-author-1606-targeted-1025160952-28551` passed: **23 passed in 3.46s**, matching candidate tree `4fc171c...`.
- Source semantics and privacy/bounds checks passed; only the two authorized files changed.
- Exact assertion custody failed: parent has 19 test functions but **160**, not 169, `ast.Assert` nodes. Five existing tests have changed assertion ASTs.
- App84857’s strict validator is incompatible with the new fields/lifecycle values and candidate helper SHA256 `4ee0424b...`. App-owned seam: `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`, especially `assertRetention`, `assertSampling`, `assertCaptureEvent`, and `readCapture`.

Checks:

- Offline pytest: `21 passed, 2 deselected`
- Ruff: passed via `/root/.local/bin/ruff` (requested venv path unavailable)
- Mypy helper: passed
- Private Python 3.11 compile: passed
- `git diff --check`: passed
- No browser, native, full, collector, activation, or duplicate central request run.

Artifacts:

- `evidence/verdict.json`
- `evidence/verdict.md`
- `evidence/source-custody.json`
- `evidence/commands-results.md`
- `evidence/facts.json`

No source edits were made. Recommended next steps: resolve the exact assertion-custody gate and update the App validator for the candidate schema/hash before qualification.