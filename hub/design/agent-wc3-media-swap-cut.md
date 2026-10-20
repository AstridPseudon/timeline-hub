# WC3 media-swap cut

## Result

`RemoteTimelines.replace_parent_media` now captures the existing native
`clip.swap-media` or `occurrence.swap-media` command and stages it in the
existing `TimelineSession` outbox. The former whole-closure authoring,
publication, and recapture path is deleted. The explicit public arguments
`occurrence_id`, `clip_id`, `source_object_id`, and `expected_head` remain;
the legacy exact `old_media`, `media`, and `expected_publication` values are
accepted as compatibility inputs.

## Deleted calls

- Removed the old parent/shot/internal revision closure assembly and its
  authoring mutation.
- Removed the `publish_parent_composition` route from replacement.
- No new endpoint, DTO, operation, root replacement, generic candidate diff,
  or sibling WC6 alias behavior was imported.

## Native capture and source selection

- The adapter opens `TimelineSession`, checks the durable outbox first, and
  flushes an existing pending/flight command without re-reading or recapturing
  media. A pending command is accepted only for the requested expected head.
- For a fresh operation it reads the pinned authoring bundle, resolves the
  exact authored target binding, and reads the exact immutable managed-media
  selection plus verified media from Runtime.
- `source_object_id` is resolved only by an exact object-identity scan across
  managed generations/variants. It must produce one candidate and its exact
  five-field selection must re-read identically; no latest/gallery/current
  guess is used.
- Explicit `old_media`/`media` are re-read and checked against the authored
  target and `source_object_id`. Missing, stale, foreign, ambiguous, or
  changed selections return the existing `DomainResult` error boundary before
  any POST.
- Native capture uses the existing `capture_parent_swap_media` or
  `capture_occurrence_swap_media`, retaining source windows, opaque/order
  fields, raw mirrors, shared isolation, and the native stale/no-write
  behavior. The command is persisted before `TimelineSession.flush`.

## Tests

- `tests/test_timeline_clip_replacement.py` now verifies no whole-closure
  publication and verifies occurrence-native capture through the session
  commit door.
- The Runtime-backed parent media conformance test now exercises the SDK
  adapter with exact selection/verification reads and rejects any whole
  closure publication.
- Central named conformance qualification passed: 2478 passed, 4 skipped,
  377 deselected, 2 expected xfails.

## Gaps / remaining hold

The adapter-specific provider test covers the real positive parent swap. The
existing TimelineSession suite covers persisted flight/retry semantics; there
is not a second provider-backed SDK adapter scenario that deliberately drops
the acknowledgement after POST. Qualification ledger remains **HELD until
qualified MERGED**, per WC3 instruction.
