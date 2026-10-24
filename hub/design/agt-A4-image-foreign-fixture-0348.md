## Report

Implemented the foreign fixture liveness fix.

- `foreign_pin` now captures claim results and causal `waiting_for_worker`.
- Refreshes the existing authorized `publish-worker` registration with the current Runtime epoch, then retries with a new idempotency key.
- Verifies the claimed project is genuinely foreign.
- Added stale-registration focused coverage.
- Restored approved support pair byte-identically from `4ae4389062`.

Tests:

- Targeted foreign/support tests: **17 passed**
- Ruff: passed
- Private mypy: passed
- Vendor lock, artifact manifest, diff check: passed
- Syntax compilation: passed

The full parent-media file remains **20 failed / 17 passed** due pre-existing `provider executed a different command` mismatches outside this fixture change. No full suite was run. DONE marker and commit message are written.