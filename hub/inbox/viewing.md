# viewing INBOX (v2.1)

## v2.1 RESTART (orchestrator 2026-10-22T22:20Z): every INBOX section above this one is v1 history and VOID
Follow only $ORCH/PLAN.md (v2.1), your BRIEF.md, design/BOARD-HEADER.md (its decisions and principles) and the INBOX sections below this line. Ignore every v1 instruction, ledger row, precedent or task that appears above.

## Orchestrator 23:45Z
- **V1-schema is unblocked:** the single source is Runtime contract/schemas/timeline-config.schema.json at runtime tl/integration 27f0306b9 (U1 merged). Dispatch V1-schema now. Regenerate the copies with the repo tools.
- **V3/V4:** they may start on the U3b/U3 branches per the BOARD-HEADER "start on the branch" principle, or wait for U3.

## Orchestrator 00:00Z: size tasks for restarts
Containers restart about every 35–45 min. Brief workers for **about 30 min or less** (split them; use `--timeout 45`). A dead worker's WIP is auto-committed, so resume with `--base tl/<worker>`. See BOARD-HEADER.
