# BOARD HEADER (orchestrator only), Timeline v2.1
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.


Clock: **H0 = 2026-10-22T21:40Z** (H3 = 00:40Z, H6 = 03:40Z, H9 = 06:40Z). Plan: `$ORCH/PLAN.md` v2.1. Lanes and IDs are in PLAN's "Who does what" table.

## Status
- C0 contract: **NOT YET APPROVED**. Nobody builds against `design/commit-v2.md` until this line reads "C0 APPROVED".
- H3 go/no-go (P1): pending.
- H8 scope check: pending.

## Decisions in force
- Owner, 22 Oct:
  - hybrid design (PLAN §1);
  - leads and orchestrator on Claude doing minimal work; managers on Codex Sol; all code, reviews and merges on Codex;
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
