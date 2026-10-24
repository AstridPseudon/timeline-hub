## Outcome

Restored authoritative preview revision status.

- Canonical previews use `canonicalComposition.headRevisionId`.
- Ordinary previews use saved timeline head identity.
- Pending/error saves display local status, never false commitment.
- Revision labels travel through the existing Player mailbox.
- Added mounted reload, accepted, and pending-status tests.

## Verification

- Focused Vitest: 4 files, 109 tests passed.
- Scoped ESLint: passed.
- `tsconfig.app.json`, root `tsconfig.json`, and `tsconfig.node.json`: passed.
- `git diff --check`: passed.
- No full/browser/e2e suite run.

Commit message and `DONE` marker are ready. Requested design filename was unavailable; plan, brief, verdict, prior report, and source history were reviewed.