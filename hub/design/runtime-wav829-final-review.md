# Runtime WAV 829 final review

Date: 2026-10-20 UTC

## Decision

**APPROVE** `8292b94dc463e28808cd57e20a6aa372d474837b` against base
`e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`, with the candidate's direct
lineage `615a95a63c2ae79c6a47400ffc79a72dedd0bc5f` ->
`25c0da16dacd78b0b453653dd05ba6a172ff5e9c` -> `8292b94` reviewed exactly.

No blocking findings remain. The assigned review worktree stayed read-only at
`e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`; no source or shared dependency
files were changed.

## Exact source and diff

Candidate commit: `8292b94dc463e28808cd57e20a6aa372d474837b`

Candidate parent: `25c0da16dacd78b0b453653dd05ba6a172ff5e9c`

Binary patch SHA-256 for `8292b94^..8292b94`:
`dd15a3ec1b940fe1b8d473fb5f748e1c739dcf560a9e2a25b6d59f997b42fb45`

Changed files are exactly:

- `runtime_protocol/cas.py`
- `runtime_protocol/service.py`
- `runtime_protocol/store.py`
- `tests/test_generation_publish_v1_settlement.py`

The product diff is limited to the existing normal `generation.publish_v1`
settlement path. `runtime_protocol/service.py:7044-7046` still returns an
exact accepted replay before lease validation, staging, CAS access, or
enrichment. The transient raw output-presence map is collected at
`service.py:7427,7647-7653`, passed privately at `service.py:7133-7136`, and
is not placed in the task result, receipt, event, variant metadata, or
catalog. `store.py:4870-4884` applies it only when the stored variant key is
absent, preserving explicit output NULL and explicit values; generation-level
explicit metadata remains governed by the existing `explicit_duration` policy
at `store.py:4809-4812`.

`cas.py:123-150` retains one opened descriptor for hash/size/stat verification
and WAV header inspection, rejects non-positive rates as unknown, and catches
the zero-rate division boundary. No ffprobe, full-buffer copy, new API/DTO,
schema/table, receipt/catalog rewrite, canonical timeline write, variant
append change, or regeneration claim is present.

## Findings

The two independent REJECT findings from
`runtime-speech615-intrinsics-review.md` are fixed:

1. Explicit output `duration_seconds: null` is retained as transient presence
   and stored as NULL in the existing variant metadata, so header derivation
   does not replace it and media selection keeps refusing unknown duration.
2. A structurally readable WAV with zero or negative sample rate settles with
   unknown duration instead of aborting with `ZeroDivisionError`; selection
   retains the existing refusal.

No new finding was found in the exact diff. Existing valid-WAV, invalid-WAV,
explicit-value, authenticated HTTP-selected-read, and replay behavior remains
covered. `generation.variant.append` and regeneration behavior are outside
this change and make no claim here.

## Evidence

Central targeted service result on the exact candidate source tree
(`de34d64765`):

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_worker_security_settlement.py \
  tests/test_timeline_verified_media_http.py
29 passed in 11.24s
```

Independent focused run from an isolated export of exact commit `8292b94`
(socket case intentionally excluded because the central service owns socket
tests):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/wav829-review.tvaNLl \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  /tmp/wav829-review.tvaNLl/tests/test_generation_publish_v1_settlement.py \
  -k 'speech_settlement and not authenticated_http'
5 passed, 10 deselected in 2.07s
```

Independent exact-replay boundary probe from the same export passed while
`ContentAddressedStore.open` was replaced with a failing function for the
retry: the second identical accepted settlement returned the stored result
without any CAS open.

`git diff --check 25c0da1..8292b94` passed. No full or broad suite was
requested or run. The central 29-test result is the authoritative evidence for
the HTTP/socket neighbors; the local direct HTTP attempt was not used because
the sandbox disallows localhost sockets.
