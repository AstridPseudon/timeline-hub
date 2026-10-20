# Stereo owned-state guard fix commands

Retained toolchain verification:

```bash
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
test "$($NODE --version)" = v20.19.4
test "$(sha256sum "$NODE" | cut -d' ' -f1)" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
```

Post-commit pure preflight/discovery command (manager review and fresh grant required; do not run from a dirty source):

```bash
TAB_AUDIO_RUN_MODE=stereo \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=0 \
bash /home/user/work/wt/vw-m3-stereo-owned-state-guard-fix/tests/e2e/timeline/setup-tab-audio-capture.sh
```

The launcher refuses dirty source before issuing a grant. A future manager-authorized one-shot run must supply a fresh exact-source grant, final SHA, preflight path, run marker, and output path under this worker's own state root; no old source, old Node alias, recycled marker, or another worker's state is valid.
