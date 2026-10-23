# D20 authenticated shared placement interface

Implementation in progress on Agent base f6116e1b658514021cbbf08d5a6f16a240523f1a.

Existing public commit carrier; registered semantic operation (no schema change):

```json
{"schema_version":1,"op":"occurrence.place-shared","version":"1","select":"occurrence:SOURCE_OCCURRENCE_ID","args":{"occurrence_id":"f2-occurrence-copy","on":12},"intent":{"ownership":"occurrence"}}
```

`on` is seconds, quantized using the parent frame rate as in occurrence.create.
The source is selected only from the authenticated destination timeline's exact
base closure. The new occurrence appends to the original order and copies the
source placement properties except occurrence identity and placement.start_ms.
The physical shot, shot revision, internal revision, original occurrences, media,
raw registry and variants remain unchanged. No shot ID/revision/source document
can be supplied in args. Occupied IDs are refused. Captured reads, selections,
creation and inverse use the existing recorder and public commit machinery.

SDK helper: `capture_occurrence_place_shared(bundle, owner, occurrence_id, *, on)`
in `astrid.sdk.timeline.native_occurrence_shared` returns a captured command.
Raw App callers may send the envelope above; provider captures authority.
All v2 request and reply fields remain handled by the unchanged commit carrier.

Historical YES source: `agent-D20-old-shared-writer-fact-1254.md` traces frozen
Runtime publish_parent_composition and its ordinary publication test with two
unique occurrences referencing the same shot/revision, plus the old App popup.

Qualification against Runtime 3b926efa and focused guards is pending. This file
publishes callable shape early, not an acceptance claim. Runtime/Proof owners can
align their callers without a generated/schema/pin change.
