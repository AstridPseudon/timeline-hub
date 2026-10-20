# Private Pulse stereo fallback commands

All commands below are preparation or review commands unless explicitly marked
central. No central command was run by this worker.

## Offline checks completed

```bash
command -v pulseaudio pactl ffmpeg ffprobe
pulseaudio --version
pactl --version
ffmpeg -version | head -1
ffprobe -version | head -1

node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-private-pulse-stereo-prep-private-pulse-stereo.controller.mjs
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-private-pulse-stereo-prep-private-pulse-stereo.probe.ts
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-private-pulse-stereo-prep-private-pulse-stereo.config.ts
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-private-pulse-stereo-prep-setup-private-pulse-stereo.sh
git -C /home/user/work/wt/vw-m3-private-pulse-stereo-prep apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-private-pulse-stereo-prep.patch
node --test /home/user/work/wt/vw-m3-stereo-owned-state-guard-fix/tests/e2e/timeline/tab-audio-capture.analysis.test.mjs /home/user/work/wt/vw-m3-stereo-owned-state-guard-fix/tests/e2e/timeline/tab-audio-capture.controller.test.mjs
```

The last command passed 2/2 files. `git diff --check` also passed. The
controller's actual `--prepare` was deliberately not invoked under this
worker's root UID: root/system mode is forbidden by the diagnostic contract.

## Central command after independent review and a fresh grant

Apply the handoff patch to the reviewed clean App source, create a new grant
bound to its final SHA, and choose unique owned paths. Then run exactly once:

```bash
APP=/home/user/work/wt/vw-m3-stereo-owned-state-guard-fix
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
STATE=$ORCH/workers/vw-m3-private-pulse-stereo-prep/central-state-<run>
mkdir -p "$STATE"
PRIVATE_PULSE_STATE_ROOT="$STATE" \
TAB_AUDIO_RUN=1 \
TAB_AUDIO_GRANT_PATH="$ORCH/workers/vw-m3-private-pulse-stereo-prep/<fresh-grant>.json" \
TAB_AUDIO_PREFLIGHT_PATH="$ORCH/workers/vw-m3-private-pulse-stereo-prep/<fresh-run>-preflight.json" \
TAB_AUDIO_RUN_MARKER="$ORCH/workers/vw-m3-private-pulse-stereo-prep/<fresh-run>-started.json" \
PLAYWRIGHT_OUTPUT_DIR="$ORCH/workers/vw-m3-private-pulse-stereo-prep/<fresh-run>-output" \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
bash "$APP/tests/e2e/timeline/setup-private-pulse-stereo.sh"
```

The placeholders are intentional and must be replaced only after review. The
existing base controller must verify the full source/package/graph/peer/
Node/Chrome/floor/flock/preflight/postflight tuple and the fresh grant; this
fallback must not run from the old 1534 or 1532 grant/marker.

If GDM is mono, accept only the recorded separate monitor channel diagnostic.
Do not rerun from that result, decode as stereo, upmix/downmix, alter the
0.001 detector, add a primer/keepalive/mute reset, realign clips, or claim
Player/export/A/V phase parity.
