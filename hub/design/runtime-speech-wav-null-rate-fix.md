# Runtime speech WAV null/rate fix

Date: 2026-10-20 UTC

## Source and scope

- Worker branch: `tl/rt-m2-speech-wav-null-rate-fix`
- Base: `25c0da16dacd78b0b453653dd05ba6a172ff5e9c`
- Review source: `ORCH/design/runtime-speech615-intrinsics-review.md`
- Final targeted-test source tree: `de34d64765611dd2baa09ff3533c448f11cab702`

This addresses only the two independent REJECT615 findings. The existing
normal speech WAV, invalid-WAV, explicit-value, exact-replay, and authenticated
HTTP-selected-read behavior remains in place.

## Changes

- `runtime_protocol/service.py:7427-7679,7133-7138` derives a transient map
  keyed by the existing output identity. It records raw
  `duration_seconds` presence/value, including explicit `null`, while keeping
  the established normalized settlement result unchanged. The map is passed
  only to settlement enrichment and is never stored or sent on the wire.
- `runtime_protocol/store.py:4777,4870-4893,5509-5586` uses that transient
  value only when the normalized output metadata key is absent. Explicit null
  therefore remains null and selection refuses it; absent duration may still
  be filled from a verified WAV header. No variant-append path was changed.
- `runtime_protocol/cas.py:136-152` treats zero or negative WAV rates as
  unknown and catches division-by-zero while retaining the existing single
  verified open-FD/hash/fstat inspection and no-full-buffer parser change.
- Added focused regressions in
  `tests/test_generation_publish_v1_settlement.py:592-664` for explicit-null
  duration and zero-rate WAVs. The null test also asserts no wire presence
  flag is emitted.

No API, DTO, schema, table, receipt, catalog digest, canonical timeline write,
ffprobe, or regeneration behavior was added or changed.

## Evidence

Central targeted run on the final source tree:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_worker_security_settlement.py \
  tests/test_timeline_verified_media_http.py
29 passed in 11.24s
```

Direct non-socket focused run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_generation_publish_v1_settlement.py \
  -k 'speech_settlement and not authenticated_http'
5 passed, 10 deselected in 0.90s
```

The broader direct command reached `21 passed, 1 deselected, 2 failed`; both
failures were pre-existing sandbox inability to open localhost sockets in
`tests/test_worker_security_settlement.py`. The central targeted run above,
which runs outside that sandbox, passed those tests and the HTTP test. `git
diff --check` passed. No full suite was requested or run.

## Conditions and next steps

The Agent 16:43 ACK conditions remain separate: this is normal Runtime
`generation.generate_speech` settlement proof only. It does not claim the
actual outer voiceover adapter/action or Agent voiceover qualification; that
adapter remains pending. No merge was performed. Recommended next step is
independent re-review of this final tree against REJECT615, followed by the
orchestrator's normal merge decision.
