Completed the settled registered artifact → authorized requester outbox → native commit path, including restart, exact retry, immutable history and guarded undo.

- Local: **123 passed, 1 strict xfail**.
- Central private pair: **9 passed, 2 unchanged legacy xfails**; outer lane **4 passed**.
- Ruff and diff checks passed.

Admission-create ACK recovery remains an explicit durability requirement. Render remains unqualified. Next: compose the reviewed native cohort, then address those separate gaps.

[Report with exact commands/results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-registered-proposal-requester/notes/report.md) · [Qualified source handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-registered-requester-handoff.md)

`commit-msg` and `DONE` written.