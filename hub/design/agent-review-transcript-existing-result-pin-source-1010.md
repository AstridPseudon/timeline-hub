# Agent transcript existing-result pin source review

Date: 2026-10-21 UTC  
Reviewed source: Agent commit `abe0fd6f504d49891eff0aa1cc1d173ba01e1cf3`  
Parent: `c4b964f6a050edf63a4278d35717e46a88a80386`  
Tree: `b2439ec434a50cac5366d8dbe900c4360d8f4fe0`  
Subject: `feat(timeline): preserve transcript result pins`

## Verdict

**APPROVE SOURCE** for composition with Runtime/App2 under the settled
dormant optional-resource contract.

**HOLD native-pin activation/release** until the coordinated Runtime ordinary
`Document` result and generated-client release supplies `content_digest`.
That is the bounded rollout hold in Runtime's 09:40 source contract, not a
defect in this Agent source.

## What was verified

- `astrid/sdk/media_transcript.py:_write_transcript_result` reads once to
  decide create/update/no-op. For create and update, the returned mutation's
  exact `result.data` is passed to `_document_pin`; its returned document ID,
  version, and digest are authoritative. There is no latest read, local
  content digest, or read-after-write.
- The no-op branch returns `_document_pin(row)` from the original successful
  `show`, preserving the original read's version and digest.
- `_read_transcript_result` returns the original `show` data and derives its
  optional pin from that same response only. `_document_pin` accepts only a
  non-empty document ID, an exact positive `int` version, and
  `sha256:<64 lowercase hex>`; missing or malformed fields return `None`.
- `read_transcript` still returns the original document data, and
  `write_transcript` still returns only the existing `created`, `updated`, or
  `unchanged` status string. The ordinary document show/create/update calls,
  CAS version, and replay behavior are not changed by this commit.
- `timeline_transcripts.sync_narration_transcripts` adds `pin` only when the
  already-returned resource is valid. Missing/malformed digest retains the
  legacy successful status/report with no pin; it does not activate native
  association or manufacture a pin.
- The commit changes only the two transcript adapter modules and
  `tests/sdk/test_media_transcript.py`; no schema, generated client, endpoint,
  store, native association, or live mutation code is included.

The 0957 author report records 84 retained tests across the adapter and direct
neighbors. This review ran the focused adapter lane below; no full or live
suite was requested.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_media_transcript.py --tb=short
=> 13 passed in 0.75s

git diff --check
=> passed
```

No Runtime, HTTP, native, browser, full, install, schema, or generated-client
test was run. Those are outside this source-only review.

## Handoff

Runtime/App2 may use this source identity: Agent commit
`abe0fd6f504d49891eff0aa1cc1d173ba01e1cf3`, tree
`b2439ec434a50cac5366d8dbe900c4360d8f4fe0`. Preserve the separate rollout
hold: callers must visibly refuse missing/malformed digest until the
coordinated ordinary-resource/generated-client release; they must not hash
locally or fall back to latest.
