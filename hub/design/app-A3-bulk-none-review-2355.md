## A3 review: PASS

- Source commit: `bf51d666a5`
- Parent/author base: `364f124b5c`
- Scope: exactly two files; no protected/oracle/generic-select edits.
- Production SHA256: `bd870acb...faa53c`
- Test SHA256: `7902cb44...a2c`
- Git blobs: `e04f155e...` / `6cf7ab2e...`

Verified the mounted caller preserves `__none__`, displays `None`, retains `{ transition: undefined }`, and leaves normal labels unchanged.

Tests/checks:

- Node20 Vitest union: 5 files, 182/182 passed.
- `tsc` app/node: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.

No full/browser/service suite run, per task limits. Review made no source edits. `DONE` and commit message were created.