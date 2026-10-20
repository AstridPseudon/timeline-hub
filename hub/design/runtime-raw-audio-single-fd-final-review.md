# Runtime raw-audio single-fd final review

## Decision

**REJECT** for merge.

Reviewed candidate `89fb7dcd113023d7e1e044d537202caca509830a` with tree
`0a7fb190b3b393fe2fb9527ec3ddb6749f43f8ba` (`tl/rt-m2-raw-audio-single-fd-fix`).

The candidate does not contain the single-descriptor fix described by
`runtime-raw-audio-single-fd-fix.md`. Its only commit after the independent
reject (`89fb7dc`) deletes `design/runtime-raw-audio-port.md`; it makes no
Runtime code or regression-test changes. `MediaReads.media_info` still calls
`_verify_child_object_bytes` at `runtime_protocol/timeline_commit_port.py:892`
and then reopens the CAS pathname at `:895` before parsing WAV metadata.

## Merge-blocking finding

The verified descriptor is not the descriptor used for capture. The first
helper opens, hashes, fstats, and closes one file descriptor. The subsequent
`self.cas.open(bare)` resolves the pathname again, so an atomic pathname swap
between those operations allows WAV metadata from bytes that were never
hashed. There is also no post-parse verification in `media_info`.

I independently reproduced this against the exact candidate tree: a hook
replaced the CAS pathname with a two-second WAV immediately after
`_verify_child_object_bytes` returned, before the later `cas.open`. The
candidate returned `duration_seconds: 2.0` while the originally verified WAV
was one second. This is the rejected read-TOCTOU, not a hypothetical race.

The required implementation must open once, verify/hash/fstat that descriptor,
rewind and parse that same descriptor, then retain the post-parse verification
needed to detect in-place mutation. Atomic pathname replacement must continue
to read the already-open original inode; in-place mutation must refuse. The
acceptance consumed-read recheck must remain in place.

## What passed

- `git diff --stat ab4c26d12f1f71e3540d3e118fdff7771bd2c73d 89fb7dcd113023d7e1e044d537202caca509830a` — only the old design document was deleted; no fix source/test was added.
- Target snapshot focused regression: `PYTHONPATH="$TARGET:$TARGET/tests" /home/user/work/venv-runtime/bin/python -m pytest -q "$TARGET/tests/test_timeline_raw_audio_port.py"` — **5 passed**. These cover base-closure authority, project ownership, unsupported WAV omission, acceptance tamper recheck, and ledger-first accepted retry, but not the claimed descriptor race.
- Direct target-tree atomic-replacement probe — **reproduced the vulnerability** as described above.
- The candidate feature remains private: no public route, generated client, schema/manifest, optional manifest, ABI version, or other public artifact changed. No inline duration/table/endpoints were added. The stray `design/runtime-raw-audio-port.md` report is absent from the candidate tree.

## Limitations and next steps

No full, broad, browser, live-socket, or central suite was run, per the brief.
The native legacy trim actual Agent/Runtime pair remains **OPEN** and is not
qualified by this Runtime-only review. Do not activate the Agent handoff pin
protocol or merge this candidate until the source actually implements the
single-open-descriptor path, adds the rename and in-place mutation regression
parameters, and reruns the focused Runtime evidence.

The matching Agent handoff pin protocol remains private and unchanged:

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

The Agent must call it only for an exact base-closure `MediaPin`, preserve
visible refusal when the private method is unavailable or metadata is
unsupported, and never forward or persist a caller duration. No public
contract or ABI change is approved by this review.
