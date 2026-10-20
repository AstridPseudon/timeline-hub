# Confirmation for owner12:22 — exact single-occurrence render cap

Captured raw closure SHA256 **ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04** equals App's copied fixture. It has EXACTLY ONE occurrence; no successor participates.

- Input: parent_revision.payload.occurrences[0].duration_ms =4000; placement.start_ms=0; source_offset=0; speed=1.
- Child: internal_timeline_revisions[0].payload.clips[0] has at0,hold5,effects.fade_out1.
- Original MAINa411 core/timeline/shot_composition_projection.py::_occurrence_window (lines272–288) reads the STORED duration_ms, converts milliseconds to seconds, returns start0,end4,duration4. It does not derive this cap from content length or next occurrence.
- _project_clip (lines291–326) computes child end5, clipped_end=min(5,4)=4, visible_duration4, then writes hold=visible_duration*child_speed=4. Current fixture child_speed=1.
- project_runtime_parent_composition calls that function with the exact stored occurrence start/end; output occurrence.duration_seconds4/hold4 and output cliphold4. Normal Timeline.for_render serialization retains4.

All SEVEN outputs were byte-equal in actual central1020115023-5447, originalRootmetadata120frames@30, actualf105RGB122/124/130 supports0.5. IndependentresultPASS. No newrender needed. Exacttrace/raw/projected/serialized artifacts under handoff-vw-m3-main-image-cap-source-vector-*; source/fullgraph/sixpeerpostflight captured under handoff-vw-m3-main-cap-locked-theme-stage-*.

Therefore the MAIN NORMAL COMPILED RENDER INPUT is stored4000ms for this closure, NOT App's derived5000ms. This confirms App's reported exact-closure mismatch; the earlier next-occurrence diagnostic cannot substitute. Agent owns the shared render golden/compiler. Preserve editor/read effective-duration positives separately; no blanket min() change/globaldefaultflip or resurrection of withdrawn renderConfig is inferred here.
