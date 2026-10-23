# D20 authenticated shared placement interface

Implemented and qualified on Agent base f6116e1b658514021cbbf08d5a6f16a240523f1a.

Existing public commit carrier; registered semantic operation (no schema change):

```json
{"schema_version":1,"op":"occurrence.place-shared","version":"1","select":"occurrence:SOURCE_OCCURRENCE_ID","args":{"occurrence_id":"f2-occurrence-copy","on":12},"intent":{"ownership":"occurrence"},"created":["occurrence:f2-occurrence-copy"]}
```

`on` is nonnegative seconds, preserved exactly as milliseconds (12 means 12000 ms,
including at fractional frame rates). It is not frame-quantized. `created` is
required by Runtime's existing creation-claim validation and names exactly the
one new occurrence. The capture helper includes it automatically.
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
The source must be an unchanged published shot/internal input; an uncommitted
edit of that child in the same batch is refused. An already shared source works.
Existing compiler-derived deep links/output identity are regenerated for the new
occurrence, while opaque fields and all original rows remain exact.

Historical YES source: `agent-D20-old-shared-writer-fact-1254.md` traces frozen
Runtime publish_parent_composition and its ordinary publication test with two
unique occurrences referencing the same shot/revision, plus the old App popup.

Qualification: 110 focused tests passed, including the real RuntimeService public
commit on Runtime 3b926efab2eed122d374540baee297d4cdcec62a, exact retry, preview,
whole undo, redo, undo of redo, reopen/retry, and stale/foreign/forged/occupied and
retired-ID no-write refusals. Provider fullclosure proof starts from both one and
two shared occurrences. No new Runtime port is needed.

Full report and exact commands:
`../workers/agt-D20-shared-placement-sol-1305/report.md`.
Complete public request/replies, before/after closures, authenticated history and
structured no-write errors:
`../workers/agt-D20-shared-placement-sol-1305/evidence/public-shared.json`.

One additional pre-existing public Runtime fork test fails identically on the
untouched Agent base and this change; the report records that separate baseline.
No full/browser/HTTP tour, schema, generated artifact, dependency or pin changes.
