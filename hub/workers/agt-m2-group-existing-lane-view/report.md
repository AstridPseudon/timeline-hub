Implemented atomic existing-lane group moves, explicit ownership bindings, typed child-lane creation, and a pure derived group view.

- Targeted tests: **704 passed, 1 deselected, 1 strict xfail** for pending shared isolation.
- Ruff, targeted mypy, and Runtime lock check passed.
- Normal Runtime admission: **1 passed**.
- Real migration probe: **7 passed, 2 failed**, still blocked by bootstrap `command.created` omission.
- No full suite or browser run. **M2 remains HELD.**

[Report with exact commands, decisions, and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-existing-lane-view/notes/report.md). Contract, candidate schema, and harness commit message written.