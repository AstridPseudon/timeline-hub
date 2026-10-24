Implemented the faithful A4 replay migration:

- Added [localSaveSession.replayProtocol.test.ts](/home/user/work/wt/app-A4-replay-protocol-0233/src/tools/video-editor/commands/localSaveSession.replayProtocol.test.ts).
- Migrated the uncertain-A/unsent-B replay case using real IndexedDB/outbox recovery.
- Preserved five old declarations unchanged where current A2 lacks equivalent APIs (`observe`, `undo`, legacy fallback, etc.).

Validation:

- Vitest: 6 files, 124 tests passed.
- TypeScript: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` all passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.

Commit message and `DONE` marker written.