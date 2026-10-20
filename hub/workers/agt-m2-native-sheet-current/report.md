Implemented native sheet export/apply through atomic `commit_many`, preserving original pins and retry identity. Added hold SET/CLEAR, asset/transition CLEAR, and built-in literal params with canvas units.

- **406 local tests passed.**
- **212 central Runtime tests passed**, including five new HTTP cases.
- Lint, generated artifacts and whitespace checks passed.
- `make check` stopped at missing `remotion/node_modules`; no full suite ran.

Kept conservative stale-export refusal. Selected inputs and remaining legacy grammar stay explicitly unsupported; legacy tests/writers remain intact. Product additions exceeded the ~120-line target because this base lacked the reviewed adapter.

[Report with exact commands, results and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-native-sheet-current/notes/report.md) · [Design and deletion mapping](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-native-sheet.md)

Runtime coordination and both commit-message files are written. Next: manager review. **M2 integration remains held.**