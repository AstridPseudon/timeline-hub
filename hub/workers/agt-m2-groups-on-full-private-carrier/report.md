## Done

Implemented the private group first slice onto full357:

- `timeline.migrate-groups`
- Existing-lane `occurrence.move`
- Pure `project_group_view` with explicit bindings
- Private schema: 57 definitions / 31 clauses
- Ordinary schema floor preserved: 55 / 29
- Current materialization and source-authority behavior preserved

Hashes:

- Full357 schema: `613123b2…aaad3`
- Private proposal schema: `428a396a…4e65`

Tests:

- Group conformance: **85 passed**
- Existing Agent neighbors: **401 passed**
- Schema checks: **5 passed**
- Ruff, JSON validation, and `git diff --check`: passed
- No full, Runtime live, App, browser, renderer, or macOS suites run.

Handoff files written:

- `report.md`
- `commit-msg`
- `commit-msg.txt`
- `DONE`

Public generation/freeze remains intentionally pending peer carrier agreement.