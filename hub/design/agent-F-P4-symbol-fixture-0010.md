Implemented the single permitted fixture edit in [cases.json](/home/user/work/wt/agt-F-P4-symbol-fixture-0010/tests/sdk/fixtures/p4_commit_cases/cases.json:21), replacing the stale symbol with `test_ordinary_edit_literal_move_uses_commit_outbox`.

Tests/checks:

- Targeted P4 + retained caller: `2 passed`
- Ruff baseline: `2148/2148`
- Private mypy baseline: `1911/1911`
- Artifact manifest: current
- Vendor lock: valid; matching frozen producer also passes
- Byte-level diff: only the symbol replacement
- `git diff --check`: passed

The required `rt-pin-8ea0766f` producer check reports its existing expected pin mismatch (`34eac004…` vs `8ea0766f…`); no pin was changed. No blockers. Completion marker and commit message were written; no commit was run.