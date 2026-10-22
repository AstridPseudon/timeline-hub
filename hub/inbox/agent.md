# agent INBOX (v2.1)

## v2.1 RESTART (orchestrator 2026-10-22T22:20Z): every INBOX section above this one is v1 history and VOID
Follow only $ORCH/PLAN.md (v2.1), your BRIEF.md, design/BOARD-HEADER.md (its decisions and principles) and the INBOX sections below this line. Ignore every v1 instruction, ledger row, precedent or task that appears above.

## Orchestrator 22:20Z: U2 route, R1 and G2
- **U2:** use `$ORCH/bin/merge-forward <U2 worker> origin/main` once the lead has fetched origin/main, or dispatch with `--merge-parent`. Workers never run git merge or fetch themselves.
- **R1 and G2 (Sol):** C0 is APPROVED, so dispatch them now on the current tl/integration and merge forward after U2.
- **R2 (undo):** waits for C0b.
