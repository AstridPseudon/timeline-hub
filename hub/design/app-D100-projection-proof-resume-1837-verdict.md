# D100/App projection verdict

**Finite result: CANDIDATE REGRESSION — App projection proof stopped.**

The required exact candidate and Runtime custody checks passed. ParentRED was meaningful: 23/27 passed and the four failures showed the expected pre-repair first-physical-item seam through the real registered Runtime route.

CandidateGREEN was not achieved: 24/27 passed, with the first failure in test_first_physical_item_preserves_custody_and_opaque_fields[False]. After the repaired path executed, the reviewed assertion that plan.bundle['source_mapping'] remain unchanged failed because _doc_patch_images was added to source_mapping. The aggregate variant failed identically. The shared-owner case retained the existing UnsupportedAuthoringEditError refusal.

Per the task gate, this is a finite regression finding. No repair, fixture receiving delta, App projection9 run, own9 run, or retry was performed. Source/security PASS remains source-only and does not establish behavioral closure.

