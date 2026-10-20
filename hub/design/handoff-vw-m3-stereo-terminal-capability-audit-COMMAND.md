# Stereo terminal capability audit command

Manager-only sequence after reviewing the exact clean worktree:

```bash
APP=/home/user/work/wt/vw-m3-stereo-owned-state-guard-fix
TAB_AUDIO_RUN_MODE=stereo \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=0 \
bash "$APP/tests/e2e/timeline/setup-tab-audio-capture.sh"
```

The command above is the pure post-commit preflight only. It must be run by
the manager after verifying the exact commit/tree, clean status, private12
graph, all 77 Composition files, six peer hashes, Node20.19.4 full SHA,
Chrome155 full tree, source pre/post identity, run-mode identity, one-test
discovery, flock, resource floor, short-temp ownership, and cleanup.

Then the manager creates one fresh grant bound to that fresh fingerprint and
queues exactly one central diagnostic. This worker must not create the grant,
request the terminal, or launch a rerun.

