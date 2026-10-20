# Runtime raw-audio single-descriptor fix

## Result

The independent reject finding is fixed on the worker source based at
`89fb7dcd113023d7e1e044d537202caca509830a`. `MediaReads.media_info` now opens
the managed CAS object once, verifies that open descriptor with the existing
bounded `_verify_open_file` helper, rewinds that same descriptor for
`wave.open`, and verifies the same descriptor again after parsing. The second
verification keeps parsed metadata from escaping after an in-place mutation.

The post-parse check intentionally reuses the existing helper instead of
comparing the first and last ctime directly: on Linux, an atomic pathname
rename changes the old inode's ctime even though its open descriptor and bytes
remain authoritative. The path-replacement race therefore parses the original
one-second WAV, while an in-place two-second replacement fails the size/hash
verification before returning metadata. Hashing remains chunked and bounded;
no whole-file buffer, decoder, ffprobe, public DTO, endpoint, or ABI change was
added.

The request-scoped `__media_info` memo, acceptance consumed-read recheck, and
accepted-retry ledger-first ordering are unchanged.

## Regression

`tests/test_timeline_raw_audio_port.py::test_raw_media_info_uses_verified_descriptor_under_storage_race`
deterministically injects the reviewer race immediately after the first
descriptor verification. Its `rename` case swaps a two-second WAV into the
CAS pathname and proves the result remains one second from the original open
descriptor. Its `inplace` case overwrites the same pathname/inode and proves
the read refuses with a CAS size/hash conflict.

## Evidence

- `PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py` — **7 passed**.
- `PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_port.py tests/test_timeline_raw_audio_port.py` — passed.
- `PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py` — **71 passed** (the pre-existing 69 plus the two race parameters).
- `git diff --check` — passed.
- No full, browser, live-socket, or central suite was run.

## Exact paired Agent handoff

Do not send or activate this handoff until the harness has committed the
worker source. The private Runtime operation remains:

```text
RequestCommitPort.media_info(pin: {
  "media_id": "sha256:<64 lowercase hex>",
  "content_digest": "sha256:<same digest>"
}) -> {
  "object_id": "sha256:<same digest>",
  "media_type": <managed object media type>,
  "size": <catalog byte size>,
  "duration_seconds": <finite positive WAV-header duration, omitted when unsupported>
}
```

The Agent adapter must call this only for an exact base-closure `MediaPin` and
must preserve visible refusal when the private port is unavailable or metadata
is unsupported. No public contract/version or generated artifact changes are
part of this fix. Native legacy-trim qualification remains open until the
actual committed Runtime/Agent pair is exercised.
