# Handoff: private Scene fixture schema repair

The private Scene proof fixture now passes the unchanged timeline schema offline. Parent and internal visual tracks are labelled `Picture`, the internal audio track is `Voice`, and all three revision digests are recomputed and verified. Render-invalid `opaque_track`, `opaque_clip`, and `rect` fields were removed only from this private render copy; shared authoring fixtures/tests are unchanged.

Targeted predecessor lane: **38 passed, 2 skipped**.

The one required central run was:

`vw-m3-scene-fixture-schema-complete-positive-scene-central-owned-suite-retarget-1020201043-11381`

It used SDK `9b887e232`, executor `23db420c1`, Runtime `2c4ac180`, Node SHA `43d6cf…`, and Composition public13/77 files. Schema admission and host startup passed, then the first saved Scene query returned `UNAVAILABLE` with `scene source binding unavailable`. Candidate, stale, positive/negative bundle, and saveNoNode evidence were not reached. No PNG/Chrome or ordinary activation claim. Do not rerun until the product source-binding blocker is fixed.
