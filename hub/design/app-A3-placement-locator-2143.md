## Report

- Confirmed root cause: protected P2 helper targets raw clip IDs, while mounted child timeline renders occurrence-qualified action IDs. Retained trace/DOM evidence shows both rendered clips exist; failure occurs at `dropFileIn` line 358 after 5 seconds.
- No production code changed. A production selector/DOM change would risk breaking gesture action identity.
- Proposed test-owner fix: qualify both helper selectors as `${occurrenceId}:${rawClipId}`. Protected spec must be updated serially by its owner.

Tests/checks:

- Focused Vitest: 2 files, 33 tests passed.
- `git diff --check`: passed.
- Protected hashes: unchanged and exact.
- Retained mounted run: failed at the selector mismatch; no browser/service rerun performed.
- TypeScript and ESLint not run because this was review-only with no source diff.

Worktree is clean. `DONE` marker and commit message were created.