Implemented and marked `DONE`.

- Updated both parity fixture `AggregateError` sites to include numbered inner error messages while preserving original errors/causes.
- Added direct regression coverage for visibility, identity, cause preservation, and sanitization.
- Tests:
  - Focused unit control: passed.
  - Direct formatter assertion: passed.
  - ESLint: passed.
  - TypeScript `--noEmit`: passed.
  - `git diff --check`: passed.
- No browser, renderer, helper, central, or full suite run.
- Commit message written to the requested path.