Implemented the launcher repair in `orch/tests/suites.conf`:

- Restored canonical `agent full` row from retained backup.
- Preserved active `full-upstream-25359` and legacy `full-current-v3-1229` rows byte-for-byte.
- Fixed premature preflight `exec`.
- Added the single permitted JUnit output argument.
- Created UTC CAS backup and evidence.
- Wrote commit message and `DONE`.

Validation:

- Outside-byte and row/hash assertions: PASS.
- `bash -n` syntax checks: PASS.
- Stub matrix: current/upstream pass → pytest once, exit 23; preflight failure → zero pytest, exit 17.
- Worktree status: clean.
- No full suite or production caller run performed, per task constraints.