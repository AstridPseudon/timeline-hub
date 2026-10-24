## Report

Implemented the reviewed A2 recovery-basis packet.

- Copied donor production/test blobs exactly.
- Removed only the seven-case legacy recovery matrix.
- Preserved current owner/lifecycle removals.
- Scope: exactly 3 App files.
- Wrote commit message and `DONE` marker.

Validation:

- Targeted union: **7 files, 106 tests passed**
- Node 20 TypeScript checks: **all 3 passed**
- Scoped ESLint (`--max-warnings 0`): **passed**
- `git diff --check`: **passed**
- Donor blob identities: **exact match**
- Base production precondition vs `5ad7907e86`: **unchanged**
- No full/browser/backend suites run.

No blockers.