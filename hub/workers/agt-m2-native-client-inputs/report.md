Implemented bounded native capture inputs using the normal Runtime 0.2.6 candidate client, preserving original guards and exact retries.

- Central: **253 passed** — preserved 207 plus 46 new cases.
- Local: **86 ingress**, **156 neighboring**, and **8 strengthened refusal checks** passed.
- Full default suite remains running; mypy is blocked by shared stub issues. Ruff baseline requires an improvement update.
- Historical new PARAM capture still refuses unavailable old Document versions. M2 remains held.

[Report with exact commands, API limits, and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-native-client-inputs/notes/report.md). Design/coordination notes and both commit-message files are written.