Implemented PIN-only guard, provider capture validation, proposal builder, and durable outbox queueing.

- **440 targeted tests passed**; touched Ruff and `git diff --check` passed.
- Paired acceptance remains blocked: Runtime lacks `producer_attempt`.
- Rendering writer remains unchanged. Next: pair Runtime and qualify lifecycle/numeric acceptance.
- Handoff and both commit-message files written.

[Report with exact commands, decisions, and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-producer-guard/notes/report.md)