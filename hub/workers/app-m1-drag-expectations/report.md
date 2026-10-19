Implemented the test-only audit fix in [useClipDrag.test.tsx](/home/user/work/wt/app-m1-drag-expectations/src/tools/video-editor/hooks/useClipDrag.test.tsx).

- Restored original success assertions for the three group/multi/cross-track cases.
- Marked exactly those three with `it.fails`; singleton tests remain ordinary.
- No product or fallback changes.

Verification:

- Vitest: 2 files passed; 20 ordinary passes, exactly 3 expected failures.
- ESLint: passed.
- `git diff --check`: passed.

Wrote the commit message and report to the requested worker paths.