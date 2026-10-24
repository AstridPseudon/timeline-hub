## Completed

- Updated only [useTimelineCommandsService.persistence.test.tsx](/home/user/work/wt/app-A4-mounted-fixture-return-0059/src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx).
- Added complete five-field old/new Runtime media selections.
- Updated assertions to the current `clip.duplicate-media` semantic request, including reads, created IDs, merge mode, steps, and reply metadata.
- Preserved legacy capture tests and production code unchanged.

## Verification

- Baseline: 6 tests failed as expected.
- A4 union: 8 files, 111/111 tests passed.
- Focused media set: 3 files, 33/33 tests passed.
- Locked App/Node/root TypeScript checks: passed.
- Scoped ESLint: passed with zero warnings.
- `git diff --check` and outside-scope audit: passed; one test file changed.

The raw `0.01 → 0` legacy normalization remains covered by the dormant capture test; the mounted fixture uses the current normalized UI form.

Commit message and `DONE` marker written. No full/browser/service suites run.