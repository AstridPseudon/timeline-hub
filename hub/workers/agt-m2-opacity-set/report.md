Implemented opacity SET/CLEAR on existing `clip.set`:

- Added closed-schema `values.opacity` (finite number, `0..1`) and `clear: ["opacity"]`.
- Preserved exact ABSENT/null/zero states, guards, undo/redo, ABA, rebase, and occurrence isolation.
- Added conformance tests and published the contract design.
- Existing scalar golden remains byte-identical.

Tests:

- Targeted Agent suites: 158 passed, 3 deselected.
- Scalar ingress neighbors: 170 passed, 40 deselected.
- Ruff, JSON parsing, and diff checks passed.

Report: [notes/report.md](/home/user/work/wt/agt-m2-opacity-set/notes/report.md)

Commit message written to the requested path.