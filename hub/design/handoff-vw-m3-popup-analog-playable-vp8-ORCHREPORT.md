# Chromium141-playable popup analog

## Result

Prepared a separately named `main-popup-analog-vp8-webm` fixture and controller test on base `e13e22658063f216155c59db23f8b3e9414f8cfc` (`tl/vw-m3-popup-main-playable-analog-prep`). The retained `main-popup-analog` H.264/MP4 fixture, its test, native fixture, renderer, host, source selector, compiler, pins, and projectors are unchanged.

The new analog is derived from `native.add.output` through an explicit manifest change list. It preserves the raw authored `at/from/to/hold/speed`, `params:null`, opaque values, source windows, occurrence placements, revision identities, and the six-row MAIN boundary candidate. Only the settled MAIN numeric FPS adaptation, built-in `video` to `media` dispatch adaptation, and separately generated media identities are represented in the analog.

## Media identities

| file | codec/type | bytes | SHA256 |
|---|---|---:|---|
| `media-1.webm` | VP8 / `video/webm` | 220030 | `490a1419a083a4238fb33dd685cf234c86fc3dda3b078ba98c3ba00e6279ecce` |
| `media-2.webm` | VP8 / `video/webm` | 5251 | `16bf35911a05050ea3c0300f3a35a6cf3a34701c24d7053d42620a81a59247c9` |

Both were generated twice with the same local ffmpeg command and compared byte-for-byte. Final ffprobe evidence for each: one VP8 video stream, 160x90, yuv420p, 24/1 average and real frame rate, 1/1000 time base, start `0.000000`, 144 frames, duration `6.000000`, WebM/Matroska container, and no audio stream. The manifest records the exact command, content type, digest-bound `/v1/objects/<encodeURIComponent(sha256:digest)>` locator, ETag identity, byte-range contract, and source filename.

The old H.264 identities remain retained in the old fixture and are explicitly listed as `prepared_h264_analog`; they are not scheduled for Chromium141. No native visual equivalence or native acceptance is claimed.

## Evidence

- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/mainPopupPlayableAnalog.test.ts src/tools/video-editor/commands/mainPopupPlayableAnalogVp8.test.ts src/tools/video-editor/lib/canonicalRenderBounds.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts` — **41 passed / 41**, 4 files, exit 0.
- `node_modules/.bin/eslint src/tools/video-editor/commands/mainPopupPlayableAnalogVp8.test.ts --max-warnings=0` — exit 0.
- `git diff --check` — exit 0.
- Regeneration command used `ffmpeg` 6.1.1 with `libvpx`, `-deadline best -cpu-used 0 -crf 4 -b:v 1M -enc_time_base 1/1000 -fps_mode passthrough -pix_fmt yuv420p -threads 1 -flags:v +bitexact -fflags +bitexact -map_metadata -1`; each output was generated twice and `cmp` passed.
- Final `ffprobe -v error -count_frames ...` — both files report VP8, video-only, 24/1, 1/1000, 144 frames, six seconds, and `matroska,webm`; `cmp` against a fresh regeneration passed.
- Native copy SHA256: `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`.
- New fixture hashes: `analog.json` `ae15beb9c10d0febb1597ef05b8b6ab49f6bd223231067b9140e08446a1b0099`; `manifest.json` `4060c2c186b5586d760aa7b961048df59b51bc320d06685eeae4eb9c183c70d0`; `main-vector.json` `02a2623e0bf917f163c2989ca65c2b1173353a3bc05af141a7c0e08b5fe82485`.

No browser, render, socket, service, network, install, or full suite was run by this worker. Chromium141 playback and range responses remain central evidence, not an offline claim.

## Handoff and remaining gate

Flat copies are in `scratchpad/orch/design/handoff-vw-m3-popup-analog-playable-vp8-*`. The deterministic media archive is `vp8-media-smallflat.tgz` in this worker ORCH directory with bare SHA `703513afa0c78b7729ae0dffa5ea778efece2747c10a6c181f13b1e329b5684d`.

Before capture, the manager must bind the new fixture root and media archive into the existing central controller, preserve Chromium141 and all source/package/browser guards, obtain Agent's corrected exact-native six-row confirmation and `READY_GRANTED`, and register the one-shot suite `e2e-viewing-popup-main-analog-vp8`. The future invocation is:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-popup-analog-playable-vp8 e2e-viewing-popup-main-analog-vp8) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That suite must run the existing manager-controlled `run-central.py --run` through the browser flock with the VP8 fixture selected; it was not run here.

Recommended next step: schedule that one central Chromium141 run against the new fixture, verify actual 200/206 routes return `video/webm` and exact source bytes, then inspect Player readiness and capture diagnostics. Do not schedule the retained H.264 analog or change the browser.
