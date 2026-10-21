# Runtime transcript initial-pin producer trace

Date: 2026-10-21  
Audience: App2/HOME, Agent, Runtime manager  
Verdict: **NO-CARRIER for initial ordinary project-transcript pin production.**

This is a source-only trace of the current public014 normal paths. It does not
propose a DTO, endpoint, store, schema, browser hash, guessed latest digest,
or new producer.

## Current public014 facts

The current published line is Runtime 0.2.14, producer commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, with the ordinary 6ba schema
(55 definitions / 29 clauses) and 76 manifest artifacts. The current Runtime
integration source is `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`; the App generated client remains
contract `0.2.14`, protocol `workspace.v1`, schema digest
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
(`src/integrations/runtime/generated-contract-metadata.ts:3-6`). These are
the current STATUS/integration facts, not a new release or pin decision.

For ordinary documents, the public014 server routes are the existing
`GET/POST /v1/projects/{project_id}/documents` and
`GET/PATCH /v1/projects/{project_id}/documents/{document_id}`
(`runtime_protocol/server.py:701-725`; OpenAPI
`contract/openapi/workspace-v1.yaml:126-145`). The public document schema is
closed and requires exactly the ordinary resource fields; it has no
`content_digest` (`contract/schemas/document.json:4-15`, especially
`additionalProperties: false`).

## Normal get/create/update/import/promotion trace

### Runtime ordinary project-document CRUD

`RuntimeService._document_resource()` loads `content_json`, renames `id` to
`document_id`, removes `content_json`, and adds parsed `content`; it does not
add a digest (`runtime_protocol/service.py:4420-4427`). `create_document()` and
`update_document()` return that resource through the existing committed
mutation envelope (`service.py:4438-4463` and `4485-4522`). The public route
returns those results directly (`server.py:701-725`). Thus the server result
for a normal transcript document is:

```text
{document_id, project_id, kind, content, version, created_at, updated_at}
```

There is no server-generated `content_digest` in this result, in its ordinary
list/get response, or in the ordinary create/update `data` resource. The
committed receipt is the existing mutation receipt; it is not a transcript
pin producer.

### Agent normal transcript helper

Agent resolves the project ID, then `read_transcript()` calls ordinary
`client.documents.show(...)` and returns `result.data` unchanged
(`astrid/sdk/media_transcript.py:44-62`). `write_transcript()` does ordinary
get, then CAS update or create, and returns only the status string
`unchanged`/`updated`/`created`; it does not return a document or pin
(`astrid/sdk/media_transcript.py:65-90`). Agent’s generic document client
also maps the ordinary resource without a digest
(`astrid/sdk/documents.py:270-291`; generated `ProjectDocument` fields are
`generators/python_client_template.py:167-178`).

### App normal project transcript repository

App’s `ProjectTranscriptDocument` contains document identity, content, version,
and timestamps, but no `content_digest`
(`src/tools/video-editor/data/typed/projectTranscript.ts:53-63`). The
repository maps ordinary list/get/create/update one-for-one through the
generic document surface (`projectTranscript.ts:82-119`). The Runtime provider
does the same: list/get return the generic client resource and create/update
parse that same resource as a `ProjectTranscriptDocument`
(`src/integrations/runtime/dataProvider.ts:403-427,428-487`). The generated
public014 App client methods are ordinary CRUD with `ProjectDocument` as the
resource type (`src/integrations/runtime/generated.ts:17,60,94,139-142`).

The App client does not have a normal-path digest field to preserve. Its
mutation decoder attaches the existing receipt out-of-band to the returned
data object (`generated.ts:94`); that receipt does not manufacture a document
pin. If a future raw response had an unknown extra property, the current
runtime JSON decoder would not actively hash or derive it, while the closed
TypeScript document types would not expose it. That is not the present gap:
the current Runtime ordinary resource does not send the property at all.

### App import, select, and promote paths

The normal App import path turns incoming transcript data into canonical
project content, computes the deterministic transcript document ID, then calls
the existing repository get/create/update path
(`src/tools/video-editor/lib/project-transcript-host.ts:756-825`). The
select path calls repository `get()` and then the common association helper
(`project-transcript-host.ts:747-755`). The promotion path calls repository
`get()` or `create()` and then that same association helper
(`project-transcript-host.ts:827-857`).

