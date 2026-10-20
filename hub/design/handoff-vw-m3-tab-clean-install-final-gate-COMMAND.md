Exact independent command record. Product/repository code was never changed. Only pure static suites and Playwright discovery ran; no service/full/browser run was requested.

The producer App worktree was recycled during review. Reviewer-owned source mirrors/cache/temp were cleaned after the recorded checks. These paths describe the actual execution; they are not an extant App entry point. The flat helper copies preserve the commands and adaptations for audit.

Initial original-worktree wrapper:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/run-checks.py
```

Result: analysis 7 pass; controller 8 pass/1 reviewer-write-boundary failure/0 skipped; environment 3 pass; source --fingerprint pass; wrapper then failed when its cwd was recycled before discovery. Original controller failure log: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-controller.log. No original test expectation was changed.

Independent physical inventory and frozen source reconstruction:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-verify.py before
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/frozen-source.py
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-verify.py after
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-private12-independent-gate-verify.py snapshot /home/user/work/app/node_modules /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-shared-before.json
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-private12-independent-gate-verify.py compare /home/user/work/app/node_modules /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-shared-after.json --baseline /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-shared-before.json
```

Final results: all exit 0; exact private READY manifest and source hashes; unchanged shared inventory. frozen-source.py's initial blob-only reconstruction failed until it followed the existing CLAUDE.md symlink, matching the controller's actual readFile behavior. The final helper is retained at /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-frozen-source.py.

Frozen mirror runner (first four commands passed; initial independent helper failed before correction):

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/run-frozen.py
```

The independent-controls command was then rerun directly, after private Python tar extraction, first exposing a helper CJS/ESM condition error, then passing after native ESM import. All attempts are retained in commands.json and the initial/cjs-resolution/final controls logs. It never altered a candidate test or source file. Successful test commands and exact shared environment follow; stdout/stderr used regular reviewer-owned log files.

```sh
export TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/tmp
export TMP=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/tmp
export TEMP=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/tmp
export XDG_CACHE_HOME=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/cache
export XDG_CONFIG_HOME=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/config
export PWTEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/transform
export NODE_PATH=''
export NODE_OPTIONS=--import=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/write-guard.mjs
export PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:/opt/node22/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-path:/opt/ruby-3.3.6/bin:/opt/rbenv/bin:/opt/rbenv/shims:/opt/node22/bin:/opt/maven/bin:/usr/lib/jvm/java-21-openjdk-amd64/bin:/opt/gradle/bin:/root/.bun/bin:/root/.codex/tmp/arg0-linux/codex-arg09d3AWo:/opt/node22/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-path:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/source
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/source/tests/e2e/timeline/tab-audio-capture.analysis.test.mjs  # frozen-analysis: exit 0
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/source/tests/e2e/timeline/tab-audio-capture.environment.test.mjs  # frozen-environment: exit 0
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/playwright/cli.js test --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/discovery.config.mjs --project=native-codec-chrome155-tab-audio --list  # frozen-discovery: exit 0
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/source/tests/e2e/timeline/setup-tab-audio-capture.sh  # frozen-shell: exit 0
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/independent-controls.mjs  # independent-controls: exit 1
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/independent-controls.mjs  # independent-controls-after-private-python-extraction: exit 1
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/independent-controls.mjs  # independent-controls-native-esm-imports: exit 0
```

Final independent results: 7 analysis passes; 3 environment passes; actual --list one test; shell syntax pass; actual-tar 77-member reconstruction/file-change/addition controls pass; all 11 packages resolve privately; pure native ESM imports and peer/graph/browser tree checks pass. Independent --list uses the unchanged committed fixture and reviewer-owned config. Its stdout hash equals the producer's exact frozen-config --list stdout. See /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-discovery.config.mjs and /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-write-guard.mjs.

Offline Chrome read used streaming Python hashlib.sha256 over /opt/google/chrome files, lstat/readlink without following directory links, complete-path canonical and recursive tuple ordering, and this package query (no executable launch):

```sh
dpkg-query -W '-f=${Version}' google-chrome-stable
```

Result: 155.0.8059.84-1, exact frozen executable/tree hashes in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-final-gate-browser.json. The unchanged environment suite independently checks the same full tree after discovery.

Producer-only type/lint/Vitest/controller evidence is in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-clean-install-source-compose-tests.json and its static.log; it was reviewed, not independently rerun in this gate. Postcommit manager pure --prepare was NOT run; it requires a restored clean App worktree. No grant or marker was written.
