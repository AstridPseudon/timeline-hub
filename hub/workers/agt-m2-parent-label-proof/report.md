Fixed fixture exposure, removed the blanket xfail, restored the original parent-pin wrapper, and added full-record and authored-payload preservation assertions.

Validation:

- Local targeted suites: **153 passed in 9.55s**.
- Central Runtime node with `--runxfail -rx`: **1 passed in 4.14s**, against Runtime `80973d34`, with the renderer off.
- Frozen-source record parity, unchanged App golden, Ruff, and diff checks passed.

No product failure was observed after correction. No scope decisions or blockers remain. Official artifact refresh still needs release qualification; no full suite or merge was performed.

[Report with exact commands, results, and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-label-proof/notes/report.md). Both commit-message files are written.