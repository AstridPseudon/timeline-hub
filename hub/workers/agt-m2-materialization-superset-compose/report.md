Implemented explicit old-regex unions and the permanent public-schema guard. Reversing only four patterns restores ordinary 0.2.3 byte for byte.

- Guard/schema/client lane: **111 passed**.
- Materialization/M1/label lane: **185 passed**.
- Ruff and whitespace checks passed.
- Fixed the guard’s unknown-keyword/null gap.

Exact commands, results and hashes: [report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-superset-compose/notes/report.md>). Both coordination documents and commit-message files are ready.

Next: harness commit, manager publishes the actual successor HEAD, then normal Runtime generation. Five capture behaviors remain pending; **M2 integration stays HELD**.