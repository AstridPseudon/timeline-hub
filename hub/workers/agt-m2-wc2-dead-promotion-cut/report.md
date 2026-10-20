Implemented WC2 deletion sweep.

- Removed `promote_approved_authoring_candidate` (47-line helper) and three SDK export entries.
- Retained WC1 publisher, codecs, closure/feedback logic, and live render assertions.
- Retired only helper-specific tests; documented mapping/reviewer approval requirement in [agent-wc2-dead-helper-test-map.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc2-dead-helper-test-map.md).
- Census: zero production callers; only three test call sites and export references existed.

Tests:

- Targeted authoring/feedback/proposal tests: **112 passed, 6 deselected**.
- Explicit producer integration lane: **5 passed**.
- Ruff and `git diff --check`: passed.
- No full suite run.

Commit message and empty `DONE` marker created. Independent reviewer approval and manager merge remain pending.