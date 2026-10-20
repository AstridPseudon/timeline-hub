Implemented the exact three fixes:

- Regenerated `elements/catalog.ts` via the normal script; only `am-presenter` revision changed.
- Replaced the bare `ASTRID_PACKS_PATH` string with the canonical constant.
- Updated the Runtime port test to use `use_runtime()` with an integration marker and removed the stale strict xfail.

Tests passed:

- Catalog: 3
- Env conformance: 4
- Text-binding neighbors: 22
- Runtime port: 1
- Scene answers: 30
- `git diff --check`

Only the three assigned files changed. No full suite was run. Detailed report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-full12-three-source-fixes/notes/report.md). DONE marker and commit message were written.