# Runtime settled speech WAV intrinsics

Status: implementation candidate complete; peer proposal sent to Agent, dependent
voiceover/RIPPLE adoption remains held pending Agent ACK and the later native
positive.

## Bounded change

The existing `generation.publish_v1` settlement path now derives
`duration_seconds` only for a `generation.generate_speech` task's `audio/wav` or
`audio/x-wav` output when the generation metadata has no explicit duration. It
derives the value after CAS publication and before the existing variant row is
inserted, so the existing generation, variant, managed association, and
five-field media-selection path remain the carriers.

`ContentAddressedStore.wav_duration` reuses the existing opened-CAS verification
shape: one descriptor is hashed with stable `fstat` checks, rewound for
header-only `wave` inspection, and checked again for stable identity. It does
not buffer the file, decode it, call ffprobe, or create a new authority path.
Malformed, unsupported, empty, non-finite, or non-positive WAV duration remains
absent; selection consequently keeps its existing refusal. Explicit generation
duration metadata is not changed.

No command, schema, API, DTO, table, provenance format, canonical timeline
write, renderer, model call, or network path changed.

## Evidence

- Direct targeted generation/import/catalog/media-selection neighbors:
  `33 passed in 10.94s`.
- Direct settlement/CAS neighbors without sockets:
  `28 passed in 4.70s`.
- Central socket-dependent targeted suite for `tests/test_object_location.py`
  and `tests/test_streaming_media_io.py`: `61 passed in 12.90s` on final tree
  `4acc1ff65a3b5dddc5b0dc885a0a5449b9b9c287`.
- The valid speech fixture proves normal task settlement, receipt, exact CAS
  bytes, attempt-bound association, five-field selection, verified `1.0`
  second duration, and unchanged canonical timeline row counts.
- The invalid-byte control proves the variant has no duration and selection
  raises the existing `invalid selected media metadata` refusal.
- Explicit-duration coverage proves a valid WAV does not replace the existing
  `2.5` second metadata.

No full suite was requested. The Agent inbox proposal was sent before the
implementation; no objection was present when implementation and tests
completed. The requested `design/runtime-speech-wav-intrinsics.md` did not
exist before this candidate and was created as this implementation report.
