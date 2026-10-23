## Result

Updated only the existing `app ap2-P1-chain-h6` row in `ORCH/tests/suites.conf`.

- Bound to App `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a`, tree `6513960eb0b2704d02c3b3298ba594b546af7565`.
- Preserved Agent/Runtime pins, receipts, graph, invocation, Gate-5 blob, and original two case hashes via title-derived ranges.
- Outside-row hash preserved: `bd5ccb38e5cde235b36a06dff00be92a5f139cc711cc01d40944c3de29f586dd`.
- Worktree remains clean.

## Tests

- Node `v20.19.4` TAP safety test: **1/1 passed**
- App, Node, and root TypeScript checks under flock: **passed**
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- Outer/inner `bash -n`, positive/negative guards, and fail-fast ordering: **passed**

No browser, backend, global setup, seed, full suite, or central integration run was performed. Manager must submit the single requested `bin/request-test integration:app ap2-P1-chain-h6 --no-cache`.

Commit message and `DONE` marker created.