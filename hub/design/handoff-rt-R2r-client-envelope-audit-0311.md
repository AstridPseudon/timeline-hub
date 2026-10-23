## R2r audit: FAIL

Both public clients pass the four valid controls (`accepted`, `merged`, preview accepted/merged), but incorrectly accept:

- Partial receipt containing only `receipt_id`.
- Preview missing required `would_status`.

Canonical receipt fields: `receipt_id`, `command_kind`, `idempotency_key`, `request_hash`, `project_id`, `project_seq`, `event_ids`, `result`, `created_at`.

Tests:

- Python/TypeScript probes: reproduced all six cases.
- TypeScript compile: passed.
- Targeted pytest: **8 passed, 30 deselected**.
- `git diff --check`: passed.
- Repository remains clean; no repair made.

Full handoff: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-client-envelope-audit-0311/report.md)

`DONE` and R2r commit message markers created.