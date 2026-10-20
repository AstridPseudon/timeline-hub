Implemented the WC3 explicit pin-type guard.

- `_pending_matches` now accepts only `None`/`None` or two exact five-field mappings.
- Added parameterized malformed-type refusal tests and valid-form tests.
- Verified outbox/session state remains unchanged on refusal.

Tests:

- Replacement tests: **20 passed**
- Sync neighbor tests: **3 passed**
- Ruff: **passed**
- `git diff --check`: **passed**

Handoff: [agent-wc3-explicit-pin-type-guard.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc3-explicit-pin-type-guard.md)

No full suite or private Runtime qualification was run. Commit message and `DONE` marker were written as requested.