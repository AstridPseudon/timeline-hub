# Runtime visibility event-proof fix

The catalog `timeline.recover` replay gate remains receipt/event based. A
receipt is replayable only when its existing `primary_stream_id` is the
requested timeline, its existing `event_ids_json` decodes to exactly one
non-empty string ID, and that ID resolves to one `timeline.recovered` event
associated with the requested timeline. The event payload must have exactly
`project_id` and `version`, identify the requested project, and carry a
positive non-boolean integer equal to the original request's
`expected_version + 1`.

This rejects empty, malformed, wrong-project, boolean-version, missing-fact,
wrong-version, and legacy `target_version` evidence with the existing
`timeline.restore` refusal. It does not compare the event version with the
latest catalog version, so an exact new receipt still replays after a later
catalog visibility change. No DTO, marker, table, hash framework, event, or
writer path is added.
