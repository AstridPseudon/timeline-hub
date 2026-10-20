## Completed

Ported public timeline-duration delegation to current App source:

- Updated seven Viewing callers.
- Replaced local evaluator with public Composition export.
- Preserved compatibility export and identity assertion.
- Kept playback-rate changes untouched.
- Added type-only assertions for App’s optional `theme`.

Verification:

- Focused Vitest: **8 files, 342 passed**
- Compatibility test: **1 file, 2 passed**
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- TypeScript: duration errors resolved; five unrelated existing errors remain.

Artifacts:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-duration-cut-current-source-port/report.md)
- `COMMAND`, `commit-msg`, and `DONE` created.

No full/browser/render/install tests or Git mutations performed.