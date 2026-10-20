<!-- main | 2026-10-20T05:35:47Z | dispatcher heartbeat 5s -->
# runtime — 2026-10-20T05:30Z
Milestone: M1 RECORDED. M2/M3 merges open in small gated units.
Integrated: Runtime tl/integration 1ad39f5. Merged this session: pack-document-read e068f27 (client 0.2.8 cand, NOT App-ready), render-pub xfail/stray-file fix 7eb4eab, working-copy-uncertified (option B) 1ad39f5 (45 targeted + capture suites pass; candidate-less working copy -> cas/UNCERTIFIED, forged claims refuse). Public10 pair CONFIRMED: 6be9706 on integration, contract/client 0.2.2, TrackSetArgs exported from root.
FULL RUN (integration 1ad39f5, suite full-restore-integration, 4842 pass / 40 fail / 18 skip): 7 baseline (runtime_boundary x6, zero_shim x1) + 33 NEW, all caused by earlier merged deletion/door-route work leaving tests that still call retired writers (RetiredRouteError / HTTP 410): empty_shell_repair x7, clip_replacement x10, shot_text_bindings x4, shot_candidate_promotion x2, runtime_domains x3, runtime_e2e (KEEP catalog CRUD!) x1, exact_idempotency x1, p1_blockers x1, stage1_completion x1, recorded_responses x2 (409->410 drift), second_client_e2e x1 (node fake product). Plain `full` suite lacks ASTRID_CHECKOUT (184 errors) — use full-restore-integration. D04/RT01/RT02/RT04 ledger rows therefore NOT yet DELETED.
In flight: rt-m2-full-triage-timeline (empty-shell 7, clip-replacement 10, stage1, p1); rt-m2-full-triage-shots (shots, domains, KEEP catalog CRUD, recorded responses, second-client).
Next 5: 1) review/merge the two triage workers, re-run ONE full, set ledger rows DELETED; 2) read-envelope -> canonical image conversion pairing with Agent; 3) fresh 0.2.5 generation when Agent union SHA posts; 4) D13 cohort qualification; 5) shell-adoption test with dependency row/scope.
Blocked/needs: Agent union SHA; Agent read-envelope conversion.
Gates: M1 PASS; gate 1/7 capture awaits Agent conversion; 6 OPEN.
Inbox: ACK through 05:12.
Resources: ~9GB free.
