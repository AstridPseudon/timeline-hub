# D136c validation

Read-only validation performed; no test, import, collection, lint, typecheck,
product execution, rerun, or source edit was performed.

- `git rev-parse HEAD HEAD^{tree}` in the assigned Runtime worktree: **PASS**;
  `777f203885ba66d89439d45d584aadd41487119f`, tree
  `2c022e367128da7c556d94613fb0a4b2d1915a09`.
- Runtime changed-path check against `ab1e4f6141987706132916e2da16477f5a019464`:
  **PASS**, exactly the two reviewed Runtime sources and one reviewed test.
- Runtime and Agent source blob/SHA-256 checks: **PASS** for the bounded
  manifest; Agent is exact d133 and Runtime is exact 777f.
- AST-only allowlist extraction from `timeline_commit_auth.py`: **PASS**;
  exactly 13 approved keys, helper returns the closed map, and the only
  `safe_details` call site is the reviewed guard.
- Retained mode-0600 XML parse: **PASS**; 9 cases, 9 setup errors, 0
  failures, 0 passes, 0 skips, exit 1. Every case has the common first-seam
  message.
- Retained XML/stdout/stderr safe-key scan: **PASS**; `safe_diagnostic` occurs
  only as traceback source text (9 XML / 9 stdout occurrences); every approved
  value key occurs 0 times. Stderr is empty.
- Retained private artifact modes: **PASS**; XML/stdout/stderr are 0600. No
  raw artifact was copied or published.
- Focused reviewed source correlation: **PASS**; the existing Runtime test
  asserts `caught.value.as_dict()` contains the safe map and that removing
  only the map leaves the exact refusal envelope unchanged. Existing review
  reports the focused three-file diagnostics test as 3 passed; that result is
  reused, not rerun.

The retained result remains `FAIL_ACTUAL_ORIGINAL9` / `NO_GO` / `UNKNOWN`.
