# Review commands

```sh
node .review-tab-audio.controller.test.mjs
git -C /home/user/banodoco/reigh-app show 'tl/vw-m3-player-tab-mix-instrument-port:tests/e2e/timeline/viewing-parity/tab-audio.ts' | node --input-type=module -e '<exact-source transpile/instrument/PTS checks>'
git -C /home/user/banodoco/reigh-app show 'tl/vw-m3-player-tab-mix-instrument-port:tests/e2e/timeline/viewing-parity/cases.ts' | node --input-type=module -e '<exact-source five-case list-only check>'
git -C /home/user/banodoco/reigh-app diff --check 'tl/vw-m3-player-tab-mix-instrument-port^' tl/vw-m3-player-tab-mix-instrument-port
```

No browser, localhost, render, network, install, or full-suite command was run.
