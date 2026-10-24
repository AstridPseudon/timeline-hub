## Report

- Added [ShotTimelinePreview.full-caller.a3.test.tsx](/home/user/work/wt/app-A3-popup-full-caller-witness-0754/src/tools/travel-between-images/components/ShotTimelinePreview.full-caller.a3.test.tsx).
- No production or existing test files changed.
- The witness mounts the real popup, exercises upload → prepared media → V2 placement, and retains strict commit request/response assertions.

Tests:

- Focused Vitest: passed with `1 expected fail`; blocked before `applyEdit` because derived `assetEntry` fields fail serialized-config validation.
- Neighboring popup/service tests: 4 files, 61 tests passed.
- ESLint: passed.
- Root, app, and node TypeScript configs: passed.
- `git diff --check`: clean.

Decision/blocker: preserved the full original expectation via `it.fails`; the product seam requires source-owner repair before the witness can reach outbox/Runtime commit. Node 20 was unavailable; validation ran on Node 22.22.0.

Commit message written and `DONE` created.