# App PCM13 restored audible port

## Source and scope

- Governing base: App `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a` (`feat(app): consume public13 continuous PCM audio`).
- Approved source acknowledged: remote request/repair `70e378e3f780308628bd98b55405115d74288a48` (`tl/vw-m3-app-pcm13-preserve-audible-cases`) versus `2e9939810cbe600d1f7cfcf16d987e50bdecaaeb`.
- This is a test-only port. No request-merge was made for the old `70e378e3f` branch.
- Product/pin identity stayed byte-identical to `35e3ebdf2`: `AudioTrack.tsx` SHA-256 `3d28283c7b607d6fbc6a1839025db6f57d897e5322ca80e28bf4c56af724c3fb`; `package.json` SHA-256 `a2ac9c9d946bd2d0ee1b2283154d94adad926f6282fff4417aeaf7520f138437`; `package-lock.json` SHA-256 `7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14`. `git diff --quiet 35e3ebdf2 --` over those paths passed.
- Public Composition input was the immutable local `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular archive members, extracted to a private read-only leaf. Shared `node_modules` was read-only; Vitest used a private cache.

## Delta

- `AudioTrack.test.tsx`: retained the consumer’s existing controls and added the missing eighth unsupported native input, `{ fadeIn: 0, fadeOut: -1 }`, completing the original unsupported-fade matrix.
- `continuousPCM.lifetime.test.tsx`: added the shared PCM/WAV oracle helpers and 248 lines of restored cases. A header explains why the shared lifecycle fixture is 574 lines (>500).
- `continuousPCM.contract.test.tsx`: no incremental edit was needed; the actual consumer already contained the public full-source positive, matching prepared positive, and four forged-negative admission assertions, including the Blob-WAV negative. Its exact admission group was rerun.
- Final worktree delta: 2 files, 249 additions, 2 deletions; no product, package, lock, fixture, or media-conformance changes.

## Original -> PCM oracle mapping

| Original audible case | Restored consumer oracle |
| --- | --- |
| Invalid speeds `0`, `-1`, `NaN` | Sanitized playback rate `1`, exact prepared WAV bytes, and frame-7 fade sample. |
| Six curves: linear, equal-power, exponential-fast/moderate/slow, s-curve | Exact public `audioEnvelopeWav` bytes for each curve. |
| Exact fade boundaries and durations, including trimmed source | 3 kHz private decoded PCM fixture; source-time samples at every original boundary. |
| Overlapping fades | Exact WAV samples at frames 0, 15, and 30 (`0`, `0.25`, `0`). |
| 24/30/60 fps, fractional fades, track gain, mute | Exact full-WAV oracle plus constant native downstream gain. |
| Authored envelope precedence and semantic rerenders | Exact samples for authored envelope, changed envelope, linear fade, and equal-power rerender; fetch count confirms rebake. |
| Native -> prepared -> native transition | Source identity, Web Audio admission, readiness hold release, and return to native source. |
| Nested multiply/minimum boost forms | Four nested envelopes, exact baked sample `4`, constant gain, Web Audio admission. |
| Nested boost silenced by minimum | Exact silent WAV sample while retaining conservative Web Audio admission. |
| Boosted occurrence samples | Exact authored-time samples under occurrence bounds, trim, and speed, plus a boosted sample outside the visible window. |
| Boosted fade frames below unity | Exact baked fade endpoints with Web Audio admission and downstream `1.00712` gain. |
| Native unsupported fades | All eight inputs, including zero/negative/NaN, string, infinity, tiny fade, and no-fade, remain on finite plain native gain. |
| Existing Blob-WAV/admission negatives | Existing full-source positive, prepared positive, wrong envelope, fractional origin, wrong child rate, and non-attempt URL remain unchanged. |

## Results

All commands used `--no-cache --configLoader=runner --maxWorkers=1`, the private public13 leaf, and a private cache directory.

- Five affected consumer suites: **5 files / 142 tests passed**, exit 0.
- Restored groups: **34 selected tests passed**, with 81 unselected, exit 0.
- Admission group: **6 selected tests passed**, with 1 unselected, exit 0.
- Targeted ESLint over the three affected test files: exit 0.
- `git diff --check`: exit 0.
- No `.skip`, `.only`, `xfail`, or `todo` controls in the affected tests.

The exact five-suite command was:

```sh
node_modules/.bin/vitest run --no-cache --configLoader=runner --maxWorkers=1 --config .pcm13-vitest.config.mjs \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.contract.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
```

No full/project suite, build, typecheck, browser, render, localhost/socket, install, normal pin adoption, physical Player/export parity, or Gate 6 evidence was run or claimed. This remains test repair on the reviewed consumer, not parity evidence.
