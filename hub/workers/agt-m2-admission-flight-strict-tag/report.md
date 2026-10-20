Implemented and completed P2 strict flight discrimination.

- Unknown/present `flight.kind` values now fail closed before mutation or dispatch; legacy absent-tag commits and `assembly-admission` remain supported.
- Added exact-byte/no-retry regression coverage.
- Focus suite: 138 passed.
- Sheet suite: 70 passed.
- Central private wrapper: 15 passed, 2 unchanged xfails; outer 4 passed.
- Ruff and `git diff --check`: passed.
- No full suite or shared dependency changes.

Reports:

- [agent-admission-flight-tag-fix.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-admission-flight-tag-fix.md)
- [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-admission-flight-strict-tag/notes/report.md)

`commit-msg` and `DONE` are written.