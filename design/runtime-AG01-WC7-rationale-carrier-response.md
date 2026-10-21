# Runtime AG01/WC7 — existing rationale carrier

**Peer response, 2026-10-21 UTC.** Reviewed against Runtime `b92d3e7` / the
requested `tl/integration` base. This is a carrier answer only; no Runtime or
contract change is needed.

## Existing carrier

The semantic reason for a whole publication belongs at request/batch scope.
`CommitRequest` already accepts optional `source`, `label`, `rationale`, and
`group_id` alongside the base revision/publication pair and ordered commands
(`runtime_protocol/timeline_commit_types.py:66-72`; the closed contract is
`contract/schemas/timeline-commit.json:103-168`). The exact EditCommand-level
carrier is also already present: `rationale?: string` and `group_id?: string`
(`runtime_protocol/timeline_commit_types.py:32`; schema
`contract/schemas/edit-command.json:897-927`). A command-level rationale is
retained inside the accepted `CommandRecord.command`; it is not an actor or
authority claim.

The accepted command record is already lossless for the edit contract:
`ordinal`, `command`, `writes`, `reads`, `selections`, `bindings`, `created`,
`dependencies`, and `derived_writes`, wrapped by `Recorder` with
`schema_version`, `commands`, `undo_of`, and `restored_from`
(`runtime_protocol/timeline_commit_types.py:82-85`; schema
`contract/schemas/timeline-commit.json:490-608`). The accepted result carries
the base and previous head pairs, accepted revision, rebase identity,
canonical document/digest, commands, ID map, provider/compiler versions,
authenticated `publisher`, and the optional request metadata
(`runtime_protocol/timeline_commit_types.py:86-91`; schema
`contract/schemas/timeline-commit.json:738-832`).

Runtime history exposes the same accepted identity plus the existing receipt,
`intent`, recorder, provider/compiler versions, `publisher`, and optional
`source`, `label`, `rationale`, and `group_id`
(`runtime_protocol/timeline_commit_types.py:95-97`; schema
`contract/schemas/timeline-commit.json:1042-1135`). The store writes those
metadata keys to the existing `timeline_commit_history.metadata_json` and
records the accepted recorder, publisher, and project sequence in the same
row (`runtime_protocol/timeline_commit_store.py:19`, `:884-910`; table shape
`runtime_protocol/canonical_schema.py:12-25`). History verifies and returns
those fields, then paginates the existing publication chain
(`runtime_protocol/timeline_commit_store.py:226-286`).

## Normal requester and outbox route

The normal requester is the existing `TimelineSession` commit path, not a
legacy whole-document writer: its route is
`/v1/projects/{project}/timelines/{timeline}/commit`
(`astrid/sdk/timeline/sync.py:124-129`). The outbox captures commands, then
atomically writes the pending state (`astrid/sdk/timeline/sync.py:256-282`).
For publication, the existing native checkout seals the message as the
outbox `rationale` and refuses a changed message on retry
(`astrid/sdk/timeline/native_checkout.py:199-227`). `_flush` builds the exact
request from the persisted base pair and commands, includes `source.via` and
the rationale, persists the flight/key, and sends that exact body through
`client.timelines.commit` (`astrid/sdk/timeline/sync.py:344-379`).

Runtime receives that ordinary `/v1` request, authenticates `projects:write`,
passes the authenticated actor as `publisher`, and calls the existing service
commit method (`runtime_protocol/server.py:294-319`). The service binds the
request body, route, idempotency key, request hash, realm, and publisher into
the commit context (`runtime_protocol/service.py:2435-2465`); acceptance then
persists the existing receipt/history/head update atomically
(`runtime_protocol/timeline_commit_store.py:712-741`, `:884-910`). The
generated client has the same public route and `Idempotency-Key` contract
(`packages/python/astrid_runtime_client/generated.py:915-925`).

## What maps, and what does not

The Main publication note currently records `reason=message`, before/after
working-copy digests, and a revision evidence item
(`astrid/sdk/timeline/publish.py:82-89`). Its semantic reason maps directly to
the existing request-level `rationale`; if the edit itself needs a reason,
the existing command-level `EditCommand.rationale` is the narrower carrier.
The accepted `publisher` is the authenticated requester identity already
captured by Runtime; it must not be turned into an invented producer identity
or synchronous proposal authority.

`group_id` is existing request/command grouping metadata, not the retry key and
not cross-publication atomicity. `source` identifies the normal ingress kind
(`cli`, `python`, `app`, `script`, or `sheet`), while `label` is display
metadata. The outbox's idempotency key remains the exact-flight/retry identity.

The note's accepted publication evidence has an existing carrier, but not a
same-named `evidence` property: use `HistoryEntry.publication_id` and
`revision_id`, its `receipt`, `previous` head, and the accepted
`document_digest`. Those are stronger accepted-publication identities than a
local note's free-form evidence object. The literal local journal-chain
fields (`seq`, `prev`, `hash`) are local journal integrity, not Runtime
publication semantics. No public shape change is required; the smallest
alternative for the one unmatched note field, `evidence`, is the existing
history identity/receipt tuple.

Do not put the note in timeline film metadata: the canonical document is the
authored film state, while the existing timeline catalog projects timeline
name/config/registry and the current head (`runtime_protocol/timeline_catalog.py:12-25`).
Do not put it in catalog state either: catalog verification accounts for
visibility receipts and head/version consistency, not edit rationale
(`runtime_protocol/timeline_catalog.py:28-33`, `:49-97`). The accepted
history metadata is the existing durable place for the publication rationale.

**Disposition:** Agent may retire the local publication note once its native
publication request supplies the existing `rationale` carrier and consumers
read the accepted history/receipt identity for publication evidence. No new
DTO, endpoint, table, journal, producer identity, or authority path is
justified by this gap.
