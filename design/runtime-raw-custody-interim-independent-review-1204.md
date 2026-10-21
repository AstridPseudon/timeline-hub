# Runtime raw custody interim independent review

## Verdict

**APPROVE the bounded internal source delta** at Runtime `d6c58babc6bf35bcdbc4a6f7bade177c97075268` (tree `daa20ef65620361dcf009d8bf487fcb9a8675f43`) against parent `07dc1d05f011556540881595f7b00b901c191321` (tree `8a0b0d9d0fb7595be97629c6b62f479a56e7832c`).

This is an independent source/custody review only. It does not qualify a
caller, public contract, generated client, HTTP route, native path, or public
adoption.

## Scope and findings

The diff is limited to:

- `runtime_protocol/timeline_commit.py`
- `runtime_protocol/timeline_commit_port.py`
- `tests/test_timeline_raw_capture.py`

The source reuses the existing `MediaManifestEntry` carrier and adds only the
private internal `MediaInfo`/`RuntimeCommitPort.raw_media_info` seam. It does
not add a DTO, endpoint, schema, table, generated client, caller duration,
allocation ID, or alternate authority.

`RequestCommitPort.raw_media_info` requires the exact two-key pin, equal
`media_id`/`content_digest` SHA-256 identities, and exact membership in the
request's recursively declared command objects. It memoizes only within the
request. `MediaReads.raw_media_info` scopes the lookup to the Runtime realm
and project-managed object relation, opens one CAS descriptor, and invokes the
existing FD verifier for regular-file identity, catalog size, full SHA-256,
and stable descriptor identity/timestamps. Its result is only object ID,
stored media type, and size.

Acceptance rechecks every captured raw pin/result inside the existing
acceptance transaction before `_persist_closure`, publication, projection, or
input persistence. It requires the same exact pin in the candidate manifest,
checks the captured identity/result, and adds only captured raw objects to the
existing authorized-media closure. Missing, foreign, unowned, undeclared, or
tampered objects therefore refuse without durable writes. Exact retry remains
ledger-first: the coordinator performs the durable lookup before creating the
provider port, and the acceptance store repeats the lookup before validation.

The BASE-only media read behavior and existing five-field `selected_media`
path are unchanged by the diff. The known inherited `07dc` item-map issue is
outside this delta and was not used as a rejection reason; any merge must
preserve the separately corrected helper through the normal merge.

## Evidence

Author-retained focused evidence from the exact candidate tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_raw_capture.py
6 passed in 1.69s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_commit_port.py tests/test_timeline_media_selection.py tests/test_timeline_commit_acceptance.py
107 passed, 1 deselected in 12.75s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_commit_restore_port.py
51 passed in 9.17s
```

The author also recorded `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check`
passed and `git diff --check` passed. The retained command/log is:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-raw-custody-interim-current-port-ready1158/log.txt`.

Independent read-only boundary checks on this review checkout:

```text
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current

git diff --check 07dc1d0..d6c58ba
passed

git show 07dc1d0:contract/artifacts.json | sha256sum
a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d

git show d6c58ba:contract/artifacts.json | sha256sum
a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
```

No full, HTTP/socket, browser, renderer, install, native, or public
qualification was run or claimed.

## Next step

The Runtime manager may carry this source into the next normal merge, with the
corrected `07dc` helper retained. Later paired Agent caller and public/native
qualification remain separate work.
