# R2 c271 early ownership assessment

Runtime-owned normalization defect reproduced offline; Agent source edits STOPPED.

The lossless archive checksum matches a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4. Using exact 060-port-prepared request/prepared/source and only its records.undo_of source history, runtime_protocol.timeline_commit_auth.validate reaches the original `inverse stage native writes do not cover its authenticated effect image` refusal at line 1373 on Runtime 2a9e347f.

At the comparison, native/effect payload differences are exactly the three missing parent.occurrences[*].shot_revision_id values. All other payload bytes and physical root keys compare equal. Native write 6 is parent ['occurrences'], an authored-only order restoration. Runtime `_inverse_stage_state` explicitly validates its before value through `_inverse_stage_occurrence_collection`, which authenticates ownership/pins then removes shot_revision_id. The write projection at lines 1198–1201 subsequently copies its authored-only after rows directly into the physical image, discarding the physical pins. Agent State.get/set intentionally represents this collection as authored placements and requires an exact row-preserving permutation. Adding physical pins to Agent native captures would violate the representation and Runtime's own comparison.

Owner request: Runtime should project this authenticated authored-row permutation while preserving each row's exact already-authenticated physical shot pin, verifying membership/order/owners/shot/internal identities and every authored byte. Do not infer aliases or copy a stage root. No Runtime or Agent patch attempted. Bounded exact capture and final checks follow in the report.
