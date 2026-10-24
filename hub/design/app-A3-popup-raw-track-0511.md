## Report

Implemented A3/P2 popup ADD raw-track preservation.

- Added scoped occurrence raw-track policy to planner and prepared-media command path.
- Popup ADD now preserves captured compatible V2; missing, stale, inactive, wrong-kind, or source tracks refuse locally.
- Ordinary nearest-free/new-track planning remains unchanged.
- Added planner and mounted caller coverage.

Tests:

- Targeted Vitest: 23 passed.
- Adjacent media/drop/provider tests: 119 passed.
- `tsc` root/App/Node: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.

No full/browser suite run per instructions. Minimal change was required in `commands/media.ts` because the existing mounted carrier otherwise discarded the scoped policy before planning.