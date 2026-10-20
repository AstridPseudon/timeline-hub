<!-- main | 2026-10-20T03:20:11Z | dispatcher heartbeat 8s -->
# runtime — 2026-10-20T03:35Z
Milestone: M0 COMPLETE. M1 Runtime EXIT COMPLETE (Runtime 4bb1d0f7 tl/integration; full 3829 PASS / 7 exact-main FAIL / 18 SKIP / 0 new). Global M1 record awaits Agent triage+full and App opaque-parity. All M2/M3 merges HELD.
Mode: Codex OUT until ~10-24; Claude fallback, 5-worker cap. Claude workers cannot approve `env ...` pytest, so integration-style tests run through the central test service. Added suite `capture-legacy-integration` (env ASTRID_CHECKOUT + `-m integration`, needs --files).
Integrated: Runtime 4bb1d0f7 / client 0.2.1; Agent 4a75f68f; App 2bfde69ea.
Branches reviewed/held: ordinary Bundle2 candidate 4c145dc6 (client 0.2.3); D13 candidate 754459365 (client 0.2.4); materialization join ad1addf2; capture validation (rt-m3-capture-provider-validation: 326 pass + 1 strict xfail, central 170 pass); capture candidate pair (rt-m3-capture-candidate-actual-pair2: 13 integration tests carried over, evidence from earlier run, not re-verified); group-helper root-pin correction (rt-m2-trusted-bootstrap-root-pins, 54 tests, awaits Agent retarget).
In flight: rt-m2-parent-media-door-proof2 (running); rt-m3-legacy-capture-replay-proof2 — test run requested on central service (rt-m3-legacy-capture-replay-proof2-capture-legacy-integration-1020031931-5424).
Next 5: 1) legacy-capture proof result then re-dispatch to finish/adapt; 2) re-run candidate-pair 13 tests centrally to verify; 3) fresh 0.2.5 itemref generation once Agent union SHA posts (superset guard first); 4) joined-map materialization qualification once Agent typed item refs land; 5) D13 historical/producer qualification and remaining writer ports/deletions, then eligible batch merges + ONE full.
Blocked/needs: Agent union SHA (0.2.5); Agent read-envelope -> canonical image conversion for saved capture golden (approved 02:42, Viewing ACK 03:05); global M1 record.
Gates: M1 targeted 2/3/4/5 PASS; M3 capture 1/7 BLOCKED on Agent conversion; 6 OPEN; 7 OPEN.
Inbox: ACK through 03:16 (Codex-out).
Resources: ~15GB free. No manager product edits/git mutations.
