# Runtime historical-audio fixture proposal

**Status:** ADVISORY PROPOSAL — bounded local test setup is authorized; no architecture decision is implied

**Date:** 2026-10-20 UTC

**Runtime base:** `285a3b437c69d20e2af281c3d7fdd212cb784d1a`

**Agent references inspected read-only:** `9bf503f98deb3051cb9caceeae3ea6a5ebd5f185` and `f97b2b87688abb20280572a5fc23e4f69ec9e3f8`

**Exact unapplied patch:** [`runtime-historical-audio-fixture-proposal.patch`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-historical-audio-fixture-proposal.patch)

## Decision boundary

The historical journey remains the original strict `xfail` until the peer-owned Agent capture support is ready. The local worker task authorizes this bounded test-environment setup repair; it is not a conversion of the archived fixture and does not require a new owner approval. The peer instruction forbids converting the archived fixture in place, so the setup does not repair or adopt the existing CAS object. It creates fresh genuine source bytes before capture through Runtime's existing Main object/bootstrap APIs.

No Agent file, Agent qualifying test, Runtime product code, or original journey assertion was changed. The patch is a review artifact only; it is not merged and the journey is not green.

## Evidence and diagnosis

The `music-documents` archive's historical audio pin is:

| Field | Existing value |
| --- | --- |
| CAS ID | `sha256:e29d6131553bfda749080174ccc5fb5f1be8eb27f2775323cb0293fcb6933a65` |
| Size | 19 bytes |
| Bytes | `b"synthetic-music-bed"` |
| Stored MIME | `audio/wav` |
| Authored registry | `{object_id: <CAS ID>, type: "audio"}`; no `duration` |
| Authored clip | `music-bed`, audio, `at: 0`, `hold: 5.5`, volume/fade preserved |

The bytes are not a WAV file. Agent 9bf's readonly raw-duration path therefore has no legitimate intrinsic duration to read, and a hold-based or authored-duration substitute would violate the settled constraints. Agent f97 supplies the CLI native preflight route but does not change that source fact.

## Proposed setup

The patch adds `tests/historical_audio_fixture.py` and changes only the `historical-audio` branch of `journey_film` in `tests/test_timeline_public_s2_mixed_cli_journey.py`. The test body, parameterization, strict `xfail`, guards, key, receipt, inverse, history, retention, and all assertions remain unchanged.

Before the journey captures `film`, the helper:

1. Generates one 6-second, mono, 8 kHz, 16-bit PCM WAV in memory. This covers the authored 5.5-second source window and the original trim range without inventing a duration field.
2. Calls `RuntimeService.ingest` on both existing Main bootstrap copies with `media_type="audio/wav"`, `original_name="music-bed.wav"`, and a setup idempotency key. The resulting CAS ID is taken from the ingest receipt; it is not hardcoded.
3. Creates a sibling `historical-audio-pcm` timeline in each copy and publishes a copy of the existing canonical parent composition through `create_timeline` and `publish_parent_composition`.
4. Replaces only the `music-bed` registry object's `object_id` and the matching dependency-manifest media ID. Existing immutable internal-timeline and shot records are reused exactly; clips, occurrences, track/audio/source fields, timing, opaque fields, transcript binding, and the original `film` timeline remain unchanged.
5. Captures the sibling timeline's receipt, head, and event baseline only after setup, then returns that prepared fixture to the unchanged journey body.

`RuntimeService.ingest` creates the normal raw object and managed project-object relation. The proposal does not call media import/generation, does not create variant or generation fields, does not add registry duration, and does not adopt the archived 19-byte object.

## Old/new input shape

| Shape | Existing historical input | Proposed setup input |
| --- | --- | --- |
| Source bytes | 19-byte `b"synthetic-music-bed"` marker | 96,044-byte RIFF/WAVE PCM: 44-byte header + 48,000 mono frames × 2 bytes |
| MIME/name | `audio/wav` / `music-bed.wav` | `audio/wav` / `music-bed.wav` |
| CAS identity | Fixed malformed digest above | `sha256:<digest of the generated WAV>`, returned by `ingest` |
| Registry asset | `object_id`, `type: audio`; no duration | Same fields; only `object_id` changes; no duration |
| Parent/clip | Existing `music-bed` clip, `at: 0`, `hold: 5.5`, volume/fade and all opaque fields | Same parent/clip fields and child closure; only the source CAS pin changes |
| Generation/variant | None | None |

The 96,044-byte size is deterministic for the proposed PCM parameters, but the digest is intentionally derived by Runtime from the bytes rather than embedded in the proposal.

## Diff proof and verification

The current worker worktree is clean. `git apply --check --verbose` against Runtime base reports:

```text
Checking patch tests/historical_audio_fixture.py...
Checking patch tests/test_timeline_public_s2_mixed_cli_journey.py...
Hunk #2 succeeded at 39 (offset 1 line).
```

The patch has exactly two target files: one new setup helper and one setup-branch import/call. It contains no Agent path, no Runtime product path, and no changes to the journey test body after fixture capture. The patch remains unapplied, so no Runtime or Agent test result is being represented as green.

## Tests and next step

No old journey was run unchanged, and no full or live-socket suite was requested. The only verification performed was the non-mutating patch applicability check above; the worktree remained clean and shared dependencies were untouched.

The bounded setup repair may be applied and locally read back with the targeted journey prerequisites, while the existing strict `xfail` remains until Agent 9bf/f97 support is paired. Do not fake hold duration, add metadata, override reads/schema/health, or alter the original assertions.
