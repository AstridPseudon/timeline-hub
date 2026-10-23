# D17 Agent source-copy draft (0851)

IN PROGRESS; UNMERGED/P1 gated. Base f77a750ad (preserved G5 WIP).

Interface accepted from Runtime handoff 0842: `port.revision_closure(source_ref)` with exact project_id, timeline_id, revision_id, publication_id, content_digest. Provider will resolve this object privately, hydrate all documents and consume each source media pin through raw_media_info. Caller bytes never constitute source authority.

Agent command: one registered `timeline.duplicate`, existing op/JSON args carrier. Args: source_ref plus complete source-shot and source-occurrence identity maps. Provider copies authenticated raw closure, derives creations/reads/effects/steps, preserves source order and repeated sharing, and rejects occupied/noninjective/source-alias IDs. The temporary occurrence.attach WIP will be folded into this semantic.

Runtime proof source available as hub ref 36f24786942acd55af2395c1372dd4ac3d4c658a, extracted read-only via git archive into this worker's scratch directory. No public wire/schema/client/pin change.

Original positive fixtures currently supply only destination Generated transport, not a source-private port/history; original assertions will remain unchanged. Qualification will distinguish real-port proof from these legacy fixture limits. Final results follow.
