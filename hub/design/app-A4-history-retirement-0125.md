Implemented A4 on `fb27e554a9`.

Changes:
- Removed `historyCommandRunner` execution and command-entry metadata from `useTimelineHistory`.
- Local undo/redo now uses existing snapshot reconstruction.
- Preserved mounted Runtime guarded undo/redo path.
- Retained all history assertions: 96 hook assertions, 37 remote-boundary assertions.
- Updated media history tests to exercise snapshot behavior.
- Changed only the three owned files.

Validation:

- Vitest: 6 files, 95 tests passed.
- Root/App/Node TypeScript checks: passed.
- Scoped ESLint: passed with `--max-warnings 0`.
- `git diff --check`: passed.
- No remaining runner references in owned history files.
- `currentmedia.test.ts` does not exist; ran existing `commands/media.test.ts` instead.

Commit message written with required `A4:` prefix. Completion marker created.