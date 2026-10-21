# Agent handoff: normal transcript pin producer is NO-CARRIER

Date: 2026-10-21  
Audience: Runtime manager, App2/HOME, orchestrator  
Scope: exact Runtime09:03 transcript-pin-producer request and App2
association-source request. No transcript redesign or implementation.

## Verdict

**NO-CARRIER.** The current normal Agent SDK transcript read/write path does
not receive an authoritative initial `{document_id, version, content_digest}`
or a `VerifiedDocument` binding. There is therefore no dropped existing
carrier for Agent to adapt. No Agent production code was changed.

The existing exact verified-read carrier remains valid after a complete pin is
already known; it cannot produce that first pin.

## Exact current source trace

Agent source in this worktree:

- `astrid/sdk/media_transcript.py:55-62`: `read_transcript()` resolves the
  project, calls `client.documents.show(...)`, and returns `result.data`
  unchanged. A successful normal document result is the ordinary document
  resource.
- `astrid/sdk/media_transcript.py:65-90`: `write_transcript()` performs the
  ordinary show/CAS update-or-create flow. It checks `result.ok` and returns
  only the status string `created`, `updated`, or `unchanged`; it does not
  return the mutation `data` or receipt.
- `astrid/sdk/documents.py:270-291`: `Documents.show/create/update` expose the
  normal remote operation results; transcript create derives only the stable
  document ID from project/media/source identity.
- `astrid/sdk/remote.py:328-437`: `_typed()` unwraps a generated mutation
  `{data, receipt}` into `DomainResult.data` and `DomainResult.receipt`. Reads
  are explicitly classified as receipt-less.
- `astrid/sdk/workspace_client.py:314-325`: the SDK deliberately preserves a
  generated mutation receipt out-of-band as the existing `{data, receipt}`
  envelope and removes any duplicate receipt key from `data`. It does not
  derive or add document metadata.
- `astrid_runtime_client/generated.py:167-178`: generated `ProjectDocument`
  has exactly `document_id`, `project_id`, `kind`, `content`, `version`,
  `created_at`, and `updated_at`; no digest or pin.
- `astrid_runtime_client/generated.py:580-590,682-690`: generated
  `MutationResult` is the ordinary mapping plus its committed receipt, and
  `_mutation_json()` requires the existing `{data, receipt}` response. It
  does not create a verified-document binding.
- `astrid_runtime_client/generated.py:790-807`: normal document create/get/
  update use the ordinary resource and mutation result described above.
- `astrid/core/receipts/contract.py:40-52,83-120`: `CommandReceipt` has the
  existing nine-key shape, including an unconstrained `result` value. The
  normal document mutation receipt is still the mutation result; its presence
  is not an initial transcript pin producer.

The exact peer Runtime source trace independently records the server side:
`runtime-transcript-initial-pin-producer-0903.md` and
`peer-runtime-to-app2-home-agent-20261021T0903-transcript-pin-producer.md`.
Those reports identify `runtime_protocol/service.py:4420-4427` as producing
the ordinary document resource, `service.py:4438-4463,4485-4522` as returning
it inside the existing committed mutation envelope, and
`contract/schemas/document.json:4-15` as a closed schema without
`content_digest`.

The same Runtime trace confirms that normal document GET/list/create/update,
Agent `read_transcript()`/`write_transcript()`, and App import/select/promote
do not return an initial pin. App2’s source request is recorded in
`peer-app2-to-runtime-20261021T0853-transcript-pin-producer.md`.

## Existing exact carrier, and why it is not a producer

The types already exist in the generated timeline contract:

- `astrid_runtime_client/timeline_commit_types.py:47` defines
  `DocumentPin = {document_id, version, content_digest}`.
- `astrid_runtime_client/timeline_commit_types.py:100-101` defines
  `VerifiedDocument = {pin: DocumentPin, document: Document}`.
- `astrid/sdk/timeline/native_source_inputs.py:80-104` requires the complete
  three-field pin, calls the existing verified-document read, checks that the
  returned pin is identical, validates project/document/version scope, and
  checks the canonical content digest. It cannot be called without the pin.
- `astrid_runtime_client/generated.py:935-937` exposes the existing verified
  read with the pin encoded in its query. This is an exact read, not a
  discovery operation.

Consequently, the existing `VerifiedDocument` result is legitimate for
retained/exact source reads only. It does not prove a first-use ordinary
project transcript. No latest-row lookup, browser/body hash, or guessed
version is an authority substitute.

## Compact witness

The current targeted SDK tests pass the existing status/read behavior. A small
in-memory witness using `CommandReceipt.result` as the normal document row
prints:

```text
{'write_status': 'created',
 'read_keys': ['content', 'created_at', 'document_id', 'kind',
               'project_id', 'updated_at', 'version'],
 'receipt_result_keys': ['content', 'created_at', 'document_id', 'kind',
                         'project_id', 'updated_at', 'version']}
```

This demonstrates both boundaries: the normal read has no digest, and the
existing committed receipt/result metadata carries the same ordinary resource,
not a `DocumentPin`. The write helper then projects that mutation to the
status-only API.

## Smallest cross-area proposal for agreement (not implemented)

Keep ordinary project-document CRUD and all current transcript writer/
association positives live. Before any code, Runtime/App2/Agent should agree
which existing normal transcript `data` result is the authoritative carrier.
The smallest bounded candidate is to use the existing `VerifiedDocument`
value for `media.transcript` normal read/create/update results:

```text
existing normal transcript result.data
    -> existing VerifiedDocument {pin: DocumentPin, document: Document}
    -> existing association input {pin, document}
```

This reuses the generated `DocumentPin`/`VerifiedDocument` types and the
existing result envelope; it adds no endpoint, route, store, producer, public
field, or new DTO. The ordinary resource shape for non-transcript project
documents stays unchanged. The SDK/App2 adapter can preserve the binding only
after Runtime formally agrees that this existing result carrier is authoritative
and documents the transcript-scoped result shape. Until then, changing
`media_transcript.py`, hashing content, reading latest, or wiring the dormant
verified-read helper would be inventing authority or adapting a carrier that
does not exist.

This is a proposal for owner/orchestrator agreement only. It is not a request
to register a transcript schema, mutate frozen017, activate a pin, retire the
existing writer, or run native/HTTP/browser/full suites.

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_media_transcript.py tests/sdk/test_runtime_response_conformance.py`
  — **28 passed** in 1.37s.
- The direct in-memory witness above — **PASS**.
- No full, daemon, HTTP, native, render, browser, install, or private-body
  run was performed.
