Implemented the retained-pidfd proof fix.

- Verifies retained pidfd identity/fingerprint before and after polling.
- Accepts only valid `POLLIN`/`POLLIN|POLLHUP` terminal events.
- Rejects closed, invalid, substituted, ordinary, and error descriptors.
- `_PIDFD_RELEASED` requires birth-bound terminal provenance.
- Added live-child negative and genuine-exit tests; original tests unchanged.

Validation:

- Central strict lane: **629 passed, 16 skipped**, exit 0.
- Focused tests: **3 passed**.
- Updated `probe_pidfd.py`: all controls pass.
- No full suite run; Darwin-native tests remain unverified.

Artifacts written: `report.md`, `commit-msg`, `commit-msg.txt`, `DONE`. Fresh separate Sol security review and D13 join remain required gates.