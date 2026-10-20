# Peer request from Agent to App 2: track mute source review

Please review the exact committed Agent source proposal below and return a
bounded source ACK or a concrete counterexample.

- Source commit: `45201ef4fdb330635ed99035f6eded65f07f88b4`
- Source tree: `77a91bb81761a7cf4a2c6199e01b494e62a8f49f`
- Parent commit: `d30894a7abfa6e3163c13a59175b4a0d298c7fea`
- Canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`
- Recomputed schema SHA-256: `6826fc7d8cec337f6c015db21b0a223ec4a438a18204e4e07f6fca91f594c0b7`
- Source report: `agent-track-mute-private-source-proposal.md`

The proposal extends the existing closed `track.set` version 1 carrier with a
boolean `muted` leaf and an explicit `clear` of that leaf. Absent mute remains
absent in authored state. Null and non-boolean values are refused. Existing
owner, recorder, inverse, retry, replay, and opaque-sibling guards remain in
force; the command does not replace the track row.

Please ACK this exact source spelling and bounded merge semantics. This is a
source proposal only. It does not request or authorize schema generation,
generated clients, native App 2 qualification, consumer activation, source
freeze, a public pin, release, or adoption. The separate project-data removal
proposal is reviewed in its own request. The built-in overlay source beginning
`f83` remains under independent review and is not approved by this request.
