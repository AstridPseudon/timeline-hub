# `vw-m3-player-tab-instrument-guard-fix`

Implemented the four requested test/controller/helper fixes in the App leaf only.

- `--ready` now refuses pending App13 adoption, requires exact Agent/Runtime source+tree pins, performs the existing viewing-parity source pre/postflight, exact five-case discovery, full Node/Chrome identities, resource/temp/private-graph checks, and fresh grant/one-shot marker binding. The current staged root correctly refuses before any capture or grant.
- Chrome uses the complete approved executable SHA, 255-file tree SHA, package/version/profile; Node 20.19.4 uses its admitted executable path and full SHA.
- Native PTS requires one nonempty packet set per stream, valid rational native timebases, finite `pts`/`pts_time`, and monotonicity independently per stream without cross-stream alignment.
- Direct recorder tests cover `error`, `abort`, missing audio, wrong cardinality, recorder start failure, and cleanup of every acquired track.

## Tests

Passed:

- `node --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`
- `node --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs`
- `node --import tsx -e "import('./tests/e2e/timeline/viewing-parity/tab-audio.test.ts').catch(e=>{console.error(e);process.exit(1)})"` — 8/8
- `npm exec -- tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --types node tests/e2e/timeline/viewing-parity/tab-audio.ts tests/e2e/timeline/viewing-parity/tab-audio.test.ts`
- `npm exec -- eslint tests/e2e/timeline/viewing-parity/tab-audio.ts tests/e2e/timeline/viewing-parity/tab-audio.test.ts --max-warnings 0`
- `git diff --check`
- `node node_modules/@playwright/test/cli.js test --config playwright.viewing-parity.native-codec.config.ts --list` — exactly 5 tests in 1 file.
- `node .../tab-audio.controller.mjs --ready . /home/user/work/agent /home/user/work/runtime` — refused as required: current `APP13.status` is `pending-consumer-adoption`.

The controller wrapper’s nested Playwright spawn could not be executed inside this sandbox (`EPERM`); the direct offline Playwright list command passed. No browser, render, capture, localhost/live socket, network, install, full suite, central capture/grant, shared dependency write, or git mutation was run.

No decisions beyond the settled handoff were made. Recommended next step: after App13 consumer adoption and the matching manager grant/marker exist, run the controller outside this sandbox and independently review its exact source tuple before any central qualification.
