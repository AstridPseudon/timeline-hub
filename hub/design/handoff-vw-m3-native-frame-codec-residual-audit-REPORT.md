# Native frame codec residual audit

Date: 2026-10-20. This is an offline audit before any new broad-browser retry. It makes no parity, negative-control, gate, PCM, or M3 claim.

## Verdict

After separating the known modal/backdrop and the two 240 px sidebands, the retained native fixture still has a small frame-content residual against the actual decoded export:

| comparison | pixels | >2/255 | fraction | max channel error | mean channel absolute error |
| --- | ---: | ---: | ---: | ---: | ---: |
| readiness Player vs actual decoded export, full frame | 2,073,600 | 526,658 | 25.3982% | 20 | 3.033262 |
| same, sidebands only | 518,400 | 518,400 | 100% | 20 | 10.333333 |
| same, 1,440×1,080 content region only | 1,555,200 | **8,258** | **0.530993%** | **4** | **0.599905** |

The full-frame residual is therefore dominated by the known sidebands: retained Player RGB is `(0,0,0)` while the export decode is `(5,6,20)` on both sidebands. The content-region residual is small, bounded to 4/255, and has per-channel means `(0.562256, 0.553855, 0.683604)`. Its raw max-error histogram is 160,919 exact, 1,129,361 at 1, 256,662 at 2, 8,112 at 3, and 146 at 4. This is consistent with the native RGB Player versus H.264 full-range YUV decode/color conversion and lossy compression; it is not a background-default difference.

## Exact source and geometry

- The checked-in source fixture’s `makePng()` is the pinned 64×48 RGB gradient, 6,297 bytes, digest `sha256:371fa835ba9c64b94118593bec78b7ae6295c44f578c1373f7efdbd06857f9c0`; the source function was executed through Node and `ffprobe` confirmed 64×48 `rgb24`.
- Frame 0 is the still clip (`parity-image`, `at: 0`, `hold: 4`); the fixture’s video starts at frame 120. The pinned source video is separately 640×360 VP8, 30 fps, 45 frames/1.5 s; it is not substituted for the frame-0 still.
- The retained rendered/player PNGs are 1920×1080. A 4:3 source in a 16:9 contain canvas yields the exact 1,440×1,080 content rectangle `x=240..1679`, with 240 px sidebands on each side. Unmodified readiness and export pixels both transition at x=240 and x=1680; no scale/crop/shift/resize was used.
- `ffprobe` on the unchanged MP4: H.264 High/avc1, 1920×1080, 30/1, 165 frames, 5.5 s, `yuvj420p`, full range, AAC-LC 48 kHz stereo, 5.5 s. The MP4 is 1,109,353 bytes, digest `sha256:ba653c490689847a31033babc48dba64f6322549fa2b98b12e615ea58658bbc9`.

## Modal and sideband separation

The positive Player PNG is not usable as an unobscured content reference: the retained trace shows the open Rendered film dialog and backdrop. Comparing that original PNG to the actual decoded export reproduces the prior `2,073,545/2,073,600`, max 203, mean 72.252703 result. Comparing positive Player to the retained cross-case readiness PNG finds the two 240 px sidebands exactly equal and all 1,555,200 content-region pixels changed (1,555,111 beyond 2/255). That is direct modal/backdrop evidence, not native content evidence.

The cross-case readiness PNG is kept explicitly as a different case. It shares the immutable still digest, but it is never claimed to be the positive case or a qualification substitute. It is used only to remove the known modal from the retained comparison and expose the content-region residual.

## Decoder/color/scale/compression conclusion

- **Decoder:** retained decoder calibration shows Chromium 141 rejects the same MP4 in blob, complete-200, and range-206 modes with MediaError 4 (`DEMUXER_ERROR_NO_SUPPORTED_STREAMS`), while Chrome 155 decodes/seeks it at 1920×1080. This browser capability divergence remains independent of a shared theme default; no new browser run was made here.
- **Color/compression:** yes, a small content-region residual remains: 8,258 pixels over 2/255, max 4/255, mean 0.599905. The source-side Player is RGB PNG; the export is H.264 `yuvj420p`/full-range and is decoded to RGB. A shared default cannot remove this codec/color path difference.
- **Scale:** no retained evidence of scale divergence. The source aspect ratio, output dimensions, sideband widths, and content boundary agree. The audit did not normalize, crop, shift, resize, or alter comparator behavior.

The settled public default black policy can explain/remediate the sideband background only. It does not make this cross-case comparison a same-case positive, does not resolve Chromium 141’s native decoder failure, and does not justify changing strict `2/255` and `.001` expectations.

## Artifacts and commands

Flat ORCH artifacts:

- `handoff-vw-m3-native-frame-codec-residual-audit-measurements.json` — hashes, ffprobe projection, region metrics, and boundary samples.
- `workers/vw-m3-native-frame-codec-residual-audit/measure-native-frame-codec-residual.py` — read-only measurement script.
- `workers/vw-m3-native-frame-codec-residual-audit/tmp/actual-export-frame000.png` — one FFmpeg decode of the unchanged MP4; temporary diagnostic output only.

Exact checks run:

```sh
ffmpeg -v error -threads 1 -i <retained-export.mp4> -map 0:v:0 -vf 'select=eq(n\,0)' -frames:v 1 -fps_mode vfr <own-ORCH-tmp>/actual-export-frame000.png
# exit 0; SHA256 87f328b7f1cf96036821cd3180ae99068110e46b03f282cc5fff52b134ee8837

ffmpeg -v error -xerror -err_detect explode -threads 1 -i <retained-export.mp4> -map 0:v:0 -frames:v 1 -f null -
# exit 0

python <own-ORCH-worker>/measure-native-frame-codec-residual.py ...
# exit 0; measurements JSON written; content outside-2 = 8258

git diff --check
# exit 0; assigned App worktree clean (no product files changed)
```

No product tests were needed or run: this worker changed no product/test source. No browser, renderer, Runtime, socket, network, install, comparator, fixture, full suite, or central test-service run was performed. The named report/R4 paths from the task were absent in this environment; the available retained handoff artifacts under `/home/user/timeline-hub/hub/design` were read-only inputs.

Recommended next step: keep the raw originals and this measurement as owner evidence; route the theme-default sideband question to the already identified Agent owner, and keep decoder compatibility as a separately qualified browser/environment issue. Do not rerun the broad browser journey without an explicit grant and frozen source tuple.
