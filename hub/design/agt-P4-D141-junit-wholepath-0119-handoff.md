# Handoff

For `agt-P4-D141-junit-binding-return-0119`:

- Preserve actual service `agent-p4-current-becfe-http-3legs-1026011042-10086` as `3/3 PASS`, exit `0`, with actual XML SHA-256 `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d` at the 0055 body-evidence path.
- Preserve custody `FAIL` until the stale `junit_paths=...agt-P4-D141-cut-controller-0047.../p4-d141c-normal.xml` identity is reconciled with the actual `...agt-P4-D141-operational-return-0055.../p4-d141c.xml`. Do not rewrite this worker's evidence or rerun the body in this lane.
- The selector path is also historical 0047, but its 0055 copy is byte-identical (SHA `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`). Treat this as a lifetime/provenance dependency, not a selector mismatch.
- Source/version checks found no mismatch. The remaining source fact is only that the body log does not record resolved module `__file__` origins; current binding rests on strict launcher preflight plus exact source/tree/hash receipts.
- App’s cumulative verdict remains held. Its source-only publication has no receiver-owned final P4/JUnit artifact binding; final review must consume the corrected custody handoff and decide the cumulative disposition.

Historical 1347 (`exit 1`, zero selectors, no JUnit), 0101 `FAIL`, and 0106 `PASS_OPERATIONAL_SOURCE / INSTALLATION_NOT_READY` remain separate. D97 is comparison context only; no D97 body was rerun.

No source, registry, launcher, test, product, contract, or shared-dependency files were changed by this worker.
