## D124 report

- Ran the authenticated 14-node host-bootstrap proof against Agent `b742893426a46a99a2f30583a54faeebe2bd98b7` / tree `ccb2f286…` and Runtime `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad` / tree `1d3e06f…`.
- Central request: `runtime-d118-upstream23-targeted-1025130322-26621`
- Result: **14 passed, 0 failed, exit 0** in 2.29s.
- XML, exact selector/member hash, AST counterpart hashes, and four real process-origin records validated successfully. All imported modules came from the exact b742/d4f496 checkouts.
- Validation passed: `ruff check`, Python AST/compile, `bash -n`, `git diff --check`.
- Evidence: `evidence/` (68 KB), including XML, source/member map, origins, central receipt, and hashes.
- One earlier request had zero test body due to the worker `tmpdir` metadata file shape; it is preserved separately as infrastructure failure, not PASS. The subsequent run was the sole actual proof.
- No product/test/generated changes; worktree is clean. `DONE` and commit message created.

Limit: this proves only the pristine b742/d4f496 14-node scope. It does not close current integration regressions, render behavior, absent neighbors, or full-suite status. No `design/` file was written per the workspace report-output restriction; this final message is the report.