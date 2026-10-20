## Completed

- Ported `dfa2fbb28` cache helper extraction and pack resource declaration.
- Ported `929bed011` native fixture environment setup.
- Preserved cache behavior and public imports.
- Verified AST/function parity and counts: `1968 → 1917` lines; helper is 63 lines.
- Wrote [ORCH report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-cache-helper-current-port.md), commit message, and `DONE`.

Tests:

- Structure: **1 passed**
- Cache/card/source neighbors: **133 passed, 19 deselected**
- Pack resource checks: **3 passed**
- Exact native lane: **19 passed, 40 deselected**
- Additional capture-label neighbor: **20 passed**
- Ruff and diff checks: **passed**

No full suite or browser/live run performed. No blockers.