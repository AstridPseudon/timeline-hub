# music.duck

`music.duck` analyzes a pinned snapshot of a currently published project
timeline and creates a ducked copy of its music bed. It does not edit or
publish the timeline. The command action is intentionally local: it receives
the selected music and voice media plus their placement metadata in one
Runtime-managed snapshot file and has no Runtime client or timeline access.

For normal use, call the caller-scoped `duck_timeline` SDK helper shown below.
It opens the current published checkout through the caller's connected
`AstridClient`, resolves managed media by digest, builds the snapshot, and
invokes `music.duck` as an action in the requested project. A detached draft is
not an input. The optional `clip` identifies one music clip; when omitted, the
helper accepts the timeline only when it has exactly one music clip. It
refuses an ambiguous bed, including multiple clips on the music track.
`voice_tracks` defaults to `["vo"]`. The analysis uses current timeline
placements and source spans, including each voice clip's placement, source
in-point, duration, speed, volume, and fades. The helper requires a
project-scoped client and timeline slug or ID, and passes those placements and
digest-verified media in the local action's required `snapshot` ZIP input. The
action itself accepts that snapshot plus the numeric controls below.

The declared controls are `bed_lu` (the target voice-minus-music loudness gap),
`cap_lu` (the minimum momentary voice-minus-music gap during voiced moments),
`slew_db_per_s` (maximum gain change rate), `smooth_s` (gain-curve smoothing
window), `floor_db` (maximum attenuation floor), and `merge_gap_s` (merge
nearby voice activity across gaps). Defaults are `bed_lu=8`, `cap_lu=4`,
`slew_db_per_s=2.0`, `smooth_s=1.0`, `floor_db=-12.0`, and `merge_gap_s=1.2`.
In particular, `cap_lu=4` caps the music level at `VO_I - 4 LU` for a 400 ms
moment; it does not mean “at most 4 dB of gain reduction.”

The analyzer evaluates voice energy per line, uses 400 ms K-weighted moments at
10 ms timeline steps, and derives a gain curve subject to the cap, floor, and
slew-rate limits. The slew limit is measured per timeline second; the
source-time control step scales with playback speed. It applies forward and
backward rate limiting, then a 1 s Hann smoothing window. The report records
requested and achieved ducking, including any overshoot caused by smoothing and
rate limits. Gain is authored in source clock and mapped through each clip's
playback speed onto the timeline.

Outputs are a WAV (`music.wav`), `duck.json`, and the universal
`manifest.json`. The managed output ports are `music` (primary WAV) and `duck`
(the analysis report); the manifest describes the run. The WAV retains the
source sample rate, channel count, integer PCM or IEEE float sample format, and
exact frame count. Its dither is deterministic, so repeating a run against the
same source and timeline evidence gives the same output bytes.

This is an analysis and media-generation action. Review the report and listen
to the result before deciding to replace a timeline clip. A replacement is a
separate, ordinary checkout edit and publish, shown in the pack guide. Refuse
`app.duck` metadata on music clips even when its value is an empty mapping;
ducking state is represented by the run report and provenance, not timeline
intent metadata.

## Connected SDK workflow

The caller must supply a project and connected client. In a task, use the task
project when available, otherwise the configured project slug. This one helper
call owns checkout, snapshot creation, action invocation, and waiting for
managed outputs:

```python
import os

from astrid.sdk import AstridClient
from astrid.packs.music.actions.duck.api import duck_timeline

project = os.environ.get("ASTRID_TASK_PROJECT") or os.environ.get("ASTRID_PROJECT_SLUG")
if not project:
    raise RuntimeError("set ASTRID_TASK_PROJECT or ASTRID_PROJECT_SLUG")

with AstridClient.open_from_launcher() as client:
    result = duck_timeline(client, project, "main-final", wait=True)
result.raise_for_error()
print(f"Review run {result.run_id} and its managed music/duck outputs before adoption.")
```

Supply `clip` when the timeline contains more than one music clip, and pass
`voice_tracks` or `DuckParameters` only when their defaults do not fit the
edit. Inspect the `duck` managed output before adopting `music`. For direct
`sdk.invoke("music.duck", kind="action", ...)` calls, supply the snapshot file
produced by the helper; the action has no timeline input or ambient Runtime
connection.

## Tagged reruns

When the selected timeline music contains a prior duck tag, the helper resolves
the original source by its content digest. It fails if that source object is
missing; it does not silently substitute the ducked file as a new source. The
helper still reads the current published timeline and remeasures current voice
placements, so changed voice timing is reflected in the new report and WAV.
Compare the new report with the tagged run before replacing media.
