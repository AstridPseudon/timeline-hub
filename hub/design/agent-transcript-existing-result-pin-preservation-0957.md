# Agent dormant transcript result-pin preservation

Date: 2026-10-21 UTC  
Scope: Agent SDK normal transcript read/write adapter; dormant producer metadata only.

## Implemented mapping

The existing transcript path now preserves an optional server-provided pin
without changing its public writer API:

```text
ordinary document resource
  {document_id, version, content_digest, ...}
        -> {document_id, version, content_digest}  # existing DocumentPin
        -> existing transcript sync result metadata: {"pin": DocumentPin}
```

`astrid/sdk/media_transcript.py` validates the resource at the adapter
boundary. It accepts an existing `Mapping` or an object resource, requires a
nonempty document ID, a positive integer version, and the exact
`sha256:<64 lowercase hex>` digest form. It never computes a digest or reads
the latest document to fill one in.

`_write_transcript_result()` takes the pin from the already-returned mutation
`result.data` for create/update, or from the already-read resource for a
no-op. `_read_transcript_result()` supplies the same optional metadata to the
existing dry-run/report path. `write_transcript()` still returns exactly the
existing status string (`created`, `updated`, or `unchanged`). The existing
document CRUD calls, CAS version, idempotency/replay path, and transcript
content remain unchanged.

## Compatibility and activation boundary

Runtime 09:23 SOURCE ACK and App2 09:40 SOURCE ACK agree on the future
optional derived `content_digest` field on the existing document resource for
GET/list/create/update. The current generated client/resource does not carry
that field, so this Agent change is dormant until the separately authorized
coordinated Runtime generated-client release. No generated type, schema,
wire field, version, endpoint, store, pin activation, generation, or Runtime
code was changed here.

If the field is missing or malformed, the normal read/write operation keeps
its existing success/status behavior and no pin is emitted. A future native
association adapter must treat that missing pin as a visible refusal; this
change does not activate or add that caller. The mutation result is retained
as-is, even if a later GET observes another version/digest.

## Evidence

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_media_transcript.py tests/sdk/test_runtime_response_conformance.py tests/test_transcribe_asset_handoff.py tests/test_preferences_documents.py --tb=short
84 passed in 1.89s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_media_transcript.py --tb=short
13 passed in 0.83s

PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/media_transcript.py astrid/sdk/timeline_transcripts.py tests/sdk/test_media_transcript.py
All checks passed

git diff --check
passed
```

No full, HTTP, native, browser, render, install, or Runtime suite was run.
