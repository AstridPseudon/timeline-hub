Implemented the scoped test correction.

- Removed obsolete canonical-collision xfail.
- Added positive assertions for same echo/different word IDs producing distinct revisions and digests.
- Preserved existing restore and anchored-reference coverage.
- No product code, schema, registry, or restore args changed.

Tests: 97 scoped cases passed across word-reference, timing, kernel, and Runtime ABI suites. `git diff --check` passed; zero xfails remain in the edited test.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-word-reference-review/notes/report.md)

Commit message files written; no commit performed.