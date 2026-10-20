Implemented the bounded SDK port.

- Updated `astrid/sdk/remote.py` to project Runtime rows through existing canonical image fieldsets before `open_authoring_bundle`.
- Added real HTTP regression coverage in `tests/sdk/test_timeline_checkout_history_runtime.py`.
- No private952 schema/client/core changes.

Tests:

- Direct neighbors: `46 passed`.
- Public013 HTTP suite: `3 passed in 17.78s`.
- `git diff --check`: passed.
- No full/private952 suites run.

Created `commit-msg` and `DONE`.