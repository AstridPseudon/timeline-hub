# Gate 6 stereo prerequisite

This is a source-only handoff for the existing standalone tab probe. The
Composition worktree does not contain the App-owned probe files, so no App,
Agent, pin, compiler, DTO, dependency, or product file was changed here.

## Existing evidence

The retained capability artifact is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix/capability-1340-output/tab-audio-capture.probe.ts-8ea9e-rome155-MediaRecorder-clock-native-codec-chrome155-tab-audio/whole-tab.webm`

Its SHA-256 is `f35483bab8f4992489ccd6177f1fbc7b37c2e3d0820eb6c8` and its
audio stream is Opus, 48 kHz, `channels: 1`, `channel_layout: mono`.
The retained audio has monotonic native PTS and both 880/1320 Hz DFT peaks,
but that is not stereo evidence.

The standalone probe's current `readDecodedAudio` keeps ffmpeg's interleaved
output and does not pass `-ac 1`; however, its WAV fixture places the same
1320 Hz signal in both channels, and `assertTone` only proves a requested tone
is present in every decoded channel. The fifth Player helper's
`inspectTabCapture` checks one video/one audio stream and monotonic packet PTS;
it does not decode channel identity or claim stereo. No existing Gate 6 check
silently downmixes, but no existing check proves faithful stereo either.

## Portable patch

`stereo-mix-capability-prep.patch` is intended for the existing App-owned
files under `tests/e2e/timeline/` in the clean-install standalone probe. It:

- retains `assertTone`, the original mono-positive behavior, and the `.001`
  presence threshold;
- adds finite 1760 Hz left-only and 1980 Hz right-only source tones to the
  existing 48 kHz stereo WAV fixture;
- captures each track's real `getSettings()` and `getCapabilities()` beside
  its kind/readiness state;
- checks the encoded stream's actual channel count and interleaved decoded
  samples with an L/R detector; one-channel output is an explicit refusal;
- leaves `getDisplayMedia({video: true, audio: true, preferCurrentTab: true})`,
  one `MediaRecorder`, native per-stream PTS, before-warm observation, and all
  existing visual/raw-PTS controls unchanged.

The existing controller already fingerprints all named standalone source
files and binds the full source, 77-member Composition package, private graph,
six peer files, Node/Chrome identities, flock, fresh marker, short temp, and
resource pre/post state. No controller logic change is required; the changed
source hash requires a fresh manager review/grant.

## Future central command

After the patch is applied to the App standalone probe, committed, and
independently re-fingerprinted, the manager may fill fresh grant/marker paths
and run one central attempt. This is a literal template, not authorization;
the angle-bracket values must be replaced only after review:

```bash
TAB_AUDIO_GRANT_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-stereo-mix-capability-prep/<NEW-manager-grant>.json \
TAB_AUDIO_FINAL_SHA=<HARNESS-COMMIT-SHA> \
TAB_AUDIO_PREFLIGHT_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-stereo-mix-capability-prep/<NEW-run>-preflight.json \
TAB_AUDIO_RUN_MARKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-stereo-mix-capability-prep/<NEW-run>-started.json \
PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-stereo-mix-capability-prep/<NEW-run>-output \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=1 \
bash /home/user/work/wt/vw-m3-tab-clean-install-source-compose/tests/e2e/timeline/setup-tab-audio-capture.sh
```

The only new positive to accept is two actual encoded audio channels with the
left/right detector passing. A mono WebM must remain a failed stereo result,
not be downmixed or relabelled.
