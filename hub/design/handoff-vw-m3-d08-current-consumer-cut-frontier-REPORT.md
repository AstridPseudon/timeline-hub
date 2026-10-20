# D08 bounded playback-rate consumer cut

## Approval packet

Exact source patch is bounded to four App files on base
`tl/integration@157eef8cf1151db09310153c10856d45d8590c87`:

- `src/tools/video-editor/lib/config-utils.ts`: delete the App
  `getSanitizedPlaybackRate` wrapper, which only delegated to the old SDK
  formula.
- `src/tools/video-editor/lib/config-utils.test.ts`: retain the two existing
  invalid-rate assertions against the public Composition export.
- `src/tools/video-editor/compositions/playerEvaluation.ts`: import the public
  sanitizer directly.
- `src/tools/video-editor/compositions/VisualClip.tsx`: import the public
  sanitizer directly.

The public 0.0.13 implementation is the already-qualified replacement and is
already consumed by `compiledAudioSourceClock.ts` plus its tests. The public
artifact remains SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Evidence

Focused neighbors: **7 files / 199 tests passed**. ESLint on all four changed
files passed with `--max-warnings 0`. `git diff --check` passed. A source sweep
finds no import of `getSanitizedPlaybackRate` from App `config-utils`; all
remaining references resolve to the public Composition package.

No assertion was deleted, skipped, weakened, or converted to an expected
failure. No package/lock/pin, public13 bytes, producer, DTO, or shared command
producer changed. No physical frame/audio parity claim is needed for this pure
sanitizer delegation.

## Limits

No full suite, browser/render journey, live socket, install, package rebuild,
or whole-App typecheck was run. The current base already contains the approved
trim/renderPipeline/fallback/D10 deletions; this packet does not repeat them.
Volume, duration, host transition, and audio-policy candidates remain open.

App home gate should review this exact patch and merge it normally. The manager
should record the bounded playback-rate leaf in the D08 ledger after merge.
