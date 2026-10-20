# WC3 exact media-swap retry repair

The adapter's retry branch is guarded by the original logical request:

- original Runtime base revision and, when supplied, publication;
- resolved owner (`parent` or the exact occurrence), raw clip selector, and
  source object identity;
- both persisted old/new media selections, each with exactly the five
  selection fields; caller-supplied selections must equal those pins exactly.

One pending command is required. An unrelated command, multiple commands,
malformed selection, owner/clip/source mismatch, or stale head/publication
returns a visible validation failure before `TimelineSession.flush`; the
outbox is not written and no POST is attempted. The full in-flight body and
key remain delegated to `TimelineSession._flight_body`, so an exact retry can
reuse the persisted request after restart or a later Runtime head. An omitted
caller key is preserved for that case; the typed receipt supplies the returned
key after acknowledgement.

The old whole-publication route remains deleted. The repair uses the existing
native swap commands and adds no DTO, endpoint, alias, or generic retry
framework.

Targeted evidence:

- `tests/test_timeline_clip_replacement.py`: 13 passed, including unrelated
  and multiple pending adversaries, source/selection/owner/head/publication
  controls, restart/lost-ACK retry, opaque pending command preservation, and
  no-key replay.
- `tests/sdk/test_timeline_sync.py`,
  `tests/sdk/test_timeline_native_frontends.py`,
  `tests/editing_conformance/test_recipe_parent_media.py`, and
  `tests/editing_conformance/test_recipe_occurrence_media.py` were run with
  the targeted local command; no broad 2478-test conformance run was used.

The real Runtime-backed parent provider lane remains a central integration
qualification, not a local fake-provider claim.
