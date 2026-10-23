# FAIL — G2/G3/G4 current join review

Current `5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026` is mechanically consistent
with the approved G3/G4 donor refs and preserves the protected schema,
generated/lock, and R2/R3/meta/R1-native bytes. Targeted author lanes passed:
280, 184 (63 deselected), 71, and 41; quality ratchets passed at Ruff 2149 and
mypy 1915. The frozen producer `34eac004` vendor-lock check and artifact check
also passed. No novel conflict-resolution edit or accidental donor report was
added.

The joined candidate nevertheless fails the explicit G4 acceptance: the live
CLI (`astrid/packs/timeline/cli.py:186`) and duplicate path call
`RemoteTimelines.create_empty` (`astrid/sdk/timeline_duplicate.py:194`), whose
implementation (`astrid/sdk/remote.py:482-552`) directly sends
`create_timeline` and `publish_parent_composition`. It does not use
`TimelineSession`, `timeline.init`, the G3 emitter, or the v2 `/commit` request.
The focused create test passes 13 tests but asserts this direct two-call route,
so it is not evidence for the required production caller. This route is
inherited from the adopted parent; no source edit was made in this read-only
review.

The other G4 production routes were verified through the session/commit paths:
selected parent-media replacement, update-element, narration, and requester
render publication. G5 legacy paths remain present and gated as required.

Next step: migrate `create_empty` to the approved bootstrap/session v2 commit
route and rerun the create/bootstrap and joined current-source checks.
