# Runtime retained transcript verified read

## Result

The existing `get_project_verified_document` path now accepts the existing
`media.transcript` kind in `_source_kind`, alongside its pre-existing config
and `astrid.project-pack` kinds. It still returns the existing
`{"pin", "document"}` VerifiedDocument carrier.

## Custody review

- No endpoint, DTO, schema, generated client, store/table, or object-read
  changes were made.
- Transcript reads continue through `capture_document_input`, which enforces
  the exact document/version/content digest pin, `media.transcript/v1` shape,
  project-owned source media, retained closure reachability, canonical content
  bytes, and first-capture update-race checks.
- `snapshot_object` is not consulted or manufactured for transcripts.
- Unsupported document kinds and foreign project pins still fail before any
  write.
- The retained V1 transcript remains readable after a V2 update, live-row
  removal, and Runtime restart.

## Evidence

- `python -m pytest -q tests/test_timeline_commit_inputs.py`: 12 passed.
- Central socket-aware targeted service:
  `tests/test_timeline_source_document_boundary.py tests/test_timeline_pack_document_read.py tests/test_timeline_commit_inputs.py`:
  29 passed.

The targeted HTTP test covers initial capture, V2 update, live-row removal,
restart, exact HTTP read, unsupported-kind refusal, foreign-scope refusal, and
zero-write refusal snapshots. No full/browser/render suite was run.
