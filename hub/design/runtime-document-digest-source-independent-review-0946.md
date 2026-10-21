# Runtime Document digest source review — 0946

**Verdict: APPROVE**

Reviewed exact commit `4e1133fb77784a494124e9a73c7c277b6a0cc51e`, tree
`5302fe1423356c20be739df4789ce63218462328`, against
`tl/rt-m2-document-derived-digest-source-0944` (base `b92d3e7`). The diff is
exactly three files and 44 added lines:

- `contract/schemas/document.json`: one optional `content_digest` property.
- `runtime_protocol/service.py`: two lines in `_document_resource`.
- `tests/test_transcript_documents.py`: additive assertions/tests only.

## Review findings

- The implementation calls the existing
  `runtime_protocol.timeline_commit_inputs.content_digest` helper. That helper
  applies `finite_json`, serializes with the existing canonical JSON settings
  (`sort_keys=True`, compact separators, `ensure_ascii=False`), encodes UTF-8,
  and returns the canonical `sha256:<64 lowercase hex>` value. The digest is
  therefore over `content` only; it does not include the resource envelope,
  project/document identity, timestamps, version, or browser state.

- `_document_resource` remains the single construction point used by ordinary
  GET, list, create, and update results. It reconstructs the existing content,
  project, identity, version, and timestamps from the same row and adds only a
  derived response key. No digest column, content rewrite, endpoint, DTO, or
  new source was added. Create/update are inside the existing durable mutation
  transaction, so a helper failure cannot leave a partial write or receipt.
  Runtime's HTTP boundary already rejects non-finite JSON; finite ordinary
  wire content preserves the existing CRUD behavior.

- Replay is ledger-first and remains unchanged. Both document mutations call
  `_command_replay` before any row resource is rebuilt. `_command_replay_state`
  reads the prior `command_idempotency.result_json` and reconstructs the
  existing receipt; it does not call `_document_resource` or refresh the
  result from the current row. Later writes insert their own ledger records and
  do not rewrite the prior result. On restart the same durable ledger row is
  read, so an accepted result from a pre-digest Runtime may remain byte/result
  equivalent and omit `content_digest`, even after newer writes. New accepted
  results include the field and replay unchanged thereafter. Existing replay
  window/expiry behavior is unaffected.

- The schema property is optional because it is absent from `required`, while
  `null` is rejected because the property type is `string` (with the canonical
  SHA-256 pattern). This preserves old resources during rollout without
  permitting a null digest.

- The helper import is local to `_document_resource`, avoiding an import cycle;
  direct imports of both `runtime_protocol.service` and
  `runtime_protocol.timeline_commit_inputs` succeeded. The unchanged
  `published014`/`private017` paths are outside this diff, and live callers,
  generated projections, release/version/pin work, and native/artifact
  qualification remain intentionally pending.

## Evidence

Author evidence reviewed from the worker log:

`PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_transcript_documents.py tests/test_timeline_document_object_contract.py`

Result: **41 passed in 11.67s**.

The source schema smoke check passed for both omitted `content_digest` and
`content_digest: null` rejection. `git diff --check` passed. No full, HTTP,
browser, render, install, generation, or release suite was run.

The 41-test addition does not create a pre-digest ledger fixture, but the
old-result replay requirement is established directly by the unchanged
control flow described above. A small future regression test may load an old
`command_idempotency.result_json` captured before this field, perform a newer
document write, restart, and assert retry returns the old field-less data and
the same receipt. This is a bounded evidence follow-up, not a source-change
blocker for this exact diff.
