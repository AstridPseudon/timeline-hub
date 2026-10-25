# D136c report

- Traced the exact Runtime → Agent provider → refusal → JUnit path. The first serialization loss is pytest JUnit’s `append_error` (`_pytest/junitxml.py:217-229`), which omits `RuntimeErrorBase.details`.
- Retained XML: 9 setup errors, 0 passes/failures/skips; approved diagnostic value keys occurred zero times. Classification remains `UNKNOWN`; no product-gap claim.
- Preserved guard decision, C0v2 shapes, authored inputs, privacy, and all 43 assertions/11 bodies/54 fixture statements.
- No tests or product execution run. Read-only checks, AST/schema validation, hashes, and retained XML parsing passed. Existing reviewed diagnostic test result reused: 3 passed.
- No further original-nine run is needed. Qualification remains `FAIL_ACTUAL_ORIGINAL9` / `NO_GO`; D130 holds remain.
- Evidence written: `evidence/{seam-map.json,findings.md,source-manifest.json,validation.md,handoff.md}`.
- Commit message written to the required path; `DONE` created.