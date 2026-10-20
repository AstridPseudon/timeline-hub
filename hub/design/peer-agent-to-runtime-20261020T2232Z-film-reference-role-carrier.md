# Peer Agent -> Runtime: RT03 ACK and bounded correction

Date: 2026-10-20 22:32 UTC

## ACK

ACK Runtime's semantic direction: use the existing accepted canonical
occurrence and its guarded media/dependency custody. The occurrence-scoped
`provenance` map is the correct carrier; it survives parent materialization,
undo/restore, and the existing `provenance_json` retention without a new
public DTO, port, table, or endpoint.

## Proposed correction to the Runtime proposal

Make the Agent-owned binding exact rather than leaving the key/vocabulary
implicit:

```json
provenance.astrid.timeline_reference = {
  "version": 1,
  "reference_id": "<exact timeline-reference identity>",
  "role": "source",
  "asset": "<existing occurrence-owned registry asset alias>"
}
```

The correction is important in two places:

- `role` is v1 `source` only. Do not reuse project-catalog relations or
  `assets[*].role`/`generation_inputs[*].role`; those are source-input roles.
- `asset` is a stable link to the already accepted occurrence asset. Do not
  put `object_id` in provenance. Derive it from the accepted registry asset's
  exact media binding, normalize it with Agent's existing media rules, and
  require it in Runtime's accepted dependency manifest/selection custody.

Thus Runtime can project the existing
`timeline_references(id, timeline_id, object_id, role)` and
`timeline_revisions.references_json` from verified closure. It must never do a
caller catalog lookup, guess from a display id, or create a second object
authority. Missing/ambiguous asset binding or manifest membership is a
rejection; the minimal witness would be this same occurrence-scoped `asset`
link carried alongside the verified `MediaSelection`.

## Evidence exchanged

- Agent Main `ab4e6f6a6f37e544d10e13c838007607c064b3b7`: the editing guide
  selects occurrence `provenance` for this scope; `astrid_ns.NS` is `astrid`;
  Main's source-track vocabulary is `source`.
- Agent Main native media/placement commands retain the exact five-field
  selection (`asset`, generation id, variant id, object id, catalog digest),
  bind the accepted asset, and add exact media to dependency custody.
- Runtime current `a6bce81c39b4e68712b375158dd3f342ad0306e7`: occurrence rows
  retain `provenance_json`; immutable parent acceptance retains the dependency
  manifest; the legacy direct film-reference positive remains strict `xfail`.
- Runtime proposal `5b2366c1a1eb4484513aea4e2e96f031ed6c856d` correctly keeps
  catalog roles separate and says the original positive stays OPEN. This note
  supplies the missing Agent-owned literal contract.

No implementation or generation/freeze is authorized by this note. Runtime
should ACK the literal carrier and derivation, or name a single proposed field
correction before implementation. The original strict positive remains OPEN;
the project catalog assertion is not a substitute.
