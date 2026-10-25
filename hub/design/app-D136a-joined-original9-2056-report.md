# D136a/D100 report

- Imported exactly the three reviewed Runtime blobs onto base `3082cad…`; source hashes and scope verified.
- Scoped checks: 45 tests passed; Ruff, mypy, compile, and diff checks passed.
- Ran the exact original9 once at 5,039,394,816 free bytes:
  - Result: **9 errors, 0 passes, 0 failures, 0 skipped; exit 1**
  - Common first seam for all selectors: `candidate: all authored fps declarations must retain their typed locations`
  - No retry, adaptation, fixture migration, or alternate Runtime used.
- Raw XML/log/metadata remain private mode `0600`.
- Evidence: [evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D136a-joined-original9-2056/evidence>)
- Commit message written: `test(agent): receive D136a source for original9 proof`
- `DONE` marker created.

Release remains held pending independent review of the actual failure.