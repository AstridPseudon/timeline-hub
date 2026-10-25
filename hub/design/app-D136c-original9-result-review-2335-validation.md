# D136c validation

## Read-only checks

- `git rev-parse HEAD HEAD^{tree} HEAD^`: PASS; carrier commit is on the
  immutable Runtime parent.
- `git diff --name-status <immutable-parent>..HEAD`: PASS; exactly two modified
  Runtime source files and one added reviewed diagnostic test.
- Reviewed-donor and carrier blob SHA-256 comparison: PASS for all three files.
- Immutable Agent auth/store preimage comparison: PASS.
- Protected Agent projection SHA-256 and AST body count: PASS; 43 predicates,
  11 test bodies, and 54 fixture statements remain recorded unchanged.
- `git diff --check`: PASS.
- Private XML aggregate parser: PASS; exact nine-case reconciliation, 9 errors,
  0 failures, 0 passes, 0 skips, and every case has an error node.
- Safe-artifact raw-content scan: PASS; no XML, traceback, URL, credential,
  private-path, or payload pattern found.
- Safe allowlist/schema AST check: PASS; source keys equal the approved keys,
  ordinal bounds are `0..1000000` or `UNKNOWN`, and digest shape/output are
  `sha256:<64 lowercase hex>` with one-way hashing only.
- Custody stat check: PASS; retained raw directory is mode 0700, raw files are
  mode 0600, and KEEP markers are present.
- Admission check: PASS; available disk was above the 5,000,000,000-byte floor;
  no active pytest, Vitest, Playwright, Chrome, or Chromium runner was found.

## Test policy

No pytest body, full suite, browser/live-socket suite, lint, typecheck, or product
execution was run by this independent review. Existing `rt-D136c-security-review-2312`
targeted results are reused for the exact reviewed source, as directed.
