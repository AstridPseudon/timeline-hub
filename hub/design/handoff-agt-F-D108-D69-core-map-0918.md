# F-D108/D69 independent semantic predicate review

Verdict: **FAIL with one precise missing-purpose finding**. Five assigned functions were reviewed against upstream `08e6b905`, captured `d629484`, and current normal `d0ecf1d`; all current source blobs match captured-new. No product code/tests changed and no behavior suite ran.

## Multiplicity

| function | removed | added | decision |
|---|---:|---:|---|
| `tests/core/test_timeline_element_publication.py:test_sameclip_exacthead_publication_preserves_closure_and_user_params` | 11 | 18 | FAIL |
| `tests/test_timeline_clip_replacement.py:test_remote_parent_media_replacement_publishes_exact_closure_once` | 2 | 18 | PASS |
| `tests/sdk/test_timeline_publish_connection.py:test_a_publish_with_no_client_writes_through_the_connection_it_opens` | 2 | 5 | PASS |
| `tests/sdk/test_timeline_publish_connection.py:test_a_publish_with_a_client_writes_through_that_client` | 2 | 5 | PASS |
| `tests/v10/test_timelines_create.py:test_remote_create_empty_generates_ulid_when_no_id_given` | 5 | 5 | PASS |

All 73 changed rows are in JSON/TSV with original membership IDs, exact AST fingerprints, source lines, and mappings. Full historical fingerprints remain in `handoff-agt-D108-D69-predicates-1-0902.json`.

## Finding

- `9:removed:0` (same-clip old line 38) checked empty `shot_revisions` and `internal_timeline_revisions`. The current v2 body has no assertion over either closure list; `body['reads']` covers only parent clips/fields and the result is flattened. This is an actual missing purpose. Smallest repair: assert the closure list on the v2 canonical document/receipt, or obtain a C0-approved scope ruling.

## Current replacements

- Same-clip checks map to v2 semantic commands, guarded `doc.patch`, reads, canonical result, receipt, and non-mutating-prefix assertions.
- Parent-media maps one legacy publication to one registered `commit_timeline` request and durable receipt, with exact base pair, label, atomic merge, source, selected payload, and expected head.
- Connection tests map legacy transport to `_commit_document`/`TimelineSession`/v2 `doc.patch`; absent-client opens once and supplied-client is reused.
- Empty creation maps generated ULID/shell identity to timeline init, history replay, and `commit_timeline`; `key-head` is source-qualified at `astrid/sdk/remote.py:518,591-593`.

## Limits

Source-only commands: `git show`, `git rev-parse`, `ast.parse`, `ast.walk`, `ast.dump`, `ast.get_source_segment`, SHA-256, JSON parse, and in-memory AST parsing. Tests/typecheck/lint are N/A by the read-only brief. No approval or retirement decision is inferred from counts; the one missing closure assertion remains FAIL.
