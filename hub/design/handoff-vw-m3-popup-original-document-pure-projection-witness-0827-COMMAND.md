# Command record

Source input was read unchanged from:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-popup-analog-playable-vp8-native.json`

The temporary probe adapted only the supplied `swap.output` into the App's
validated canonical graph shape, then called the existing functions:

- local: `projectCanonicalComposition(prepared, undefined, {clampToOccurrenceDuration: false})`
- accepted: `projectCanonicalComposition(prepared)`
- resolved: `buildTimelineData(projected.config, {assets: projected.config.registry})`

No source, fixture, product, assertion, package, or shared dependency file was
changed by the witness.

```bash
TMPDIR="$PWD/.tmp-vw-m3" node node_modules/vitest/vitest.mjs run \
  --no-cache --silent=false --reporter=verbose \
  --config config/testing/vitest.config.ts --maxWorkers=1 \
  src/tools/video-editor/data/popupProjectionWitness.temp.test.ts
```
