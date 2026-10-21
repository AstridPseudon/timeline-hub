# Gate 1 retained transcript SDK read

## Candidate scope

This candidate owns only the Agent SDK boundary for attached native word
anchors. It preserves the existing `clip.anchor` carrier and outbox command,
then materializes the command's exact `choice.document` pin through the
existing `WorkspaceClient.get_project_verified_document` call before local
preview/replay.

The materializer is intentionally narrow:

- It reads only exact `document_id`, `version`, and `content_digest` values
  already present in the command.
- It verifies response pin, project, document identity, version, canonical
  content digest, `media.transcript/v1` shape, segment/word identities, and
  bounded timing.
- It deep-copies the returned document into the existing
  `source_mapping.pinned_documents` capture. A stale capture for the same pin
  is replaced by the newly verified read.
- It never calls `documents.show`, derives a current/latest pin, accepts an
  inline transcript, trusts a caller hash, or refreshes a command guard.

Attached queueing hydrates the source for the new command before execution.
Fresh/restarted attach hydrates all pending anchor pins before replay. The
preview comparison ignores only the read-only hydrated capture, so source
materialization cannot masquerade as an authored local mutation. Existing
command captures, basis guards, flight bodies, and retry idempotency remain
unchanged.

The public verified-document-object API remains the selected project-pack
object pair. Transcript documents have no `snapshot_object` descriptor, so an
object read is not invented or substituted for the canonical transcript
document read.

## Direct evidence

`tests/sdk/test_timeline_native_checkout.py` covers:

- exact read on fresh queue followed by a second read on restarted attach;
- foreign-project, version, and content-hash mismatch refusal with bundle and
  outbox unchanged;
- existing positive anchor, clear, timing, inverse/redo, and refusal lanes.

The test fake now exposes the same verified-document method boundary and
records exact calls; it does not add a current-document fallback.

## Runtime boundary finding

The requested central proof is blocked by the selected Runtime95bd reference.
Runtime's public `get_project_verified_document` route reaches
`runtime_protocol/timeline_commit_port.py:_source_kind`, which accepts only
registered config or `astrid.project-pack` kinds and rejects
`media.transcript`. The same reference's internal commit-port path already
has a transcript source reader, so this is a public read-boundary mismatch,
not an SDK reason to weaken the pin checks.

The exact central trace is:

```text
WorkspaceClientError: source input requires a registered config or project pack kind
```

The SDK candidate therefore remains fail-closed until Runtime exposes the
existing retained `media.transcript/v1` custody through that exact verified
document API. No new endpoint, DTO, store, field, grant, or Runtime edit is
included here.

