## Completed

- Added a narrow allowlist for exactly the three audited drag `it.fails` callsites.
- Preserved `MAX_SRC_ENTRIES = 0` and rejection of unrelated, fourth, duplicate, or misplaced markers.
- Added positive and negative gate tests.
- Wrote commit message and report to the requested paths.

## Verification

- Gate unit tests: passed.
- `npm run check:known-failures`: passed — 3 authorized, 0 forbidden.
- Drag Vitest: 2 files passed — 20 ordinary tests passed, exactly 3 expected failures.
- `git diff --check`: passed.

No product behavior is claimed restored; the three expected failures remain M2 work.