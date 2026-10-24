---
name: music
description: Analyze imported music alignment, loudness and beat grids, and bake speech-keyed music ducking for timeline editing.
---

# Music

Use `music.align` for a MIDI transcription against its recording or to find where a passage in one arrangement occurs in another. `offset_s` means **target time minus reference time**; for a `ref_s` anchor, the matching target time is `ref_s * tempo_ratio + offset_s`. The score is a normalized feature similarity and the baseline is the same measurement after shuffling reference frames. Inspect the match by ear before editing a timeline.

Use `music.level` on each clip's actual source span (`from_s`, `to_s`). Its `gain_db` is `target_lufs - integrated_lufs`; it does not alter audio. Short or silent spans cannot produce a meaningful gated loudness and fail clearly.

Use `music.beats` for imported audio. `beats.json` has the `chiptune.compose` timing keys: `bpm`, `beats`, `downbeats`, `bars` (four-bar phrase starts), and `sections: []`. Times are source seconds. Accent-based downbeat phase is a heuristic; verify the phase against the arrangement before snapping edits. Attach the output with `timelines edit --clip X --beats run:<id>/beats`.

Use the caller-scoped `duck_timeline` helper to create a ducked music-bed WAV from one currently published timeline. The helper reads a pinned timeline checkout, resolves the music source by digest, packages selected source media and placements into a Runtime-managed snapshot, and invokes the local `music.duck` action. It refuses ambiguous music beds. The report shows line-by-line loudness, achieved gaps, slope and smoothing overshoot. The default `bed_lu=8` is the target voice-minus-music gap in LU; `cap_lu=4` caps music at `VO_I - 4 LU` for each voiced 400 ms moment. The approved launch-film mix informed these defaults: a 15 LU gap buried the music, and fast gain changes sounded like stark leaps. The 2 dB/s slew and 1 s Hann smoothing keep movements gradual; the -12 dB floor limits attenuation, and the 1.2 s merge holds ducking through natural speech gaps. See the [`music.duck` action guide](../actions/duck/STAGE.md) for the complete helper call, input contract, and output ports.

`music.duck` does not change the timeline. After reviewing and listening to the WAV, adopt it through the ordinary checkout and publish flow. The snippet below replaces only the selected clip's media reference. It checks that the authored placement and mix properties stayed the same; the generated WAV preserves source sample rate, channels, format, and frame count, so a whole-source music clip retains its duration.

```python
import copy

from astrid.sdk import AstridClient
from astrid.sdk.timeline_checkout import Checkout

with AstridClient.open_from_launcher(start_pack_host=False) as client:
    tl = Checkout.open("demo", "main-final", client=client)
    clip = tl.clip("music-bed-clip-id")
    if clip.track != "music":
        raise RuntimeError(f"expected music track, found {clip.track!r}")
    before = copy.deepcopy(clip.data)
    with tl.edit("replace music bed with reviewed ducked WAV", check=False, quiet=True):
        clip.swap_asset("run:DUCK_RUN_ID/music")
        replacement_asset = clip.data["asset"]
        # swap_asset can follow replacement-file duration. Restore the exact
        # authored clip record while retaining its newly registered media key.
        clip.data.clear()
        clip.data.update(before)
        clip.data["asset"] = replacement_asset
    check = tl.check()
    if not check.valid:
        raise RuntimeError("timeline check failed: " + "; ".join(check.problems))
    receipt = tl.publish("replace music bed with reviewed ducked WAV",
                         idempotency_key="music-duck-review-01", client=client)
```

Use the clip ID from the report/timeline inspection and the completed run ID.
`clip.swap_asset` is scoped to that clip. `tl.replace_asset(key, handle)`
repoints every clip sharing an asset key, so use it only when that broader
change is intended. Both replacement helpers can update the duration of a
whole-file audio clip if the new file length differs; the duck action's exact
frame-count preservation keeps the source duration aligned. Review the check
report and publication receipt as with any timeline edit.

Never change the clip's start, from, speed, fades or volume when adopting the
WAV. After a re-cut, call `duck_timeline` again on the published cut: the WAV's
RIFF LIST/INFO tag resolves the original source by digest and recalculates the
gain from current placements. Missing original media is an error.

`music.align`, `music.level`, and `music.beats` are local analyses that require
ffmpeg and numpy and write a result manifest. Invoke them with the Astrid SDK
using `kind="action"`; pass source media handles or paths as file inputs.
