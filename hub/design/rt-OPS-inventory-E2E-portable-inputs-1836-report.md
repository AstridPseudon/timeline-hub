Implemented portable whole-maker E2E fixture correction.

- Packaged exact parent `0857a5…` and candidate `c3226b…` makers with modes/hashes.
- Removed archive `.git`/source-sibling dependency.
- Added private `tests/suites.conf` projection baseline before Store initialization.
- Added exhaustive non-mutating `--check-only`, including interpreter, wheel/bootstrap, Git/source, Store API, `df`, path, and hash checks.
- Added required evidence files and `DONE` marker.

Tests passed:

- `unittest discover`: 40/40
- Ruff, AST/compile, shell syntax, `git diff --check`
- Offline dependency wheel build: exact hashes
- Check-only negative census: exit 2, 19 simultaneous missing prerequisites, no mutation
- Maker/verifier hash preservation: PASS

Genuine whole-maker E2E was not run: free space was ~4.99GB, below the unchanged 5.905GB start reserve. Evidence is under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-E2E-portable-inputs-1836/evidence/`

Commit message written; harness will commit changes.