Implemented durable admission recovery in the existing outbox. Original body/key replay exactly; changed intent refuses; ACK cleanup preserves pending edits. The original strict xfail now passes.

- Local: **133 passed**.
- Central: **15 passed, 2 held legacy xfails**; outer **4 passed**.
- Ruff and whitespace checks passed.

No task blocker. The unrelated archived M1 visualization failure remains reported; rendering/decode/macOS remain unqualified.

[Report with exact commands and source tuple](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-assembly-admission-durable-flight/notes/report.md) · [Handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-assembly-admission-durable-handoff.md)

Commit message and `DONE` written. Next: review and compose the narrow changes while preserving current stage guards.