Static candidate only. No permission, central request, browser, or capture has been created. Empty manager template: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-manager-only-grant-template.json (zero bytes; not a valid grant).

Exact offline checks already run from /home/user/work/wt/vw-m3-tab-clean-install-source-compose:

```bash
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/run-static.py
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/audit-graph.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-graph-post.json
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/tmp /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/e2e/timeline/tab-audio-capture.controller.mjs --fingerprint
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/tmp /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/e2e/timeline/tab-audio-capture.controller.mjs --discover
```

The exact seven individual test/type/lint/Vitest/shell command arrays and results are in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-tests.json; all environment assignments are in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-run-static.py. Pure Vitest uses `--configLoader=runner --no-cache` and /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-pure-preflight.config.mjs; its cacheDir is /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/vite-cache. ESLint uses `--no-cache`. No default App config is loaded. Node child discovery uses temporary regular output files under this worker, removes them in finally, and validates the real CLI's one-test output; it never substitutes a fabricated list.

After the harness commits, the manager must first review the exact commit and candidate byte hashes. The following command is PURE, requires clean committed source, shared browser flock, absent QUIET and >=10 GiB; it creates no grant/run marker and starts no browser/listener. It is a proposed manager command; this worker did not invoke it because its source additions are not committed yet:

```bash
env -u TAB_AUDIO_RUN -u TAB_AUDIO_GRANT_PATH -u TAB_AUDIO_FINAL_SHA -u TAB_AUDIO_PREFLIGHT_PATH -u TAB_AUDIO_RUN_MARKER \
  TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
  bash /home/user/work/wt/vw-m3-tab-clean-install-source-compose/tests/e2e/timeline/setup-tab-audio-capture.sh \
  > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/manager-postcommit-pure-preflight.json
```

Review that output and independently compare final source, controller, CLI, whole new physical graph, complete Composition12 77 members, six peer-file hashes, Node, and Chrome155 tree/version/executable. Only the manager can issue a NEW, separate actual grant matching every field enforced by assertGrant: approved/profile/browserExecutable/browserVersion/backendOrder, sourceSha/sourceTree/fullTrackedHash/inputHash/packageGraphHash/finalSha, nodeVersion/nodeExecutableSha256, browserTreeSha256/browserExecutableSha256, packages/renderGraphHashes/privateGraph/discovery/environmentApprovalReference. No old grant or old marker is usable for this new profile and final source. The manager must fill a distinct actual grant path after review, not treat the empty template as approval.

ONE future named central capability command may be registered only after that fresh review/grant. This is a template, NOT authorization or a submitted request; angle-bracket values must come from the manager's new approval. Absolute one-shot paths must be previously nonexistent:

```bash
TAB_AUDIO_GRANT_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/<NEW-manager-grant>.json \
TAB_AUDIO_FINAL_SHA=<HARNESS-COMMIT-SHA> \
TAB_AUDIO_PREFLIGHT_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/<NEW-run>-preflight.json \
TAB_AUDIO_RUN_MARKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/<NEW-run>-started.json \
PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/<NEW-run>-output \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=1 \
bash /home/user/work/wt/vw-m3-tab-clean-install-source-compose/tests/e2e/timeline/setup-tab-audio-capture.sh
```

The setup holds shared FD9 flock throughout; repeats QUIET/floor/source/whole-graph/browser/discovery checks; claims an exclusive one-shot marker; starts only the standalone HTML/WAV fixture; and runs fingerprint postflight in EXIT cleanup even after failure. Playwright owns private profile/temp cleanup; fixture finally closes connections/server. All transform/cache/temp/config/profile/output paths are inside /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose; HOME is untouched. Tab capture precedes any separately approved private-pulse fallback. No pulse daemon is started by this candidate.

Historical 1020073136-18181 stays FAILED (pre-browser fixture-loader failure). MAIN reference PASS is unrelated. This capability can only establish the standalone tab's two live tracks, both declared tones, and native per-stream PTS. No App startup, Runtime/token, certification, current release, Player/export or parity claim.
