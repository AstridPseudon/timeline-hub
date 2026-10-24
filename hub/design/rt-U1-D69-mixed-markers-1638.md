## Report

Implemented U1-D69:

- Removed both blanket whole-test xfails.
- Preserved strict live catalog predicates and the project-reference idempotency test body.
- Removed only retired publication/timeline-positive segments.
- Added exact ledger-entry proposal under worker evidence; production ledger unchanged.
- Wrote commit message and `DONE`.

Validation:

- Targeted central runtime tests: **6 passed**.
- Python compile, Ruff, TypeScript `tsc --noEmit`, and `git diff --check`: passed.
- Pyright: 13 inherited test-typing diagnostics.
- Conformance generator check: pre-existing stale generated artifacts; unchanged.
- Broader refusal-guard collection was blocked by missing `ASTRID_CHECKOUT`; no source failure established.

No full suite run.