The common helper receives a `ProjectTranscriptDocument`, writes the existing
timeline association, and returns only `{assetId, sourceId, documentId,
version, importedSegments, replacedSegments, replacedExistingSource,
associationSaved, message?}` (`project-transcript-host.ts:600-674`). The
public panel receipt type is closed to exactly those fields and also has no
digest (`src/sdk/video/transcript.ts:111-120`). `listProjectSources()` exposes
only `{documentId, sourceId, version}` (`project-transcript-host.ts:710-746`).
Therefore import, select, and promote do not receive or forward an initial
`DocumentPin`.

## Existing exact-pin carrier, and why it is not production

The existing Runtime read carrier is real and sufficient once a pin already
exists. `CommitPort._document()` checks that the supplied pin is declared or
reachable, selects the transcript kind/schema, calls
`capture_document_input(..., pin, ...)`, and returns the concrete mapping:

```text
{ "pin": capture.pin, "document": capture.document }
```

(`runtime_protocol/timeline_commit_port.py:294-321`, especially
`:314-317`). This is the exact result-to-`{pin, document}` mapping consumed by
Agent/App2’s transcript association path.

The capture helper validates the complete three-field pin before looking up a
live or retained row (`timeline_commit_inputs.py:140-154,422-455`). For a
retained accepted input, `_binding_document()` obtains the stored digest and
constructs both sides of the carrier as follows:

```text
pin      = {document_id, version, content_digest}
document = {document_id, project_id, kind, content,
            version, created_at, updated_at}
```

(`timeline_commit_inputs.py:334-367`, especially `:348-359`). For a live
first-use capture, `_live_capture()` compares the content digest to the
supplied pin and stores the supplied pin plus the ordinary document
(`timeline_commit_inputs.py:378-419`, especially `:384-417`). The digest
calculation is therefore a verification step after a complete pin has arrived,
not a public initial-pin response.

The acceptance retention result does include the exact pin fields
(`timeline_commit_inputs.py:650-706`, especially `:700-706`), but this is an
internal acceptance helper result, not the normal project transcript
get/create/update/import/promotion response or a public producer endpoint.

The public verified-read route has the same boundary: it accepts the three
query pin fields, then invokes `get_project_verified_document()`
(`runtime_protocol/server.py:59-62,546-575`). The service method passes that
pin to the exact read helper (`runtime_protocol/service.py:2557-2565`). It
cannot be called to discover the initial digest because the full
`{document_id, version, content_digest}` is required before invocation.

## Concrete NO-CARRIER conclusion

Across the actual normal paths:

| Path | Existing result | `content_digest` / pin producer? |
|---|---|---|
| Runtime document GET/list | ordinary resource | No digest |
| Runtime document create/update | `{data: ordinary resource, receipt}` | No digest in data; receipt is not a pin |
| Agent `read_transcript` | ordinary `result.data` | No digest |
| Agent `write_transcript` | status string only | No document/pin |
| App project transcript get/list | `ProjectTranscriptDocument` | No digest |
| App import/select/promote | association receipt with document ID/version/counts | No digest/pin |
| Runtime verified transcript read | `{pin, document}` | Yes, but only after caller supplies the exact pin and authority |

The gap is therefore not that App drops a server-provided initial digest from
the normal transcript response. The current public014 ordinary server/client
contract never carries that initial digest. The only existing carrier that
already returns `{pin, document}` is the authorized exact-pin resolver, which
is a retained/exact read and must not be confused with initial pin production.

## Smallest existing seam needing owner agreement

No Runtime code change is requested by this trace. The smallest existing seam
is the ordinary transcript mutation result at the point App2/HOME already
receives `r.create()`/`r.update()`/`r.get()`:

```text
Runtime ordinary document result
  -> App RuntimeDataProvider projectTranscripts repository
  -> App transcript host import/select/promote receipt
```

Owner agreement is needed only on which existing normal mutation/read result
is authoritative for carrying the initial exact pin into the existing
`{pin, document}` association input. Until that agreement exists, App2 should
keep ordinary association visibly unsupported for initial pin production and
may continue using the existing exact-pin read when a pin was already supplied
by an authorized accepted closure. No browser hashing, guessed latest row,
digest inference, new DTO/endpoint/store/schema, or re-admission during save is
justified by the current source.

No tests were run: this was a read-only source trace as requested.
