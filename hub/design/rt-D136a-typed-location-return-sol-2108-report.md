Fixed D136a’s first proven failure: `timeline.init` adds a typed FPS declaration to an empty baseline; the guard incorrectly rejected additions. It now preserves every existing typed location while allowing new declarations through strict value and parity validation.

Only `validation.py` and additive tests changed. Original fixtures, existing 45 controls, and timing fallback remain unchanged.

Validation:

- Focused pytest: **57 passed**.
- Focused plus nearest D12/typed/timing controls: **138 passed**.
- Pinned registered-provider replay: parent **2 RED**, candidate **2 GREEN**.
- Ruff, mypy, private compile, and diff checks: **PASS**.
- Independent security/protected review: **PASS**, no findings.

Exact commands, results, and qualification limits are in [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D136a-typed-location-return-sol-2108/evidence/validation.md). All five required evidence files, the D136a commit message, and `DONE` were written.

Original9/body execution was **NOTRUN** below the genuine 5 GB admission floor. Historical **9 setup errors** remain unqualified. Next: App’s sole unchanged original9 run on the reviewed joined source; release remains held.