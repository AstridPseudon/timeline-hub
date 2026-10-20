> REVIEW HOLD 2026-10-20T16:05:47Z: candidate ab4c REJECTED read-TOCTOU; rt-m2-raw-audio-single-fd-fix active. No merge/native trim qualification. See runtime-raw-audio-port-final-review.md.

# Runtime raw-audio port

Implemented the Runtime-side candidate from `runtime-audio-raw-metadata-proposal.md`
after the Runtime manager's 2026-10-20 ACK and the Agent inbox confirmation.

## Private method

`RequestCommitPort.media_info(pin)` accepts only the existing two-field
`MediaPin`:

```text
{
  "media_id": "sha256:<64 lowercase hex>",
  "content_digest": "sha256:<64 lowercase hex>"
}
```

It returns the internal descriptor:

```text
{
  "object_id": "sha256:<64 lowercase hex>",
  "media_type": string,
  "size": integer,
  "duration_seconds"?: finite positive number
}
```

The pin must be an exact entry in the observed request base revision's media
closure. Runtime then requires the same-project `managed` association and
verifies the recorded size and SHA-256 against the immutable CAS object. The
result is memoized only for the request. Acceptance re-reads only memoized
`media_info` pins; accepted idempotent retries are resolved by the ledger before
the provider/port is constructed.

Duration is derived only with Python's WAV header reader over the verified CAS
object. Invalid, unsupported, zero/invalid-rate, or non-finite WAV metadata
returns a descriptor without `duration_seconds`. No decoder, ffprobe, renderer,
catalog duration, generation/variant adoption, table, public route, DTO, or
caller-supplied duration was added.

## Compatibility and Agent handoff

The existing Runtime provider ABI remains `astrid-v1`, interface version `1`,
with the existing public schema digest and generated clients unchanged. The
port method is a private optional seam; no port compatibility manifest or ABI
revision requires changing at this candidate. Agent's adapter should obtain the
exact pin from its base closure, call `media_info` during capture/replay, record
the existing exact `media` dependency plus the `duration_seconds` read, and
fail visibly if the optional method is unavailable. It must not forward or
persist a caller duration. The historical raw-audio trim positive remains open
until that paired Agent adapter is integrated.

## Evidence

Targeted command:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_timeline_raw_audio_port.py \
  tests/test_timeline_commit_port.py \
  tests/test_timeline_commit_contract.py
```

Result: **69 passed**. `git diff --check` and Python compilation of the changed
modules/tests also pass. No full or live/browser suite was run. The Agent
adapter and the paired historical trim proof remain unverified and open.

