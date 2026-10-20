# Stereo tab source-unit commands

All local commands used the retained executable only after checking:

```bash
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
test "$($NODE --version)" = v20.19.4
test "$(sha256sum "$NODE" | cut -d' ' -f1)" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
```

Passed directly in the assigned worktree:

```bash
$NODE --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs
$NODE node_modules/typescript/bin/tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --allowJs --resolveJsonModule --types node tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts
$NODE node_modules/eslint/bin/eslint.js --no-cache tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts tests/e2e/timeline/tab-audio-capture.analysis.mjs tests/e2e/timeline/tab-audio-capture.analysis.test.mjs --max-warnings 0
$NODE --check tests/e2e/timeline/tab-audio-capture.analysis.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
git diff --check
```

The lifecycle test and actual Playwright list were run from a disposable copy of the probe/controller inputs, with an owned symlink to the readonly private12 graph and caches/output under disposable worker state:

```bash
$NODE "$PRIVATE12/playwright/cli.js" test --config "$SANDBOX/tests/e2e/timeline/tab-audio-capture.config.ts" --project=native-codec-chrome155-tab-audio --list
```

Result: `Total: 1 test in 1 file`. The lifecycle environment lane passed 4/4. No browser or test execution was requested.

## Manager-only later command

Do not run this from the dirty worker. After commit, fresh source fingerprint, independent review, and a new manager grant, the manager may substitute concrete run-scoped paths and run exactly one attempt through the existing launcher:

```bash
TAB_AUDIO_GRANT_PATH=/tmp/.../<new-grant>.json \
TAB_AUDIO_FINAL_SHA=<committed-source-sha> \
TAB_AUDIO_PREFLIGHT_PATH=/tmp/.../<new-run>-preflight.json \
TAB_AUDIO_RUN_MARKER=/tmp/.../<new-run>-started.json \
PLAYWRIGHT_OUTPUT_DIR=/tmp/.../<new-run>-output \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=1 \
bash tests/e2e/timeline/setup-tab-audio-capture.sh
```

This is a template, not a grant or authorization. The result must report actual track settings/capabilities, native recorder channels, native PTS, and detector leakage; mono or swapped output is negative.
