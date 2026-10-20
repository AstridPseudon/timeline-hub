Implemented bounded attached-checkout parent move publication with explicit outbox ownership, persisted rationale, original guards, and exact lost-ACK retry. Detached publication remains unchanged because its handles cannot safely establish occurrence ownership.

- Targeted tests: **199 passed, 17 deselected**.
- Ruff on changed implementation modules and `git diff --check`: passed.
- Three HTTP cases collected; execution remains for MANAGER with public013/current source.
- Result tree: `0c68c122143ff8d75337bc40295bcbe836559cba`.
- Wrote `commit-msg`, `commit-msg.txt`, and `DONE`.

[Report with exact commands, HTTP nodes, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-wc7-owned-move-outbox/REPORT.md).