# Stereo terminal capability audit

## Scope and verdict

This is a read-only audit of one future standalone tab-audio capability run.
The reviewed source is App commit
`6323b5bd6fdfc1bb680eba6f8a1a46f21acf6adb`, tree
`132ed7f49cc42398676c3d32f80d445ca106e9be`, on the rehydrated clean
worktree `/home/user/work/wt/vw-m3-stereo-owned-state-guard-fix`.

**Offline source verdict: READY for one manager-controlled central attempt,
subject to a fresh manager `--prepare` fingerprint and grant.** No central
terminal ID had been issued at the time of this report, so no capture result
or backend-support verdict is claimed here.

## Controller and run-mode audit

- `RUN_MODE` is the literal `stereo`; `TAB_AUDIO_RUN_MODE` is required by
  `assertRunMode()` and is forced to `stereo` by the shell launcher.
- The Playwright config calls `assertRunMode()` before loading the config and
  passes the run mode through the isolated environment. A non-stereo caller
  is refused.
- `sourceFingerprint()` includes `runMode`; `assertGrant()` requires the
  grant, fingerprint, final SHA, source/tree hashes, package graph, private
  graph, discovery result, Node identity, Chrome tree, and Remotion/Player
  hashes to match. The controller also requires a clean committed source.
- The launcher uses one pinned Node `v20.19.4` executable with the admitted
  full SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`, the
  private12 graph, Chrome155, one-test discovery, the shared flock, a fresh
  direct `/tmp/timeline-tab-audio-*` task directory, and source pre/post
  checks. The manager must still run the literal post-commit `--prepare` on
  the rehydrated worktree before granting.

## Probe audit

- `getDisplayMedia({video: true, audio: true, preferCurrentTab: true})` is
  used after the real button click.
- The probe snapshots each captured track's `getSettings()` and
  `getCapabilities()` immediately after stream acquisition, before the warm
  interaction and before playback starts. Those objects are retained in the
  outcome attachment.
- There is one `MediaRecorder` with native `video/webm;codecs=vp8,opus`.
  Recorder chunks are retained in delivery order; native stream PTS are read
  with `ffprobe`, and both video and audio require nonempty, monotonic packet
  sets and native time bases.
- The audio stream's native `ffprobe` `channels` value is checked for exactly
  `2` before `readDecodedAudio()` is called. A mono result is an unsupported
  stereo diagnostic, not downmixed or upmixed evidence.
- Decoded interleaved samples are then checked with independent 1760 Hz left
  and 1980 Hz right tones. Expected-channel amplitude, cross-channel leakage,
  and swapped/mono negative controls are handled by `assertStereoTones()`.
  The existing 880 Hz WebAudio and 1320 Hz HTML-audio tone-presence checks
  remain intact.
- No primer, keepalive, mute reset, OS audio setting, PulseAudio attempt,
  waveform replacement, resampling, normalization, phase/amplitude claim,
  or per-clip alignment is introduced. The existing tab backend is attempted
  first; unsupported output must remain a literal failure with its settings.

## Historical boundary

The retained old 80,477-byte WebM (`f35483bab8f4992489ccd617ca4c2375599dc9337f1fbc7b37c2e3d0820eb6c8`)
is an Opus **mono** capture from source `2b388e769d9e153122e43b16b5d21e6e1ddf5b71`.
It proves only presence of the 880/1320 Hz tones and native video/audio PTS.
It is not stereo evidence and must remain a historical tone-presence PASS.
The prior `1020124802-7076` socket-path startup failure remains a failure
before recording, not an unsupported-backend or Player regression claim.

This diagnostic is limited to standalone native tab capture capability. It
does not claim Player/export parity, Composition parity, Gate 6 completion,
or product behavior.

## Evidence and pending terminal

Prior exact-source offline evidence (from the corrected post-commit review):

- Node syntax, shell syntax, three controller/analysis/environment Node test
  modules: passed.
- Playwright `--list`: one test collected, no browser launched.
- Source guards, private12 graph, all 77 Composition files, six peer hashes,
  Node full hash, Chrome155 full tree, flock/resource/temp/one-shot logic:
  reviewed offline.
- No grant, browser, capture, render, network, install, live socket, or full
  suite was run by this audit.

At report time the manager had rehydrated the exact clean source, but no
fresh `--prepare` result, grant, or central test request/terminal ID was
visible. The manager must publish those before this report can be amended to
an actual result; do not reuse an old grant, marker, source path, or terminal.

