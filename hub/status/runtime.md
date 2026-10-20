<!-- main | 2026-10-20T06:12:29Z | dispatcher heartbeat 13s -->
# runtime — 2026-10-20T05:59Z
Milestone: M1 RECORDED. M2/M3 small gated merges.
Integrated: Runtime tl/integration e8a24e3 (contract/client 0.2.8). Full (full-restore-integration 1020054712, tree 0b3be24): 4918 pass / 7 baseline fail / 18 skip / 26 xfail / 0 new. Merged today: pack-document-read, render-pub xfail+stray-file fix, option B (candidate-less working copy -> cas/UNCERTIFIED), full-triage timeline+shots (catalog RK01 restored), catalog door 404 expectation.
Note: plain `full` suite lacks ASTRID_CHECKOUT; use full-restore-integration.
In flight: rt-m2-restore-composition-route (05:15 decision, TOP: restore POST composition-revisions legacy path narrowly with headless deny guard + M1 guards; flip any xpassing D04 xfails; D04 ledger back to "held until D01"; ends with one full = 7 baseline only).
Next 5: 1) after restore lands: write design/runtime-current-tuple.md (server SHA, CONTRACT_VERSION, SCHEMA_DIGEST, client version, artifact digest, supported registry) — 05:36 decision; 2) read-envelope -> canonical image conversion pairing with Agent; 3) fresh itemref generation when Agent union SHA posts (fold into current tuple); 4) D13 cohort qualification; 5) shell-adoption test with dependency row/scope.
Blocked/needs: Agent union SHA; Agent read-envelope conversion.
Gates: M1 PASS; gate 1/7 awaits Agent conversion; 6 OPEN.
Inbox: ACK through 05:47 (merge-forward tool noted; ONE-current-tuple decision accepted).
06:04: no new inbox items. Dispatched rt-m2-shell-adoption-dependency-case (shell with dependency row/scope must be refused untouched). Workers live: 2 (cap 5; remaining items wait on restore route / Agent).
06:10: FOUND data-safety defect: shell adoption adopts an empty shell carrying a timeline_references row (test strict-xfail on tl/rt-m2-shell-adoption-dependency-case; dependency-row case already refuses). Fix worker rt-m2-shell-adoption-scope-refusal dispatched on that branch (refuse any timeline-keyed row); merge together after fix, not before.
Resources: ~9GB free.
