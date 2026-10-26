Ask: publish the two evidence folders below as flat design/farm-shot-layering-prep-* notes / Owner: lead / By: next pass

F-shot-layering-prep is DONE (read-only, checkouts clean, no renders/tests/installs/fetch). Two workers, both exit 0, each with KEEP:

1. tf-shot-layering-remap-1320 (parts 1+3). Evidence: workers/tf-shot-layering-remap-1320/evidence/{remap.md,remap.json,shot-layering-v1.json}; report workers/tf-shot-layering-remap-1320/report.md.
- 108 PLAN.md refs (Agent 38, App 60, Runtime 10). Agent ecdc242e: 19 unchanged / 19 moved. App 82e9e13d (ours): 33 unchanged / 22 moved / 5 changed. App upstream tip 00a014e2a393ebfb080c4fd85d5a08bc97bc6671 (origin/main, no fetch): 60/60 unchanged. Runtime 95d98f03: 1 unchanged / 5 moved / 3 changed / 1 moved-far (service.py:2580 now runtime_protocol/service.py:2731).
- Re-read before editing: App shotCompositionProjection.ts:318-433, :440-590; shotTimelineDataProvider.ts:191-234, :135-156; external-drop-utils.ts:280-400; Runtime visual_seam.py:312-346 (plan says "left alone" for :337-346 but our head rewrote it), store.py:2312-2326; the false comment is now at timeline_inspection.py:492.
- Caveats: H1-H8 files were not remapped (PLAN.md only); Agent base inference rests on one file (managed_timeline.py); the agent-tests head 14ccf296 was read as a git object (no receipt; not an ancestor of the Agent head); three refs without a file were inferred by identifier.
- Fixture draft: 6 cases (one per PLAN 4.1 case), every ungrounded value is the string UNKNOWN, plus an open_items list. Design file only, not in any repo.

2. tf-shot-layering-verify-1320 (part 2). Evidence: workers/tf-shot-layering-verify-1320/evidence/{verify.md,verify.json}; report workers/tf-shot-layering-verify-1320/report.md.
- (a) pinned-row AI buttons (e2bfb1304d): VERIFIED. Buttons only put an unsent draft in the agent composer; the one clip-writing path is the effect-drag fallback via insertEffectLayerAt (external-drop-utils.ts:148-221), no shot-row check, and PLAN 4.3 omits it. e2bfb1304d also removes the text drag tool. Our App head 82e9e13d does not contain e2bfb1304d.
- (b) remapIndependentInternalTimeline guard: PARTIAL. Guard is at shotCompositionEditor.ts:160 (not ":305-309"); code-read risk (not executed): a settings-only edit on a shared shot whose clip ids are already prefixed would double-prefix (S2:S1:x); no test covers it.
- (c) expand_shot_clips callers outside Runtime: VERIFIED none in production (only Runtime timeline_inspection.py:505); only HEAD of each checkout searched.
- (d) element frames clip-local: PARTIAL. Clip-local without transitions; with transitions it depends on the path; settling it needs a render (not allowed in this job).
