## Done

- Added real HTTP CLI move qualification: lost ACK → restart → exact retry → undo.
- Added fallback coverage for symbolic, occurrence, draft, and unsupported/mixed flags.
- Preserved WC7/WC8 helpers; AG02 remains partial with no deletion marking.

Tests:

- 29 targeted unit tests passed.
- 3 real Runtime HTTP integration tests passed.
- Ruff passed.
- `git diff --check` passed.

No full suite, `make check`, or browser tests run. Report and commit message are recorded; DONE marker created.