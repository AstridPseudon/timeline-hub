# D118 WC6three report

Changed only `tests/sdk/test_wc6_completion_capture.py`:

- Updated the source blob assertion to current/original `070dfc5` blob `adc6fb…`.
- Updated the mounted caller error expectation to `transport_error`.

Checks passed:

- Ruff
- Mypy
- Py_compile
- `git diff --check`
- AST assertion conservation and exact input-source comparison

Targeted tests: `12 passed, 3 failed`.

Remaining blockers are outside scope:

- Protected runtime qualname assertion fails because the current method is wrapped.
- Protected offline cause assertion exposes missing `clear_replay_memo`.
- Runner guard rejects helper hash `f17c…` versus pinned `067e…`; helper/pin files were not authorized.

No product, helper, pin, socket, full-suite, or service changes made. Future qualification belongs to Agent core service selector `agent-core-full` after owner fixes. Commit message and `DONE` are recorded.