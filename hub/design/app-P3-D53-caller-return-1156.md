## Completed

- Repaired only `caller-publication.py` and `caller-custody.json`.
- Added immutable hash/provenance checks for D53 source, pure qualification, normal dispatch, branch, and checkout receipt.
- Rejected caller-supplied proof manifests and forged review/receipt inputs.
- Refreshed custody to current P2/registry state.

Production identities:

- Source: `2357df…`, tree `50070b…`
- Final HOME: `602f8b…`, tree `a38844…`, parents `2e3c8f…` + `2357df…`
- Registry: 249 lines; 248 outside rows; outside SHA-256 `b9c97f…`
- Current P2 row SHA-256: `6a45d0…`
- Candidate file hashes:
  - `caller-publication.py`: `7c70d2…`
  - `caller-custody.json`: `4683e7…`

## Tests

- `TMPDIR=... python3 caller-publication.py` — `PREPARED`
- `python3 -m py_compile caller-publication.py` — passed
- `python3 -m json.tool caller-custody.json` — passed
- `bash -n` decoded/wrapped P2/P3 rows — 6/6 passed
- Provenance negative controls — all refused
- C0 wire-field preservation — request 29, reply 56
- `git diff --check` — passed
- Exact delta — two files only

No install, registry write, service, browser, build, backend, native, HTTP, full suite, or original journey was run.

Commit message written to the requested path; `DONE` marker created. Independent cumulative review remains downstream/unverified.