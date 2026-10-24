# R2r D83 report

- Added one isolated `d83-request-lock-2135-integration` suite row; no product/test-body changes.
- Exact pins: Runtime `bc04caa23f4b503fc55e49769ead20677904702a` / tree `fa696b342468ae191735409822fa3c7c66f8a590`; Agent `5fc1f300fb4fe5913a7bdc990b1f531402c2f258` / tree `a17033330871619d059677cef919d2b788b2cd8f`.
- Prepared control copied byte-exactly; SHA-256 `a7133d389fc72fca216a277c2f1687515673ea29251a42bdcee84baa2916dc80`.

Tests:

- One `request-test ... --no-cache` submitted.
- Initial launcher attempt: zero-body failure because the central snapshot uses a synthetic `HEAD`; recorded separately.
- Corrected only that assertion to use `HEAD^`, then reran the same ID.
- Genuine control executed: 3 accepted commits, history count 2→3, overlapping history/third-commit completed.
- Result: `1 failed`; required `_historical_sequential` span was absent. Classification remains `UNKNOWN`; no causal lock conclusion.

Evidence: [control.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-lock-service-2135/evidence/control.xml), [metrics.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-lock-service-2135/evidence/metrics.json), [safe summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-lock-service-2135/evidence/control-safe-summary.json). Raw stacks remain mode `0600`.

Commit message and `DONE` were created.