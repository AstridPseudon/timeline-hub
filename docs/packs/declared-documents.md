# Declared project documents

`Documents.for_pack(entry, project=..., subject=..., source=...)` binds a
canonical V3 pack entry to exact host-selected identities. Its public operations
are `read(kind, subject, source)`, `list(kind, subject, source)`, and
`write(kind, subject, source, content=..., expected_version=...,
idempotency_key=...)`. Results use the existing `DomainResult` envelope.
`GenericPackHost.document_facade` makes the same binding after checking its
configured source roots and `document_source_digest(entry)`. The trusted host
supplies an existing authenticated `Documents` instance; worker registration
tokens are not silently upgraded to document credentials. This local Python
binding is not a sandbox for arbitrary untrusted Python code.

Opt in through the existing document declarations:

```yaml
schema_version: 3
id: demo
name: Demo
version: 1.0.0
# Other action/UI/resource declarations keep their existing meaning.
documents:
  analysis:
    format_version: 1
    schema:
      $id: demo.analysis/v1
      type: object
      required: [text]
      properties:
        text: {type: string}
      additionalProperties: false
    runtime:
      kind: demo.analysis
      schema_id: demo.analysis
      schema_version: 1
      identity: subject-source-v1
      access: [read, list, write]
extensions:
  data_namespace:
    owner: pack_demo
    schema_id: demo.data
    version: 1
    writable: [notes]
    schema:
      $id: demo.data/v1
      type: object
      required: [v]
      properties:
        v: {const: 1}
        notes: {}
      additionalProperties: true
```

The schema may instead name an admitted JSON file using an existing safe relative
resource path. Only draft 2020-12 schemas with locally resolvable references are
supported. Old document-format declarations without `runtime` grant no facade
access. Each operation must be explicitly listed; none supplies Runtime actor,
project, or route grants. A missing namespace declaration or unsupported owner
data version disables owner writes while declared reads remain available.

`DocumentKind` in `astrid.core.pack.document_access` is the single ID/schema
helper. `subject-source-v1` applies only to kinds and schemas qualified by the
admitted pack ID. It uses the existing stable document identity with a canonical
JSON pair of exact subject/source as its name. `stable_document_id` remains
exported from `astrid.sdk.documents` with its existing default-name behavior.
The content envelope is exactly:

```json
{"kind":"demo.analysis","schema_id":"demo.analysis","schema_version":1,
 "subject":"media:one","source":"producer:one","data":{"text":"synthetic"}}
```

Use `DocumentKind.envelope` to construct it. `expected_version=0` selects existing
createDocument; positive versions select updateDocument with CAS. The explicit
idempotency key and unchanged content/expected version go back to Runtime on a
retry; the facade has no replay/history store. Generic updates first read the
stored kind to exclude timeline documents, so those updates also need the
existing document-read grant. Runtime decides actual CAS, replay and conflict
acceptance. No document mutation can adopt data into a timeline or replace an
EditCommand transaction.

Listing follows the SDK's existing complete, bounded kind pagination (refusing
malformed or repeated cursors), then filters exact subject/source client-side.
There is no new server filter, query endpoint or latest/ambiguous-source choice.
The facade uses a pinned canonical project ID directly, without resolving a
mutable project alias. Manifest/resource changes invalidate existing bindings.
The source digest includes the exact root, manifest bytes and declared resources;
it is an evidence/selection identity, not a wire compatibility version.

Owner identity is derived from the selected manifest ID as `pack_<id>` and bound
to admitted source, independently of contribution labels. `astrid` is reserved;
a pack called `transcript` gets `app.pack_transcript`, never `app.transcript`.
`OwnerData` provides immutable reads and detached whole-property set/clear
results on existing config/clip carriers. It preserves foreign namespaces,
unknown/underscore data, literal null and clear-shaped values. Malformed or
unsupported owned values refuse changes; explicit `clear` removes presence.
It does not persist data or add a generic timeline owner-property command.
Adopting these detached results requires an admitted semantic EditCommand.
Arrays are whole properties here; there is no index mutation intent.

Document `schema_version`, document authoring `format_version`, contribution API
versions and namespace `app.pack_<id>.v` are separate. Existing `app.astrid.v`
and reserved transcript, identity, timing, cache and track semantics are untouched.
No rule for a shared upstream transcript producer is asserted by this identity
helper. Such a consumer needs its exact source-admitted per-kind identity/schema
and validated transcript import/binding operation. The current Caption Foundry
dev module uses legacy patches and requires a separately admitted App change
before this facade can be claimed as its real command-only consumer.
