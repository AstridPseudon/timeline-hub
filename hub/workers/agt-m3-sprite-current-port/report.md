Implemented the approved AM-sprite port onto `8e310785` only.

Changed:

- Sprite component with shared draw/capability geometry.
- Direct sprite capability test.
- Generated catalog: AM-sprite revision only.
- Preserved protected current bytes and excluded snap-plate/presenter/theme/core changes.

Tests:

- Sprite tests: 17 passed.
- Sprite + scene-host + SDK neighbors: 33 passed.
- Catalog freshness: 1 passed.
- Ruff and `git diff --check`: passed.

No full suite, render/export, browser, or live-socket tests run.

Reports:

- [Design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-sprite-current-port.md)
- [Worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-sprite-current-port/notes/report.md)

Completion marker and commit message were written.