# Agent M2 native audio/media-preserve report

## Result

Implemented the private successor changes on top of frozen Agent `310e5484`.
No schema, DTO, endpoint, opcode, registry-row shape, compiler, DSP, or Runtime
worktree changes were made. The proposal-cut API was not imported.

Native `clip.add-media` and `occurrence.add-media` now admit Runtime-verified
`audio/*` selections, preserve the existing five-field `MediaSelection`, require
an active explicit audio track, validate the normal source window against
`VerifiedMedia.duration_seconds`, and create the existing registry binding with
`type: audio`. Image/video paths and their existing source-window/hold guards
remain unchanged. Audio rows may use the existing `clipType: media` carrier.

Native `clip.trim` now accepts literal `clipType: audio` and requires an active
audio track plus an audio registry asset. If the existing registry `duration`
is absent, the deterministic recorder can use only an exact matching
`ctx.verified_media` selection and its positive server-provided
`duration_seconds`; the exact verified carrier is recorded in `trim.source`, so
replay and inverse remain guarded. No registry duration is written.

## Main behavior and source comparison

Main’s actual implementation is `astrid/sdk/timeline/model.py:424-468`:

* `Clip.trim` accepts an audio clip (`self.is_audio`) or a media clip.
* `_source_duration` first reads authored registry `duration`, then asks the
  existing media store for duration; it refuses when neither is authoritative.
* It preserves raw integer endpoints for exact range checks, then delegates the
  established `trim_source_interval` rounding/hold behavior.

The native implementation previously accepted only `clipType: media` and only
`registry.duration`. This patch preserves the Main endpoint/range behavior and
rounding helper, adding the verified-media fallback only for missing duration.
The voiceover producer’s authored rows in
`astrid/packs/video_editing/shared/draft_voiceover.py` use an audio track,
`clipType: media`, asset alias, and literal `from`/`to`; no producer/proposal
API was changed.

## Capture and contract

The existing `_media_inputs._verified` path remains the sole admission point:
it accepts image/video/audio MIME families, positive size, and positive video or
audio duration. `_clip` selects `visual` for image/video and `audio` for audio;
the source window must equal authored hold and fit the verified duration. The
existing `_registry` binding and dependency machinery are reused.

`MediaSelection` remains exactly the existing five fields. No caller-provided
duration, file probe, guessed media length, audio-as-video coercion, epsilon,
clamp, or arbitrary registry write was added. `capture_clip_trim` gained only a
non-wire `verified_media` argument so deterministic capture can exercise the
same server-carried metadata as execution.

## Runtime peer ACK / exact-carrier boundary

The current Runtime `timeline_commit_port.py:selected_media` implementation
only returns metadata for a selection already declared by the request. Current
`clip.trim` has no media-selection field, and the historical imported audio
registry row has no complete declared selection tuple. The public S2 literal
journey and Runtime reports likewise leave that original audio positive open.

Therefore this Agent patch does not invent a trim carrier or silently call
`selected_media` for an undeclared selection. Historical audio trim is positive
when an exact retained/verified media carrier is already present; the real
provider path for an old unregistered audio row remains OPEN until Runtime
supplies the agreed small exact carrier. Changed/missing/wrong verified input,
kind, track, source window, and range fail before writes.

## Tests

Focused command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_commit_runtime_parent_media.py tests/editing_conformance/test_commit_runtime_occurrence_media.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_m2_clip_trim.py tests/sdk/test_timeline_clip_trim_provider.py
```

Result: `275 passed, 84 deselected`.

Lint command:

```text
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_media_inputs.py astrid/sdk/timeline/_trim_commands.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_recipe_m2_clip_trim.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py
```

Result: `All checks passed!`

No full or HTTP/browser suite was run. Real tiny-WAV CAS/provider acceptance
and the historical imported-audio positive remain unverified/open pending the
Runtime exact-carrier decision.
