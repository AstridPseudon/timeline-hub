# BOARD HEADER (orchestrator only), Timeline v2.1

Clock: **H0 = (set at kickoff)**. Plan: `$ORCH/PLAN.md` v2.1. Lanes and IDs are in PLAN's "Who does what" table.

## Status
- C0 contract: **NOT YET APPROVED**. Nobody builds against `design/commit-v2.md` until this line reads "C0 APPROVED".
- H3 go/no-go (P1): pending.
- H8 scope check: pending.

## Decisions in force
- Owner, 22 Oct:
  - hybrid design (PLAN §1);
  - managers on Claude, all code, reviews and merges on Codex;
  - Sol only for the tasks marked Sol;
  - gate 6 parity deferred (signed);
  - WC8-style stale working copies refused;
  - upstream freeze before the final merge.
- **Build on our integration branches.** Upstream main is merged into them (U1–U3), never rebased. The App takes upstream's editor files (U3b), but keeps the outbox, the commit transport and the Runtime client.

## Cut list (in order, only if behind)
1. V4
2. push / dashboard extras

**Never cut** writer migrations or tests of promised behaviour.

## Farm schedule
- H0: upstream baselines.
- H6, H9: integrated full suites, the tour and the journey.
- Final.
