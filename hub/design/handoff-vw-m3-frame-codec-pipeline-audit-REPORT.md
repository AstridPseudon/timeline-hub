# Frame codec pipeline audit (offline)

## Verdict

One actionable pipeline defect is proved: `tests/e2e/timeline/viewing-parity/frames.ts:27-35` probes the input dimensions, but `decodeRgb()` still gives `execFile()` a fixed stdout cap of `640 * 360 * 3 + 1024 = 692224` bytes. The retained normal MP4 and retained PNG are both `1920x1080`; one RGB frame is `6220800` bytes. Running the existing decoder against either retained file fails with `ERR_CHILD_PROCESS_STDIO_MAXBUFFER` before the comparator can evaluate pixels.

Candidate fix for the viewing owner: derive `maxBuffer` from the probed dimensions (`dimensions.width * dimensions.height * 3 + 1024`, with an explicit reasonable upper bound if desired), then retain the existing strict comparator contract. This would make oversized diagnostics fail at the comparator's existing `640x360` contract check instead of failing ambiguously in child-process plumbing. It is diagnostic hardening, not a parity fix, and was not applied because this task is review-only.

This does **not** diagnose the remaining actual parity failure. The retained positive Player PNG is the known Rendered-film modal/backdrop capture, and the unobscured readiness PNG is from a different case. There is no qualified unobscured same-case Player frame here; no same-case positive or remaining parity claim is made.

## Source trace

- PNG capture: `capturePlayerFrame()` saves the existing Playwright locator screenshot as PNG; `decodePlayerCapture()` calls the shared `decodeRgb()` path.
- Export extraction: `decodeExportFrame()` calls the same `decodeRgb()` path with `-map 0:v:0 -an -vf select=eq(n\,frame)`.
- Both paths then ask FFmpeg for `-f rawvideo -pix_fmt rgb24`; no crop, resize, color normalization, codec/profile substitution, or threshold change occurs.
- `ffprobeDimensions()` reads only width/height. It does not use codec/color metadata to alter the comparison.
- `compareRgbFrames()` checks exact `640x360` dimensions and raw RGB bytes, counts a pixel when any channel differs by more than 2, and `assertFrameWithinBound()` keeps the unchanged `.001` fraction limit. The strict channel-2/fraction-.001 policy is intact.

## Retained normal MP4 metadata

The retained normal MP4 is 1,109,353 bytes, 1920×1080, H.264 High/avc1, 30/1, 165 frames, `yuvj420p`, full range (`pc`), `bt470bg` matrix, centered chroma, AAC-LC 48 kHz stereo, 5.5 seconds. The retained PNG inputs are `rgb24`, full range, `gbr`.

The earlier retained transfer evidence records the native request as `GET Range: bytes=0-`, response `206`, `Content-Range: bytes 0-1109352/1109353`, `Content-Length: 1109353`, `Content-Type: video/mp4`, and `Accept-Ranges: bytes`. No new service/browser request was made.

Direct FFmpeg extraction of frame 0 from the retained export MP4 and direct FFmpeg extraction of the retained export frame-0 PNG both produced 6,220,800 RGB bytes with the same SHA-256:

```text
8b7f4fffacc9a82fd8266dbc3a2fe982268d06836f6f2748d657c6429bb073a7
```

That proves the retained export PNG and the MP4 frame-0 extraction agree through this RGB conversion path. It is export-vs-export evidence, not Player-vs-export evidence.

## Same comparator controls

Small local controls were generated only in a temporary directory and passed through the repository's existing `decodePlayerCapture()`, `decodeExportFrame()`, `compareRgbFrames()`, and `assertFrameWithinBound()` functions:

| control | result |
| --- | --- |
| solid PNG → FFV1/RGB24 lossless video | 0/230400 outside 2, max 0, mean 0; accepted |
| text PNG → FFV1/RGB24 lossless video | 0/230400 outside 2, max 0, mean 0; accepted |
| solid PNG → full-range H.264 `yuvj420p`/`bt470bg` video | 0/230400 outside 2, max 1, mean 0.667; accepted |
| text PNG → full-range H.264 `yuvj420p`/`bt470bg` video | 8753/230400 outside 2 (0.03799045), max 70, mean 0.805; rejected |
| lossless frame with 231 planted 10-level red-channel pixels | 231/230400 outside 2 (0.00100260), max 10; rejected |

