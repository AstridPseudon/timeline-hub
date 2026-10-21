# Runtime transcript Document.content_digest contract proposal

Date: 2026-10-21 UTC  
Status: **UNAPPLIED SOURCE CONTRACT PROPOSAL**  
Base: Runtime `tl/integration` `b92d3e7a05eec65c142294ef4873edd059e9b31d`  
Related: Agent 09:30 proposal, App2 09:13 proposal, Runtime SOURCE ACK 09:23

## Decision

Add one optional field, `content_digest`, to the existing ordinary `Document`
resource in `contract/schemas/document.json`. The next coordinated Runtime
source release that implements this proposal emits the field as a non-null
canonical SHA-256 digest on every ordinary document resource it returns. The
schema keeps the field optional during rollout so older resources and clients
remain valid; a pin-producing caller must refuse a resource that does not
contain a valid field rather than derive or guess one.

The field is:

```json
"content_digest": "sha256:<64 lowercase hexadecimal characters>"
```

It is derived from the document's `content` only, using the same existing
source-capture helper Runtime already trusts:

* `runtime_protocol/timeline_commit_inputs.py:125-137`,
  `content_digest(content)` -> `_content_bytes(content)`;
* `_content_bytes` first applies `finite_json`, serializes with
  `runtime_protocol/util.py:24-25`, `canonical_json` (`sort_keys=True`, compact
  separators, `ensure_ascii=False`), encodes UTF-8, and returns
  `sha256:` plus the SHA-256 hex digest of those bytes.

The digest never includes the resource envelope, project ID, document ID,
version, `created_at`, or `updated_at`; it never hashes browser content. The
resource's exact project/document/version identity remains separate. The
existing `DocumentPin` is formed directly as:

```text
{ document_id: resource.document_id,
  version: resource.version,
  content_digest: resource.content_digest }
```

The project is supplied to the existing exact-read/capture call. Runtime then
continues to enforce the project/document/version/digest binding and the
existing kind/schema/source checks.

## Exact source diff

The sibling unapplied patch is
`runtime-transcript-document-digest-contract-0940.patch`. It changes only the
normal `Document` schema:

```diff
@@
     "content": {},
+    "content_digest": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" },
     "version": { "type": "integer", "minimum": 1 },
```

`content_digest` is deliberately absent from `required`; present values are
non-null by the string schema. No second source schema template is needed:
`DocumentPage.items` and the existing GET response already reference
`./schemas/document.json`, while create/update use the existing
`CommittedMutation` envelope whose `data` is the ordinary resource. No
OpenAPI route, request schema, endpoint, DTO, persistence column, or separate
resource is added.

## Existing result construction and CRUD behavior

The implementation seam is the existing
`runtime_protocol/service.py:4420-4427` `_document_resource(row)`. The
implementation of this proposal derives `content_digest` there from the
already validated `content`, with no `project_documents` column and no field
inserted into `content_json`.

That one construction is already used by all ordinary paths:

* GET `/v1/projects/{project_id}/documents/{document_id}` returns the ordinary
  resource with the field.
* GET `/v1/projects/{project_id}/documents` returns each ordinary list item
  with the field through `_page_rows` and `resource_fn`.
* POST create returns the same resource in existing `data` at
  `service.py:4461-4463`, with the existing committed receipt unchanged.
* PATCH update returns the new version's same resource in existing `data` at
  `service.py:4520-4522`, so a content change changes the digest exactly with
  the new content and version.

For a retry with the same idempotency key and the same request hash, Runtime
must return the exact previously recorded `data` and the exact existing
receipt via `_command_replay_state`/`_command_record`. It must not rewrite old
accepted receipts or synthesize a newly refreshed resource during replay.
Retries of mutations first accepted by a Runtime that predates this field may
therefore legitimately return old `data` without `content_digest`. That is a
bounded rollout HOLD: a pin-producing caller visibly refuses that result and
keeps the selected/new draft and any outbox state intact; it does not hash
locally, fall back to latest, or re-admit/save the document. New accepted
results from the implementing Runtime include the field and replay
identically thereafter.

All ordinary content and CRUD semantics remain live. Existing retained exact
verified-read custody remains live: `timeline_commit_inputs.py:334-367`
reconstructs the retained `{pin, document}` pair, and
`:378-419` recomputes the same helper for a live exact row before accepting a
pin. This source proposal does not alter retention, accepted closures,
versioning, draft preservation, or the existing successful association
receipts. Foreign project rows, unsupported document kind/schema, missing
digest, malformed digest, and digest/version mismatch remain visible refusal
cases.

## Normal generation and type consequence

`contract/manifest.json` already lists `schemas/document.json`; after an
authorized application, normal `python generators/generate.py` must be run by
the owning release work. That changes the contract digest and corresponding
generated metadata. The generated client types must expose the additive
optional field (`content_digest: str | None` / `content_digest?: string`) and
preserve it in their `from_json`/resource mapping. This is a normal generated
follow-up, not part of this source-only proposal; no generator was executed
and no generated file was edited here. Existing generated clients remain a
bounded HOLD for callers that need to consume the field until the coordinated
contract/client release.

## Focused eventual acceptance checks

1. For ordinary transcript create, GET, list, and update, assert the returned
   digest equals `runtime_protocol.timeline_commit_inputs.content_digest` over
   that exact returned `content`; also assert it is unchanged for identical
   reads and changes with the updated content. A digest of the full resource
   envelope must fail this check.
2. Capture/associate V1, update the ordinary document to V2, restart Runtime,
   then resolve the retained V1 pin. Assert the retained result is V1 with its
   original `DocumentPin` and content, while the live ordinary read is V2.
   Retry the accepted mutation and assert its original result/receipt is
   returned byte-for-byte rather than rewritten.
3. Assert a foreign-project pin, an unsupported kind/schema, a missing or
   malformed optional digest, and a digest/version mismatch are visibly
   refused; selected/new transcript draft content remains intact. No browser
   hashing, latest fallback, or separate producer is allowed.

## Scope and disposition

This is source-only and unapplied. Live callers changed: **NONE**. No version
allocation, pin, private017 extension, generated artifact, release, endpoint,
schema-source fork, or generator execution is authorized by this proposal.
The only open inconsistency is the bounded old-resource/old-replay HOLD
described above; it is resolved by the coordinated generated client/runtime
release, not by rewriting historical receipts.
