---
name: music
description: Analyze imported music alignment, used-span EBU R128 loudness, and beat grids for timeline editing.
---

# Music

Use `music.align` for a MIDI transcription against its recording or to find where a passage in one arrangement occurs in another. `offset_s` means **target time minus reference time**; for a `ref_s` anchor, the matching target time is `ref_s * tempo_ratio + offset_s`. The score is a normalized feature similarity and the baseline is the same measurement after shuffling reference frames. Inspect the match by ear before editing a timeline.

Use `music.level` on each clip's actual source span (`from_s`, `to_s`). Its `gain_db` is `target_lufs - integrated_lufs`; it does not alter audio. Short or silent spans cannot produce a meaningful gated loudness and fail clearly.

Use `music.beats` for imported audio. `beats.json` has the `chiptune.compose` timing keys: `bpm`, `beats`, `downbeats`, `bars` (four-bar phrase starts), and `sections: []`. Times are source seconds. Accent-based downbeat phase is a heuristic; verify the phase against the arrangement before snapping edits. Attach the output with `timelines edit --clip X --beats run:<id>/beats`.

All three actions are local, require ffmpeg and numpy, and write a result manifest. Invoke with the Astrid SDK using `kind="action"`; pass source media handles or paths as file inputs.
