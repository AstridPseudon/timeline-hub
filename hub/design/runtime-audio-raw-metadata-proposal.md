# Runtime legacy-audio raw metadata proposal

Status: **proposal only; no Runtime or Agent product change has been made**
(2026-10-20). This answers Agent's 15:19 request and supersedes the earlier
assumption that a persisted intrinsic-metadata record is required.

## Boundary agreed with Agent

The historical music object is authoritative through the existing closure:

1. the raw `MediaPin` (`media_id`/`content_digest`);
2. its `project_objects(project_id, digest, relation='managed')` association; and
3. the immutable CAS bytes, checked against the object size and SHA-256 digest.

It has no generation, variant, or catalog-duration identity. The existing
five-field `MediaSelection` remains reserved for the managed
generation/variant/object path. No caller may forge one for this object.

The proposed carrier is therefore the **existing two-field media pin**, with a
request-scoped Runtime read that derives metadata from those exact bytes. There
is no new intrinsic-metadata row, generation adoption, registry duration,
`.config`, inline client claim, journal, table, or public endpoint/DTO.

## Small protocol and result

Add one internal method to the already-authorized `RequestCommitPort`:

```text
media_info(pin: {
  media_id: "sha256:<64 lowercase hex>",
  content_digest: "sha256:<64 lowercase hex>"
}) -> {
  object_id: "sha256:<64 lowercase hex>",
  media_type: string,
  size: integer,
  duration_seconds?: finite positive number,
  width?: positive integer,
  height?: positive integer
}
```

This is an internal port result, not a generated `VerifiedMedia` DTO. It uses
the existing verified-media meanings for `media_type`, `size`, duration, and
dimensions, but deliberately has no `selection`: a raw object has no valid
five-field selection. Unknown optional values are omitted, matching Main's
`media_seconds(...) -> None` behavior. A malformed pin, unauthorized object,
missing bytes, size mismatch, or digest mismatch is an error; an authorized
object whose supported metadata is unavailable returns the descriptor with the
optional metadata absent, so the existing trim validator refuses it as
“cannot read the source file's duration.”

The read is request-scoped and has no idempotency key or durable result. The
port may memoize the exact `(pin, result)` only until the request closes.

## Authorization and exact byte proof

`RequestCommitPort.media_info` must refuse unless all of the following hold:

* the pin is an exact media entry in an observed **base revision closure**;
  candidate-only or arbitrary digest claims are not eligible;
* both pin fields are equal and canonical; the project and Runtime realm match;
* the object row exists and the project association is `managed`; and
* the existing CAS open/verification path confirms the recorded size and hashes
  the bytes to the pinned digest.

The read then inspects those verified bytes while the request owns the existing
read/authority boundary. It does not read a mutable registry or a latest
catalog child. The existing accepted closure continues to retain the same media
pin and CAS object; no new retention mechanism is needed.

## Source of computation and supported unknown semantics

Main's current source is `astrid/sdk/timeline/store.py:447-485`:

* `Clip._source_duration` uses authored registry `duration` first;
* otherwise `media_seconds` reads the exact object bytes;
* WAV-like input is inspected with Python's `wave.open` and
  `getnframes() / getframerate()`; and
* read/probe failure becomes unknown (`None`), after which trim refuses.

For this bounded legacy carrier, Runtime should use only that deterministic
WAV-header branch: `wave.open` over the verified CAS bytes, with a positive,
finite `nframes / framerate` result. `wave.Error`, `EOFError`, zero/invalid
framerate, non-finite output, and unsupported/non-WAV audio produce an omitted
`duration_seconds`. Audio dimensions remain absent. This is metadata
inspection, not decoding, scene evaluation, or rendering, and introduces no
launcher, ffprobe invocation, or external dependency into save.

The normal CLI/SDK object/media-info preflight remains unchanged:
`client.media.show` reads the existing object descriptor and Main's
`media_seconds` may use its existing WAV-header path and, outside Runtime save,
its existing ffprobe fallback. That preflight is useful for an early
user-facing refusal but is never authority and never forwards a duration in
the commit request; it does not become a new public endpoint or DTO.

## Capture, acceptance, and replay

1. **Capture.** Agent resolves the legacy asset to the existing media pin in
   the base closure. It calls the internal `media_info` read through the
   provider context. The command records the existing exact `media`
   dependency (`trim.source`, `policy: exact`) and the existing read shape,
   for example:

   ```json
   {
     "ref": "media:sha256:<digest>",
     "path": ["duration_seconds"],
     "state": {"state": "present", "value": 1.0}
   }
   ```

   An unknown duration uses the existing `state: absent`. The duration is not
   written into the registry or canonical document. Trim preserves Main's
   source `from`/`to`, finite endpoint checks, speed, source-time hold, and
   existing quantization. No duration is guessed from the registry or clip
   length.

2. **Acceptance.** Before provider acceptance completes, the port re-reads the
   same pin through `media_info` and compares the result with the captured
   request-scoped value. Any changed/missing/unowned object, changed bytes, or
   changed supported metadata refuses atomically before document writes. The
   existing manifest validator independently rechecks every retained media
   digest and size.

3. **Replay and inverse.** A deterministic provider replay uses the recorded
   exact media pin and obtains the same request-scoped read; it never trusts a
   caller-supplied duration. An accepted exact retry after restart uses the
   existing command ledger/closure replay; the retained media manifest and
   existing closure verifier remain the byte-retention proof. Guarded inverse
   and redo reuse the existing recorded source pin and source-range guards; no
   new journal or metadata record is introduced.

## Required implementation seam after approval

Agent needs one private provider-context adapter that exposes the Runtime port
read and one capture/replay assertion for the existing `trim.source` media
dependency. Runtime needs one `RequestCommitPort.media_info` implementation
and request-scoped capture/recheck wiring in the existing provider acceptance
path. Neither side needs a public client method, OpenAPI operation, generated
type, generation/variant lookup, or schema DTO change.

## Precise manager decision still required

The substantive proposal is settled, but implementation should wait for an
explicit Agent/Runtime-manager ACK on this one boundary:

* approve the private `media_info(existing MediaPin)` port method and the
  internal descriptor-plus-optional-VerifiedMedia-fields result above;
* approve WAV-header-only computation in Runtime save, with non-WAV/invalid
  metadata remaining unknown/refused rather than invoking ffprobe; and
* confirm that the provider-port compatibility/release manifest can carry this
  internal method without a public schema/artifact release. If that manifest
  hashes method shape, the manager must name the one private ABI revision; no
  public DTO or generated-client release is justified.

Until that ACK, the historical music-trim positive remains an open strict
expectation. No test is converted to a refusal.

## Evidence

The existing decisive raw-WAV witness remains the normal-ingest probe recorded
in `design/runtime-legacy-audio-metadata-carrier.md`: a valid 8 kHz mono
16-bit PCM WAV with 8,000 frames retained byte-for-byte, passed
`object_location(...)["verified"]`, and produced zero generations/variants.
Its object/location reads exposed no duration, which is exactly why the
request-scoped byte-derived read is needed. No broad suite, matrix, or new
fixture is required for this proposal.
