Implemented exact source-bound allocation maps, stable replay/inverse handling, both item codecs, typed item births, and verified SDK ACK validation.

- Tests: **584 passed, 1 default deselection**.
- Scoped Ruff and `git diff --check`: passed.
- Product delta: **+397 lines**; budget overrun and counterexamples documented.
- Both commit-message files are ready.

Official paired generation, App ACK updates, and actual Runtime admission tests remain unverified. No full suite ran.

[Report with exact commands and decisions](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-map-impl/notes/report.md) · [Contract handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-materialization-map.md)