The lossless controls prove the PNG decode → raw RGB → comparator path is exact for known solid/text inputs. The H.264 controls show ordinary lossy/chroma conversion errors, especially at sharp text edges, without any comparator conversion bug. The planted control proves the existing strict bound detects a mismatch just above the unchanged fraction threshold. These controls do not qualify the actual same-case pair.

## Exact commands and results

All commands were run from the assigned App worktree; no browser, render, Runtime/Agent service, socket, network, install, central test service, or full suite was run.

```sh
node --import tsx --test \
  tests/e2e/timeline/viewing-parity/compare.test.ts \
  tests/e2e/timeline/viewing-parity/media.test.ts \
  tests/e2e/timeline/viewing-parity/directframes.test.ts
# exit 0; 3 file-level subtests passed, 0 failed
```

The same-comparator synthetic-control invocation was:

```sh
node --import tsx --input-type=module -e "import { decodePlayerCapture, decodeExportFrame } from './tests/e2e/timeline/viewing-parity/frames.ts'; import { compareRgbFrames, assertFrameWithinBound } from './tests/e2e/timeline/viewing-parity/compare.ts'; /* generated solid/text PNG, FFV1, and full-range H.264 controls; compare each; mutate 231 lossless pixels */"
# exit 0; results are tabulated above
```

The retained 1920×1080 decoder failure was reproduced with:

```sh
node --import tsx --input-type=module -e "import { decodePlayerCapture, decodeExportFrame } from './tests/e2e/timeline/viewing-parity/frames.ts'; const png='/home/user/timeline-hub/hub/design/handoff-vw-m3-native-frame-zero-triage-export-frame000.png'; const mp4='/tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/viewing-parity/final-export.mp4'; for (const [name, fn] of [['png',()=>decodePlayerCapture(png)],['mp4',()=>decodeExportFrame(mp4,0)]]) { try { const frame=await fn(); console.log(JSON.stringify({name,dimensions:[frame.width,frame.height],bytes:frame.bytes.length})); } catch (error) { const e=error; console.log(JSON.stringify({name,code:e.code,message:e.message,stdoutBytes:e.stdout?.length ?? null,stdoutLimit:'PARITY_WIDTH*PARITY_HEIGHT*3+1024 = 692224'})); } }"
# both calls: ERR_CHILD_PROCESS_STDIO_MAXBUFFER; fixed cap 692224 bytes
```

The exact retained-file metadata/hash probes were:

```sh
ffprobe -v error -show_entries stream=index,codec_name,codec_type,width,height,pix_fmt,color_range,color_space,color_primaries,color_transfer,chroma_location,r_frame_rate,avg_frame_rate,time_base,nb_frames -show_entries format=format_name,duration,size -of json /tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/viewing-parity/final-export.mp4
ffmpeg -v error -i /home/user/timeline-hub/hub/design/handoff-vw-m3-native-frame-zero-triage-export-frame000.png -frames:v 1 -f rawvideo -pix_fmt rgb24 pipe:1 | sha256sum
ffmpeg -v error -i /tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/viewing-parity/final-export.mp4 -map 0:v:0 -an -vf 'select=eq(n\,0)' -frames:v 1 -f rawvideo -pix_fmt rgb24 pipe:1 | sha256sum
```

The two hashes were both `8b7f4fffacc9a82fd8266dbc3a2fe982268d06836f6f2748d657c6429bb073a7`; each raw stream was 6,220,800 bytes.

`git diff --check` passed and the App worktree remains clean. No product, fixture, comparator, threshold, profile, settings, or repository documentation was changed.

## Recommended next step

Treat the dynamic FFmpeg buffer as a small owner-reviewed test-pipeline fix if the diagnostic must accept native-size captures. Keep the comparator's 640×360 contract and strict 2/.001 policy unchanged. Await the qualified actual12 same-case pair before making any parity-cause or Gate 6 statement.
