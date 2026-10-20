Static handoff only; no permission, grant, central request, browser, capture, or listener was created.

Exact targeted checks run from `/home/user/work/wt/vw-m3-tab-short-owned-tmp-fix`:

```bash
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/e2e/timeline/tab-audio-capture.controller.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs tests/e2e/timeline/tab-audio-capture.environment.test.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/eslint/bin/eslint.js --no-cache tests/e2e/timeline/tab-audio-capture.controller.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs tests/e2e/timeline/tab-audio-capture.environment.test.mjs --max-warnings 0
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/typescript/bin/tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --allowJs --resolveJsonModule --types node tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts
git diff --check
```

Actual no-browser discovery before READY:

```bash
env -u TAB_AUDIO_TASK_TMPDIR -u PLAYWRIGHT_OUTPUT_DIR -u TAB_AUDIO_RUN \
  /tmp/vw-m3-agent-gate-node20.19.4/bin/node \
  tests/e2e/timeline/tab-audio-capture.controller.mjs --discover \
  > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-short-owned-tmp-fix-playwright-list.json
```

After the harness commits this source, the manager's pure preflight is:

```bash
env -u TAB_AUDIO_RUN -u TAB_AUDIO_GRANT_PATH -u TAB_AUDIO_FINAL_SHA \
  -u TAB_AUDIO_PREFLIGHT_PATH -u TAB_AUDIO_RUN_MARKER -u PLAYWRIGHT_OUTPUT_DIR \
  -u TAB_AUDIO_TASK_TMPDIR \
  TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
  bash /home/user/work/wt/vw-m3-tab-short-owned-tmp-fix/tests/e2e/timeline/setup-tab-audio-capture.sh \
  > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix/manager-postcommit-pure-preflight.json
```

The launcher allocates a new short task temp itself. Do not provide `TAB_AUDIO_TASK_TMPDIR`; do not reuse any old grant, marker, preflight, or output directory. This command performs only the source/environment/discovery preflight and does not run Chrome.

If the manager later authorizes the one-shot capability, it must first create a distinct fresh grant after committed-source review and use previously nonexistent absolute paths for the grant, preflight, marker, and output. The zero-byte companion grant template is only a placeholder:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tab-short-owned-tmp-fix-manager-only-grant-template.json
```
