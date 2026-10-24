## Result

Migrated `commitSession.genericPatch.test.ts` off `createTimelineCommandSession`/`genericPatchPort` onto `createLocalSaveSession` and the durable outbox.

- Preserved all five cases.
- Preserved exact `doc.patch` request body, commands, protected track-label property, retry bytes, and idempotency key.
- Guard cases now exercise the current local-save handoff source guard with null displayed publication.
- Added only [localSaveSessionEnvironment.ts](/home/user/work/wt/app-A4-session-test-migration-0116/src/tools/video-editor/commands/__tests__/localSaveSessionEnvironment.ts).

## Tests

Passed:

- Vitest: 4 files, 57 tests
- ESLint scoped, `--max-warnings 0`
- TypeScript App, Node, and root configs with `--noEmit --incremental false`
- `git diff --check`

No full/browser/HTTP suite run, per task scope.

Commit message written and `DONE` marker created.