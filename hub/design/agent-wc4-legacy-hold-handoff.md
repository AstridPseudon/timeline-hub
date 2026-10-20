# WC4 legacy HOLD — review handoff

Ready for bounded owner12:32 review on `tl/agt-m2-wc4-legacy-hold-preserve`, based on `a6098b5d`. Harness commit pending.

Same-selected-element literal HOLD uses only guarded `clip.set`, with no snapshot/admission selection, portable bytes, client disk authority, or implicit re-admission. Empty/absent params stay exact. Explicit unchanged params retain native write records without snapshot reads. Equivalent numeric values and bool distinction use existing recursive JSON equality. Real revision reselection without portable snapshot still visibly refuses `pack snapshot unavailable; re-admit pack`; use the existing explicit admission flow outside save.

Original-format frozen flights retain exact body/key/pin; acknowledged rebased/lost-ACK/restart/paginated-history recovery remains covered. New permanent tests use the genuine legacy resolver/build-receipt fixture and actual normal Runtime 0.2.13 acceptance/reload/inverse/retry.

Final targeted evidence: **75 actual helper/schema/scalar passed**, **359 neighboring cases passed**, Ruff and `git diff --check` passed. No full suite requested. No schema/pin/DTO or integration/shared dependency edits.

Full report and exact commands: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-wc4-legacy-hold-preserve/notes/report.md`.

The retained review's exact draft-to-admitted case is revision reselection, so the settled refusal remains; the permanent positive selects the same admitted revision using that genuine fixture. Its external test was not altered.

**Owner12:16 original-PARAM authority remains HELD.** The inherited changed-PARAM batch/path is unchanged and is not production-qualified by this correction. Integrate the separate accepted-original-pin rule before approving that boundary. **WC4 remains held; do not mark DELETED until review/merge and the remaining PARAM boundary are settled.**
