Implemented the bounded migration candidate with lossless provenance and exact pure undo/redo. Ordinary Bundle2 schema content and all 16 existing fixtures remain preserved.

- Targeted regression: **648 passed, 1 deselected**
- Registry/staging/labels: **38 passed**
- Runtime popup pair: **48 passed**
- Real migration pair: **7 passed, 2 failed**

The real pair now passes official root-key validation, then fails because the trusted bootstrap command omits `created`. Runtime/helper changes, group movement, derived App view, and new group artifact generation remain followups. No full suite or browser tests ran; M2 remains held.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-official-root-proof/notes/report.md). Contract and both commit-message files are written.