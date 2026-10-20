# D09 / VW-LABEL final gate — REJECT

Decision: **REJECT** exact Agent tree `815714e8bdb75a8ce1bb422c18466bcb3edb7fc2` (tree `1e6fc112e17e8b811e7aaf206a556ebfa63551f3`) over `634867fed71b4ae53acaa3c3162315527c2bdb23`.

## Blocking finding

The port correctly changes metadata-only/legacy/native-CAS labels to `UNCERTIFIED` and keeps candidate base/draft hints. However, the completed branch leaves two preserved positive expectations in `tests/packs/rendering/test_scene_source_carry.py` unchanged:

- `test_candidate_retains_real_compiled_candidate_and_base_label` still expects `unsaved candidate based on committed revision parent:old` from metadata-only `snapshot_label(snapshot)`.
- `test_historical_capture_and_managed_labels_name_their_consumed_revision` still expects metadata-only `committed revision parent:old`.

The exact target source reproduces this mismatch: the transport candidate case fails with `UNCERTIFIED unsaved candidate <draft> (base parent:old)`, and the historical case fails with `UNCERTIFIED preview (claimed revision parent:old)`. These are not skips, xfails, or refusal-positive replacements; they are stale old semantics. Update them one-to-one to the new uncertified expectations while retaining the real host-minted positive coverage in `test_live_source_label_native.py`. Do not weaken or remove the underlying candidate/native scene behavior tests.

The native parameter of the first test was environment-blocked in my private replay because the extracted test environment had no provisioned Node peers. That is not used as a product result; the transport failure and historical failure are sufficient blockers.

## What passed / what was verified

- Exact target commit and current source tuple checked. Current Agent `tl/integration` is `04c24768cbfa758d1a2c41c107140a051cda8773`, a merge containing `634867fed`; the target diff remains limited to `provenance.py`, `test_fast_lane.py`, `test_live_source_label_native.py`, and two filmstrip expectation files.
- Target `tests/packs/rendering/test_fast_lane.py`: **13 passed in 0.18s** in a private extracted target tree, with `PYTHONDONTWRITEBYTECODE=1`, no pytest cache, and the shared Agent venv used read-only.
- Adjacent worker evidence: **100 targeted neighbor/NoNode cases passed in 17.38s**; **18 central integration cases passed in 96.60s** on tree `1e6fc112e17e8b811e7aaf206a556ebfa63551f3`. Those tests cover Runtime capture/admission, saved and real-candidate paths, existing host materialization, verified source handoff, final Root lifetime, forged-input refusal before writes, exact source/profile/addresses/compiled pair, and public scene `UNKNOWN` without fresh PNG/capture labels.
- The central report records the complete pre/post manifest as byte-identical (`e1b4ad6c9a53e0e439de9264ec55685f8e9c5060e694c6bf8135ea4d2309c3ed`).
- Static scope review found no SDK publish/transaction/check/core-provider/save/DTO/pin edits, no `CaptureSceneLabels`, and no eager scene import in the production diff. The only scene import is in the new read-only integration test.
- `VerifiedTimelineSource` on current `tl/integration` has the same `read`, snapshot validation, prepared-pair validation, and host-mint contract used by the port. The current integration also contains the newer scene-save-core separation; the label helper does not import or activate it.
- Existing production call sites intentionally continue calling `snapshot_label(snapshot)` without a source, so exported-page certification and fresh-PNG scene-row/cache activation remain separate work. No D09 ledger deletion is justified by this branch.

## Exact test commands

See the adjacent `handoff-vw-m3-live-source-label-final-gate-COMMAND.md`. No full, browser, socket, live render, install, network, or shared-dependency mutation was run.

## Required next step

Agent owner should update the two preserved `test_scene_source_carry.py` metadata expectations to `UNCERTIFIED` equivalents, retain the real positive source-bound labels, rerun the narrow source-label controls and the existing neighbor lane, then resubmit the same bounded helper port for review. No broad `2a` ancestry merge is needed.
