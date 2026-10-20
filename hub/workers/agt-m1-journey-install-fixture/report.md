## Done

Updated only `tests/journeys/test_journey_plumbing.py`:

- Replaced obsolete empty schema/theme package stubs.
- Added minimal valid `@banodoco/timeline-composition@0.0.8` manifest.
- Added required compiled `dist` export files.
- Preserved `npm ci` hint, `remotion-cli` hint, and final success.

Checks:

- Focused test: passed.
- Composition readiness tests: `6 passed, 1 deselected`.
- Full journey file: `79 passed, 6 failed, 2 deselected`; failures are unrelated localhost socket restrictions.
- Ruff: passed.
- `git diff --check`: passed.
- Commit messages written to both required paths.

No product, dependency, lockfile, or other test changes.