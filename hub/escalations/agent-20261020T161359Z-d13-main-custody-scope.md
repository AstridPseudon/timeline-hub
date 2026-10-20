D13 native staged014 render completes functional assertions but teardown refuses CPU custody cleanup.
Worker agt-m2-d13-custody-cleanup-finish produced a reviewable 3-file +67/-2 patch in Main custody_broker.py/process_group.py and direct tests.
It treats a retained, readable pidfd as proof that the exact old descendant incarnation exited, while unproven PID reuse still refuses.
Those paths are outside my Timeline ownership; requested worker stop preserves WIP and prevents further core edits. Final central registered014-render-integration already submitted; no result claimed.
Recommendation: grant a bounded Main custody fix only after independent source/security-guard review and original strict process tests + real2render positives; otherwise owner takes patch.
D13 stays held; no skip/ignored teardown/guard weakening or integration merge.
Not covered because: the Timeline render failure led into unowned general process custody; no existing grant covers these two core files.
Rule that would let me decide next time: delegate bounded Main infrastructure false-refusal fixes to its source owner with unchanged safety invariants and independent review.
