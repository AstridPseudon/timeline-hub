## Report

Implemented A3 carrier preservation.

- Added optional `mediaSelection?: MediaSelection` to `TimelineProvisionedAsset`.
- Preserved Runtime selection through `prepareGenerationAsset`.
- Confirmed existing `ShotTimelineMediaControls` consumer forwards it unchanged.
- Added qualified and missing-selection regression coverage.

Tests passed:

- Focused Vitest: 2 files, 14 tests passed.
- App TypeScript check under lock: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Scope limited to 4 permitted files.

Commit message written and `DONE` marker created.