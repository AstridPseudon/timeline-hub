# Runtime source ACK — derived transcript DocumentPin field

Date: 2026-10-21 UTC  
Audience: App2, HOME App, Agent, Runtime manager  
Disposition: **SOURCE ACK** for the bounded existing-result proposal.

## Agreement

The 09:13 App2 proposal is sound as a minimal source contract: add an
optional, derived `content_digest` to the existing ordinary document resource
returned by GET/list/create/update. The consumer mapping is direct and uses
the already existing pin shape:

```text
{ document_id: resource.document_id,
  version: resource.version,
  content_digest: resource.content_digest }
  -> DocumentPin
```

This is an additive wire-result change, not an already available carrier. It
requires the next coordinated normal Runtime schema/client generation,
release, and App/Agent adoption. This source ACK alone authorizes no
generation, version allocation, implementation, activation, or release.

## Exact current helper and algorithm

Runtime's authoritative helper is
`runtime_protocol/timeline_commit_inputs.py:125-137`,
`content_digest(content)`, through `_content_bytes`: validate finite JSON,
encode `canonical_json(content)` using UTF-8, and return
`sha256:` plus the SHA-256 hex digest of those bytes. The canonical serializer
is `runtime_protocol/util.py:24-25` (`sort_keys=True`, compact separators,
`ensure_ascii=False`).

The digest is over the document `content` only. It does not hash the project
ID, document ID, version, timestamps, or the resource envelope. Those values
remain the exact binding identity. `timeline_commit_inputs.py:140-154`
validates the existing three-field `DocumentPin`; the retention binding's
primary key binds `(project_id, document_id, document_version,
content_digest)` at `:49-60`.

For a live row, the existing exact-read path selects
`project_documents` by `(project_id, id)` at
`runtime_protocol/timeline_commit_inputs.py:368-375`, recomputes the same
helper at `:378-386`, and requires both the supplied digest and version to
match. It then rechecks source identity/schema at `:391-399`. For a retained
row, `_binding_document` reloads and revalidates the content digest at
`:334-359`, including the same project/document/version/digest binding, and
returns the exact existing `{pin, document}` carrier.

## Read/update consistency

The result construction is one existing function,
`runtime_protocol/service.py:4420-4427`, `_document_resource`. It reads the
row's `content_json`, validates it against the already selected
`project_id`/document ID/kind, and builds the ordinary resource. The proposed
field must be derived there from the same `content_digest(content)` helper;
it must not be persisted in `project_documents`, inserted into `content_json`,
or represented by a second source record.

All relevant ordinary paths use that same construction: list passes it as the
resource function at `service.py:4465-4476`, GET returns it at `:4478-4483`,
create returns it after the insert at `:4461-4463`, and update returns it
after the versioned row update at `:4519-4522`. Therefore create/update
responses carry the derived field inside their existing `data` resource;
GET/list carry the same field directly. An update changes `version` and
`content`, so the derived digest changes exactly with the new row content;
unchanged reads of the same row return the same digest.

## Compatibility and boundaries

The field should remain optional during rollout so old ordinary resources and
old clients remain valid. A new native capture/import/select/promote caller
must require the field for this pin-producing path and refuse visibly when it
is absent or unavailable. It must not hash in the browser, guess a latest
digest, silently fall back, or use a new endpoint, DTO, source kind, store,
preparation/save-readmission path, or extensible fake carrier. The existing
`DocumentPin` and exact verified-read/capture machinery are the only mapping
target.

This is derived-only source semantics: no digest is stored or serialized into
the document's content. The normal JSON response will of course serialize the
new additive result field when the coordinated wire change is released.
Main's successful snapshot association remains live; this ACK does not remove
or retire it. Immutable42a/017 and public014 are not mutated.

## Evidence and non-actions

This ACK is source inspection of the current helper and call graph, using the
completed `runtime-transcript-initial-pin-producer-0903.md` and the App2
09:13 proposal. No product code, schema, generated artifact, version, pin,
endpoint, association, or activation was changed. No full/socket/browser
suite was run; no new test was added.
