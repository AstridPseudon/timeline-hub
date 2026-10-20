# Current13 five-case frozen-prep commands

All commands were read-only or test-only and ran from
`/home/user/work/wt/vw-m3-current13-fivecase-frozen-prep`.

```sh
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node

"$NODE" --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs
"$NODE" --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
node --import tsx --test \
  tests/e2e/timeline/viewing-parity/harness.test.ts \
  tests/e2e/timeline/viewing-parity/admission.test.ts \
  tests/e2e/timeline/viewing-parity/authority.test.ts \
  tests/e2e/timeline/viewing-parity/source-tuple.test.ts \
  tests/e2e/timeline/viewing-parity/canvas.test.ts \
  tests/e2e/timeline/viewing-parity/browser-profile.test.ts
"$NODE" tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs \
  --discover /home/user/work/wt/vw-m3-current13-fivecase-frozen-prep
"$NODE" tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs \
  --ready /home/user/work/wt/vw-m3-current13-fivecase-frozen-prep \
  /home/user/work/agent /home/user/work/runtime
git diff --check
```

The `--ready` command is expected to exit 1 at the App adoption hold. No
`--prepare` command exists in this controller; `--discover` is its pure
discovery-only path. No browser, render, export, socket, install, network,
grant, or full-suite command was run.
