# Agent raw-audio trim private adapter

This adapter preserves the historical `clip.trim` recipe for raw audio clips
whose registry asset intentionally has no authored duration. It is private
Runtime integration only; the command schema and public SDK surface remain
unchanged.

## Contract

For a raw audio trim, Agent identifies the exact existing base media pin from
the immutable dependency manifest. During Runtime commit it calls the optional
private `RequestCommitPort.media_info` port with that pin. The returned
request-scoped descriptor is checked for:

- the exact `object_id`;
- an audio `media_type`;
- a positive integer `size`; and
- a finite positive `duration_seconds`.

The descriptor is consumed only by the trim handler to establish source-time
defaults and bounds. It is not put in the command, an authoring DTO, a public
endpoint, durable timeline metadata, or a registry duration. Runtime remains
authoritative: it reloads the exact base closure, recomputes the descriptor,
and the Runtime port rechecks the pin and bytes before the command is
accepted.

Raw audio also requires an active audio track and an audio registry asset.
Hold, speed, half-open source intervals, and six-decimal boundaries continue
to use the existing trim implementation. Missing/unknown metadata, a foreign
descriptor, malformed WAV metadata, a changed CAS object, or an unavailable
port refuses before writes.

The authoring session has a nonauthoritative preflight convenience: it reads
the existing exact media bytes and derives a positive WAV-header duration so a
valid raw-audio trim can be queued. This claim is request-local and is never
trusted by Runtime; a failed or stale preflight remains a visible refusal.

## Pairing status

The Agent adapter is prepared against the peer-acknowledged proposal. The
Runtime counterpart is held until its worker commit is available, so this
worktree does not claim an end-to-end paired acceptance test. Pure Agent
conformance covers successful request-scoped metadata, absent/foreign/
malformed metadata, zero-write refusal, source-time hold, and inverse
preservation.
