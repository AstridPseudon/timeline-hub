# Decision needed: original stale-window positive versus D12a

This confirms Viewing's pending 05:49 scope question with a meaningful repaired-source run; it does not add a different policy question.

Original `test_stale_anchor_refuses_when_intervening_window_excludes_selected_word` expects an intervening source-window change to 4..6 to succeed while the existing selected word is at 3..3.5, then expects the stale anchor request to conflict. Independent Viewing review0545 and Agent author b42b7d72a both show the source change invalidates that existing anchor. Current C0/D12a therefore refuses the source change, before the stale request can execute.

Please decide whether this case is delivery-deferred relational timing evidence (a third case, not yet authorized by D14), or specify the intended contract treatment. No new exemption, test edit, skip, or success claim has been applied. The strict refusal remains. Evidence: design/handoff-vw-V4-ad4-five-review-0545-REPORT.md; design/agent-V2-boundaries-return-0553.md. The latter's original three run is 2 PASS / 1 FAIL: the two unrelated legacy setup failures are repaired independently and are in Luna review0606 now. Nullable speed also follows existing canonical behavior; R2's final redo proof proceeds once this bounded fix merges. Those fixes do not wait for this decision.
