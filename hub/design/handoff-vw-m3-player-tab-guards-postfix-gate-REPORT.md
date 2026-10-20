# Player tab guard postfix review

## Verdict

**APPROVE future qualified case; current `--ready` remains correctly refused.**

Reviewed App commit `247bfce2721e4fd0804faf8313b394e94157c2ee` over the prior
`c60cef9470d0e02abc42c4850cdbd4d1112e7c76` rejection. No Composition source
change is needed.

The four blocking corrections are present:

1. `--ready` fails closed while `APP13.status` is
   `pending-consumer-adoption`; after adoption it checks the exact App source
   and tree, Agent/Runtime source and trees, clean sources, source pre/postflight,
   and a matching grant/marker.
2. The controller now checks the complete Node executable SHA, complete Chrome
   executable SHA, Chrome package/version, the 255-file Chrome tree hash, the
   77-file Composition graph, the whole private graph, six pinned peer files,
   exact five-case discovery, flock, resource floor, short private temp, and
   source identity before/after the preflight. The old 8-hex Chrome prefix is
   gone.
3. `assertNativePts` requires exactly one video and one audio stream, valid
   native rational time bases, nonempty packet sets, finite native `pts` and
   `pts_time`, and per-stream monotonicity.
4. Direct lifecycle coverage now rejects recorder `error`, `abort`, missing or
   extra tracks, and recorder start failure while stopping all acquired tracks.

The c60 fifth case remains before the planted picture-only negative. The four
existing cases, normal App Render/download path, strict RGB-2 comparison,
audio-0.001 controls, mute/0.5 gain controls, observer-before-warm ordering,
and existing keepalive/mute-reset/OS behavior are unchanged by 247's four-file
diff. No physical-mix claim is made.

## Evidence

All checks used an isolated tiny extract of the exact App commit and the shared
dependencies read-only:

- `node --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs` — PASS.
- `node --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs` — PASS.
- `node --import .../tsx/dist/loader.mjs -e "import('./tests/e2e/timeline/viewing-parity/tab-audio.test.ts')..."` — **8/8 PASS**.
- `tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --types node .../tab-audio.ts .../tab-audio.test.ts` — PASS.
- `eslint .../tab-audio.ts .../tab-audio.test.ts --max-warnings 0` — PASS.
- Playwright CLI `test --config playwright.viewing-parity.native-codec.config.ts --list` — **exactly 5 tests in 1 file**.
- `git diff --check c60cef947 247bfce27 --` on the four candidate files — PASS.
- Candidate controller `--ready` with current App/Agent/Runtime roots — exits 1 with `App13 consumer adoption is pending; --ready remains refused`, before capture/grant work.

## Limits and next step

No App13 adoption pin, manager grant, fresh one-shot marker, browser, render,
capture, localhost/live socket, network, install, or full suite was run. The
current refusal is therefore the only valid readiness result. Once App13 is
actually adopted and a new manager grant plus fresh marker exist, rerun the
controller in the central environment and only then request the central actual
capture. This review does not claim physical audio parity.
