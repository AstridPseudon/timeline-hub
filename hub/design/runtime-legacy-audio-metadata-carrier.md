# Runtime legacy raw-audio metadata carrier

Status: **bounded block; no Runtime product change made** (2026-10-20).

## Peer answer

There is no existing exact carrier that can turn the historical raw-audio CAS
object into `VerifiedMedia.duration_seconds` without introducing a generation /
variant tuple, adopting the object into the catalog, trusting client inline
metadata, or decoding the bytes during the commit path. I did not implement any
of those alternatives. The original historical music trim remains a positive
expectation and remains open, not an expected refusal.

## Existing closure traced

The smallest closure that exists for the historical object is:

1. `objects.digest/size/media_type/original_name/created_at`;
2. `project_objects(project_id, digest, relation='managed')`; and
3. the CAS bytes, verified by the normal ingest/object-location path.

`RuntimeService._ingest_transfer` (`runtime_protocol/service.py:4135-4203`)
publishes and hashes the bytes, records exactly that object descriptor, and adds
the managed project association. `RuntimeService.object` and
`object_location` (`service.py:4655-4728`) can read the descriptor and verify
the bytes/path. Neither read has intrinsic duration or dimensions.

The existing verified-media route is a different closure. `MediaReads.selected`
(`runtime_protocol/timeline_commit_port.py:733-835`) joins
`generations -> generation_variants -> objects -> project_objects`, requires a
completed generation/variant/object identity, validates the catalog digest, and
only then returns `duration_seconds`, `width`, or `height` from generation or
variant metadata. `RuntimeService.get_project_verified_media` is only a thin
read over that method (`service.py:2538-2541`), and
`RequestCommitPort.selected_media` additionally requires the exact five-field
selection to be declared (`timeline_commit_port.py:267-274`). A raw historical
object has no valid five-field selection. There is no `CommitPort.media_info`
or `MediaReads.media_info` implementation in this Runtime tree.

`RuntimeService.import_media` accepts an optional duration, but its normal
settlement deliberately creates the generation/variant catalog pair
(`service.py:4347-4458, 4496-4522`). That is explicitly outside this request;
it cannot be used as a hidden historical adoption path.

## Evidence

The direct normal-service probe used a freshly generated, valid mono PCM WAV:
8 kHz, 16-bit, 8,000 frames (1.0 seconds), and called only
`RuntimeService.ingest`, `object`, and `object_location`. It observed:

```text
object keys: created_at, digest, media_type, original_name, size
location keys: digest, filename, local_path, media_type, object_id, size, storage, verified
bytes_equal: True
verified: True
generations: 0
generation_variants: 0
```

The object was therefore retained and byte-authoritative, but no
`duration_seconds` was available to expose. This is a small raw-WAV control,
not a new fixture or a replacement for the historical film.

Main's corresponding fallback is also explicit: `Clip._source_duration`
(`astrid/sdk/timeline/model.py:424-431`) first uses registry `duration`, then
`astrid.sdk.timeline.store.media_seconds` (`store.py:499-538`), which reads
remote CAS bytes and WAV-decodes or ffprobes them. That is a client-side
fallback returning unknown on failure, not a Runtime intrinsic-metadata
authority. The commit path must not add a generic decoder or scene/save
dependency. Current Agent `clip.trim` also requires a positive registry source
duration (`astrid/sdk/timeline/_trim_commands.py:59-81`), explaining the
historical pre-POST refusal.

Focused Runtime evidence:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_media_selection.py tests/test_timeline_verified_media.py tests/test_imported_media_catalog.py
49 passed in 14.19s
```

The broader neighbour command also ran. It retained the same 101 passes, but
four `tests/test_streaming_media_io.py` daemon cases could not bind a local
socket in this sandbox (`PermissionError: [Errno 1] Operation not permitted`).
Those four are environment-blocked, not silently skipped.

## Bounded proposal, pending Agent agreement

Do not implement until Agent agrees on the source-side carrier and the Runtime
manager approves the required contract/release decision. If the owners decide
to support this historical shape, the smallest safe seam is:

- keep the existing raw `MediaPin`/object identity, managed project association,
  and CAS hash/size verification unchanged;
- add no generation, variant, adoption, guessed registry duration, `.config`,
  or inline client duration;
- establish an immutable Runtime-owned intrinsic metadata record for that exact
  object before capture (at minimum positive finite `duration_seconds` in
  seconds; optional positive integer dimensions only when known); and
- expose that record through a narrow existing-port read used by the provider,
  returning the same verified-media metadata semantics as the managed path.

The read must fail closed when the object association, bytes, MIME, size, or
metadata identity is absent or changed. `duration_seconds` is seconds; booleans
are invalid, unknown remains absent, and no coercion or decoder belongs in the
commit/save path. The provider must declare and record the exact object metadata
input and re-read it at acceptance/replay, while preserving the original
music trim guards, source range, speed, and inverse/retry behavior.

The current Runtime has no place to obtain that immutable intrinsic metadata
for a historical raw ingest, so this is a cross-contract decision rather than
missing method plumbing. The manager must choose the authoritative metadata
creation/retention operation and release shape with Agent before any product
implementation. Until then, the historical positive stays strict/open.

