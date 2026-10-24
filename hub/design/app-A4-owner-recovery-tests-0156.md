## Report

- Migrated exactly two owner-recovery cases from `commitSession.test.ts` to new [`localSaveSession.ownerRecovery.test.ts`](/home/user/work/wt/app-A4-owner-recovery-tests-0156/src/tools/video-editor/commands/localSaveSession.ownerRecovery.test.ts).
- Preserved explicit recovery, lost ACK retry bytes, dependent B guards/display basis, key ordering, lock exclusion, canonical data, local preview, and zero legacy writes.
- Changed only the two assigned test files; helper and D31 remain untouched.
- Commit message written; `DONE` marker created.

Validation:

- Targeted Vitest: 6 files, 105 tests passed.
- TypeScript: root/app/node `tsc --noEmit --incremental false` passed.
- ESLint scoped with `--max-warnings 0`: passed.
- Diff/path/title census: passed; each title appears once in the new file and zero times in `commitSession.test.ts`.
- No full, browser, backend, service, or live-suite tests run.