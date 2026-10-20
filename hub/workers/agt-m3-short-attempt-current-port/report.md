Implemented the short ephemeral-attempt port.

- Added owner-only `0700` ephemeral roots with stable reclaim prefix.
- Added bounded `.r-*` Remotion scratch allocation and diagnostics.
- Preserved `RenderRequest.verified_source` and strict source validation unchanged.
- Added ownership, cleanup, symlink/foreign-root, socket-path, and envelope tests.

Tests passed:

- `71 passed in 11.39s`
- `6 passed, 27 deselected in 3.26s`
- `py_compile` passed
- `git diff --check` passed

Browser/MP4, full, and live-socket suites were not run per instruction. Report, commit messages, and `DONE` marker are written.