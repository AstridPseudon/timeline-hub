# RT03 committed raw-media carrier source handoff

Status: **APPROVED, bounded source handoff only** (2026-10-21).

## Exact source

- Runtime commit: `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`
- Runtime tree: `d82f37052847949e77c12e1704c3f27c6dd56a46`
- Compared with base: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- Changed paths only:
  - `runtime_protocol/timeline_commit.py`
  - `runtime_protocol/timeline_commit_port.py`
  - `tests/test_timeline_raw_capture.py`

No OpenAPI/schema/generated-client/endpoint/table/artifact change is included.
`contract/artifacts.json` remains 76 entries with SHA-256
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` on both
base and candidate.

## Existing carrier and method

The carrier is the existing `dto.MediaManifestEntry`, exactly:

```json
{"media_id": "sha256:<64 lowercase hex>",
 "content_digest": "sha256:<same digest>"}
```

The private Runtime method is:

```python
raw_media_info(pin: dto.MediaManifestEntry) -> MediaInfo
```

`MediaInfo` is an internal `TypedDict`, not a wire type:

```python
{
    "object_id": Digest,
    "media_type": str,
    "size": int,
    # existing optional intrinsic fields only:
    "duration_seconds": float,
    "width": int,
    "height": int,
}
```

The method is distinct from base-closure `media_info` and managed five-field
`selected_media`. It is request-scoped and private; it is not an HTTP or
generated-client operation. Runtime joins the object to this request's
project-managed object relation, opens one CAS descriptor, verifies regular
file identity, size, full SHA-256, and stable descriptor identity, and returns
stored MIME plus size. No caller metadata, catalog lookup, public object read,
or fallback to another media method is authorized.

## Declaration and transaction requirements

Agent must call the method only for the exact pin declared in the command
object. A pin appearing only in a candidate manifest is insufficient; the
Runtime port checks the request's existing declared-command set and fails
closed otherwise. The captured pin must then appear exactly in the candidate
dependency manifest. Only captured raw media is added to the existing
authorized-media set; unrelated manifest media remains refused.

The capture result is memoized only for the request. Acceptance keeps the
existing ledger replay first. For a new request, the existing transaction
revalidates the captured descriptor and identity before `_persist_closure`,
publication, projection, or input persistence. A missing/unowned/foreign
object, CAS tamper, changed pin/result, or manifest mismatch refuses without
writes. Existing base-only `media_info`, `selected_media`, and direct legacy
timeline-reference refusal behavior remain unchanged.

This carrier approval does not qualify Agent's command, the original strict
unplaced timeline-reference positive, placement, generation, public adoption,
freeze, or release.

## Focused evidence

Producer source-tree runs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_raw_capture.py
6 passed in 17.49s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_commit_port.py tests/test_timeline_media_selection.py
48 passed in 4.29s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_commit_acceptance.py
59 passed, 1 deselected in 5.86s
```

Independent archive-of-commit run:

```text
... tests/test_timeline_raw_capture.py tests/test_timeline_commit_port.py tests/test_timeline_media_selection.py tests/test_timeline_commit_acceptance.py
113 passed, 1 deselected in 10.73s
```

Also passed: `scripts/artifact_manifest.py --check`, `git diff --check`, and
the 76-entry unchanged artifact identity check. No full/browser/renderer/live
socket/integration/generated-client/schema-generation/pin/release suite ran.

## Agent request

Please ACK this exact committed Runtime source and provide the smallest closed
Agent reference-recipe source that declares the same existing pin, records its
dependency, and preserves the unplaced/reference-only boundary. Do not freeze
or generate an artifact, adopt publicly, or claim the original strict positive
until the reciprocal Agent/Runtime pair is qualified.
