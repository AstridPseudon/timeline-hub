# vw-m3-app35-pcm-preserve-progress

## Result

Fixed the narrow App35 rejection on top of committed parent `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a`.

- `AudioTrack.tsx`: restored source-chunk progress renewal for the existing readiness/starvation hold. Preparation reads `Response.body` chunks, calls the attempt-owned progress reset for each chunk, joins the bytes, and preserves the existing abort/stale, retry, Blob URL, AudioContext-close, native progress, and 10-second starvation behavior.
- `continuousPCM.lifetime.test.tsx`: restored the approved 70e378e3f PCM assertions for invalid speeds, all six curves, exact boundaries, overlap/unsupported behavior, nested multiply/minimum boost and silence admission, semantic rerenders, native/prepared transitions, boosted occurrence timing, and below-unity boosted fade samples. Added the explicit stalled/slow source-chunk regression.
- `AudioTrack.test.tsx`: restored the eighth approved unsupported-fade input (`fadeIn: 0, fadeOut: -1`).

Only these three allowed files are changed. No root/pin/DTO/store/compiler/public API change.

The restored lifetime suite is byte-identical to the approved `tl/vw-m3-app-pcm13-preserve-audible-cases` version after its source-repair additions. Public13 identity was independently checked: archive SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; installed leaf version `0.0.13`; all 77 archive files compared byte-for-byte with the private installed leaf.

## Tests

- `node node_modules/vitest/vitest.mjs run --no-cache --maxWorkers=1 --config /tmp/vw-m3-app35-pcm-public13.config.mjs [five files]`: **PASS**, 5 files / 143 tests. The config used the private public13 leaf/all-77 graph; shared dependencies were not modified.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/compositions/AudioTrack.tsx src/tools/video-editor/compositions/AudioTrack.test.tsx src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx src/tools/video-editor/compositions/continuousPCM.contract.test.tsx src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx --max-warnings 0`: **PASS**.
- `node node_modules/typescript/bin/tsc -p tsconfig.strict-islands.json --noEmit --pretty false`: **PASS**.
- `git diff --check HEAD`: **PASS**.
- `git diff --check HEAD^ -- <five scoped paths>`: **PASS**.
- Private package verification: `compared=77 bad=0`; public13 exports include `applyAudioEnvelope`, `audioEnvelopeWav`, `computeMediaTrim`, `encodedEnvelopeSource`, `getSanitizedPlaybackRate`, and `compileAudioEnvelope`.

An initial direct run against the shared App `node_modules` was invalid because it resolved Composition 0.0.8 and lacked public13 exports; it was not counted as qualification. The private public13 rerun above is the qualification result.

## Not run / blocked

No browser, render, localhost/socket, network/install, full suite, or physical Player/export parity run was performed. These remain owner/integration gates.

## Recommended next steps

Review/merge this corrective descendant, then run the central physical parity and remaining owner gates against the integrated public13 tree.

