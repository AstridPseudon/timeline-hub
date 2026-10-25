## D134 report

- Result: **UNAPPLIED**; no source changes.
- The required semantic setup is unavailable: `occurrence.create` cannot reproduce the declared shot-item correspondence; duplicate/place-shared require an authenticated source closure.
- Preserved all authored inputs, predicates, assertions, and behavior. No seed, API, guard, or product changes.

Validation:

- `py_compile` — PASS
- scoped Ruff — PASS
- scoped mypy — PASS
- `git diff --check` — PASS
- Targeted case reached the documented setup refusal: `shot item correspondence changed`

Evidence: `evidence/{source-manifest,predicate-map,setup-proof,validation,outcomes,progress}.*`

Blocked marker and commit message were written.