# Stereo controller frozen final gate commands

All commands were read-only against App/Composition repositories. The exact App commit was tested from a disposable `/tmp` archive; its `node_modules` resolved to the readonly private12 graph. No browser or capture was run.

```bash
APP=/home/user/work/app
COMP=/home/user/work/wt/vw-m3-stereo-controller-frozen-final-gate
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node

git -C "$APP" show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' bca5ed45c
git -C "$APP" diff --check 2b388e769d9e153122e43b16b5d21e6e1ddf5b71 bca5ed45c -- \
  tests/e2e/timeline/tab-audio-capture.analysis.mjs \
  tests/e2e/timeline/tab-audio-capture.analysis.test.mjs \
  tests/e2e/timeline/tab-audio-capture.probe.ts

"$NODE" --test \
  tests/e2e/timeline/tab-audio-capture.analysis.test.mjs \
  tests/e2e/timeline/tab-audio-capture.controller.test.mjs \
  tests/e2e/timeline/tab-audio-capture.environment.test.mjs

"$NODE" node_modules/typescript/bin/tsc --noEmit --target ES2022 \
  --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict \
  --skipLibCheck --allowJs --resolveJsonModule --types node \
  tests/e2e/timeline/tab-audio-capture.probe.ts \
  tests/e2e/timeline/tab-audio-capture.config.ts

"$NODE" --check tests/e2e/timeline/tab-audio-capture.analysis.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
sha256sum "$NODE"; "$NODE" --version
```

Results: three Node test modules passed; strict TypeScript, syntax, shell syntax, and diff checks passed; Node output was `v20.19.4` and `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

The exact Playwright list command was attempted with `TAB_AUDIO_TASK_TMPDIR` and own worker cache/output paths. It reached the committed config, then refused with `Probe state must stay inside its own worker folder` because the controller constant still names `vw-m3-tab-short-owned-tmp-fix`. Pure committed-source preflight is therefore not approved or run; the stale Node constant would independently fail the controller identity check.
