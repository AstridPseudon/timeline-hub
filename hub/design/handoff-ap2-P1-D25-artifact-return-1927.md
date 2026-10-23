# Handoff: P1/D25 bounded failure artifacts

PASS. On top of `53b5733c3cc930bab55b3216b9f72f1bee112888`, the App failure continuation now persists its minimal parseable artifact before any potentially hanging IndexedDB or DOM collection. Enrichment is bounded per read at 150 ms and overall at 1,000 ms; artifact writes/attachments are bounded at 500 ms. Unknowns remain explicit and the original assertion remains primary.

Only the three allowed test files changed. The second-case collector call and both protected test bodies are unchanged. Protected hashes: first `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; second `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`.

Evidence: focused safety 15/15, root/App/Node no-emit PASS, scoped ESLint PASS, Playwright list exactly 2 PASS, diff/scope checks PASS. No browser/service/full run. Harness must create the commit from this worktree; no commit or Git ref was written by the worker.

