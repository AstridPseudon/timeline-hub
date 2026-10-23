# Runtime D17 source-input interface

Status: stable after Runtime real-port/store acceptance checks, 2026-10-23.

Runtime's request-private `RequestCommitPort` accepts an exact source reference
through the existing semantic command `args` JSON envelope. The Agent semantic
provider calls:

```python
source = port.revision_closure({
    "project_id": source_project_id,
    "timeline_id": source_timeline_id,
    "revision_id": source_revision_id,
    "publication_id": source_publication_id,
    "content_digest": source_parent_content_digest,
})
```

The same operation is also available as the explicit
`port.source_revision_closure(source_ref)`. The reference is an exact object
with precisely those five fields. `content_digest` is the immutable
`source["parent_revision"]["content_digest"]`, not a digest supplied by the
provider for newly assembled data.

Runtime verifies, at source capture and again immediately before acceptance:

- the source project is the destination project and the source timeline is a
  different active timeline;
- the existing authenticated caller callback authorizes the source timeline;
- the accepted historical publication maps to the exact source revision;
- the source parent content digest matches the requested digest;
- the complete immutable source closure, including occurrence order, shot and
  internal revision pins, media manifest, and document manifest, still matches.

Runtime does not refresh a source ref to the source head, infer a pair from a
revision ID, accept a caller/provider boolean grant, or make source closure
data part of the destination closure scope. Foreign, outside, archived/stale,
pair-mismatched, digest-mismatched, changed-capture, and forged-media inputs
remain refusals under the existing Runtime authority errors.

The provider must consume source inputs through the existing port before
acceptance: call `raw_media_info(pin)` for each source media pin that it copies,
and `config_source(pin)` or `transcript_source(pin)` for each source document
pin it copies. Those calls are request-private and are revalidated against the
existing managed media/document custody. The resulting semantic candidate must
retain the source pins in its normal authenticated records/manifest.

Agent owns the one semantic source-copy command and all meaning: fresh
destination IDs, repeated sharing, occurrence/order mapping, inverse/undo,
idempotency, and provider-derived records. It uses the existing semantic
command carrier and does not add a Runtime tuple, schema, generated client, or
pin. Runtime owns only source authority/input capture and destination
acceptance/revalidation; it remains free of semantic execution.

Runtime evidence: `tests/test_timeline_source_duplicate_authority.py` exercises
the real `RuntimeService`/`RequestCommitPort` path for exact historical source,
foreign/outside/archived source, pair and digest mismatch, forged media,
revoked caller access, and source mutation after capture. Agent still needs to
qualify semantic fresh-ID/order/sharing/undo/idempotency/archive-cleanup
behavior against this interface.
