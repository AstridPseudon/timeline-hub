Implemented D13/RT07 native assembler consumer replacement.

- Replaced old whole-candidate publication with durable native admission → settlement → requester commit.
- Removed `GenericPackHost._publish_assembled_timeline` and its call path.
- Added strict `assembly-admission` lost-ACK recovery.
- Preserved normal render/stitch routes; unsafe legacy admissions visibly refuse.
- Added required reports, commit message, and `DONE` marker.

Tests:

- Targeted Agent tests: `158 passed`.
- Central targeted snapshot: `77 passed, 2 deselected, 1 xfailed`.
- Ruff and `git diff --check`: passed.
- Broader host tests: `318 passed, 6 failed` due sandbox socket permission errors; no native-seam failure.
- Full/live HTTP/socket qualification was not run.

Reports: [design](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-d13-native-current-cut.md>) · [worker notes](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-native-current-cut/notes/report.md>)