# vw-m3-tab-short-owned-tmp-fix

## Result

Fixed the Chrome singleton-socket path failure in the standalone tab-audio preflight. The launcher now allocates exactly one fresh direct child of `/tmp` (`timeline-tab-audio-*`) for each attempt, binds `TMPDIR`, `TMP`, `TEMP`, and `TAB_AUDIO_TASK_TMPDIR` to that directory, and keeps caches/config/transform/output under this worker's own state root. The `EXIT` trap runs postflight when appropriate and then removes only the directory allocated by that attempt, including launcher failures.

The controller's direct `--discover` path uses the same short directory policy and finally-cleans its own allocation when no launcher-owned directory is supplied. It refuses to clean directories not allocated by the current controller process. No `HOME`, PulseAudio, global system temp, shared cache, or product/runtime setting was changed.

The calibration uses the bounded Chrome singleton suffix `com.google.Chrome.12345678901234567890/SingletonSocket`:

- old worker-root path: 175 bytes (`> 108`)
- fresh `/tmp/timeline-tab-audio-XXXXXX` path: 85 bytes (`< 108`)

The worker state root and cache/output defaults are now bound to `vw-m3-tab-short-owned-tmp-fix`, so a future grant must use a new source fingerprint. Existing grants and markers were not read or reused; no grant was created.

## Tests and static evidence

Passed:

```text
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/e2e/timeline/tab-audio-capture.controller.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs tests/e2e/timeline/tab-audio-capture.environment.test.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/eslint/bin/eslint.js --no-cache tests/e2e/timeline/tab-audio-capture.controller.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs tests/e2e/timeline/tab-audio-capture.environment.test.mjs --max-warnings 0
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/typescript/bin/tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --allowJs --resolveJsonModule --types node tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts
git diff --check
```

The actual pinned Playwright discovery command was run through the controller before any READY/grant step:

```text
env -u TAB_AUDIO_TASK_TMPDIR -u PLAYWRIGHT_OUTPUT_DIR -u TAB_AUDIO_RUN /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/e2e/timeline/tab-audio-capture.controller.mjs --discover
```

It passed with exactly one collected test and no Chrome execution, browser, fixture listener, socket, network, install, full suite, central request, or grant. The captured list is in `handoff-vw-m3-tab-short-owned-tmp-fix-playwright-list.json`. The attempted launcher `--prepare` was correctly refused because this worker is uncommitted; no clean-source guard was bypassed.

## Manager handoff

The manager must wait for the harness commit, then use the pure-preflight command in the companion `-commands.md`. It must review the new committed source SHA/tree, full/input hashes, Chrome155 tree/version/executable, exact 77-file Composition graph, six peer-file hashes, exact private graph, and one-test discovery before deciding whether to issue a fresh grant. The companion `-manager-only-grant-template.json` is intentionally zero bytes and is not an approval or usable grant.

Historical `1020124802-7076` remains a failed pre-recording Chrome startup incident; this change does not turn it into an unsupported-backend claim and does not make any parity/current-API/capture claim.
